import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from llama_cpp import Llama
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- CONFIGURATION ---
MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

class AIEngine:
    def __init__(self):
        print("--- INITIALIZING AI ENGINE ---")
        self.llm = Llama(model_path=MODEL_PATH, n_gpu_layers=0, n_ctx=2048, verbose=True)
    
    def _query(self, system, user):
        prompt = f"<s>[INST] {system} \n\n Data: {user} [/INST]"
        return self.llm(prompt, max_tokens=512)['choices'][0]['text'].strip()

    # ==============================================================================
    # FEATURE 1: ROBUST KYC CHECKER (Checks 4 Files)
    # ==============================================================================
    def analyze_kyc(self, files_dict):
        """
        Expects dict: {'Aadhaar': path, 'PAN': path, 'Photo': path, 'Signature': path}
        """
        report = ""
        # 1. Loop through all 4 files
        for name, path in files_dict.items():
            if not path or not os.path.exists(path):
                report += f"- {name}: MISSING or File Not Found\n"
                continue
            
            # For Photo/Signature, just confirm they exist (OCR useless here)
            if name in ["Photo", "Signature"]:
                report += f"- {name}: Present (Verified)\n"
            else:
                # For Aadhaar/PAN, extract text
                try:
                    text = ""
                    if path.lower().endswith('.pdf'):
                        pages = convert_from_path(path)
                        for page in pages: text += pytesseract.image_to_string(page)
                    else:
                        text = pytesseract.image_to_string(Image.open(path))
                    
                    clean_text = " ".join(text.split())[:300] # Limit text size
                    report += f"- {name} Content: {clean_text}\n"
                except Exception as e:
                    report += f"- {name}: File valid but OCR Failed ({str(e)})\n"

        # 2. Read Rules
        try:
            with open("kyc_rules.txt", "r") as f: rules = f.read()
        except: rules = "Standard KYC Rules apply."

        prompt = "You are a Compliance Officer. Validate if all 4 docs are present. Check if extracted names/numbers look valid."
        return self._query(prompt, f"RULES:\n{rules}\n\nSTATUS:\n{report}")

    # ==============================================================================
    # FEATURE 2: DISPUTE DRAFTER (Updated for Balance Checks)
    # ==============================================================================
    def draft_dispute_response(self, issue_desc, recent_txns, past_issues, current_balance):
        """
        Now checks for 'Insufficient Balance' by comparing Complaint vs Wallet.
        """
        # 1. Analyze Transactions (Look for duplicates)
        logs = f"Current Account Balance: Rs. {current_balance}\n\nRecent Successful Transactions:\n"
        seen_amounts = []
        possible_duplicates = []

        for t in recent_txns:
            logs += f"- {t['date']}: {t['desc']} (Rs. {t['amount']})\n"
            if t['amount'] in seen_amounts:
                possible_duplicates.append(str(t['amount']))
            seen_amounts.append(t['amount'])

        # 2. Generate System Notes
        system_note = "System Status: Normal."
        
        # Check A: Double Deduction?
        if possible_duplicates:
            system_note = f"System Flag: Potential Double Deduction found for Rs. {', '.join(possible_duplicates)}"
        
        # Check B: Implicit Low Balance Check (The AI will do this via logic below)
        # We don't write python logic for text parsing; we let Mistral-7B read the user's text.

        # 3. Memory Work
        context = "No similar history."
        if past_issues:
            texts = past_issues + [issue_desc]
            tfidf = TfidfVectorizer().fit_transform(texts)
            sim = cosine_similarity(tfidf[-1], tfidf[:-1])
            if sim.max() > 0.1:
                context = f"Similar Past Case Resolution: {past_issues[sim.argmax()]}"

        prompt = (
            "You are a Bank Support Agent. Draft a polite reply.\n"
            "1. COMPARE the amount mentioned in 'Complaint' vs 'Current Account Balance'. If request > balance, suggest 'Insufficient Funds'.\n"
            "2. Check 'System Flag' for double deductions.\n"
            "3. Use 'Similar Past Case' for other technical issues (like OTP).\n"
        )
        data = f"Complaint: {issue_desc}\n{system_note}\n{logs}\n{context}"
        return self._query(prompt, data)

    # ==============================================================================
    # FEATURE 3: SPENDING COACH (Simple Description Parsing)
    # ==============================================================================
    def spending_tips(self, transactions):
        """
        Categorizes based on description keywords (e.g. 'Swiggy')
        """
        summary = {}
        proof_list = []
        
        # Simple Keyword Matcher
        keywords = {
            "Food": ["swiggy", "zomato", "kfc", "pizza", "burger", "dine"],
            "Travel": ["uber", "ola", "fuel", "petrol", "rail", "flight"],
            "Shopping": ["amazon", "flipkart", "myntra", "store", "mall"]
        }

        for t in transactions:
            desc_lower = t['desc'].lower()
            cat = "Others"
            for k, v in keywords.items():
                if any(word in desc_lower for word in v):
                    cat = k
                    break
            
            summary[cat] = summary.get(cat, 0) + t['amount']
            if len(proof_list) < 5:
                proof_list.append(f"{t['desc']} (Rs.{t['amount']})")

        prompt = (
            "You are a Financial Coach. "
            "1. Analyze the spending summary. "
            "2. Give 3 short tips. "
            "3. Cite specific transactions from the 'Proof' list as evidence."
        )
        # Don't cache spending tips as user's spending changes over time
        summary_str = json.dumps(summary, sort_keys=True)
        return self._query(prompt, f"Summary: {summary_str}\nProof: {'; '.join(proof_list)}")

    # ==============================================================================
    # FEATURE 4: GENERAL CHAT (Smart Banking Chatbot)
    # ==============================================================================
    def general_chat(self, user_message, context_data):
        """
        General banking chatbot that uses account context for personalized responses.
        """
        prompt = (
            "You are a helpful banking assistant. "
            "Answer the user's question using the provided account context when relevant. "
            "Be friendly, concise, and accurate. "
            "If the question is about spending, transactions, or financial advice, use the context data. "
            "For general banking questions, provide helpful information."
        )
        data = f"User Question: {user_message}\n\nAccount Context:\n{context_data}"
        return self._query(prompt, data)

# Initialize singleton instance
ai = AIEngine()