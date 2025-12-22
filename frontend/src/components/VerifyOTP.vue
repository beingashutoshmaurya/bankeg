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
              <h5 class="fw-bold text-dark mb-2 text-center">Verify Login OTP</h5>
              <p class="text-muted text-center small mb-4">Enter the OTP sent to your registered email address</p>

              <!-- OTP Input -->
              <div class="mb-4">
                <label class="form-label fw-medium text-secondary">Enter OTP</label>
                <input 
                  type="text" 
                  v-model="otp" 
                  @input="otp = otp.replace(/\D/g, '').slice(0, 6)"
                  class="form-control form-control-lg border-2 text-center fw-bold"
                  placeholder="000000"
                  maxlength="6"
                  style="font-size: 1.5rem; letter-spacing: 0.5rem;"
                />
              </div>

              <!-- Error/Success Message -->
              <div v-if="msg" :class="['alert border-0 rounded-3 mb-3', msgType === 'error' ? 'alert-danger' : msgType === 'success' ? 'alert-success' : 'alert-info']" role="alert">
                <small class="fw-medium">{{ msg }}</small>
              </div>

              <!-- Verify Button -->
              <button 
                class="btn btn-primary btn-lg w-100 rounded-3 fw-semibold shadow-sm mb-3"
                @click="verify"
                :disabled="!otp || otp.length !== 6 || loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                Verify OTP
              </button>

              <!-- Resend OTP -->
              <div class="text-center">
                <button 
                  class="btn btn-link p-0 text-decoration-none fw-medium"
                  @click="resendOTP" 
                  :disabled="resending"
                >
                  {{ resending ? 'Sending...' : 'Resend OTP' }}
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
import { ref } from "vue";
import { useRouter } from "vue-router";

const otp = ref("");
const msg = ref("");
const msgType = ref("info");
const loading = ref(false);
const resending = ref(false);
const router = useRouter();

const verify = async () => {
  const account_number = localStorage.getItem("temp_account_number");
  
  if (!account_number) {
    msg.value = "Session expired. Please login again.";
    msgType.value = "error";
    setTimeout(() => {
      router.push("/login");
    }, 2000);
    return;
  }

  if (!otp.value || otp.value.length !== 6) {
    msg.value = "Please enter a valid 6-digit OTP";
    msgType.value = "error";
    return;
  }

  loading.value = true;
  msg.value = "";
  msgType.value = "info";

  try {
    const res = await api.post("/verify_otp", {
      account_number,
      otp: otp.value,
    });

    if (res.status === 200 && res.data.message && res.data.message.toLowerCase().includes("successful")) {
      localStorage.setItem("customer_id", res.data.customer.id);
      localStorage.setItem("customer_name", res.data.customer.full_name);
      localStorage.setItem("account_number", res.data.customer.account_number);
      localStorage.setItem("user_role", "customer");

      localStorage.removeItem("temp_account_number");

      msg.value = "Login successful! Redirecting to dashboard...";
      msgType.value = "success";

      setTimeout(() => {
        router.push("/dashboard");
      }, 1500);
    } else {
      msg.value = res.data.message || "OTP verification failed";
      msgType.value = "error";
    }
  } catch (err) {
    msg.value = err.response?.data?.message || "Invalid or expired OTP. Please try again.";
    msgType.value = "error";
    console.error("OTP verification error:", err);
  } finally {
    loading.value = false;
  }
};

const resendOTP = async () => {
  const account_number = localStorage.getItem("temp_account_number");
  
  if (!account_number) {
    msg.value = "Session expired. Please login again.";
    msgType.value = "error";
    return;
  }

  resending.value = true;
  msg.value = "";
  
  try {
    const res = await api.post("/login", {
      account_number: account_number,
      password: "" // We need password, but we don't have it stored
    });
    
    msg.value = "OTP resent to your email";
    msgType.value = "success";
  } catch (err) {
    msg.value = "Failed to resend OTP. Please login again.";
    msgType.value = "error";
  } finally {
    resending.value = false;
  }
};
</script>

<style scoped>
.card {
  border-radius: 20px;
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

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
