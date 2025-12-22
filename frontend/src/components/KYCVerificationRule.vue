<template>
  <div class="kyc-rule">
    <h2>KYC Verification with AI Rule Assistant</h2>

    <div class="details">
      <p><strong>Customer Name:</strong> Emma Wilson</p>
      <p><strong>Account Number:</strong> ****2345</p>
      <p><strong>Request Type:</strong> New Account</p>
      <p><strong>Submitted Date:</strong> 2025-10-14</p>
    </div>

    <h3>Document Upload & OCR Processing</h3>
    <div class="upload-section">
      <div>
        <p>Aadhaar Card</p>
        <input type="file" />
        <p>OCR Status: Ready</p>
      </div>
      <div>
        <p>PAN Card</p>
        <input type="file" />
        <p>OCR Status: Ready</p>
      </div>
    </div>

    <button>Extract Text with Tesseract OCR</button>
  </div>
</template>

<style scoped>
.kyc-rule { padding: 20px; }
.upload-section { display: flex; gap: 20px; margin-top: 10px; }
.upload-section div { border: 1px dashed #aaa; padding: 10px; }
</style>
