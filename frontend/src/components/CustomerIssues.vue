<template>
  <div class="dashboard-container p-4">
    <!-- Issue Resolution Section -->
    <section class="issues-section">
      <h2>Customer Issue Resolution</h2>

      <!-- Loading -->
      <div v-if="loadingIssues" class="loading">
        <div class="spinner"></div>
        <p>Loading issues...</p>
      </div>

      <!-- If No Issues -->
      <div v-else-if="issues.length === 0" class="empty-state">
        <p>No customer issues pending!</p>
      </div>

      <!-- Issues List -->
      <div v-else class="issue-list">
        <div
          class="issue-item"
          :class="getIssueStatusClass(issue.status)"
          v-for="issue in issues"
          :key="issue.id"
        >
          <div class="issue-info">
            <div class="issue-header">
              <p class="issue-title">{{ issue.title }}</p>
              <span :class="['issue-status-badge', isIssueResolved(issue.status) ? 'resolved' : 'pending']">
                {{ isIssueResolved(issue.status) ? 'Resolved' : 'Pending' }}
              </span>
            </div>
            <p class="issue-desc">{{ issue.description }}</p>
            <p class="issue-cust">Customer ID: <strong>{{ issue.customer_id }}</strong></p>
            <p class="issue-date">{{ formatDate(issue.created_date) }}</p>
          </div>

          <!-- Buttons - Only show if status is pending -->
          <div v-if="!isIssueResolved(issue.status)" class="issue-actions">
            <button 
              class="action-btn ai-btn" 
              @click="analyzeIssue(issue.id)"
              :disabled="isGeneratingDraft || isSendingEmail"
              :title="isGeneratingDraft ? 'Please wait for current AI generation to complete' : (isSendingEmail ? 'Please wait for email to be sent' : '')"
            >
              <span v-if="isGeneratingDraft && selectedIssueId === issue.id" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i class="bi bi-robot me-2"></i>
              {{ isGeneratingDraft && selectedIssueId === issue.id ? 'Generating...' : 'AI Draft Reply' }}
            </button>

            <button 
              v-if="!issue.emailSent"
              class="action-btn send-btn" 
              @click="sendEmailToCustomer(issue.id)"
              :disabled="draftReadyForIssue !== issue.id || isGeneratingDraft || isSendingEmail"
              :title="draftReadyForIssue !== issue.id ? 'Please generate AI draft reply first' : ''"
            >
              <span v-if="isSendingEmail && sendingEmailForIssue === issue.id" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i class="bi bi-send me-2"></i>
              {{ isSendingEmail && sendingEmailForIssue === issue.id ? 'Sending...' : 'Send As Email' }}
            </button>

            <button 
              v-else
              class="action-btn resolved-btn" 
              disabled
            >
              <i class="bi bi-check-circle me-2"></i>
              Resolved
            </button>
          </div>

          <!-- AI Output - Only show if status is pending -->
          <div v-if="!isIssueResolved(issue.status) && selectedIssueId === issue.id" class="ai-output-container">
            <div class="ai-output-header">
              <div class="d-flex align-items-center gap-2">
                <i class="bi bi-sparkles" style="font-size: 1.25rem; color: white;"></i>
                <h5 class="mb-0 fw-bold text-white">AI Suggested Reply</h5>
                <span v-if="isGeneratingDraft" class="badge bg-info ms-2">
                  <span class="spinner-border spinner-border-sm me-1" role="status"></span>
                  Generating...
                </span>
                <span v-else-if="draftReadyForIssue === issue.id" class="badge bg-success ms-2">
                  <i class="bi bi-check-circle me-1"></i>
                  Ready
                </span>
              </div>
            </div>
            <div class="ai-output-content">
              <div v-if="isGeneratingDraft" class="loading-draft">
                <div class="spinner-border text-primary mb-3" role="status"></div>
                <p class="text-muted mb-0">AI is analyzing the issue and generating a response...</p>
              </div>
              <div v-else-if="aiDraft && aiDraft !== 'Error generating AI draft.'" class="draft-text">
                {{ aiDraft }}
              </div>
              <div v-else class="error-draft">
                <i class="bi bi-exclamation-triangle text-warning me-2"></i>
                <span>Error generating AI draft. Please try again.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Email Sent Confirmation Modal -->
    <div v-if="showEmailSentModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);" @click.self="closeEmailSentModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
          <!-- Modal Header -->
          <div class="modal-header bg-success bg-gradient text-white border-0 py-4">
            <div class="d-flex align-items-center justify-content-center gap-3 w-100">
              <div>
                <h5 class="fw-bold mb-0">GIROBANK</h5>
                <small class="opacity-75">Email Sent</small>
              </div>
            </div>
            <button type="button" class="btn-close btn-close-white" @click="closeEmailSentModal" aria-label="Close"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <div class="mb-3">
                <i class="bi bi-check-circle-fill" style="font-size: 3rem; color: #198754;"></i>
              </div>
              <h6 class="fw-bold text-dark mb-2">Email Sent Successfully!</h6>
              <p class="text-muted mb-0">The AI-generated response has been sent to the customer's email address.</p>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer border-0 pt-0 px-4 pb-4">
            <button type="button" class="btn btn-success px-4" @click="closeEmailSentModal">OK</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const issues = ref([]);
const loadingIssues = ref(true);
const selectedIssueId = ref(null);
const aiDraft = ref("");
const isGeneratingDraft = ref(false);
const draftReadyForIssue = ref(null); // Track which issue has a completed draft
const isSendingEmail = ref(false);
const sendingEmailForIssue = ref(null);
const showEmailSentModal = ref(false);
const employeeName = ref(localStorage.getItem("employee_name") || "Employee");

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

