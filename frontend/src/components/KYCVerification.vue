<template>
  <div class="kyc">
    <h2>KYC Verification</h2>
    <div class="stats">
      <div>Pending Tasks: 3</div>
      <div>Completed: 2</div>
      <div>Verifications: 3</div>
      <div>High Priority: 2</div>
    </div>

    <button @click="$router.push('/employee-dashboard/kyc-rule')">+ Create New Task</button>

    <div v-for="(req, i) in requests" :key="i" class="req-card">
      <p><strong>{{ req.name }}</strong></p>
      <p>Account: {{ req.account }}</p>
      <p>Request Type: {{ req.type }}</p>
      <p>Submitted: {{ req.date }}</p>
      <button @click="$router.push('/employee-dashboard/kyc-rule')">Verify with KYC Assistant</button>
    </div>
  </div>
</template>

<script setup>
const requests = [
  { name: "Emma Wilson", account: "****2345", type: "New Account", date: "2025-10-14" },
  { name: "Michael Davis", account: "****6789", type: "KYC Update", date: "2025-10-13" },
  { name: "Sophia Martinez", account: "****0123", type: "Address Change", date: "2025-10-12" },
];
</script>

<style scoped>
.kyc { padding: 20px; }
.req-card { border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; }
</style>
