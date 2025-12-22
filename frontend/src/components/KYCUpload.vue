<template>
  <div class="d-flex min-vh-100 align-items-center justify-content-center bg-light font-sans py-4" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-7">
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
              <h5 class="fw-bold text-dark mb-2 text-center">Upload KYC Documents</h5>
              <p class="text-muted text-center small mb-4">Please upload the following documents to complete your registration</p>

              <!-- File Uploads -->
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-medium text-secondary">
                    Aadhaar Card (PDF/Image)
                  </label>
                  <input 
                    type="file" 
                    @change="handleFileChange($event, 'aadhaar')"
                    accept="image/*,.pdf"
                    class="form-control form-control-lg border-2"
                  />
                  <small v-if="aadhaar" class="text-success">
                    ✓ {{ aadhaar.name }}
                  </small>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-medium text-secondary">
                    PAN Card (PDF/Image)
                  </label>
                  <input 
                    type="file" 
                    @change="handleFileChange($event, 'pan')"
                    accept="image/*,.pdf"
                    class="form-control form-control-lg border-2"
                  />
                  <small v-if="pan" class="text-success">
                    ✓ {{ pan.name }}
                  </small>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-medium text-secondary">
                    Photograph
                  </label>
                  <input 
                    type="file" 
                    @change="handleFileChange($event, 'photo')"
                    accept="image/*"
                    class="form-control form-control-lg border-2"
                  />
                  <small v-if="photo" class="text-success">
                    ✓ {{ photo.name }}
                  </small>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-medium text-secondary">
                    Signature
                  </label>
                  <input 
                    type="file" 
                    @change="handleFileChange($event, 'signature')"
                    accept="image/*"
                    class="form-control form-control-lg border-2"
                  />
                  <small v-if="signature" class="text-success">
                    ✓ {{ signature.name }}
                  </small>
                </div>
              </div>

              <!-- Message Alert -->
              <div v-if="msg" :class="['alert border-0 rounded-3 mt-4', msgType === 'error' ? 'alert-danger' : 'alert-success']" role="alert">
                <small class="fw-medium">{{ msg }}</small>
              </div>

              <!-- Submit Button -->
              <div class="mt-4">
                <button 
                  class="btn btn-primary btn-lg w-100 rounded-3 fw-semibold shadow-sm"
                  @click="uploadKYC"
                  :disabled="!isFormValid || loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  Upload Documents & Continue
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
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const msg = ref("");
const msgType = ref("info");
const loading = ref(false);

const aadhaar = ref(null);
const pan = ref(null);
const photo = ref(null);
const signature = ref(null);

const handleFileChange = (event, type) => {
  const file = event.target.files[0];
  if (type === 'aadhaar') aadhaar.value = file;
  else if (type === 'pan') pan.value = file;
  else if (type === 'photo') photo.value = file;
  else if (type === 'signature') signature.value = file;
};

const isFormValid = computed(() => {
  return aadhaar.value && pan.value && photo.value && signature.value;
});

const uploadKYC = async () => {
  if (!isFormValid.value) {
    msg.value = "Please upload all required documents";
    msgType.value = "error";
    return;
  }

  loading.value = true;
  msg.value = "";
  msgType.value = "info";

  const formData = new FormData();
  formData.append("aadhaar", aadhaar.value);
  formData.append("pan", pan.value);
  formData.append("photo", photo.value);
  formData.append("signature", signature.value);

  try {
    const uploadRes = await api.post(`/kyc/upload/${route.params.customer_id}`, formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    if (uploadRes.status === 200) {
      msg.value = "Documents uploaded successfully. Sending OTP to your email...";
      msgType.value = "success";

      await api.post(`/kyc/send_otp/${route.params.customer_id}`);

      setTimeout(() => {
        router.push(`/kyc-otp/${route.params.customer_id}`);
      }, 1500);
    }
  } catch (err) {
    msg.value = err.response?.data?.message || "Upload failed. Please try again.";
    msgType.value = "error";
    console.error("KYC upload error:", err);
  } finally {
    loading.value = false;
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
