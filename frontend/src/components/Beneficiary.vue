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
          @click="router.push('/profile')"
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
              $route.path === item.path
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
      <!-- <div class="p-3 border-top border-secondary border-opacity-25">
        <button class="btn btn-ghost-dark text-danger-emphasis w-100 d-flex align-items-center justify-content-center gap-2 py-2 hover-bg-danger-subtle" @click="handleLogout">
          <LogOut :size="18" />
          <span class="fw-medium">Sign Out</span>
        </button>
      </div> -->
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
    <div class="flex-grow-1 overflow-auto" style="margin-left: 280px;">
      <!-- Top Header -->
      <header 
        class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center sticky-top shadow-sm"
        :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'"
        :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''"
      >
        <div>
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Beneficiaries</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">Manage your trusted contacts for easy transfers.</p>
        </div>
        <div class="d-flex align-items-center gap-3">
          <button class="btn btn-light rounded-circle p-2 position-relative">
            <Bell :size="20" class="text-secondary" />
            <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle" v-if="unreadCount > 0">
              <span class="visually-hidden">New alerts</span>
            </span>
          </button>
        </div>
      </header>

      <div class="p-4 p-lg-5" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
        <div class="row g-4">
          <!-- Add Beneficiary Form -->
          <div class="col-lg-5">
            <div class="card border-0 shadow-sm rounded-4" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
              <div class="card-header border-bottom p-4" :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''">
                <h5 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Add New Beneficiary</h5>
              </div>
              <div class="card-body p-4" :style="isDarkMode ? 'background-color: #1e293b;' : ''">
                <form @submit.prevent="addBeneficiary">
                  <div class="mb-3">
                    <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Full Name</label>
                    <input 
                      v-model="beneficiary.name" 
                      type="text" 
                      class="form-control border-0 py-2" 
                      :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                      :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                      placeholder="e.g John Doe" 
                      required
                    >
                  </div>
                  <div class="mb-3">
                    <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Bank Name</label>
                    <input 
                      v-model="beneficiary.bank_name" 
                      type="text" 
                      class="form-control border-0 py-2" 
                      :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                      :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                      placeholder="e.g. HDFC Bank" 
                      required
                    >
                  </div>
                  <div class="mb-3">
                    <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Account Number</label>
                    <input 
                      v-model="beneficiary.account_number" 
                      @input="beneficiary.account_number = beneficiary.account_number.replace(/\D/g, '')"
                      type="text" 
                      class="form-control border-0 py-2" 
                      :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                      :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                      placeholder="Enter account number" 
                      required
                    >
                  </div>
                  <div class="mb-3">
                    <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">IFSC Code</label>
                    <input 
                      v-model="beneficiary.ifsc_code" 
                      type="text" 
                      class="form-control border-0 py-2" 
                      :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                      :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                      placeholder="e.g. HDFC0001234" 
                      required
                    >
                  </div>
                  <div class="mb-4">
                    <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Transfer Mode</label>
                    <select 
                      v-model="beneficiary.transfer_mode" 
                      class="form-select border-0 py-2"
                      :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                      :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                    >
                      <option value="IMPS">IMPS</option>
                      <option value="NEFT">NEFT</option>
                      <option value="RTGS">RTGS</option>
                    </select>
                  </div>
                  <button type="submit" class="btn btn-primary w-100 py-2 fw-medium shadow-sm hover-lift">
                    <i class="bi bi-plus-circle-fill me-2"></i>
                    Add Beneficiary
                  </button>
                </form>
              </div>
            </div>
          </div>

          <!-- Beneficiary List -->
          <div class="col-lg-7">
            <div class="card border-0 shadow-sm rounded-4 h-100" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
              <div class="card-header border-bottom p-4" :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''">
                <h5 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Your Beneficiaries</h5>
              </div>
              <div class="card-body p-0">
                <div v-if="beneficiaries.length === 0" class="p-5 text-center" :class="isDarkMode ? 'text-white-50' : 'text-muted'">
                  <Users :size="48" class="mb-3 opacity-25" />
                  <p>No beneficiaries added yet.</p>
                </div>
                <div v-else class="list-group list-group-flush">
                  <div 
                    v-for="b in beneficiaries" 
                    :key="b.id" 
                    class="list-group-item p-4 d-flex align-items-center justify-content-between transition-all"
                    :class="isDarkMode ? 'border-secondary' : 'border-light hover-bg-light'"
                    :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''"
                  >
                    <div class="d-flex align-items-center gap-3">
                      <div class="rounded-circle bg-primary-subtle text-primary p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
                        <span class="fw-bold">{{ b.name.charAt(0) }}</span>
                      </div>
                      <div>
                        <h6 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">{{ b.name }}</h6>
                        <small :class="isDarkMode ? 'text-white-50 d-block' : 'text-muted d-block'">{{ b.bank_name }} • {{ b.account_number }}</small>
                      </div>
                    </div>
                    <div class="text-end">
                      <span :class="['badge rounded-pill', getStatusBadgeClass(b.status)]">
                        {{ b.status }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- OTP Modal -->
    <div v-if="showOtpDialog" class="modal-backdrop fade show"></div>
    <div v-if="showOtpDialog" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">Verify Beneficiary</h5>
            <button type="button" class="btn-close" @click="showOtpDialog = false"></button>
          </div>
          <div class="modal-body p-4">
            <p class="text-muted small mb-4">An OTP has been sent to your registered email. Please enter it below to verify this beneficiary.</p>
            <input v-model="otp" @input="otp = otp.replace(/\D/g, '').slice(0, 6)" type="text" class="form-control form-control-lg text-center letter-spacing-2" placeholder="Enter 6-digit OTP" maxlength="6">
          </div>
          <div class="modal-footer border-0 pt-0 px-4 pb-4">
            <button type="button" class="btn btn-light" @click="showOtpDialog = false">Cancel</button>
            <button type="button" class="btn btn-primary px-4" @click="verifyBeneficiaryOtp">Verify</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { 
  LayoutDashboard, 
  Users, 
  Send, 
  FileText, 
  MessageSquare, 
  LogOut, 
  Bell,
  Wallet,
  Moon,
  Sun,
  AlertCircle
} from 'lucide-vue-next'
import { useDarkMode } from "@/composables/useDarkMode";

const router = useRouter()
const { isDarkMode, toggleDarkMode } = useDarkMode()

const customerId = ref(Number(localStorage.getItem("customer_id")) || 1)
const customerName = ref(localStorage.getItem("customer_name") || "Customer")
const unreadCount = ref(0)
const beneficiaries = ref([])
const showOtpDialog = ref(false)
const otp = ref("")
const pendingBeneficiaryAcc = ref("")

const beneficiary = ref({
  name: "",
  bank_name: "",
  account_number: "",
  ifsc_code: "",
  transfer_mode: "IMPS",
})

const customerInitials = computed(() => {
  return customerName.value
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



const navigate = (path) => {
  router.push(path)
}

const handleLogout = () => {
  localStorage.clear()
  router.push('/')
}

const fetchBeneficiaries = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:5000/customer/beneficiaries/${customerId.value}`)
    beneficiaries.value = res.data
  } catch (err) {
    console.error("Error fetching beneficiaries:", err)
  }
}

const addBeneficiary = async () => {
  try {
    const res = await axios.post("http://127.0.0.1:5000/customer/add-beneficiary", {
      customer_id: customerId.value,
      ...beneficiary.value,
    })
    alert("OTP sent to your registered email. Please check your inbox.")
    pendingBeneficiaryAcc.value = beneficiary.value.account_number
    showOtpDialog.value = true
    // Reset form but keep account number for verification context if needed
    beneficiary.value = { name: "", bank_name: "", account_number: "", ifsc_code: "", transfer_mode: "IMPS" }
  } catch (err) {
    alert(err.response?.data?.message || "Error adding beneficiary")
  }
}

const verifyBeneficiaryOtp = async () => {
  try {
    await axios.post("http://127.0.0.1:5000/customer/verify-beneficiary-otp", {
      customer_id: customerId.value,
      account_number: pendingBeneficiaryAcc.value,
      otp: otp.value,
    })
    alert("Beneficiary verified successfully.")
    showOtpDialog.value = false
    otp.value = ""
    fetchBeneficiaries()
  } catch (err) {
    alert(err.response?.data?.message || "OTP verification failed")
  }
}

const getStatusBadgeClass = (status) => {
  if (status === "Active") return "bg-success-subtle text-success"
  if (status === "Cooling Period") return "bg-warning-subtle text-warning"
  return "bg-danger-subtle text-danger"
}


onMounted(() => {
  fetchBeneficiaries()
})
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

.hover-bg-light:hover {
  background-color: #f8f9fa !important;
}

.hover-bg-danger-subtle:hover {
  background-color: #f8d7da !important;
  color: #842029 !important;
}

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-3px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
}

.transition-all {
  transition: all 0.2s ease-in-out;
}

.letter-spacing-2 {
  letter-spacing: 2px;
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

.cursor-pointer {
  cursor: pointer;
}

.hover-bg-light-transition {
  transition: background-color 0.2s ease;
}

.hover-bg-light-transition:hover {
  background-color: rgba(255,255,255,0.1) !important;
}

.modal-backdrop {
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
