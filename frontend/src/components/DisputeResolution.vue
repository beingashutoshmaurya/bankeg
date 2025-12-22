<template>
  <div class="dispute">
    <h2>Dispute Resolution</h2>

    <div class="stats">
      <div>Pending Tasks: 3</div>
      <div>Completed: 2</div>
      <div>Verifications: 2</div>
      <div>High Priority: 2</div>
    </div>

    <button>+ Create New Task</button>

    <div v-for="(dispute, i) in disputes" :key="i" class="dispute-card">
      <p><strong>{{ dispute.title }}</strong></p>
      <span :class="dispute.priority">{{ dispute.priority.toUpperCase() }}</span>
      <p>Customer: {{ dispute.customer }}</p>
      <p>{{ dispute.complaint }}</p>
      <p><strong>Transaction ID:</strong> {{ dispute.txn }}</p>
      <p><strong>Date:</strong> {{ dispute.date }}</p>
      <button>Generate Evidence Pack</button>
    </div>
  </div>
</template>

<script setup>
const disputes = [
  {
    title: "Transaction Dispute – Failed Payment",
    priority: "high",
    customer: "John Doe (ID: 1234)",
    complaint: "Payment failed but amount was debited",
    txn: "TXN987654321",
    date: "2025-10-14",
  },
  {
    title: "Unauthorized Transaction Query",
    priority: "medium",
    customer: "Alice Smith (ID: 5678)",
    complaint: "Did not authorize transfer of $500",
    txn: "TXN123456789",
    date: "2025-10-13",
  },
];
</script>

<style scoped>
.dispute { padding: 20px; }
.dispute-card { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
.high { color: red; }
.medium { color: orange; }
</style>
