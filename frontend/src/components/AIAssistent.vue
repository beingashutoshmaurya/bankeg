<template>
  <div class="d-flex min-vh-100 font-sans" :class="isDarkMode ? 'bg-dark' : 'bg-light'" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
    <!-- Sidebar -->
    <div class="sidebar d-flex flex-column shadow-sm" style="width: 280px; position: fixed; height: 100vh; overflow-y: auto; z-index: 1000; background-color: #1e293b;">
      <!-- Logo/Header -->
      <div class="p-4 mb-2">
        <div class="d-flex align-items-center gap-3 mb-4">
          <div>
            <h5 class="fw-bold text-white mb-0">GIROBANK</h5>
            <small class="text-white-50">Premium Banking</small>
          </div>
        </div>
        
        <div 
          class="user-profile p-3 rounded-3 d-flex align-items-center gap-3 cursor-pointer hover-bg-light-transition" 
          style="background-color: rgba(255,255,255,0.05);"
          @click="$router.push('/profile')"
        >
          <div class="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center fw-bold">
            {{ customerInitials }}
          </div>
          <div class="overflow-hidden">
            <h6 class="text-white mb-0 text-truncate">{{ customerName }}</h6>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <div class="flex-grow-1 px-3">
        <p class="text-uppercase text-white-50 fw-bold ms-2 mb-2" style="font-size: 0.75rem; letter-spacing: 1px;">Menu</p>
        <div class="d-grid gap-1">
          <button
            v-for="item in navItems"
            :key="item.id"
            @click="navigate(item.path)"
            :class="[
              'btn text-start d-flex align-items-center gap-3 px-3 py-2 rounded-3 transition-all',
              $route.path === item.path || (item.id === 'chatbot')
                ? 'bg-primary text-white shadow-sm'
                : 'btn-ghost-dark text-white-50 hover-text-white'
            ]"
          >
            <component :is="item.icon" :size="20" />
            <span class="fw-medium">{{ item.label }}</span>
          </button>
        </div>
      </div>

      <!-- Dark Mode Toggle -->
      <div class="px-3 py-2 border-top border-secondary border-opacity-25">
        <button 
          class="btn btn-ghost-dark text-white-50 w-100 d-flex align-items-center justify-content-between px-3 py-2 rounded-3 transition-all hover-text-white"
          @click="toggleDarkMode"
        >
          <div class="d-flex align-items-center gap-3">
            <component :is="isDarkMode ? Sun : Moon" :size="20" />
            <span class="fw-medium">{{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}</span>
          </div>
        </button>
      </div>

      <!-- Logout -->
      <div class="p-3 border-top border-secondary border-opacity-25">
        <button 
          class="logout-btn w-100 d-flex align-items-center justify-content-center gap-2 py-2"
          @click="handleLogout"
        >
          <LogOut :size="18" />
          <span class="fw-semibold">Sign Out</span>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column h-100 overflow-hidden" style="margin-left: 280px;">
      <!-- Header -->
      <header 
        class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center shadow-sm z-1"
        :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'"
        :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''"
      >
        <div>
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Personalised Spending Coach</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">Your personal financial advisor.</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <div class="badge bg-success-subtle text-success border border-success-subtle d-flex align-items-center gap-1 px-3 py-2 rounded-pill">
            <div class="rounded-circle bg-success" style="width: 8px; height: 8px;"></div>
            <span>Online</span>
          </div>
        </div>
      </header>

      <!-- Chat Area -->
      <div 
        class="flex-grow-1 p-4 overflow-auto d-flex flex-column"
        :class="isDarkMode ? 'bg-dark' : 'bg-light'"
        :style="isDarkMode ? 'background-color: #0f172a;' : ''"
      >
        <div class="container-fluid p-0 h-100 d-flex flex-column" style="max-width: 900px;">
          
          <!-- Messages List -->
          <div class="flex-grow-1 d-flex flex-column gap-4 mb-4">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="d-flex gap-3"
              :class="msg.type === 'user' ? 'flex-row-reverse' : 'flex-row'"
            >
              <!-- Avatar -->
              <div
                class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 shadow-sm overflow-hidden"
                :class="msg.type === 'user' ? 'bg-primary text-white' : (isDarkMode ? 'bg-dark' : 'bg-white')"
                :style="msg.type === 'bot' && isDarkMode ? 'background-color: #1e293b;' : ''"
                style="width: 40px; height: 40px;"
              >
                <component v-if="msg.type === 'user'" :is="User" :size="20" />
                <img v-else :src="haalandImage" alt="AI Assistant" style="width: 100%; height: 100%; object-fit: cover;" />
              </div>

              <!-- Message Bubble -->
              <div class="d-flex flex-column" :class="msg.type === 'user' ? 'align-items-end' : 'align-items-start'" style="max-width: 75%;">
                <div
                  class="p-3 shadow-sm"
                  :class="[
                    msg.type === 'user' 
                      ? 'bg-primary text-white rounded-top-left-3 rounded-bottom-3' 
                      : (isDarkMode ? 'bg-dark text-white rounded-top-right-3 rounded-bottom-3' : 'bg-white text-dark rounded-top-right-3 rounded-bottom-3')
                  ]"
                  :style="msg.type === 'bot' && isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''"
                  style="border-radius: 1rem;"
                >
                  <p class="mb-0" style="white-space: pre-wrap;">{{ msg.text }}</p>

                  <!-- Rich Content: Spending Data -->
                  <div v-if="msg.spendingData" class="mt-3">
                    <div class="card border-0 shadow-sm overflow-hidden mb-2" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #0f172a; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
                      <div class="card-body p-3" :class="isDarkMode ? 'bg-dark' : 'bg-light'" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                          <span :class="isDarkMode ? 'text-white-50 small fw-bold text-uppercase' : 'text-secondary small fw-bold text-uppercase'">{{ msg.spendingData.category }}</span>
                          <span :class="isDarkMode ? 'text-white fw-bold' : 'text-dark fw-bold'">₹{{ msg.spendingData.amount }}</span>
                        </div>
                        <div class="progress" style="height: 6px;">
                          <div class="progress-bar bg-warning" role="progressbar" style="width: 75%"></div>
                        </div>
                        <small :class="isDarkMode ? 'text-white-50 mt-1 d-block' : 'text-muted mt-1 d-block'">75% of monthly budget used</small>
                      </div>
                    </div>

                    <div class="rounded-3 border overflow-hidden" :class="isDarkMode ? 'bg-dark border-secondary' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #0f172a; border-color: rgba(255,255,255,0.1) !important;' : ''">
                      <div v-for="(txn, idx) in msg.spendingData.transactions" :key="idx" class="d-flex justify-content-between align-items-center p-2 border-bottom last-border-0" :class="isDarkMode ? 'border-secondary' : 'border-light'" :style="isDarkMode ? 'border-color: rgba(255,255,255,0.1) !important;' : ''">
                        <div class="d-flex align-items-center gap-2">
                          <div class="rounded p-1" :class="isDarkMode ? 'bg-dark' : 'bg-light'" :style="isDarkMode ? 'background-color: #1e293b;' : ''">
                            <Coffee :size="14" :class="isDarkMode ? 'text-white-50' : 'text-secondary'" />
                          </div>
                          <div>
                            <div :class="isDarkMode ? 'fw-medium text-white small' : 'fw-medium text-dark small'">{{ txn.merchant }}</div>
                            <div :class="isDarkMode ? 'text-white-50 x-small' : 'text-muted x-small'" style="font-size: 0.75rem;">{{ txn.date }}</div>
                          </div>
                        </div>
                        <span :class="isDarkMode ? 'fw-bold text-white small' : 'fw-bold text-dark small'">₹{{ txn.amount }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <small :class="isDarkMode ? 'text-white-50 mt-1 mx-1' : 'text-muted mt-1 mx-1'" style="font-size: 0.75rem;">{{ msg.time }}</small>
              </div>
            </div>
            
            <!-- Loading Indicator -->
            <div v-if="isLoading" class="d-flex gap-3">
              <div 
                class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 shadow-sm overflow-hidden" 
                :class="isDarkMode ? 'bg-dark' : 'bg-white'"
                :style="isDarkMode ? 'background-color: #1e293b;' : ''"
                style="width: 40px; height: 40px;"
              >
                <img :src="haalandImage" alt="AI Assistant" style="width: 100%; height: 100%; object-fit: cover;" />
              </div>
              <div class="d-flex align-items-start">
                <div 
                  class="p-3 shadow-sm rounded-top-right-3 rounded-bottom-3" 
                  :class="isDarkMode ? 'bg-dark text-white' : 'bg-white text-dark'"
                  :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''"
                  style="border-radius: 1rem;"
                >
                  <div class="d-flex gap-2 align-items-center">
                    <div class="spinner-border spinner-border-sm text-primary" role="status">
                      <span class="visually-hidden">Loading...</span>
                    </div>
                    <span :class="isDarkMode ? 'text-white-50 small' : 'text-muted small'">Thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Input Area -->
      <div 
        class="border-top p-4"
        :class="isDarkMode ? 'bg-dark border-secondary' : 'bg-white border-light'"
        :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''"
      >
        <div class="container-fluid p-0" style="max-width: 900px;">
          <!-- Quick Actions -->
          <div class="d-flex gap-2 mb-3 overflow-auto pb-2 no-scrollbar">
            <button
              v-for="(action, index) in quickActions"
              :key="index"
              class="btn btn-outline-secondary btn-sm rounded-pill text-nowrap px-3 hover-bg-light"
              @click="handleQuickAction(action)"
            >
              {{ action }}
            </button>
          </div>

          <div class="input-group input-group-lg shadow-sm rounded-pill overflow-hidden border border-light">
            <input
              v-model="inputMessage"
              @keyup.enter="handleSendMessage"
              type="text"
              class="form-control border-0 ps-4"
              :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
              :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
              placeholder="Ask me anything about your finances..."
              :disabled="isLoading"
            />
            <button 
              class="btn btn-primary px-4 d-flex align-items-center gap-2" 
              @click="handleSendMessage"
              :disabled="isLoading || !inputMessage.trim()"
            >
              <span v-if="!isLoading">Send</span>
              <span v-else class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <Send v-if="!isLoading" :size="18" />
            </button>
          </div>
          <div class="text-center mt-2">
            <small :class="isDarkMode ? 'text-white-50 x-small' : 'text-muted x-small'">AI can make mistakes. But you can trust this one more than others!!!</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  LayoutDashboard, 
  Users, 
  Send, 
  FileText, 
  MessageSquare, 
  LogOut, 
  Bot, 
  User, 
  Coffee, 
  TrendingDown,
  Wallet,
  AlertCircle,
  Moon,
  Sun
} from 'lucide-vue-next'

