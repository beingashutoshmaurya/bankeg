<template>
  <div class="d-flex min-vh-100 align-items-center justify-content-center bg-light font-sans py-4" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow-lg border-0 rounded-4 overflow-hidden">
            <!-- Header -->
            <div class="card-header bg-primary bg-gradient text-white text-center py-4 border-0">
              <div class="d-flex align-items-center justify-content-center gap-3 mb-2">
                <div class="logo-box bg-white bg-opacity-20 text-white rounded-3 d-flex align-items-center justify-content-center shadow-sm overflow-hidden" style="width: 50px; height: 50px;">
                  <img src="@/assets/bank.png" alt="GIROBANK" style="width: 100%; height: 100%; object-fit: contain; padding: 4px;" />
                </div>
                <div>
                  <h4 class="fw-bold mb-0">GIROBANK</h4>
                  <small class="opacity-75">Premium Banking</small>
                </div>
              </div>
            </div>

            <!-- Body -->
            <div class="card-body p-4">
              <h5 class="fw-bold text-dark mb-4 text-center">
                {{ form.role === 'customer' ? 'Register Customer' : form.role === 'employee' ? 'Register Employee' : 'Register Manager' }}
              </h5>

              <!-- Role Selection -->
              <div class="mb-4">
                <label class="form-label fw-medium text-secondary">Register as</label>
                <select 
                  v-model="form.role" 
                  @change="onRoleChange"
                  class="form-select form-select-lg border-2"
                >
                  <option value="customer">Customer</option>
                  <option value="employee">Employee</option>
                  <option value="manager">Manager</option>
                </select>
              </div>

              <!-- Customer Registration Fields -->
              <template v-if="form.role === 'customer' || !form.role">
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Full Name</label>
                  <input 
                    type="text" 
                    v-model="form.full_name" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your full name"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Email</label>
                  <input 
                    type="email" 
                    v-model="form.email" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your email"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Phone</label>
                  <input 
                    type="tel" 
                    v-model="form.phone" 
                    @input="form.phone = form.phone.replace(/\D/g, '').slice(0, 15)"
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your phone number"
                    maxlength="15"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Login Password</label>
                  <input 
                    type="password" 
                    v-model="form.login_password" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter login password (min 6 characters)"
                  />
                </div>
                <div class="mb-4">
                  <label class="form-label fw-medium text-secondary">Transaction Password</label>
                  <input 
                    type="password" 
                    v-model="form.transaction_password" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter transaction password (min 6 characters)"
                  />
                </div>
              </template>

              <!-- Employee Registration Fields -->
              <template v-else-if="form.role === 'employee'">
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Full Name</label>
                  <input 
                    type="text" 
                    v-model="form.name" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your full name"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Email</label>
                  <input 
                    type="email" 
                    v-model="form.email" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your email"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Contact Number</label>
                  <input 
                    type="tel" 
                    v-model="form.contact_number" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your contact number"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Password</label>
                  <input 
                    type="password" 
                    v-model="form.password" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter password (min 6 characters)"
                  />
                </div>
                <div class="mb-4">
                  <label class="form-label fw-medium text-secondary">Manager ID</label>
                  <input 
                    type="number" 
                    v-model="form.manager_id" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your manager's ID"
                  />
                  <small class="text-muted">Enter the ID of the manager who will supervise you</small>
                </div>
              </template>

              <!-- Manager Registration Fields -->
              <template v-else-if="form.role === 'manager'">
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Full Name</label>
                  <input 
                    type="text" 
                    v-model="form.name" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your full name"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Email</label>
                  <input 
                    type="email" 
                    v-model="form.email" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your email"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Contact Number</label>
                  <input 
                    type="tel" 
                    v-model="form.contact_number" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your contact number"
                  />
                </div>
                <div class="mb-4">
                  <label class="form-label fw-medium text-secondary">Password</label>
                  <input 
                    type="password" 
                    v-model="form.password" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter password (min 6 characters)"
                  />
                </div>
              </template>

              <!-- Message Alert -->
              <div v-if="msg" :class="['alert border-0 rounded-3 mb-3', msgType === 'error' ? 'alert-danger' : 'alert-success']" role="alert">
                <small class="fw-medium">{{ msg }}</small>
              </div>

              <!-- Submit Button -->
              <button 
                class="btn btn-primary btn-lg w-100 rounded-3 fw-semibold shadow-sm mb-3"
                @click="register" 
                :disabled="!isFormValid || loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                {{ getRegisterButtonText() }}
              </button>

              <!-- Login Link -->
              <div class="text-center">
                <small class="text-muted">Already have an account?</small>
                <button 
                  class="btn btn-link p-0 ms-1 text-decoration-none fw-medium"
                  @click="$router.push('/login')"
                >
                  Login
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from "../services/api";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const msg = ref("");
const msgType = ref("info");
const loading = ref(false);