// Fetch Issues
const fetchIssues = async () => {
  try {
    loadingIssues.value = true;
    const res = await fetch("http://127.0.0.1:5000/api/issue/get");
    if (!res.ok) throw new Error("Failed to load issues");
    const data = await res.json();
    // Add emailSent property to track if email has been sent
    issues.value = data.map(issue => ({
      ...issue,
      emailSent: issue.emailSent || false
    }));
  } catch (err) {
    console.error("Issue fetch error", err);
  } finally {
    loadingIssues.value = false;
  }
};

// AI Draft Call
const analyzeIssue = async (issueId) => {
  selectedIssueId.value = issueId;
  isGeneratingDraft.value = true;
  draftReadyForIssue.value = null;
  aiDraft.value = "";

  try {
    const res = await fetch(
      `http://127.0.0.1:5000/api/employee/draft-dispute/${issueId}`
    );
    
    if (!res.ok) {
      throw new Error("Failed to generate draft");
    }
    
    const data = await res.json();
    let draft = data.suggested_response || "No response generated.";
    
    // Replace [Your name] with employee name
    draft = draft.replace(/\[Your name\]/gi, employeeName.value);
    draft = draft.replace(/\[your name\]/gi, employeeName.value);
    draft = draft.replace(/Your name/gi, employeeName.value);
    
    aiDraft.value = draft;
    
    // Mark draft as ready for this issue
    draftReadyForIssue.value = issueId;
  } catch (err) {
    console.error("AI draft error:", err);
    aiDraft.value = "Error generating AI draft.";
    draftReadyForIssue.value = null;
  } finally {
    isGeneratingDraft.value = false;
  }
};

// Send Email to Customer
const sendEmailToCustomer = async (issueId) => {
  // Prevent action if draft is not ready
  if (draftReadyForIssue.value !== issueId || isSendingEmail.value) {
    return;
  }

  isSendingEmail.value = true;
  sendingEmailForIssue.value = issueId;

  try {
    const issue = issues.value.find(i => i.id === issueId);
    if (!issue) throw new Error("Issue not found");

    const res = await fetch(
      `http://127.0.0.1:5000/api/employee/send-dispute-email/${issueId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          draft_message: aiDraft.value,
          employee_name: employeeName.value
        })
      }
    );

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ message: "Failed to send email" }));
      throw new Error(errorData.message || "Unable to send email");
    }

    // Show success modal
    showEmailSentModal.value = true;
    
    // Close modal and refresh page after a short delay
    setTimeout(() => {
      showEmailSentModal.value = false;
      // Refresh the page to get updated issue status
      window.location.reload();
    }, 2000);
  } catch (err) {
    console.error("Send email error:", err);
    alert(`Error sending email: ${err.message}`);
    isSendingEmail.value = false;
    sendingEmailForIssue.value = null;
  }
};

const closeEmailSentModal = () => {
  showEmailSentModal.value = false;
};

// Normalize issue status for comparison
const isIssueResolved = (status) => {
  if (!status) return false;
  return status.toLowerCase() === 'complete' || status.toLowerCase() === 'resolved';
};

// Get CSS class for issue status
const getIssueStatusClass = (status) => {
  return isIssueResolved(status) ? 'issue-resolved' : 'issue-pending';
};

onMounted(() => {
  fetchIssues();
});
</script>

<style scoped>
.dashboard-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  color: #333;
}

.issues-section {
  margin-top: 40px;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.issues-section h2 {
  font-size: 1.8rem;
  color: #4a90e2;
  margin-bottom: 20px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4a90e2;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  padding: 60px;
  text-align: center;
  font-size: 1.3rem;
  color: #666;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.issue-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.issue-item {
  padding: 18px;
  background: #fafafa;
  border-left: 5px solid #e67e22;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.issue-item.issue-pending {
  background: #fff4e6;
  border-left-color: #ff9800;
}

.issue-item.issue-resolved {
  background: #e8f5e9;
  border-left-color: #4caf50;
}

.issue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.issue-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  flex: 1;
}

.issue-status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.issue-status-badge.resolved {
  background-color: #4caf50;
  color: white;
}

.issue-status-badge.pending {
  background-color: #ff9800;
  color: white;
}

.issue-desc {
  margin: 5px 0;
  color: #444;
}

.issue-actions {
  margin-top: 15px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.action-btn:active:not(:disabled) {
  transform: translateY(0);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.ai-btn {
  background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
  color: white;
}

.ai-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #0a58ca 0%, #084298 100%);
}

.resolve-btn {
  background: linear-gradient(135deg, #198754 0%, #157347 100%);
  color: white;
}

.resolve-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #157347 0%, #0f5132 100%);
}

.resolve-btn:disabled {
  background: #6c757d;
  color: white;
}

.send-btn {
  background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
  color: white;
}

.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #0a58ca 0%, #084298 100%);
}

.send-btn:disabled {
  background: #6c757d;
  color: white;
}

.resolved-btn {
  background: #6c757d;
  color: white;
  cursor: not-allowed;
}

.modal {
  z-index: 1055;
}

.modal-content {
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.ai-output-container {
  margin-top: 20px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border: 2px solid #e0e7ff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.1);
  overflow: hidden;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.ai-output-header {
  background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
  color: white;
  padding: 16px 20px;
  border-bottom: 2px solid #0a58ca;
}

.ai-output-content {
  padding: 20px;
  background: white;
}

.loading-draft {
  text-align: center;
  padding: 30px 20px;
}

.draft-text {
  color: #212529;
  font-size: 1rem;
  line-height: 1.7;
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #0d6efd;
  margin: 0;
}

.error-draft {
  color: #856404;
  background: #fff3cd;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 4px solid #ffc107;
  display: flex;
  align-items: center;
}
</style>