import axios from 'axios'
import { useDarkMode } from "@/composables/useDarkMode"
import haalandImage from '@/assets/Haaland.png'

export default {
  name: 'AIAssistant',
  components: {
    LayoutDashboard,
    Users,
    Send,
    FileText,
    MessageSquare,
    LogOut,
    Bot,
    User,
    Coffee,
    TrendingDown,
    Wallet,
    AlertCircle,
    Moon,
    Sun
  },
  setup() {
    const router = useRouter()
    const { isDarkMode, toggleDarkMode } = useDarkMode()
    const customerName = localStorage.getItem("customer_name") || "Customer"
    
    const customerInitials = computed(() => {
      return customerName
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    })

    const navItems = [
      { id: 'dashboard', label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
      { id: 'beneficiary', label: 'Beneficiaries', path: '/beneficiary', icon: Users },
      { id: 'transfer', label: 'Transfer Money', path: '/transfer', icon: Send },
      { id: 'history', label: 'Transactions', path: '/history', icon: FileText },
      { id: 'payments', label: 'Payments', path: '/payments', icon: Wallet },
      { id: 'chatbot', label: 'AI Assistant', path: '/chatbot', icon: MessageSquare },
      { id: 'disputes', label: 'Disputes', path: '/disputes', icon: AlertCircle }
    ]

    const inputMessage = ref('')
    const customerId = Number(localStorage.getItem('customer_id'))
    const quickActions = ['Analyze my spending', 'Food spending tips', 'Travel spending advice', 'Shopping habits']
    const isLoading = ref(false)

    // Helper functions for localStorage
    function getChatStorageKey() {
      return `ai_chat_${customerId || 'guest'}`
    }

    function saveMessagesToStorage() {
      if (customerId && !isNaN(customerId)) {
        try {
          localStorage.setItem(getChatStorageKey(), JSON.stringify(messages.value))
        } catch (error) {
          console.error('Error saving messages to localStorage:', error)
          // If storage is full, try to clear old data
          try {
            // Clear messages older than the last 50
            if (messages.value.length > 50) {
              messages.value = messages.value.slice(-50)
              localStorage.setItem(getChatStorageKey(), JSON.stringify(messages.value))
            }
          } catch (e) {
            console.error('Error clearing old messages:', e)
          }
        }
      }
    }

    function loadMessagesFromStorage() {
      if (customerId && !isNaN(customerId)) {
        try {
          const savedMessages = localStorage.getItem(getChatStorageKey())
          if (savedMessages) {
            const parsed = JSON.parse(savedMessages)
            // Validate that it's an array and has valid structure
            if (Array.isArray(parsed) && parsed.length > 0) {
              // Check if messages have required fields
              const isValid = parsed.every(msg => msg.id && msg.type && msg.text && msg.time)
              if (isValid) {
                return parsed
              }
            }
          }
        } catch (error) {
          console.error('Error loading messages from localStorage:', error)
          // Clear corrupted data
          localStorage.removeItem(getChatStorageKey())
        }
      }
      // Return default messages if nothing saved or invalid
      return [
        {
          id: 1,
          type: 'bot',
          text: "Hello! I'm your personal spending coach and banking assistant. How can I help you today?",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
        {
          id: 2,
          type: 'bot',
          text: 'I can analyze your spending patterns, provide financial advice, answer account questions, and help you make better financial decisions. Try asking me about your spending habits!',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]
    }

    // Initialize messages from localStorage or use defaults
    const messages = ref(loadMessagesFromStorage())

    // Check if message is asking for spending analysis
    function isSpendingQuery(message) {
      const spendingKeywords = ['spending', 'expense', 'expenditure', 'budget', 'spend', 'food', 'travel', 'shopping', 'habits', 'analyze', 'analysis']
      const lowerMsg = message.toLowerCase()
      return spendingKeywords.some(keyword => lowerMsg.includes(keyword))
    }

    async function handleSendMessage() {
      if (!inputMessage.value.trim() || isLoading.value) return
      
      const userMsg = {
        id: messages.value.length + 1,
        type: 'user',
        text: inputMessage.value,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }

      messages.value.push(userMsg)
      saveMessagesToStorage() // Save after user message
      inputMessage.value = ''
      isLoading.value = true

      let botResponse
      const nextId = messages.value.length + 1
      
      try {
        // Check if it's a spending-related query
        if (isSpendingQuery(userMsg.text) && customerId && !isNaN(customerId)) {
          // Use spending coach endpoint
          console.log('Using spending coach endpoint for customer:', customerId)
          const res = await axios.get(`http://127.0.0.1:5000/api/customer/coach/${customerId}`, {
            timeout: 300000 // 5 minutes timeout for AI processing
          })
          console.log('Spending coach response:', res.data)
          botResponse = {
            id: nextId,
            type: 'bot',
            text: res.data.advice || "I've analyzed your spending patterns. Here are some insights...",
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        } else {
          // Use general chat endpoint
          console.log('Using general chat endpoint, customerId:', customerId)
          const res = await axios.post('http://127.0.0.1:5000/api/chat', {
            message: userMsg.text,
            user_id: customerId && !isNaN(customerId) ? customerId : null
          }, {
            timeout: 300000 // 5 minutes timeout for AI processing
          })
          console.log('General chat response:', res.data)
          botResponse = {
            id: nextId,
            type: 'bot',
            text: res.data.response || "I'm here to help with your banking needs.",
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        }
      } catch (error) {
        console.error('AI Assistant Error:', error)
        console.error('Error details:', error.response?.data, error.message)
        botResponse = {
          id: nextId,
          type: 'bot',
          text: error.response?.data?.error || error.message || "Sorry, I'm having trouble connecting to the server. Please try again.",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      }

      messages.value.push(botResponse)
      saveMessagesToStorage() // Save after bot response
      isLoading.value = false
      
      // Auto-scroll to bottom
      setTimeout(() => {
        const chatArea = document.querySelector('.overflow-auto')
        if (chatArea) {
          chatArea.scrollTop = chatArea.scrollHeight
        }
      }, 100)
    }

    async function handleQuickAction(action) {
      inputMessage.value = action
      await handleSendMessage()
    }

    const handleLogout = () => {
      // Clear chat history for this user before clearing all localStorage
      if (customerId && !isNaN(customerId)) {
        localStorage.removeItem(getChatStorageKey())
      }
      localStorage.clear()
      router.push('/')
    }

    return { 
      navItems, 
      messages, 
      inputMessage, 
      quickActions, 
      handleSendMessage, 
      handleQuickAction,
      handleLogout,
      customerName,
      customerInitials,
      isLoading,
      isDarkMode,
      toggleDarkMode,
      haalandImage,
      Moon,
      Sun
    }
  },
  methods: {
    navigate(path) {
      this.$router.push(path)
    }
  }
}
</script>

<style scoped>
.font-sans {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.logo-box {
  width: 48px;
  height: 48px;
}

.avatar {
  width: 40px;
  height: 40px;
}

.btn-ghost-dark {
  background: transparent;
  border: none;
}

.btn-ghost-dark:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white !important;
}

.hover-text-white:hover {
  color: white !important;
}

.transition-all {
  transition: all 0.3s ease;
}

.logout-btn {
  background: #fff;
  border: 1px solid rgba(220, 53, 69, 0.35);
  color: #dc3545;
  border-radius: 12px;
  transition: all 0.25s ease-in-out;
  box-shadow: 0 2px 6px rgba(255, 0, 0, 0.06);
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 0.08);
  border-color: rgba(220, 53, 69, 0.7);
  box-shadow: 0 4px 10px rgba(220, 53, 69, 0.15);
  transform: translateY(-2px);
}

.logout-btn:active {
  transform: scale(0.98);
  background: rgba(220, 53, 69, 0.16);
}

.rounded-top-left-3 { border-top-left-radius: 1rem !important; }
.rounded-top-right-3 { border-top-right-radius: 1rem !important; }
.rounded-bottom-3 { border-bottom-left-radius: 1rem !important; border-bottom-right-radius: 1rem !important; }

.last-border-0:last-child {
  border-bottom: none !important;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.hover-bg-light:hover {
  background-color: #f8f9fa !important;
}

.cursor-pointer {
  cursor: pointer;
}

.hover-bg-light-transition {
  transition: background-color 0.2s ease;
}

.hover-bg-light-transition:hover {
  background-color: rgba(255,255,255,0.1) !important;
}
</style>