const form = ref({
  role: 'customer',
  // Customer fields
  full_name: "",
  email: "",
  phone: "",
  login_password: "",
  transaction_password: "",
  // Employee/Manager fields
  name: "",
  contact_number: "",
  password: "",
  manager_id: ""
});

const isFormValid = computed(() => {
  if (!form.value.role) return false;
  
  if (form.value.role === 'customer') {
    return form.value.full_name && 
           form.value.email && 
           form.value.phone && 
           form.value.login_password && 
           form.value.transaction_password;
  } else if (form.value.role === 'employee') {
    return form.value.name && 
           form.value.email && 
           form.value.contact_number && 
           form.value.password && 
           form.value.manager_id;
  } else if (form.value.role === 'manager') {
    return form.value.name && 
           form.value.email && 
           form.value.contact_number && 
           form.value.password;
  }
  return false;
});

const onRoleChange = () => {
  form.value.full_name = "";
  form.value.email = "";
  form.value.phone = "";
  form.value.login_password = "";
  form.value.transaction_password = "";
  form.value.name = "";
  form.value.contact_number = "";
  form.value.password = "";
  form.value.manager_id = "";
  msg.value = "";
  msgType.value = "info";
};

const getRegisterButtonText = () => {
  if (form.value.role === 'customer') {
    return 'Continue to KYC';
  } else if (form.value.role === 'employee') {
    return 'Register Employee';
  } else {
    return 'Register Manager';
  }
};

const register = async () => {
  loading.value = true;
  msg.value = "";
  msgType.value = "info";

  try {
    if (form.value.role === 'customer') {
      const res = await api.post("/register", {
        full_name: form.value.full_name,
        email: form.value.email,
        phone: form.value.phone,
        login_password: form.value.login_password,
        transaction_password: form.value.transaction_password
      });
      
      msg.value = res.data.message;
      msgType.value = "success";
      
      setTimeout(() => {
        router.push(`/kyc-upload/${res.data.customer_id}`);
      }, 1500);
      
    } else if (form.value.role === 'employee') {
      const res = await api.post("/api/employee/register", {
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
        contact_number: form.value.contact_number,
        manager_id: parseInt(form.value.manager_id)
      });
      
      msg.value = res.data.message;
      msgType.value = res.status === 201 ? "success" : "error";
      
      if (res.status === 201) {
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      }
      
    } else if (form.value.role === 'manager') {
      const res = await api.post("/api/manager/register", {
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
        contact_number: form.value.contact_number
      });
      
      msg.value = res.data.message;
      msgType.value = res.status === 201 ? "success" : "error";
      
      if (res.status === 201) {
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      }
    }
  } catch (e) {
    msg.value = e.response?.data?.message || "Registration failed. Please try again.";
    msgType.value = "error";
    console.error("Registration error:", e);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.card {
  border-radius: 20px;
}

.form-control:focus,
.form-select:focus {
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

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
