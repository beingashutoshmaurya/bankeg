import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import VerifyOtp from '../components/VerifyOTP.vue'
import ForgotPassword from '../components/ForgotPassword.vue'
import ResetPassword from '../components/ResetPassword.vue'
import Dashboard from '../components/Dashboard.vue'
import KYCUpload from "../components/KYCUpload.vue";
import Beneficiary from '../components/Beneficiary.vue'
import KYCOTP from '@/components/KYCOTP.vue'
import AIAssistent from '@/components/AIAssistent.vue'
import ManagerPanel from '@/components/ManagerPanel.vue'
import ManagerDashboardLayout from '@/components/ManagerDashboardLayout.vue'
import ManagerDashboardHome from '@/components/ManagerDashboardHome.vue'
import ManagerActiveTasks from '@/components/ManagerActiveTasks.vue'
import ManagerCreateTask from '@/components/ManagerCreateTask.vue'
import EmployeeDashboard from '@/components/EmployeeDashboard.vue'
import EmployeeDashboardHome from '@/components/EmployeeDashboardHome.vue'
import PendingKYC from '@/components/PendingKYC.vue'
import CustomerIssues from '@/components/CustomerIssues.vue'
import Payments from '@/components/Payments.vue'
import Profile from '@/components/Profile.vue'
import TransactionConfirm from '@/components/TransactionConfirm.vue'
import TransactionConfirmBill from '@/components/TransactionConfirmBill.vue'
import CustomerDisputes from '@/components/CustomerDisputes.vue'

const routes = [
  // Customer routes (flat structure - preserved)
  { path: '/', name: 'home', component: Home },
  { path: "/login", name: 'login', component: Login },
  { path: "/register", name: 'register', component: Register },
  { path: "/verify", name: 'VerifyOtp', component: VerifyOtp },
  { path: "/forgot", name: 'ForgotPassword', component: ForgotPassword },
  { path: "/reset", name: 'ResetPassword', component: ResetPassword },
  { path: "/dashboard", name: 'Dashboard', component: Dashboard },
  { path: "/transfer", name: 'Transfer', component: Dashboard },
  { path: "/beneficiary", name: 'Beneficiary', component: Beneficiary },
  { path: "/history", name: 'History', component: Dashboard },
  { path: "/kyc-upload/:customer_id", component: KYCUpload },
  { path: "/kyc-otp/:customer_id", component: KYCOTP },
  { path: "/chatbot", component: AIAssistent},
  { path: "/payments", name: "Payments", component: Payments },
  { path: "/profile", name: "Profile", component: Profile },
  { path: "/disputes", name: "CustomerDisputes", component: CustomerDisputes },
  { path: "/transaction-confirm", name: "TransactionConfirm", component: TransactionConfirm },
  { path: "/transaction-confirm-bill", name: "TransactionConfirmBill", component: TransactionConfirmBill },
  
  // Manager routes (nested structure)
  { path: "/manager", component: ManagerPanel}, // Keep existing for backward compatibility
  {
    path: "/manager-dashboard",
    component: ManagerDashboardLayout,
    children: [
      { path: '', component: ManagerDashboardHome },
      { path: 'active-tasks', component: ManagerActiveTasks },
      { path: 'create-task', component: ManagerCreateTask }
    ]
  },
  
  // Employee routes (nested structure)
  {
    path: "/employee-dashboard",
    component: EmployeeDashboard,
    children: [
      { path: '', component: EmployeeDashboardHome },
      { path: 'pending-kyc', component: PendingKYC },
      { path: 'customer-issues', component: CustomerIssues }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Update document title
router.beforeEach((to, from, next) => {
  document.title = 'GIROBANK';
  next();
})

export default router
