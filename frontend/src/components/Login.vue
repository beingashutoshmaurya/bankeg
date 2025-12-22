<template>
  <div class="d-flex min-vh-100 align-items-center justify-content-center bg-light font-sans" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5 col-lg-4">
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
              <h5 class="fw-bold text-dark mb-4 text-center">Login</h5>

              <!-- Role Selection -->
              <div class="mb-4">
                <label class="form-label fw-medium text-secondary">Login as</label>
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

              <!-- Customer Login Fields -->
              <template v-if="form.role === 'customer' || !form.role">
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Account Number</label>
                  <input 
                    type="text" 
                    v-model="form.account_number" 
                    @input="form.account_number = form.account_number.replace(/\D/g, '').slice(0, 15)"
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your account number"
                    maxlength="15"
                  />
                  <small v-if="form.account_number && form.account_number.length !== 15" class="text-danger">Account number must be 15 digits</small>
                </div>
                <div class="mb-4">
                  <label class="form-label fw-medium text-secondary">Login Password</label>
                  <input 
                    type="password" 
                    v-model="form.password" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your password"
                  />
                </div>
              </template>

              <!-- Employee/Manager Login Fields -->
              <template v-else>
                <div class="mb-3">
                  <label class="form-label fw-medium text-secondary">Email</label>
                  <input 
                    type="email" 
                    v-model="form.email" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your email"
                  />
                </div>
                <div class="mb-4">
                  <label class="form-label fw-medium text-secondary">Password</label>
                  <input 
                    type="password" 
                    v-model="form.password" 
                    class="form-control form-control-lg border-2"
                    placeholder="Enter your password"
                  />
                </div>
              </template>

              <!-- Error Message -->
              <div v-if="errorMessage" class="alert alert-danger border-0 rounded-3 mb-3" role="alert">
                <small class="fw-medium">{{ errorMessage }}</small>
              </div>

              <!-- Success Message -->
              <div v-if="successMessage" class="alert alert-success border-0 rounded-3 mb-3" role="alert">
                <small class="fw-medium">{{ successMessage }}</small>
              </div>

              <!-- Submit Button -->
              <button 
                class="btn btn-primary btn-lg w-100 rounded-3 fw-semibold shadow-sm mb-3"
                @click="login" 
                :disabled="!isFormValid || loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                {{ form.role === 'customer' || !form.role ? 'Send OTP' : 'Login' }}
              </button>

              <!-- Register Link -->
              <div class="text-center">
                <small class="text-muted">Don't have an account?</small>
                <button 
                  class="btn btn-link p-0 ms-1 text-decoration-none fw-medium"
                  @click="$router.push('/register')"
                >
                  Register
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

const form = ref({ 
  role: 'customer',
  account_number: "", 
  email: "",
  password: "" 
});
const errorMessage = ref("");
const successMessage = ref("");
const loading = ref(false);

const isFormValid = computed(() => {
  if (!form.value.role) return false;
  if (form.value.role === 'customer') {
    return form.value.account_number && form.value.account_number.length === 15 && form.value.password;
  } else {
    return form.value.email && form.value.password;
  }
});

const onRoleChange = () => {
  form.value.account_number = "";
  form.value.email = "";
  form.value.password = "";
  errorMessage.value = "";
  successMessage.value = "";
};

const login = async () => {
  errorMessage.value = "";
  successMessage.value = "";
  loading.value = true;

  try {
    if (form.value.role === 'customer') {
      const res = await api.post("/login", {
        account_number: form.value.account_number,
        password: form.value.password
      });
      
      if (res.status === 200) {
        successMessage.value = "OTP sent to your email. Please verify.";
        localStorage.setItem("temp_account_number", form.value.account_number);
        setTimeout(() => {
          router.push("/verify");
        }, 1500);
      }
    } else if (form.value.role === 'employee') {
      const res = await api.post("/api/employee/login", {
        email: form.value.email,
        password: form.value.password
      });
      
      if (res.status === 201 || res.data?.message === "Login successful") {
        localStorage.setItem("employee_id", res.data.employee_id);
        localStorage.setItem("employee_name", res.data.name || "Employee");
        localStorage.setItem("employee_email", res.data.email);
        localStorage.setItem("user_role", "employee");
        router.push("/employee-dashboard");
      }
    } else if (form.value.role === 'manager') {
      const res = await api.post("/api/manager/login", {
        email: form.value.email,
        password: form.value.password
      });
      
      if (res.status === 201 || res.data?.message === "Login successful") {
        localStorage.setItem("manager_id", res.data.manager_id);
        localStorage.setItem("manager_name", res.data.name || "Manager");
        localStorage.setItem("manager_email", res.data.email);
        localStorage.setItem("user_role", "manager");
        router.push("/manager-dashboard");
      }
    }
  } catch (err) {
    errorMessage.value = err.response?.data?.message || "Login failed. Please check your credentials.";
    console.error("Login error:", err);
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
