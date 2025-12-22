<template>
  <div class="dashboard-container p-4">
    <!-- Pending KYC Section -->
    <section class="content-section">
      <h2>Pending KYC</h2>
      <div class="kyc-actions" style="display:flex;gap:12px;align-items:center;margin-bottom:12px;">
        <button class="retry-btn" @click="fetchPendingKyc" :disabled="loadingPending">
          {{ loadingPending ? 'Refreshing...' : 'Refresh Pending KYC' }}
        </button>
        <div v-if="pendingKyc.length === 0" style="color:#666">No pending KYC</div>
      </div>

      <div v-if="loadingPending" class="loading" style="padding:20px;">
        <div class="spinner"></div>
        <p>Loading pending KYC...</p>
      </div>

      <div v-else class="kyc-list">
        <div
          v-for="kyc in pendingKyc"
          :key="kyc.kyc_id"
          class="task-item"
          style="flex-direction:column;align-items:stretch;"
        >
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;width:100%;">
            <div>
              <p style="font-weight:700;margin:0;">{{ kyc.customer_name }} <small style="color:#777">(#{{ kyc.customer_id }})</small></p>
              <p style="margin:4px 0;color:#555;font-size:0.95rem;">Submitted: <strong>{{ formatDate(kyc.submitted_at) }}</strong></p>
              <p style="margin:4px 0;color:#444;font-size:0.95rem;">
                Files:
                <span v-if="kyc.aadhaar_file">Aadhaar</span>
                <span v-if="kyc.pan_file">, PAN</span>
                <span v-if="kyc.photo_file">, Photo</span>
                <span v-if="kyc.signature_file">, Signature</span>
              </p>
            </div>

            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;">
              <div style="display:flex;gap:8px;">
                <button class="complete-btn" @click="analyzeKyc(kyc)" :disabled="kyc.analysisLoading">
                  <span v-if="kyc.analysisLoading">Analyzing...</span>
                  <span v-else>Analyze</span>
                </button>
                <button class="retry-btn" @click="viewFiles(kyc)">View</button>
              </div>
              <div v-if="kyc.ai_status" style="font-weight:700;margin-top:6px;">{{ kyc.ai_status }}</div>
            </div>
          </div>

          <!-- AI result -->
          <div v-if="kyc.aiResult" class="ai-result-container">
            <div class="ai-result-header">
              <div class="d-flex align-items-center gap-2 mb-3">
                <i class="bi bi-robot" style="font-size: 1.5rem; color: #0d6efd;"></i>
                <h6 class="fw-bold mb-0 text-primary">AI Analysis Complete</h6>
                <span :class="getStatusBadgeClass(kyc.ai_status)" class="status-badge">
                  {{ kyc.ai_status }}
                </span>
              </div>
            </div>

            <div class="ai-result-content">
              <div class="ai-remarks-section">
                <div class="section-header">
                  <i class="bi bi-chat-left-text me-2"></i>
                  <strong>AI Remarks</strong>
                </div>
                <div class="remarks-text">
                  {{ kyc.aiResult }}
                </div>
              </div>

              <div class="action-section">
                <div class="comment-section">
                  <label class="form-label fw-medium text-secondary mb-2">
                    <i class="bi bi-pencil-square me-1"></i>
                    Manager Comment (Optional)
                  </label>
                  <textarea 
                    v-model="kyc.managerComment" 
                    placeholder="Add your comments here..." 
                    class="form-control manager-comment"
                    rows="3"
                  ></textarea>
                </div>

                <div class="action-buttons">
                  <button 
                    class="btn btn-outline-danger px-4" 
                    @click="rejectKyc(kyc)" 
                    :disabled="kyc.actionLoading"
                  >
                    <i class="bi bi-x-circle me-2"></i>
                    Reject
                  </button>
                  <button 
                    class="btn btn-success px-4" 
                    @click="approveKyc(kyc)" 
                    :disabled="kyc.actionLoading"
                  >
                    <i class="bi bi-check-circle me-2"></i>
                    Approve
                  </button>
                </div>

                <div v-if="kyc.actionLoading" class="processing-indicator">
                  <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
                  <span class="text-muted">Processing...</span>
                </div>
              </div>
            </div>
          </div>

          <!-- waiting message -->
          <div v-else-if="kyc.analysisLoading" style="margin-top:12px;color:#777;">Waiting for AI response...</div>
        </div>
      </div>
    </section>

    <!-- Approve Confirmation Modal -->
    <div v-if="showApproveModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);" @click.self="closeApproveModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
          <!-- Modal Header -->
          <div class="modal-header bg-success bg-gradient text-white border-0 py-4">
            <div class="d-flex align-items-center justify-content-center gap-3 w-100">
              <div>
                <h5 class="fw-bold mb-0">GIROBANK</h5>
                <small class="opacity-75">Approve KYC</small>
              </div>
            </div>
            <button type="button" class="btn-close btn-close-white" @click="closeApproveModal" :disabled="isProcessing" aria-label="Close"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <div class="mb-3">
                <i class="bi bi-check-circle-fill" style="font-size: 3rem; color: #198754;"></i>
              </div>
              <h6 class="fw-bold text-dark mb-2">Approve KYC Submission</h6>
              <p class="text-muted mb-0">Are you sure you want to approve this KYC submission?</p>
            </div>

            <!-- KYC Details -->
            <div class="bg-light rounded-3 p-3 mb-4">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted small">Customer Name:</span>
                <span class="fw-bold text-dark">{{ selectedKyc?.customer_name || 'N/A' }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted small">Customer ID:</span>
                <span class="fw-medium text-dark">#{{ selectedKyc?.customer_id || 'N/A' }}</span>
              </div>
              <div v-if="selectedKyc?.ai_status" class="d-flex justify-content-between align-items-center">
                <span class="text-muted small">AI Status:</span>
                <span :class="getStatusBadgeClass(selectedKyc.ai_status)" class="status-badge">{{ selectedKyc.ai_status }}</span>
              </div>
            </div>

            <!-- Manager Comment Display -->
            <div v-if="selectedKyc?.managerComment" class="mb-3">
              <label class="form-label fw-medium text-secondary mb-2">Your Comment:</label>
              <div class="bg-white border rounded-3 p-3">
                <p class="mb-0 text-dark">{{ selectedKyc.managerComment }}</p>
              </div>
            </div>

            <!-- Success/Error Message -->
            <div v-if="actionMessage.type" :class="`alert alert-${actionMessage.type === 'success' ? 'success' : 'danger'} mb-0`" role="alert">
              <i :class="`bi bi-${actionMessage.type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2`"></i>
              {{ actionMessage.text }}
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer border-0 pt-0 px-4 pb-4">
            <button type="button" class="btn btn-light px-4" @click="closeApproveModal" :disabled="isProcessing">Cancel</button>
            <button type="button" class="btn btn-success px-4" @click="confirmApprove" :disabled="isProcessing">
              <span v-if="isProcessing" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              {{ isProcessing ? 'Processing...' : 'Confirm & Approve' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Reject Confirmation Modal -->
    <div v-if="showRejectModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);" @click.self="closeRejectModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
          <!-- Modal Header -->
          <div class="modal-header bg-danger bg-gradient text-white border-0 py-4">
            <div class="d-flex align-items-center justify-content-center gap-3 w-100">
              <div>
                <h5 class="fw-bold mb-0">GIROBANK</h5>
                <small class="opacity-75">Reject KYC</small>
              </div>
            </div>
            <button type="button" class="btn-close btn-close-white" @click="closeRejectModal" :disabled="isProcessing" aria-label="Close"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <div class="mb-3">
                <i class="bi bi-x-circle-fill" style="font-size: 3rem; color: #dc3545;"></i>
              </div>
              <h6 class="fw-bold text-dark mb-2">Reject KYC Submission</h6>
              <p class="text-muted mb-0">Are you sure you want to reject this KYC submission?</p>
            </div>

            <!-- KYC Details -->
            <div class="bg-light rounded-3 p-3 mb-4">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted small">Customer Name:</span>
                <span class="fw-bold text-dark">{{ selectedKyc?.customer_name || 'N/A' }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted small">Customer ID:</span>
                <span class="fw-medium text-dark">#{{ selectedKyc?.customer_id || 'N/A' }}</span>
              </div>
              <div v-if="selectedKyc?.ai_status" class="d-flex justify-content-between align-items-center">
                <span class="text-muted small">AI Status:</span>
                <span :class="getStatusBadgeClass(selectedKyc.ai_status)" class="status-badge">{{ selectedKyc.ai_status }}</span>
              </div>
            </div>

            <!-- Manager Comment Display -->
            <div v-if="selectedKyc?.managerComment" class="mb-3">
              <label class="form-label fw-medium text-secondary mb-2">Your Comment:</label>
              <div class="bg-white border rounded-3 p-3">
                <p class="mb-0 text-dark">{{ selectedKyc.managerComment }}</p>
              </div>
            </div>

            <!-- Warning Message -->
            <div class="alert alert-warning mb-0" role="alert">
              <i class="bi bi-exclamation-triangle me-2"></i>
              <small>This action cannot be undone. The customer will be notified of the rejection.</small>
            </div>

            <!-- Success/Error Message -->
            <div v-if="actionMessage.type" :class="`alert alert-${actionMessage.type === 'success' ? 'success' : 'danger'} mt-3 mb-0`" role="alert">
              <i :class="`bi bi-${actionMessage.type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2`"></i>
              {{ actionMessage.text }}
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer border-0 pt-0 px-4 pb-4">
            <button type="button" class="btn btn-light px-4" @click="closeRejectModal" :disabled="isProcessing">Cancel</button>
            <button type="button" class="btn btn-danger px-4" @click="confirmReject" :disabled="isProcessing">
              <span v-if="isProcessing" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              {{ isProcessing ? 'Processing...' : 'Confirm & Reject' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Analyze Confirmation Modal -->
    <div v-if="showAnalyzeModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);" @click.self="closeAnalyzeModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
          <!-- Modal Header -->
          <div class="modal-header bg-primary bg-gradient text-white border-0 py-4">
            <div class="d-flex align-items-center justify-content-center gap-3 w-100">
              <div>
                <h5 class="fw-bold mb-0">GIROBANK</h5>
                <small class="opacity-75">Confirm Analysis</small>
              </div>
            </div>
            <button type="button" class="btn-close btn-close-white" @click="closeAnalyzeModal" aria-label="Close"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <div class="mb-3">
                <i class="bi bi-shield-check" style="font-size: 3rem; color: #0d6efd;"></i>
              </div>
              <h6 class="fw-bold text-dark mb-2">Analyze KYC Documents</h6>
              <p class="text-muted mb-0">Are you sure you want to analyze this KYC submission?</p>
            </div>

            <!-- KYC Details -->
            <div class="bg-light rounded-3 p-3 mb-4">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted small">Customer Name:</span>
                <span class="fw-bold text-dark">{{ selectedKyc?.customer_name || 'N/A' }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted small">Customer ID:</span>
                <span class="fw-medium text-dark">#{{ selectedKyc?.customer_id || 'N/A' }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-muted small">Submitted:</span>
                <span class="fw-medium text-dark">{{ selectedKyc ? formatDate(selectedKyc.submitted_at) : 'N/A' }}</span>
              </div>
            </div>

            <div class="alert alert-info mb-0" role="alert">
              <small><i class="bi bi-info-circle me-2"></i>This will use AI to analyze the KYC documents and provide verification status.</small>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer border-0 pt-0 px-4 pb-4">
            <button type="button" class="btn btn-light px-4" @click="closeAnalyzeModal">Cancel</button>
            <button type="button" class="btn btn-primary px-4" @click="confirmAnalyze" :disabled="isAnalyzing">
              <span v-if="isAnalyzing" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              {{ isAnalyzing ? 'Analyzing...' : 'Confirm & Analyze' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const pendingKyc = ref([]);
const loadingPending = ref(false);
const showAnalyzeModal = ref(false);
const showApproveModal = ref(false);
const showRejectModal = ref(false);
const selectedKyc = ref(null);
const isAnalyzing = ref(false);
const isProcessing = ref(false);
const actionMessage = ref({ type: '', text: '' });
const BASE = 'http://127.0.0.1:5000';

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

const getStatusBadgeClass = (status) => {
  if (!status) return 'badge bg-secondary';
  const statusLower = status.toLowerCase();
  if (statusLower.includes('approved') || statusLower.includes('verified') || statusLower === 'valid') {
    return 'badge bg-success';
  } else if (statusLower.includes('rejected') || statusLower.includes('invalid') || statusLower === 'fraud') {
    return 'badge bg-danger';
  } else if (statusLower.includes('pending') || statusLower.includes('review')) {
    return 'badge bg-warning text-dark';
  }
  return 'badge bg-info';
};

const fetchPendingKyc = async () => {
  loadingPending.value = true;
  try {
    const res = await fetch(`${BASE}/manager/kyc/pending`);
    if (!res.ok) throw new Error('Failed to fetch pending KYC');
    const data = await res.json();
    pendingKyc.value = data.map(k => ({
      ...k,
      analysisLoading: false,
      actionLoading: false,
      aiResult: null,
      ai_status: null,
      managerComment: ''
    }));
  } catch (err) {
    console.error('fetchPendingKyc error', err);
    alert('Could not load pending KYC at this time.');
  } finally {
    loadingPending.value = false;
  }
};

const viewFiles = (kyc) => {
  const fileUrl = kyc.aadhaar_file || kyc.pan_file || kyc.photo_file || kyc.signature_file;
  if (!fileUrl) {
    alert('No file link available.');
    return;
  }
  const encodedPath = encodeURIComponent(fileUrl);
  const fullUrl = `${BASE}/profile/kyc_docs/${encodedPath}`;
  window.open(fullUrl, '_blank');
};

const analyzeKyc = (kyc) => {
  selectedKyc.value = kyc;
  showAnalyzeModal.value = true;
};

const closeAnalyzeModal = () => {
  if (!isAnalyzing.value) {
    showAnalyzeModal.value = false;
    selectedKyc.value = null;
  }
};

const confirmAnalyze = async () => {
  if (!selectedKyc.value) return;

  const kyc = selectedKyc.value;
  isAnalyzing.value = true;
  kyc.analysisLoading = true;
  kyc.aiResult = null;
  kyc.ai_status = null;

  try {
    const res = await fetch(`${BASE}/api/kyc/analyze/${kyc.kyc_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`AI analyze failed: ${text}`);
    }

    const json = await res.json();
    kyc.aiResult = json.ai_remarks || 'No remarks returned';
    kyc.ai_status = json.ai_status || 'Unknown';
    
    // Close modal on success
    showAnalyzeModal.value = false;
    selectedKyc.value = null;
  } catch (err) {
    console.error('analyzeKyc error', err);
    alert('AI analysis failed. See console for details.');
  } finally {
    kyc.analysisLoading = false;
    isAnalyzing.value = false;
  }
};

const approveKyc = (kyc) => {
  selectedKyc.value = kyc;
  actionMessage.value = { type: '', text: '' };
  showApproveModal.value = true;
};

const closeApproveModal = () => {
  if (!isProcessing.value) {
    showApproveModal.value = false;
    selectedKyc.value = null;
    actionMessage.value = { type: '', text: '' };
  }
};

const confirmApprove = async () => {
  if (!selectedKyc.value) return;

  const kyc = selectedKyc.value;
  isProcessing.value = true;
  kyc.actionLoading = true;
  actionMessage.value = { type: '', text: '' };

  try {
    const payload = { comment: kyc.managerComment || '' };
    const res = await fetch(`${BASE}/manager/kyc/approve/${kyc.kyc_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(errText || 'Approve failed');
    }
    const json = await res.json();
    actionMessage.value = { type: 'success', text: json.message || 'KYC approved successfully!' };
    
    // Close modal and remove from list after a short delay
    setTimeout(() => {
      showApproveModal.value = false;
      pendingKyc.value = pendingKyc.value.filter(p => p.kyc_id !== kyc.kyc_id);
      selectedKyc.value = null;
    }, 1500);
  } catch (err) {
    console.error('approveKyc error', err);
    actionMessage.value = { type: 'error', text: err.message || 'Failed to approve KYC. Please try again.' };
  } finally {
    kyc.actionLoading = false;
    isProcessing.value = false;
  }
};

const rejectKyc = (kyc) => {
  selectedKyc.value = kyc;
  actionMessage.value = { type: '', text: '' };
  showRejectModal.value = true;
};

const closeRejectModal = () => {
  if (!isProcessing.value) {
    showRejectModal.value = false;
    selectedKyc.value = null;
    actionMessage.value = { type: '', text: '' };
  }
};

const confirmReject = async () => {
  if (!selectedKyc.value) return;

  const kyc = selectedKyc.value;
  isProcessing.value = true;
  kyc.actionLoading = true;
  actionMessage.value = { type: '', text: '' };

  try {
    const payload = { comment: kyc.managerComment || '' };
    const res = await fetch(`${BASE}/manager/kyc/reject/${kyc.kyc_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(errText || 'Reject failed');
    }
    const json = await res.json();
    actionMessage.value = { type: 'success', text: json.message || 'KYC rejected successfully!' };
    
    // Close modal and remove from list after a short delay
    setTimeout(() => {
      showRejectModal.value = false;
      pendingKyc.value = pendingKyc.value.filter(p => p.kyc_id !== kyc.kyc_id);
      selectedKyc.value = null;
    }, 1500);
  } catch (err) {
    console.error('rejectKyc error', err);
    actionMessage.value = { type: 'error', text: err.message || 'Failed to reject KYC. Please try again.' };
  } finally {
    kyc.actionLoading = false;
    isProcessing.value = false;
  }
};

onMounted(() => {
  fetchPendingKyc();
});
</script>

<style scoped>
.dashboard-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  color: #333;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

.content-section h2 {
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

.retry-btn {
  background-color: #4a90e2;
  color: white;
  padding: 10px 25px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.retry-btn:hover {
  background-color: #357abd;
}

.complete-btn {
  background-color: #4a90e2;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.complete-btn:hover {
  background-color: #357abd;
}

.kyc-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 8px;
}

.task-item {
  background: #ffffff;
  padding: 18px 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.ai-result-container {
  margin-top: 16px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border: 2px solid #e0e7ff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.1);
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

.ai-result-header {
  border-bottom: 2px solid #e0e7ff;
  padding-bottom: 12px;
  margin-bottom: 16px;
}

.status-badge {
  font-size: 0.75rem;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ai-result-content {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 20px;
}

.ai-remarks-section {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.section-header {
  color: #495057;
  font-size: 0.9rem;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.remarks-text {
  color: #212529;
  font-size: 0.95rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  border-left: 3px solid #0d6efd;
}

.action-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-section {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.manager-comment {
  border: 1px solid #dee2e6;
  border-radius: 6px;
  resize: vertical;
  font-size: 0.9rem;
}

.manager-comment:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.action-buttons .btn {
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.action-buttons .btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.processing-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  font-size: 0.85rem;
}

@media (max-width: 992px) {
  .ai-result-content {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .btn {
    width: 100%;
  }
}

.modal {
  z-index: 1055;
}

.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
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
</style>


