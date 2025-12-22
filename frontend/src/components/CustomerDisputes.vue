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
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Customer Disputes</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">Raise and track your disputes with the bank</p>
        </div>
      </header>

      <!-- Content Area -->
      <div class="p-4">
        <div class="row g-4">
          <!-- Left Column - Disputes List -->
          <div class="col-lg-7">
            <div class="card border-0 shadow-sm rounded-4" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
              <div class="card-header border-bottom p-4" :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''">
                <h5 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">My Disputes</h5>
              </div>
              <div class="card-body p-4">
                <div v-if="loading" class="text-center py-5">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div v-else-if="disputes.length === 0" class="text-center py-5">
                  <p :class="isDarkMode ? 'text-white-50' : 'text-muted'">No disputes raised yet</p>
                </div>
                <div v-else class="d-flex flex-column gap-3">
                  <div
                    v-for="dispute in disputes"
                    :key="dispute.id"
                    class="card border-0 shadow-sm rounded-3 p-4 transition-all dispute-card"
                    :class="[
                      dispute.status.toLowerCase() === 'pending' ? 'issue-pending' : 'issue-resolved',
                      expandedDisputes[dispute.id] ? 'expanded' : ''
                    ]"
                    :style="dispute.status.toLowerCase() === 'pending' 
                      ? 'background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(255, 193, 7, 0.05) 100%); border-left: 4px solid #ffc107 !important;' 
                      : 'background: linear-gradient(135deg, rgba(25, 135, 84, 0.1) 0%, rgba(25, 135, 84, 0.05) 100%); border-left: 4px solid #198754 !important;'"
                    @click="toggleDispute(dispute.id)"
                  >
                    <div class="d-flex justify-content-between align-items-start mb-3">
                      <div class="flex-grow-1">
                        <h6 :class="isDarkMode ? 'fw-bold text-white mb-2' : 'fw-bold text-dark mb-2'">{{ dispute.title }}</h6>
                        <p :class="isDarkMode ? 'text-white-50 mb-2 small' : 'text-muted mb-2 small'">{{ dispute.description }}</p>
                        <small :class="isDarkMode ? 'text-white-50' : 'text-muted'">
                          Raised on: {{ formatDate(dispute.created_date) }}
                        </small>
                      </div>
                      <span 
                        class="badge rounded-pill px-3 py-2 fw-medium"
                        :class="dispute.status.toLowerCase() === 'pending' ? 'bg-warning text-dark' : 'bg-success text-white'"
                      >
                        {{ dispute.status }}
                      </span>
                    </div>
                    <div v-if="dispute.resolution_summary" class="expand-section">
                      <div 
                        v-if="!expandedDisputes[dispute.id]"
                        class="d-flex align-items-center gap-2 mt-2 pt-2 border-top expand-hint"
                        :style="isDarkMode ? 'border-color: rgba(255,255,255,0.1) !important;' : ''"
                        @click.stop="toggleDispute(dispute.id)"
                      >
                        <i class="bi bi-arrows-angle-expand" :class="isDarkMode ? 'text-white-50' : 'text-muted'"></i>
                        <small :class="isDarkMode ? 'text-white-50' : 'text-muted'">Click to view full summary</small>
                      </div>
                      <div 
                        v-else
                        class="mt-3 pt-3 border-top resolution-content"
                        :style="isDarkMode ? 'border-color: rgba(255,255,255,0.1) !important;' : ''"
                      >
                        <p :class="isDarkMode ? 'text-white-50 mb-2 small fw-medium' : 'text-muted mb-2 small fw-medium'">
                          <i class="bi bi-check-circle me-2"></i>Resolution:
                        </p>
                        <p :class="isDarkMode ? 'text-white mb-0' : 'text-dark mb-0'" style="white-space: pre-wrap; line-height: 1.6;">{{ dispute.resolution_summary }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column - Create New Dispute Form -->
          <div class="col-lg-5">
            <div class="card border-0 shadow-sm rounded-4" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
              <div class="card-header border-bottom p-4" :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''">
                <h5 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Raise New Dispute</h5>
              </div>
              <div class="card-body p-4">
                <form @submit.prevent="createDispute">
                  <div class="mb-3">
                    <label class="form-label fw-medium" :class="isDarkMode ? 'text-white' : 'text-secondary'">Title</label>
                    <input 
                      type="text" 
                      v-model="newDispute.title"
                      class="form-control border-2"
                      :class="isDarkMode ? 'bg-dark text-white border-secondary' : ''"
                      placeholder="Enter dispute title"
                      required
                    />
                  </div>
                  <div class="mb-4">
                    <label class="form-label fw-medium" :class="isDarkMode ? 'text-white' : 'text-secondary'">Description</label>
                    <textarea 
                      v-model="newDispute.description"
                      class="form-control border-2"
                      :class="isDarkMode ? 'bg-dark text-white border-secondary' : ''"
                      rows="5"
                      placeholder="Describe your dispute in detail..."
                      required
                    ></textarea>
                  </div>
                  <div v-if="errorMessage" class="alert alert-danger border-0 rounded-3 mb-3" role="alert">
                    <small class="fw-medium">{{ errorMessage }}</small>
                  </div>
                  <div v-if="successMessage" class="alert alert-success border-0 rounded-3 mb-3" role="alert">
                    <small class="fw-medium">{{ successMessage }}</small>
                  </div>
                  <button 
                    type="submit"
                    class="btn btn-primary w-100 rounded-3 fw-semibold shadow-sm"
                    :disabled="submitting"
                  >
                    <span v-if="submitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    {{ submitting ? 'Submitting...' : 'Submit Dispute' }}
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {
  LayoutDashboard,
  Send,
  Users,
  FileText,
  MessageSquare,
  LogOut,
  Wallet,
  Moon,
  Sun,
  AlertCircle
} from "lucide-vue-next";
import { useDarkMode } from "@/composables/useDarkMode";

export default {
  name: "CustomerDisputes",
  components: {
    LayoutDashboard,
    Send,
    Users,
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
      customerId: Number(localStorage.getItem("customer_id")),
      customerName: localStorage.getItem("customer_name") || "Customer",
      disputes: [],
      loading: false,
      submitting: false,
      errorMessage: "",
      successMessage: "",
      expandedDisputes: {}, // Track which disputes are expanded
      newDispute: {
        title: "",
        description: ""
      },
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
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    },
    toggleDispute(disputeId) {
      // Only allow expansion if there's a resolution summary
      const dispute = this.disputes.find(d => d.id === disputeId);
      if (dispute && dispute.resolution_summary) {
        this.expandedDisputes[disputeId] = !this.expandedDisputes[disputeId];
      }
    },
    async fetchDisputes() {
      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/issue/get?customer_id=${this.customerId}`);
        if (response.status === 200) {
          this.disputes = response.data;
          // Sort: pending first, then resolved
          this.disputes.sort((a, b) => {
            if (a.status.toLowerCase() === 'pending' && b.status.toLowerCase() !== 'pending') return -1;
            if (a.status.toLowerCase() !== 'pending' && b.status.toLowerCase() === 'pending') return 1;
            return 0;
          });
        }
      } catch (error) {
        console.error("Error fetching disputes:", error);
      } finally {
        this.loading = false;
      }
    },
    async createDispute() {
      if (!this.newDispute.title.trim() || !this.newDispute.description.trim()) {
        this.errorMessage = "Please fill in all fields";
        return;
      }

      this.submitting = true;
      this.errorMessage = "";
      this.successMessage = "";

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/issue/create', {
          title: this.newDispute.title,
          description: this.newDispute.description,
          customer_id: this.customerId
        });

        if (response.status === 201) {
          this.successMessage = "Dispute raised successfully!";
          this.newDispute.title = "";
          this.newDispute.description = "";
          // Refresh disputes list
          await this.fetchDisputes();
          // Clear success message after 3 seconds
          setTimeout(() => {
            this.successMessage = "";
          }, 3000);
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Failed to create dispute. Please try again.";
        console.error("Error creating dispute:", error);
      } finally {
        this.submitting = false;
      }
    }
  },
  mounted() {
    this.fetchDisputes();
  }
};
</script>

<style scoped>
.issue-pending {
  transition: all 0.3s ease;
}

.issue-pending:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.2) !important;
}

.issue-resolved {
  transition: all 0.3s ease;
}

.issue-resolved:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25, 135, 84, 0.2) !important;
}

.dispute-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.dispute-card:hover {
  transform: translateY(-2px);
}

.expand-hint {
  cursor: pointer;
  transition: all 0.2s ease;
}

.expand-hint:hover {
  opacity: 0.8;
}

.expand-hint i {
  transition: transform 0.3s ease;
}

.dispute-card.expanded .expand-hint i {
  transform: rotate(180deg);
}

.resolution-content {
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 1000px;
  }
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

.sidebar {
  flex-shrink: 0;
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

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.avatar {
  width: 40px;
  height: 40px;
  font-size: 14px;
}

.font-sans {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
</style>

