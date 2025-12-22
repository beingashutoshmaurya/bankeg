<template>
  <v-container>
    <v-card class="pa-5 mx-auto" max-width="400">
      <v-card-title>Reset Password</v-card-title>
      <v-card-text>
        <v-text-field label="Email" v-model="form.email" />
        <v-text-field label="OTP" v-model="form.otp" />
        <v-text-field label="New Password" v-model="form.new_password" type="password" />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="resetPassword">Reset</v-btn>
      </v-card-actions>
      <v-alert v-if="msg" type="info" class="mt-2">{{ msg }}</v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref } from "vue";

const form = ref({ email: "", otp: "", new_password: "" });
const msg = ref("");

const resetPassword = async () => {
  const res = await api.post("/reset_password", form.value);
  msg.value = res.data.message;
};
</script>
