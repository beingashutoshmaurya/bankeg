<template>
  <v-container>
    <v-card class="pa-4 mt-6" max-width="520" style="margin:auto;">
      <h2 class="mb-4">Confirm Transaction</h2>

      <div>
        <div><strong>Beneficiary:</strong> {{ beneficiary_account }}</div>
        <div><strong>Amount:</strong> ₹{{ amount }}</div>
        <div v-if="remarks"><strong>Remarks:</strong> {{ remarks }}</div>
      </div>

      <v-alert v-if="info" type="info" class="mt-3">{{ info }}</v-alert>

      <v-row class="mt-4" align="center">
        <v-col cols="8">
          <v-text-field
            v-model="otp"
            @input="otp = otp.replace(/\D/g, '').slice(0, 6)"
            label="Transaction OTP"
            maxlength="6"
            hint="Enter 6-digit OTP sent to your email"
            persistent-hint
          />
        </v-col>
        <v-col cols="4">
          <v-btn :disabled="resendDisabled" @click="resendOtp">Resend</v-btn>
        </v-col>
      </v-row>

      <v-text-field
        v-model="transaction_password"
        label="Transaction Password"
        type="password"
        class="mt-2"
      />

      <v-row justify="end" class="mt-4">
        <v-btn text @click="$router.back()">Cancel</v-btn>
        <v-btn color="success" @click="confirmTransfer">Confirm Transfer</v-btn>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "TransactionConfirm",
  data() {
    return {
      session_id: this.$route.query.session_id || null,
      customer_id: this.$route.query.customer_id || Number(localStorage.getItem("customer_id")),
      amount: this.$route.query.amount || "",
      beneficiary_account: this.$route.query.beneficiary_account || "",
      remarks: this.$route.query.remarks || "",
      otp: "",
      transaction_password: "",
      info: "An OTP was sent to your registered email when you initiated the transaction.",
      resendDisabled: false,
      resendTimer: 0,
      resendIntervalId: null
    };
  },
  mounted() {
    // if session_id missing, we should not proceed — show alert and go back
    if (!this.session_id) {
      alert("Session missing. Please initiate transfer again from dashboard.");
      this.$router.push({ name: "Dashboard" }); // adjust name if different
    }
  },
  methods: {
    startResendTimer(sec = 30) {
      this.resendDisabled = true;
      this.resendTimer = sec;
      this.resendIntervalId = setInterval(() => {
        this.resendTimer -= 1;
        if (this.resendTimer <= 0) {
          clearInterval(this.resendIntervalId);
          this.resendDisabled = false;
        }
      }, 1000);
    },

    async resendOtp() {
      try {
        this.resendDisabled = true;
        // Call initiate-transfer again to generate a new OTP (it will create a new OTPVerification row)
        const res = await axios.post("http://127.0.0.1:5000/customer/initiate-transfer", {
          customer_id: this.customer_id,
          amount: this.amount,
          beneficiary_account: this.beneficiary_account,
          remarks: this.remarks
        });
        this.session_id = res.data.session_id;
        this.info = "A new OTP was sent to your registered email.";
        this.startResendTimer(30);
      } catch (err) {
        this.resendDisabled = false;
        alert(err.response?.data?.message || "Failed to resend OTP");
      }
    },

    async confirmTransfer() {
      if (!this.otp || !this.transaction_password) {
        alert("Please enter OTP and transaction password");
        return;
      }

      try {
        const res = await axios.post("http://127.0.0.1:5000/customer/confirm-transfer", {
          session_id: this.session_id,
          otp: this.otp,
          transaction_password: this.transaction_password,
          customer_id: this.customer_id,
          amount: this.amount,
          beneficiary_account: this.beneficiary_account,
          remarks: this.remarks
        });

        // Backend's confirm-transfer calls transfer_funds internally and returns its response
        alert(res.data.message || "Transfer completed");
        // refresh dashboard data after returning
        this.$router.push({ name: "Dashboard" });
      } catch (err) {
        alert(err.response?.data?.message || "Verification/Transfer failed");
      }
    }
  },
  beforeDestroy() {
    if (this.resendIntervalId) clearInterval(this.resendIntervalId);
  }
};
</script>




