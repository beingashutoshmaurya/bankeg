<template>
  <v-container class="mt-6">
    <v-card class="pa-6">
      <h2 class="mb-4">Confirm Transaction</h2>

      <v-form @submit.prevent="confirmTransaction">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="otp"
              @input="otp = otp.replace(/\D/g, '').slice(0, 6)"
              label="Enter OTP"
              outlined
              required
              maxlength="6"
              hint="Enter 6-digit OTP"
              persistent-hint
            />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="transactionPassword"
              label="Transaction Password"
              type="password"
              outlined
              required
            />
          </v-col>

          <v-col cols="12" class="text-center">
            <v-btn color="primary" type="submit">Confirm Transaction</v-btn>
          </v-col>
        </v-row>
      </v-form>

      <v-snackbar v-model="snackbar.show" :color="snackbar.color">
        {{ snackbar.message }}
      </v-snackbar>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "TransactionConfirmBill",
  data() {
    return {
      otp: "",
      transactionPassword: "",
      snackbar: { show: false, message: "", color: "success" },
      sessionData: {}
    };
  },
  methods: {
    showSnackbar(message, color) {
      this.snackbar.message = message;
      this.snackbar.color = color;
      this.snackbar.show = true;
    },

    async confirmTransaction() {
      if (!this.otp || !this.transactionPassword) {
        this.showSnackbar("Please enter OTP and transaction password", "error");
        return;
      }

      const payload = {
        session_id: this.sessionData.session_id,
        customer_id: this.sessionData.customer_id,
        amount: this.sessionData.amount,
        otp: this.otp,
        transaction_password: this.transactionPassword
      };

      let url = "";
      switch (this.sessionData.type) {
        case "pay-bill":
          url = "http://127.0.0.1:5000/customer/confirm-pay-bill";
          payload.bill_type = this.sessionData.bill_type;
          payload.biller = this.sessionData.biller;
          payload.bill_account = this.sessionData.bill_account;
          break;
        case "recharge":
          url = "http://127.0.0.1:5000/customer/confirm-recharge";
          payload.recharge_type = this.sessionData.recharge_type;
          payload.operator = this.sessionData.operator;
          payload.number = this.sessionData.number;
          break;
        case "fastag":
          url = "http://127.0.0.1:5000/customer/confirm-fastag";
          payload.vehicle_number = this.sessionData.vehicle_number;
          payload.tag_id = this.sessionData.tag_id;
          break;
        default:
          this.showSnackbar("Invalid transaction type", "error");
          return;
      }

      try {
        const res = await axios.post(url, payload);
        this.showSnackbar(res.data.message || "Transaction successful", "success");
        // Optionally redirect to dashboard or success page
        setTimeout(() => this.$router.push({ path: "/payments" }), 1500);
      } catch (err) {
        this.showSnackbar(
          err.response?.data?.message || "Transaction failed",
          "error"
        );
      }
    }
  },
  mounted() {
    // Grab query params passed from initiate page
    this.sessionData = this.$route.query;
    
    // Check if session_id is present
    if (!this.sessionData.session_id) {
      alert("Session missing. Please initiate the transaction again.");
      this.$router.push({ path: "/payments" });
    }
  }
};
</script>


