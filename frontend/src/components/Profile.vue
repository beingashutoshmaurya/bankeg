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
            {{ getInitials(customerName) }}
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
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Profile</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">View your account information.</p>
        </div>
      </header>

      <div class="p-4 p-lg-5" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
        <!-- Loading Spinner -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3 text-white-50 fw-medium">Fetching your profile...</p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="alert alert-danger rounded-4 border-0 shadow-sm">
          <div class="d-flex align-items-center gap-2">
            <div class="flex-shrink-0">
              <div class="rounded-circle bg-danger bg-opacity-10 d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                <span class="text-danger fw-bold">!</span>
              </div>
            </div>
            <div class="flex-grow-1">
              <strong>Error:</strong> {{ error }}
            </div>
          </div>
        </div>

        <!-- Profile Content -->
        <div v-if="profile && !loading">
          <!-- CUSTOMER DETAILS -->
          <div 
            class="card border-0 shadow-lg mb-4 rounded-4 overflow-hidden profile-card" 
            :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : 'background-color: #f8f9fa; border: 1px solid rgba(0,0,0,0.05) !important;'"
          >
            <div class="card-header-profile-customer p-4" :style="isDarkMode ? 'background-color: rgba(13, 110, 253, 0.2); border-bottom: 1px solid rgba(13, 110, 253, 0.3);' : 'background-color: rgba(13, 110, 253, 0.1); border-bottom: 1px solid rgba(13, 110, 253, 0.2);'">
              <div class="d-flex align-items-center gap-3">
                <div class="profile-icon-box bg-primary bg-opacity-20 rounded-3 d-flex align-items-center justify-content-center" style="width: 56px; height: 56px;">
                  <Users :size="28" class="text-primary" />
                </div>
                <div>
                  <h5 :class="isDarkMode ? 'fw-bold text-white mb-1' : 'fw-bold text-dark mb-1'">Customer Details</h5>
                  <p :class="isDarkMode ? 'text-white-50 small mb-0' : 'text-muted small mb-0'">Personal information and account status</p>
                </div>
              </div>
            </div>
            <div class="card-body p-4" :style="isDarkMode ? 'background-color: #1e293b;' : 'background-color: #f8f9fa;'">
              <div class="row g-4">
                <div class="col-md-6">
                  <div class="profile-info-item">
                    <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Full Name</label>
                    <p :class="['profile-value', isDarkMode ? 'text-white' : '']">{{ profile.full_name }}</p>
                  </div>
                  <div class="profile-info-item">
                    <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Email Address</label>
                    <p :class="['profile-value', isDarkMode ? 'text-white' : '']">{{ profile.email }}</p>
                  </div>
                  <div class="profile-info-item">
                    <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Phone Number</label>
                    <p :class="['profile-value', isDarkMode ? 'text-white' : '']">{{ profile.phone }}</p>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="profile-info-item">
                    <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Account Status</label>
                    <div>
                      <span :class="['status-badge', profile.is_active ? 'status-active' : 'status-inactive']">
                        {{ profile.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </div>
                  </div>
                  <div class="profile-info-item">
                    <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Member Since</label>
                    <p :class="['profile-value', isDarkMode ? 'text-white' : '']">{{ formatDateTime(profile.created_at) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ACCOUNT DETAILS -->
          <div 
            class="card border-0 shadow-lg mb-4 rounded-4 overflow-hidden profile-card" 
            :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : 'background-color: #f8f9fa; border: 1px solid rgba(0,0,0,0.05) !important;'"
          >
            <div class="card-header-profile-account p-4" :style="isDarkMode ? 'background-color: rgba(25, 135, 84, 0.2); border-bottom: 1px solid rgba(25, 135, 84, 0.3);' : 'background-color: rgba(25, 135, 84, 0.1); border-bottom: 1px solid rgba(25, 135, 84, 0.2);'">
              <div class="d-flex align-items-center gap-3">
                <div class="profile-icon-box bg-success bg-opacity-20 rounded-3 d-flex align-items-center justify-content-center" style="width: 56px; height: 56px;">
                  <LayoutDashboard :size="28" class="text-success" />
                </div>
                <div>
                  <h5 :class="isDarkMode ? 'fw-bold text-white mb-1' : 'fw-bold text-dark mb-1'">Account Information</h5>
                  <p :class="isDarkMode ? 'text-white-50 small mb-0' : 'text-muted small mb-0'">Banking account details and balance</p>
                </div>
              </div>
            </div>
            <div class="card-body p-4" :style="isDarkMode ? 'background-color: #1e293b;' : 'background-color: #f8f9fa;'">
              <div v-if="profile.account && profile.account.account_number">
                <div class="row g-4">
                  <div class="col-md-6">
                    <div class="profile-info-item">
                      <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Account Number</label>
                      <p 
                        :class="['profile-value account-number', isDarkMode ? 'text-white' : '', 'cursor-pointer']"
                        @mouseenter="revealAccountNumber"
                        @mouseleave="hideAccountNumber"
                        :title="showAccountNumber ? '' : 'Hover to reveal account number'"
                        style="transition: all 0.3s ease; user-select: none;"
                      >
                        {{ maskedAccountNumber }}
                      </p>
                    </div>
                    <div class="profile-info-item">
                      <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Account Type</label>
                      <p :class="['profile-value', isDarkMode ? 'text-white' : '']">
                        <span class="account-type-badge">{{ profile.account.account_type }}</span>
                      </p>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="profile-info-item">
                      <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Available Balance</label>
                      <p :class="['profile-value balance-amount', isDarkMode ? 'text-white' : '']">₹{{ Number(profile.account.balance).toFixed(2) }}</p>
                    </div>
                    <div class="profile-info-item">
                      <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Account Created</label>
                      <p :class="['profile-value', isDarkMode ? 'text-white' : '']">{{ formatDateTime(profile.account.created_at) }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-4">
                <div class="text-muted">
                  <p class="mb-0">No account created yet.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- KYC DETAILS -->
          <div 
            class="card border-0 shadow-lg rounded-4 overflow-hidden profile-card" 
            :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : 'background-color: #f8f9fa; border: 1px solid rgba(0,0,0,0.05) !important;'"
          >
            <div class="card-header-profile-kyc p-4" :style="isDarkMode ? 'background-color: rgba(255, 193, 7, 0.2); border-bottom: 1px solid rgba(255, 193, 7, 0.3);' : 'background-color: rgba(255, 193, 7, 0.1); border-bottom: 1px solid rgba(255, 193, 7, 0.2);'">
              <div class="d-flex align-items-center gap-3">
                <div class="profile-icon-box bg-warning bg-opacity-20 rounded-3 d-flex align-items-center justify-content-center" style="width: 56px; height: 56px;">
                  <FileText :size="28" class="text-warning" />
                </div>
                <div>
                  <h5 :class="isDarkMode ? 'fw-bold text-white mb-1' : 'fw-bold text-dark mb-1'">KYC Information</h5>
                  <p :class="isDarkMode ? 'text-white-50 small mb-0' : 'text-muted small mb-0'">Verification status and documents</p>
                </div>
              </div>
            </div>
            <div class="card-body p-4" :style="isDarkMode ? 'background-color: #1e293b;' : 'background-color: #f8f9fa;'">
              <div class="row g-4 mb-4">
                <div class="col-md-6">
                  <div class="profile-info-item">
                    <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">KYC Status</label>
                    <div>
                      <span :class="['status-badge', getKycStatusBadgeClass(profile.kyc.status)]">
                        {{ profile.kyc.status || 'Not Submitted' }}
                      </span>
                    </div>
                  </div>
                  <div class="profile-info-item">
                    <label class="profile-label">OTP Verified</label>
                    <div>
                      <span :class="['status-badge', profile.kyc.otp_verified ? 'status-verified' : 'status-unverified']">
                        {{ profile.kyc.otp_verified ? "Verified" : "Not Verified" }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="profile-info-item">
                    <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Submitted At</label>
                    <p :class="['profile-value', isDarkMode ? 'text-white' : '']">{{ formatDateTime(profile.kyc.submitted_at) }}</p>
                  </div>
                  <div class="profile-info-item">
                    <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Reviewed At</label>
                    <p :class="['profile-value', isDarkMode ? 'text-white' : '']">{{ formatDateTime(profile.kyc.reviewed_at) }}</p>
                  </div>
                </div>
              </div>

              <div v-if="profile.kyc.reviewer_comment" class="mb-4">
                <label :class="['profile-label', isDarkMode ? 'text-white-50' : '']">Reviewer Comment</label>
                <div 
                  class="reviewer-comment-box p-3 rounded-3" 
                  :style="isDarkMode ? 'background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);' : 'background-color: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.1);'"
                >
                  <p :class="isDarkMode ? 'mb-0 text-white' : 'mb-0 text-dark'">{{ profile.kyc.reviewer_comment }}</p>
                </div>
              </div>

              <hr class="my-4" :style="isDarkMode ? 'border-color: rgba(255,255,255,0.1);' : 'border-color: rgba(0,0,0,0.1);'">

              <!-- DOCUMENTS -->
              <div>
                <h6 :class="isDarkMode ? 'fw-bold mb-3 text-white' : 'fw-bold mb-3 text-dark'">Uploaded Documents</h6>
                <div class="row g-3">
                  <div v-for="doc in kycDocs" :key="doc.label" class="col-md-6">
                    <div 
                      class="document-item p-3 rounded-3 d-flex align-items-center justify-content-between" 
                      :style="isDarkMode ? 'background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);' : 'background-color: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.1);'"
                    >
                      <div class="d-flex align-items-center gap-3">
                        <div 
                          class="document-icon-box rounded-2 d-flex align-items-center justify-content-center" 
                          :style="isDarkMode ? 'width: 40px; height: 40px; background-color: rgba(255,255,255,0.1);' : 'width: 40px; height: 40px; background-color: rgba(0,0,0,0.05);'"
                        >
                          <FileText :size="20" :class="isDarkMode ? 'text-white-50' : 'text-muted'" />
                        </div>
                        <div>
                          <p :class="isDarkMode ? 'mb-0 fw-medium text-white' : 'mb-0 fw-medium text-dark'">{{ doc.label }}</p>
                          <small :class="isDarkMode ? 'text-white-50' : 'text-muted'">{{ doc.file ? 'Uploaded' : 'Not uploaded' }}</small>
                        </div>
                      </div>
                      <div>
                        <a v-if="doc.file" href="#" @click.prevent="openModal(doc.file)" class="btn btn-sm btn-outline-primary rounded-pill px-3">
                          View
                        </a>
                        <span v-else class="text-muted small">—</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- File Preview Modal -->
    <div v-if="showModal" class="modal-backdrop" @click="showModal = false" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 2000; display: flex; align-items: center; justify-content: center;">
      <div class="bg-white rounded-4 shadow-lg modal-container" style="width: 30vw; height: 30vh; z-index: 2001; display: flex; flex-direction: column;" @click.stop>
        <div class="p-4 border-bottom d-flex justify-content-between align-items-center" style="flex-shrink: 0;">
          <h5 class="fw-bold mb-0">Document Preview</h5>
          <button class="btn btn-link p-0" @click="showModal = false" style="font-size: 1.5rem; line-height: 1;">&times;</button>
        </div>
        <div class="modal-body" style="flex: 1; display: flex; align-items: center; justify-content: center; padding: 15px; overflow: auto; min-height: 0;">
          <iframe v-if="modalFile" :src="fileUrl(modalFile)" class="document-iframe" style="border: none; width: 100%; height: 85%;"></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { 
  LayoutDashboard, 
  Users, 
  Send, 
  FileText, 
  MessageSquare, 
  LogOut, 
  Wallet,
  Moon,
  Sun,
  AlertCircle
} from 'lucide-vue-next';
import { useDarkMode } from "@/composables/useDarkMode";

export default {
  name: "Profile",
  components: {
    LayoutDashboard,
    Users,
    Send,
    FileText,
    MessageSquare,
    LogOut,
    Wallet,
    Moon,
    Sun,
    AlertCircle
  },
  setup() {
    const { isDarkMode, toggleDarkMode } = useDarkMode()
    return {
      isDarkMode,
      toggleDarkMode,
      Moon,
      Sun
    }
  },
  data() {
    return {
      loading: true,
      error: null,
      profile: null,
      showModal: false,
      modalFile: null,
      customerId: Number(localStorage.getItem("customer_id")) || 1,
      customerName: localStorage.getItem("customer_name") || "Customer",
      showAccountNumber: false,
      accountNumberTimer: null,
      navItems: [
        { id: 'dashboard', label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
        { id: 'beneficiary', label: 'Beneficiaries', path: '/beneficiary', icon: Users },
        { id: 'transfer', label: 'Transfer Money', path: '/transfer', icon: Send },
        { id: 'history', label: 'Transactions', path: '/history', icon: FileText },
        { id: 'payments', label: 'Payments', path: '/payments', icon: Wallet },
        { id: 'chatbot', label: 'AI Assistant', path: '/chatbot', icon: MessageSquare },
        { id: 'disputes', label: 'Disputes', path: '/disputes', icon: AlertCircle }
      ]
    };
  },
  computed: {
    kycDocs() {
      if (!this.profile || !this.profile.kyc) return [];
      return [
        { label: "Aadhaar", file: this.profile.kyc.aadhaar_file },
        { label: "PAN", file: this.profile.kyc.pan_file },
        { label: "Photo", file: this.profile.kyc.photo_file },
        { label: "Signature", file: this.profile.kyc.signature_file },
      ];
    },
    maskedAccountNumber() {
      if (!this.profile || !this.profile.account || !this.profile.account.account_number) {
        return '***';
      }
      const accountNumber = this.profile.account.account_number.toString();
      let displayNumber;
      
      if (this.showAccountNumber) {
        displayNumber = accountNumber;
      } else {
        // Return asterisks equal to the number of digits in the account number
        displayNumber = '*'.repeat(accountNumber.length);
      }
      
      // Add space after every 5 digits
      return displayNumber.replace(/(.{5})/g, '$1 ').trim();
    }
  },
  methods: {
    getInitials(name) {
      return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    },
    navigate(path) {
      this.$router.push(path);
    },
    handleLogout() {
      localStorage.clear();
      this.$router.push("/");
    },
    fileUrl(path) {
      return `http://127.0.0.1:5000/profile/kyc_docs/${encodeURIComponent(path)}`;
    },
    kycStatusClass(status) {
      const classes = {
        approved: "text-success",
        rejected: "text-danger",
        pending: "text-warning",
      };
      return classes[status] || "text-muted";
    },
    getKycStatusBadgeClass(status) {
      const classes = {
        approved: "status-approved",
        rejected: "status-rejected",
        pending: "status-pending",
        not_submitted: "status-not-submitted"
      };
      return classes[status] || "status-not-submitted";
    },
    formatDateTime(timestamp) {
      if (!timestamp) return 'N/A';
      const date = new Date(timestamp);
      return date.toLocaleString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    async loadProfile() {
      try {
        const id = this.$route.params.customer_id || this.customerId;
        const res = await axios.get(`http://127.0.0.1:5000/customer/profile/${id}`);
        this.profile = res.data;
      } catch (err) {
        this.error = "Unable to load profile.";
        console.error("Error loading profile:", err);
      } finally {
        this.loading = false;
      }
    },
    openModal(file) {
      this.modalFile = file;
      this.showModal = true;
    },
    revealAccountNumber() {
      // Clear any existing timer
      if (this.accountNumberTimer) {
        clearTimeout(this.accountNumberTimer);
        this.accountNumberTimer = null;
      }
      
      // Show the account number
      this.showAccountNumber = true;
      
      // Set timer to hide after 3 seconds
      this.accountNumberTimer = setTimeout(() => {
        this.showAccountNumber = false;
        this.accountNumberTimer = null;
      }, 3000);
    },
    hideAccountNumber() {
      // Clear the timer if user moves mouse away before 3 seconds
      if (this.accountNumberTimer) {
        clearTimeout(this.accountNumberTimer);
        this.accountNumberTimer = null;
      }
      // Hide the account number immediately when mouse leaves
      this.showAccountNumber = false;
    }
  },
  beforeUnmount() {
    // Clean up timer when component is destroyed
    if (this.accountNumberTimer) {
      clearTimeout(this.accountNumberTimer);
      this.accountNumberTimer = null;
    }
  },
  mounted() {
    this.loadProfile();
  }
};
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
  transition: all 0.2s ease-in-out;
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

.modal-container {
  display: flex;
  flex-direction: column;
  width: 30vw;
  height: 30vh;
  min-width: 400px;
  min-height: 400px;
}

.modal-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 0;
  overflow: auto;
  padding: 15px;
  position: relative;
}

.document-iframe {
  width: 100%;
  height: 85%;
  border: none;
  flex-shrink: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.text-success {
  color: #198754 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.text-warning {
  color: #ffc107 !important;
}

.text-muted {
  color: #6c757d !important;
}

.profile-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.profile-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.1) !important;
}

.card-header-profile-customer {
  background: linear-gradient(135deg, rgba(13, 110, 253, 0.05) 0%, rgba(13, 110, 253, 0.02) 100%);
  border-bottom: 2px solid rgba(13, 110, 253, 0.1);
}

.card-header-profile-account {
  background: linear-gradient(135deg, rgba(25, 135, 84, 0.05) 0%, rgba(25, 135, 84, 0.02) 100%);
  border-bottom: 2px solid rgba(25, 135, 84, 0.1);
}

.card-header-profile-kyc {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.05) 0%, rgba(255, 193, 7, 0.02) 100%);
  border-bottom: 2px solid rgba(255, 193, 7, 0.1);
}

.profile-info-item {
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.profile-info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.profile-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #495057;
  margin-bottom: 0.5rem;
}

.profile-value {
  font-size: 1rem;
  font-weight: 500;
  color: #212529;
  margin-bottom: 0;
}

.account-number {
  font-family: 'Courier New', monospace;
  font-size: 1.1rem;
  font-weight: 600;
  color: #0d6efd;
  letter-spacing: 1px;
}

.balance-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #198754;
  font-family: 'Inter', sans-serif;
}

.account-type-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: rgba(13, 110, 253, 0.15);
  color: #0d6efd;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-active {
  background-color: rgba(25, 135, 84, 0.15);
  color: #198754;
}

.status-inactive {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
}

.status-approved {
  background-color: rgba(25, 135, 84, 0.15);
  color: #198754;
}

.status-rejected {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
}

.status-pending {
  background-color: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.status-not-submitted {
  background-color: rgba(108, 117, 125, 0.15);
  color: #6c757d;
}

.status-verified {
  background-color: rgba(25, 135, 84, 0.15);
  color: #198754;
}

.status-unverified {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
}

.reviewer-comment-box {
  background-color: rgba(255,255,255,0.05);
  border-left: 4px solid #0d6efd;
}

.document-item {
  background-color: rgba(255,255,255,0.05);
  transition: all 0.2s ease;
}

.document-item:hover {
  background-color: rgba(255,255,255,0.1);
  border-color: #0d6efd !important;
  transform: translateX(4px);
}

.document-icon-box {
  background-color: rgba(255,255,255,0.1) !important;
}

.profile-icon-box {
  transition: transform 0.2s ease;
}

.profile-card:hover .profile-icon-box {
  transform: scale(1.05);
}
</style>
