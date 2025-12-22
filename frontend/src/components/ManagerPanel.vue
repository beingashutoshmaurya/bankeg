<!-- <template>
  <v-container>
    <h2 class="mb-5">Manager – KYC Verification Panel</h2>

    <v-data-table :headers="headers" :items="kycList" class="elevation-1">
      <template v-slot:item.identity_file="{ item }">
        <a :href="fileUrl(item.identity_file)" target="_blank">View ID</a>
      </template>

      <template v-slot:item.address_file="{ item }">
        <a :href="fileUrl(item.address_file)" target="_blank">View Address</a>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-btn small color="success" @click="approve(item.kyc_id)">Approve</v-btn>
        <v-btn small color="error" class="ml-2" @click="reject(item.kyc_id)">Reject</v-btn>
      </template>
    </v-data-table>

    <v-alert v-if="msg" type="info" class="mt-3">{{ msg }}</v-alert>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref, onMounted } from "vue";

const kycList = ref([]);
const msg = ref("");

const headers = [
  { title: "KYC ID", key: "kyc_id" },
  { title: "Customer Name", key: "full_name" },
  { title: "Email", key: "email" },
  { title: "Phone", key: "phone" },
  { title: "ID Proof", key: "identity_file" },
  { title: "Address Proof", key: "address_file" },
  { title: "Actions", key: "actions", sortable: false },
];

const fileUrl = (filename) => {
  return `http://localhost:5000/uploads/${filename}`;
};

const loadKYC = async () => {
  const res = await api.get("/manager/kyc/pending");
  kycList.value = res.data.pending_kyc;
};

const approve = async (id) => {
  const res = await api.post(`/manager/kyc/approve/${id}`);
  msg.value = res.data.message;
  loadKYC();
};

const reject = async (id) => {
  const reason = prompt("Enter rejection reason:");
  if (!reason) return;

  const res = await api.post(`/manager/kyc/reject/${id}`, { reason });
  msg.value = res.data.message;
  loadKYC();
};

onMounted(loadKYC);
</script> -->


<template>
  <v-container>
    <h2 class="mb-4">KYC Pending Approvals</h2>

    <v-data-table
      :headers="headers"
      :items="pendingKyc"
      class="elevation-1"
    >

      <template v-slot:item.actions="{ item }">
        <v-btn color="green" small @click="approve(item.kyc_id)">Approve</v-btn>
        <v-btn color="red" small @click="reject(item.kyc_id)">Reject</v-btn>
      </template>

      <template v-slot:item.documents="{ item }">
        <v-btn small :href="docUrl(item.aadhaar_file)" target="_blank">Aadhaar</v-btn>
        <v-btn small :href="docUrl(item.pan_file)" target="_blank">PAN</v-btn>
        <v-btn small :href="docUrl(item.photo_file)" target="_blank">Photo</v-btn>
        <v-btn small :href="docUrl(item.signature_file)" target="_blank">Signature</v-btn>
      </template>

    </v-data-table>

    <!-- Reject Dialog -->
    <v-dialog v-model="rejectDialog" persistent max-width="400">
      <v-card>
        <v-card-title>Enter Rejection Comment</v-card-title>
        <v-card-text>
          <v-textarea v-model="rejectionComment" outlined></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="rejectDialog = false">Cancel</v-btn>
          <v-btn color="red" @click="confirmReject">Reject</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      pendingKyc: [],
      rejectDialog: false,
      rejectId: null,
      rejectionComment: "",
      headers: [
        { text: "Customer", value: "customer_name" },
        { text: "Submitted At", value: "submitted_at" },
        { text: "Documents", value: "documents" },
        { text: "Actions", value: "actions" },
      ]
    };
  },

  created() {
    this.loadPending();
  },

  methods: {
    loadPending() {
      axios.get("http://localhost:5000/manager/kyc/pending")
        .then(res => this.pendingKyc = res.data);
    },

    docUrl(fileName) {
      return `http://localhost:5000/kyc_docs/${fileName}`;
    },

    approve(id) {
      axios.post(`http://localhost:5000/manager/kyc/approve/${id}`)
        .then(() => this.loadPending());
    },

    reject(id) {
      this.rejectId = id;
      this.rejectDialog = true;
    },

    confirmReject() {
      axios.post(`http://localhost:5000/manager/kyc/reject/${this.rejectId}`, {
        comment: this.rejectionComment
      }).then(() => {
        this.rejectDialog = false;
        this.rejectionComment = "";
        this.loadPending();
      });
    }
  }
};
</script>
