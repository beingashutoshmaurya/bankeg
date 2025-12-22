<template>
  <div class="d-flex min-vh-100 font-sans" :class="isDarkMode ? 'bg-dark' : 'bg-light'" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
    <!-- Sidebar -->
    <div class="sidebar d-flex flex-column shadow-sm" style="width: 280px; position: fixed; height: 100vh; overflow-y: auto; z-index: 1000; background-color: #1e293b;">
      <!-- Logo/Header -->
      <div class="p-4 mb-2">
        <div class="d-flex align-items-center gap-3 mb-4">
          <div>
            <h5 class="fw-bold text-white mb-0">GIROBANK</h5>
            <small class="text-white-50">Premium Banking</small>
          </div>
        </div>
        
        <div 
          class="user-profile p-3 rounded-3 d-flex align-items-center gap-3 cursor-pointer hover-bg-light-transition" 
          style="background-color: rgba(255,255,255,0.05);"
          @click="$router.push('/profile')"
        >
          <div class="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center fw-bold">
            {{ getInitials(customerName) }}
          </div>
          <div class="overflow-hidden">
            <h6 class="text-white mb-0 text-truncate">{{ customerName }}</h6>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <div class="flex-grow-1 px-3">
        <p class="text-uppercase text-white-50 fw-bold ms-2 mb-2" style="font-size: 0.75rem; letter-spacing: 1px;">Menu</p>
        <div class="d-grid gap-1">
          <button
            v-for="item in navItems"
            :key="item.id"
            @click="navigate(item.path)"
            :class="[
              'btn text-start d-flex align-items-center gap-3 px-3 py-2 rounded-3 transition-all',
              $route.path === item.path
                ? 'bg-primary text-white shadow-sm'
                : 'btn-ghost-dark text-white-50 hover-text-white'
            ]"
          >
            <component :is="item.icon" :size="20" />
            <span class="fw-medium">{{ item.label }}</span>
          </button>
        </div>
      </div>

      <!-- Dark Mode Toggle -->
      <div class="px-3 py-2 border-top border-secondary border-opacity-25">
        <button 
          class="btn btn-ghost-dark text-white-50 w-100 d-flex align-items-center justify-content-between px-3 py-2 rounded-3 transition-all hover-text-white"
          @click="toggleDarkMode"
        >
          <div class="d-flex align-items-center gap-3">
            <component :is="isDarkMode ? Sun : Moon" :size="20" />
            <span class="fw-medium">{{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}</span>
          </div>
        </button>
      </div>

      <!-- Logout -->
      <div class="p-3 border-top border-secondary border-opacity-25">
        <button 
          class="logout-btn w-100 d-flex align-items-center justify-content-center gap-2 py-2"
          @click="handleLogout"
        >
          <LogOut :size="18" />
          <span class="fw-semibold">Sign Out</span>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-grow-1 overflow-auto" style="margin-left: 280px;">
      <!-- Top Header -->
      <header 
        class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center sticky-top shadow-sm"
        :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'"
        :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''"
      >
        <div>
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Payments & Recharges</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">Manage your utility bills, recharges, and Fastag top-ups.</p>
        </div>
        <div class="d-flex align-items-center gap-3">
          <button class="btn btn-light rounded-circle p-2 position-relative">
            <Bell :size="20" class="text-secondary" />
            <!-- <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle" v-if="unreadCount > 0">
              <span class="visually-hidden">New alerts</span>
            </span> -->
          </button>
        </div>
      </header>

      <div class="p-4 p-lg-5" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
        
        <!-- Payment Sections using Tabs or Accordion-like simplified stacked cards -->
        <div class="row g-4">
            
          <!-- Pay a Bill -->
          <div class="col-lg-4">
             <div class="card border-0 shadow-sm rounded-4 h-100" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
                <div class="card-header border-bottom p-4" :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''">
                  <div class="d-flex align-items-center gap-3">
                     <div class="rounded-circle bg-primary-subtle text-primary p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
                        <FileText :size="24" />
                     </div>
                     <h5 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Pay Bill</h5>
                  </div>
                </div>
                <div class="card-body p-4" :style="isDarkMode ? 'background-color: #1e293b;' : ''">
                   <form @submit.prevent="payBill">
                      <div class="mb-3">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Bill Type</label>
                         <div class="dropdown">
                           <button 
                             :class="[
                               'btn w-100 text-start d-flex align-items-center justify-content-between border-0 py-2',
                               isDarkMode ? 'bg-dark text-white' : 'btn-light',
                               {'text-muted': !bill.bill_type && !isDarkMode, 'text-white-50': !bill.bill_type && isDarkMode}
                             ]"
                             :style="isDarkMode ? 'background-color: #0f172a; color: white;' : 'background-color: #f8f9fa;'"
                             type="button" 
                             id="billTypeDropdown"
                             data-bs-toggle="dropdown" 
                             aria-expanded="false"
                           >
                             <span class="d-flex align-items-center gap-2">
                               <component 
                                 v-if="bill.bill_type && getBillTypeIcon(bill.bill_type)" 
                                 :is="getBillTypeIcon(bill.bill_type)" 
                                 :size="20"
                                 class="text-primary"
                               />
                               <span>{{ bill.bill_type || 'Select Bill Type' }}</span>
                             </span>
                             <i class="bi bi-chevron-down"></i>
                           </button>
                           <ul class="dropdown-menu w-100" aria-labelledby="billTypeDropdown">
                             <li v-for="type in billOptions.bill_types" :key="type">
                               <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" @click.prevent="selectBillType(type)">
                                 <component 
                                   v-if="getBillTypeIcon(type)" 
                                   :is="getBillTypeIcon(type)" 
                                   :size="20"
                                   class="text-primary"
                                 />
                                 <span>{{ type }}</span>
                               </a>
                             </li>
                           </ul>
                         </div>
                      </div>
                      <div class="mb-3">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Biller</label>
                         <div class="dropdown">
                           <button 
                             :class="[
                               'btn w-100 text-start d-flex align-items-center justify-content-between border-0 py-2',
                               isDarkMode ? 'bg-dark text-white' : 'btn-light',
                               {'text-muted': !bill.biller && !isDarkMode, 'text-white-50': !bill.biller && isDarkMode}
                             ]"
                             :style="isDarkMode ? 'background-color: #0f172a; color: white;' : 'background-color: #f8f9fa;'"
                             type="button" 
                             :id="'billerDropdown'"
                             data-bs-toggle="dropdown" 
                             aria-expanded="false"
                           >
                             <span class="d-flex align-items-center gap-2">
                               <img 
                                 v-if="bill.biller && getServiceLogo(bill.biller)" 
                                 :src="getServiceLogo(bill.biller)" 
                                 :alt="bill.biller"
                                 style="width: 24px; height: 24px; object-fit: contain;"
                                 class="rounded"
                               />
                               <span>{{ bill.biller || 'Select Biller' }}</span>
                             </span>
                             <i class="bi bi-chevron-down"></i>
                           </button>
                           <ul class="dropdown-menu w-100" :aria-labelledby="'billerDropdown'">
                             <li v-for="biller in getBillerList(bill.bill_type)" :key="biller">
                               <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" @click.prevent="selectBiller(biller)">
                                 <img 
                                   v-if="getServiceLogo(biller)" 
                                   :src="getServiceLogo(biller)" 
                                   :alt="biller"
                                   style="width: 24px; height: 24px; object-fit: contain;"
                                   class="rounded"
                                   onerror="this.style.display='none'"
                                 />
                                 <span>{{ biller }}</span>
                               </a>
                             </li>
                           </ul>
                         </div>
                      </div>
                      <div class="mb-3">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Consumer No</label>
                         <input 
                           v-model="bill.bill_account" 
                           type="text" 
                           class="form-control border-0 py-2" 
                           :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                           :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                           placeholder="Account / Consumer No" 
                           required
                         >
                      </div>
                      <div class="mb-4">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Amount</label>
                         <input 
                           v-model="bill.amount" 
                           type="number" 
                           class="form-control border-0 py-2" 
                           :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                           :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                           placeholder="Enter amount" 
                           required
                         >
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 fw-medium shadow-sm hover-lift" :disabled="isLoadingBill">
                        <Loader2 v-if="isLoadingBill" :size="18" class="me-2 spinner" />
                        {{ isLoadingBill ? 'Processing...' : 'Pay Bill' }}
                      </button>
                   </form>
                </div>
             </div>
          </div>

          <!-- Recharge -->
          <div class="col-lg-4">
             <div class="card border-0 shadow-sm rounded-4 h-100" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
                <div class="card-header border-bottom p-4" :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''">
                  <div class="d-flex align-items-center gap-3">
                     <div class="rounded-circle bg-success-subtle text-success p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
                        <Smartphone :size="24" />
                     </div>
                     <h5 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Recharge</h5>
                  </div>
                </div>
                <div class="card-body p-4" :style="isDarkMode ? 'background-color: #1e293b;' : ''">
                   <form @submit.prevent="recharge">
                      <div class="mb-3">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Type</label>
                         <div class="dropdown">
                           <button 
                             :class="[
                               'btn w-100 text-start d-flex align-items-center justify-content-between border-0 py-2',
                               isDarkMode ? 'bg-dark text-white' : 'btn-light',
                               {'text-muted': !rechargeData.recharge_type && !isDarkMode, 'text-white-50': !rechargeData.recharge_type && isDarkMode}
                             ]"
                             :style="isDarkMode ? 'background-color: #0f172a; color: white;' : 'background-color: #f8f9fa;'"
                             type="button" 
                             id="rechargeTypeDropdown"
                             data-bs-toggle="dropdown" 
                             aria-expanded="false"
                           >
                             <span class="d-flex align-items-center gap-2">
                               <component 
                                 v-if="rechargeData.recharge_type && getRechargeTypeIcon(rechargeData.recharge_type)" 
                                 :is="getRechargeTypeIcon(rechargeData.recharge_type)" 
                                 :size="20"
                                 class="text-success"
                               />
                               <span>{{ rechargeData.recharge_type || 'Select Type' }}</span>
                             </span>
                             <i class="bi bi-chevron-down"></i>
                           </button>
                           <ul class="dropdown-menu w-100" aria-labelledby="rechargeTypeDropdown">
                             <li>
                               <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" @click.prevent="selectRechargeType('Mobile')">
                                 <Smartphone :size="20" class="text-success" />
                                 <span>Mobile</span>
                               </a>
                             </li>
                             <li>
                               <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" @click.prevent="selectRechargeType('DTH')">
                                 <Zap :size="20" class="text-warning" />
                                 <span>DTH</span>
                               </a>
                             </li>
                           </ul>
                         </div>
                      </div>
                      <div class="mb-3">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Operator</label>
                         <div class="dropdown">
                           <button 
                             :class="[
                               'btn w-100 text-start d-flex align-items-center justify-content-between border-0 py-2',
                               isDarkMode ? 'bg-dark text-white' : 'btn-light',
                               {'text-muted': !rechargeData.operator && !isDarkMode, 'text-white-50': !rechargeData.operator && isDarkMode}
                             ]"
                             :style="isDarkMode ? 'background-color: #0f172a; color: white;' : 'background-color: #f8f9fa;'"
                             type="button" 
                             :id="'operatorDropdown'"
                             data-bs-toggle="dropdown" 
                             aria-expanded="false"
                           >
                             <span class="d-flex align-items-center gap-2">
                               <img 
                                 v-if="rechargeData.operator && getServiceLogo(rechargeData.operator)" 
                                 :src="getServiceLogo(rechargeData.operator)" 
                                 :alt="rechargeData.operator"
                                 style="width: 24px; height: 24px; object-fit: contain;"
                                 class="rounded"
                               />
                               <span>{{ rechargeData.operator || 'Select Operator' }}</span>
                             </span>
                             <i class="bi bi-chevron-down"></i>
                           </button>
                           <ul class="dropdown-menu w-100" :aria-labelledby="'operatorDropdown'">
                             <li v-for="op in (rechargeData.recharge_type === 'Mobile' ? billOptions.mobile_operators : billOptions.dth_providers)" :key="op">
                               <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" @click.prevent="selectOperator(op)">
                                 <img 
                                   v-if="getServiceLogo(op)" 
                                   :src="getServiceLogo(op)" 
                                   :alt="op"
                                   style="width: 24px; height: 24px; object-fit: contain;"
                                   class="rounded"
                                   onerror="this.style.display='none'"
                                 />
                                 <span>{{ op }}</span>
                               </a>
                             </li>
                           </ul>
                         </div>
                      </div>
                      <div class="mb-3">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Number</label>
                         <input 
                           v-model="rechargeData.number" 
                           type="text" 
                           class="form-control border-0 py-2" 
                           :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                           :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                           placeholder="Mobile / DTH Number" 
                           required
                         >
                      </div>
                      <div class="mb-4">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Amount</label>
                         <input 
                           v-model="rechargeData.amount" 
                           type="number" 
                           class="form-control border-0 py-2" 
                           :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                           :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                           placeholder="Enter amount" 
                           required
                         >
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 fw-medium shadow-sm hover-lift" :disabled="isLoadingRecharge">
                        <Loader2 v-if="isLoadingRecharge" :size="18" class="me-2 spinner" />
                        {{ isLoadingRecharge ? 'Processing...' : 'Recharge' }}
                      </button>
                   </form>
                </div>
             </div>
          </div>

          <!-- Fastag -->
          <div class="col-lg-4">
             <div class="card border-0 shadow-sm rounded-4 h-100" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
                <div class="card-header border-bottom p-4" :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''">
                  <div class="d-flex align-items-center gap-3">
                     <div class="rounded-circle bg-warning-subtle text-warning d-flex align-items-center justify-content-center" style="width: 50px; height: 50px; overflow: hidden;">
                        <img src="/Fastag-logo.png" alt="FASTag" style="width: 42px; height: 42px; object-fit: contain;" />
                     </div>
                     <h5 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">FASTag</h5>
                  </div>
                </div>
                <div class="card-body p-4" :style="isDarkMode ? 'background-color: #1e293b;' : ''">
                   <form @submit.prevent="fastagTopup">
                      <div class="mb-3">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Vehicle Number</label>
                         <input 
                           v-model="fastag.vehicle_number" 
                           type="text" 
                           class="form-control border-0 py-2" 
                           :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                           :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                           placeholder="e.g. KA01AB1234" 
                           required
                         >
                      </div>
                      <div class="mb-3">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Tag ID</label>
                         <input 
                           v-model="fastag.tag_id" 
                           type="text" 
                           class="form-control border-0 py-2" 
                           :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                           :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                           placeholder="Optional Tag ID"
                         >
                      </div>
                      <div class="mb-4">
                         <label :class="isDarkMode ? 'form-label small text-white-50 fw-bold' : 'form-label small text-muted fw-bold'">Amount</label>
                         <input 
                           v-model="fastag.amount" 
                           type="number" 
                           class="form-control border-0 py-2" 
                           :class="isDarkMode ? 'bg-dark text-white' : 'bg-light'"
                           :style="isDarkMode ? 'background-color: #0f172a; color: white;' : ''"
                           placeholder="Enter amount" 
                           required
                         >
                      </div>
                      <div class="mb-3" style="visibility: hidden;"> <!-- Spacer to align buttons -->
                        <label class="form-label small">&nbsp;</label>
                        <input type="text" class="form-control border-0 py-2">
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 fw-medium shadow-sm hover-lift" :disabled="isLoadingFastag">
                        <Loader2 v-if="isLoadingFastag" :size="18" class="me-2 spinner" />
                        {{ isLoadingFastag ? 'Processing...' : 'Top-up FASTag' }}
                      </button>
                   </form>
                </div>
             </div>
          </div>

        </div>

      </div>
    </div>

    <!-- OTP Confirmation Modal -->
    <div v-if="showOTPModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);" @click.self="closeOTPModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
          <!-- Modal Header -->
          <div class="modal-header bg-primary bg-gradient text-white border-0 py-4">
            <div class="d-flex align-items-center justify-content-center gap-3 w-100">
              <div class="logo-box bg-white bg-opacity-20 text-white rounded-3 d-flex align-items-center justify-content-center shadow-sm overflow-hidden" style="width: 50px; height: 50px;">
                <img src="@/assets/bank.png" alt="GIROBANK" style="width: 100%; height: 100%; object-fit: contain; padding: 4px;" />
              </div>
              <div>
                <h5 class="fw-bold mb-0">GIROBANK</h5>
                <small class="opacity-75">Confirm Transaction</small>
              </div>
            </div>
            <button type="button" class="btn-close btn-close-white" @click="closeOTPModal" aria-label="Close"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <h6 class="fw-bold text-dark mb-2">Enter OTP & Transaction Password</h6>
              <p class="text-muted small mb-0">An OTP has been sent to your registered email address</p>
            </div>

            <!-- Transaction Details -->
            <div class="bg-light rounded-3 p-3 mb-4">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted small">Amount:</span>
                <span class="fw-bold text-dark">₹{{ otpModalData.amount }}</span>
              </div>
              <div v-if="otpModalData.type === 'pay-bill'" class="d-flex justify-content-between align-items-center">
                <span class="text-muted small">Bill Type:</span>
                <span class="fw-medium text-dark">{{ otpModalData.bill_type }}</span>
              </div>
              <div v-if="otpModalData.type === 'recharge'" class="d-flex justify-content-between align-items-center">
                <span class="text-muted small">Type:</span>
                <span class="fw-medium text-dark">{{ otpModalData.recharge_type }}</span>
              </div>
            </div>

            <!-- OTP Input -->
            <div class="mb-3">
              <label class="form-label fw-medium text-secondary">Enter OTP</label>
              <input 
                type="text" 
                v-model="otp" 
                class="form-control form-control-lg border-2 text-center fw-bold"
                placeholder="000000"
                maxlength="6"
                style="font-size: 1.5rem; letter-spacing: 0.5rem;"
              />
            </div>

            <!-- Transaction Password Input -->
            <div class="mb-4">
              <label class="form-label fw-medium text-secondary">Transaction Password</label>
              <input 
                type="password" 
                v-model="transactionPassword" 
                class="form-control form-control-lg border-2"
                placeholder="Enter transaction password"
              />
            </div>

            <!-- Error/Success Message -->
            <div v-if="otpMessage" :class="['alert border-0 rounded-3 mb-3', otpMessageType === 'error' ? 'alert-danger' : otpMessageType === 'success' ? 'alert-success' : 'alert-info']" role="alert">
              <small class="fw-medium">{{ otpMessage }}</small>
            </div>

            <!-- Confirm Button -->
            <button 
              class="btn btn-primary btn-lg w-100 rounded-3 fw-semibold shadow-sm mb-3"
              @click="confirmTransaction"
              :disabled="!otp || otp.length !== 6 || !transactionPassword || isConfirming"
            >
              <span v-if="isConfirming" class="spinner-border spinner-border-sm me-2" role="status"></span>
              {{ isConfirming ? 'Confirming...' : 'Confirm Transaction' }}
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import { 
  LayoutDashboard, 
  Users, 
  Send, 
  FileText, 
  MessageSquare, 
  LogOut, 
  Bell,
  Smartphone,
  Zap,
  Wallet,
  Moon,
  Sun,
  AlertCircle,
  Loader2,
  X,
  Bolt,
  Flame,
  Wifi,
  Car,
  Utensils,
  MoreHorizontal
} from 'lucide-vue-next';
import { useDarkMode } from "@/composables/useDarkMode";

// Store icon components for use in methods
const BillTypeIcons = {
  'Electricity': Bolt,
  'Gas': Flame,
  'Internet': Wifi,
  'Transport': Car,
  'Food': Utensils,
  'Others': MoreHorizontal
};

const RechargeTypeIcons = {
  'Mobile': Smartphone,
  'DTH': Zap
};

export default {
  name: "Payments",
  components: {
    LayoutDashboard,
    Users,
    Send,
    FileText,
    MessageSquare,
    LogOut,
    Bell,
    Smartphone,
    Zap,
    Wallet,
    Moon,
    Sun,
    AlertCircle,
    Loader2,
    X,
    Bolt,
    Flame,
    Wifi,
    Car,
    Utensils,
    MoreHorizontal
  },
  setup() {
    const { isDarkMode, toggleDarkMode } = useDarkMode()
    return {
      isDarkMode,
      toggleDarkMode,
      Moon,
      Sun
    }
  },
  data() {
    return {
      customerId: localStorage.getItem("customer_id") || 1,
      customerName: localStorage.getItem("customer_name") || "Customer",
      billOptions: {
        bill_types: [],
        electricity_providers: [],
        gas_providers: [],
        internet_providers: [],
        mobile_operators: [],
        dth_providers: [],
        transport_providers: [],
        food_providers: [],
        others_providers: [],
      },
      bill: { bill_type: "", biller: "", bill_account: "", amount: "" },
      rechargeData: {
        recharge_type: "",
        operator: "",
        number: "",
        amount: "",
      },
      fastag: { vehicle_number: "", tag_id: "", amount: "" },
      navItems: [
        { id: 'dashboard', label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
        { id: 'beneficiary', label: 'Beneficiaries', path: '/beneficiary', icon: Users },
        { id: 'transfer', label: 'Transfer Money', path: '/transfer', icon: Send },
        { id: 'history', label: 'Transactions', path: '/history', icon: FileText },
        { id: 'payments', label: 'Payments', path: '/payments', icon: Wallet },
        { id: 'chatbot', label: 'AI Assistant', path: '/chatbot', icon: MessageSquare },
        { id: 'disputes', label: 'Disputes', path: '/disputes', icon: AlertCircle }
      ],
      isLoadingBill: false,
      isLoadingRecharge: false,
      isLoadingFastag: false,
      showOTPModal: false,
      otpModalData: {
        session_id: null,
        type: null,
        customer_id: null,
        amount: null,
        bill_type: null,
        biller: null,
        bill_account: null,
        recharge_type: null,
        operator: null,
        number: null,
        vehicle_number: null,
        tag_id: null
      },
      otp: "",
      transactionPassword: "",
      otpMessage: "",
      otpMessageType: "",
      isConfirming: false
    };
  },
  methods: {
    getInitials(name) {
       return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    },
    navigate(path) {
      this.$router.push(path);
    },
    handleLogout() {
      localStorage.clear();
      this.$router.push("/");
    },
    async fetchBillOptions() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/customer/bill-options");
        this.billOptions = res.data;
      } catch (err) {
        console.error("Error loading bill options:", err);
      }
    },
    getBillerList(type) {
      switch (type) {
        case "Electricity":
          return this.billOptions.electricity_providers || [];
        case "Gas":
          return this.billOptions.gas_providers || [];
        case "Internet":
          return this.billOptions.internet_providers || [];
        case "Transport":
          return this.billOptions.transport_providers || [];
        case "Food":
          return this.billOptions.food_providers || [];
        case "Others":
          return this.billOptions.others_providers || [];
        default:
          return [];
      }
    },
    getServiceLogo(serviceName) {
      if (!serviceName) return null;
      
      // Normalize service name for matching (lowercase, remove spaces/special chars)
      const normalized = serviceName.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
      
      // Logo mapping - match service names to logo files
      const logoMap = {
        // Transport
        'ola': require('@/assets/OLA_icon.png'),
        'uber': require('@/assets/Uber_logo_new.png'),
        'rapido': require('@/assets/Rapido_icon.png'),
        'metro' : require('@/assets/Metro_logo.png'),
        
        // Food
        'swiggy': require('@/assets/Swiggy_icon.png'),
        'zomato': require('@/assets/Zomato_icon.png'),
        'zepto': require('@/assets/zepto-logo-app-icon.png'),
        
        // Mobile Operators
        'airtel': require('@/assets/Airtel_logo.png'),
        'bsnl': require('@/assets/BSNL_logo.png'),
        'jio': require('@/assets/Reliance_Jio_Logo.svg'),
        'reliance_jio': require('@/assets/Reliance_Jio_Logo.svg'),
        'vodafone': require('@/assets/Vodafone_Idea_logo.svg'),
        'vodafone_idea': require('@/assets/Vodafone_Idea_logo.svg'),
        'idea': require('@/assets/Vodafone_Idea_logo.svg'),
        
        // DTH Providers
        'dish_tv': require('@/assets/Dish_tv_logo.png'),
        'dish': require('@/assets/Dish_tv_logo.png'),
        'tatasky': require('@/assets/TataSky_logo.png'),
        'tata_sky': require('@/assets/TataSky_logo.png'),
        'sun_direct': require('@/assets/Sun_direct_logo.png'),
        'sundirect': require('@/assets/Sun_direct_logo.png'),
      };
      
      // Try exact match first
      if (logoMap[normalized]) {
        return logoMap[normalized];
      }
      
      // Try partial match (e.g., "Jio" in "Reliance Jio")
      for (const [key, logo] of Object.entries(logoMap)) {
        if (normalized.includes(key) || key.includes(normalized)) {
          return logo;
        }
      }
      
      return null;
    },
    getBillTypeIcon(billType) {
      if (!billType) return null;
      return BillTypeIcons[billType] || null;
    },
    getRechargeTypeIcon(rechargeType) {
      if (!rechargeType) return null;
      return RechargeTypeIcons[rechargeType] || null;
    },
    selectBillType(type) {
      this.bill.bill_type = type;
      // Reset biller when bill type changes
      this.bill.biller = "";
      // Close dropdown
      this.$nextTick(() => {
        const dropdownElement = document.querySelector('#billTypeDropdown');
        if (dropdownElement && window.bootstrap) {
          const dropdown = window.bootstrap.Dropdown.getInstance(dropdownElement);
          if (dropdown) {
            dropdown.hide();
          } else {
            const menu = dropdownElement.nextElementSibling;
            if (menu) {
              menu.classList.remove('show');
              dropdownElement.setAttribute('aria-expanded', 'false');
            }
          }
        }
      });
    },
    selectRechargeType(type) {
      this.rechargeData.recharge_type = type;
      // Reset operator when recharge type changes
      this.rechargeData.operator = "";
      // Close dropdown
      this.$nextTick(() => {
        const dropdownElement = document.querySelector('#rechargeTypeDropdown');
        if (dropdownElement && window.bootstrap) {
          const dropdown = window.bootstrap.Dropdown.getInstance(dropdownElement);
          if (dropdown) {
            dropdown.hide();
          } else {
            const menu = dropdownElement.nextElementSibling;
            if (menu) {
              menu.classList.remove('show');
              dropdownElement.setAttribute('aria-expanded', 'false');
            }
          }
        }
      });
    },
    selectBiller(biller) {
      this.bill.biller = biller;
      // Close dropdown using Bootstrap's dropdown API
      this.$nextTick(() => {
        const dropdownElement = document.querySelector('#billerDropdown');
        if (dropdownElement && window.bootstrap) {
          const dropdown = window.bootstrap.Dropdown.getInstance(dropdownElement);
          if (dropdown) {
            dropdown.hide();
          } else {
            // Fallback: remove show class from dropdown menu
            const menu = dropdownElement.nextElementSibling;
            if (menu) {
              menu.classList.remove('show');
              dropdownElement.setAttribute('aria-expanded', 'false');
            }
          }
        }
      });
    },
    selectOperator(operator) {
      this.rechargeData.operator = operator;
      // Close dropdown using Bootstrap's dropdown API
      this.$nextTick(() => {
        const dropdownElement = document.querySelector('#operatorDropdown');
        if (dropdownElement && window.bootstrap) {
          const dropdown = window.bootstrap.Dropdown.getInstance(dropdownElement);
          if (dropdown) {
            dropdown.hide();
          } else {
            // Fallback: remove show class from dropdown menu
            const menu = dropdownElement.nextElementSibling;
            if (menu) {
              menu.classList.remove('show');
              dropdownElement.setAttribute('aria-expanded', 'false');
            }
          }
        }
      });
    },
    async payBill() {
      if (!this.bill.bill_type || !this.bill.biller || !this.bill.amount) {
        alert("Please fill all required fields");
        return;
      }

      this.isLoadingBill = true;
      this.otpMessage = "";
      
      try {
        // Step 1: Initiate Bill Payment
        const res = await axios.post("http://127.0.0.1:5000/customer/initiate-pay-bill", {
          customer_id: this.customerId,
          bill_type: this.bill.bill_type,
          biller: this.bill.biller,
          bill_account: this.bill.bill_account,
          amount: this.bill.amount
        });

        // Show OTP modal instead of redirecting
        this.otpModalData = {
          session_id: res.data.session_id,
          type: "pay-bill",
          customer_id: this.customerId,
          bill_type: this.bill.bill_type,
          biller: this.bill.biller,
          bill_account: this.bill.bill_account,
          amount: this.bill.amount
        };
        this.showOTPModal = true;
        this.otp = "";
        this.transactionPassword = "";
      } catch (err) {
        alert(err.response?.data?.message || "Error initiating bill payment");
      } finally {
        this.isLoadingBill = false;
      }
    },
    async recharge() {
      if (!this.rechargeData.recharge_type || !this.rechargeData.operator || !this.rechargeData.number || !this.rechargeData.amount) {
        alert("Please fill all required fields");
        return;
      }

      this.isLoadingRecharge = true;
      this.otpMessage = "";

      try {
        // Step 1: Initiate Recharge
        const res = await axios.post("http://127.0.0.1:5000/customer/initiate-recharge", {
          customer_id: this.customerId,
          recharge_type: this.rechargeData.recharge_type,
          operator: this.rechargeData.operator,
          number: this.rechargeData.number,
          amount: this.rechargeData.amount
        });

        // Show OTP modal instead of redirecting
        this.otpModalData = {
          session_id: res.data.session_id,
          type: "recharge",
          customer_id: this.customerId,
          recharge_type: this.rechargeData.recharge_type,
          operator: this.rechargeData.operator,
          number: this.rechargeData.number,
          amount: this.rechargeData.amount
        };
        this.showOTPModal = true;
        this.otp = "";
        this.transactionPassword = "";
      } catch (err) {
        alert(err.response?.data?.message || "Error initiating recharge");
      } finally {
        this.isLoadingRecharge = false;
      }
    },
    async fastagTopup() {
      if (!this.fastag.vehicle_number || !this.fastag.amount) {
        alert("Please fill all required fields");
        return;
      }

      this.isLoadingFastag = true;
      this.otpMessage = "";

      try {
        // Step 1: Initiate FASTag Top-up
        const res = await axios.post("http://127.0.0.1:5000/customer/initiate-fastag", {
          customer_id: this.customerId,
          vehicle_number: this.fastag.vehicle_number,
          tag_id: this.fastag.tag_id,
          amount: this.fastag.amount
        });

        // Show OTP modal instead of redirecting
        this.otpModalData = {
          session_id: res.data.session_id,
          type: "fastag",
          customer_id: this.customerId,
          vehicle_number: this.fastag.vehicle_number,
          tag_id: this.fastag.tag_id,
          amount: this.fastag.amount
        };
        this.showOTPModal = true;
        this.otp = "";
        this.transactionPassword = "";
      } catch (err) {
        alert(err.response?.data?.message || "Error initiating FASTag top-up");
      } finally {
        this.isLoadingFastag = false;
      }
    },
    closeOTPModal() {
      this.showOTPModal = false;
      this.otp = "";
      this.transactionPassword = "";
      this.otpMessage = "";
      this.otpModalData = {
        session_id: null,
        type: null,
        customer_id: null,
        amount: null,
        bill_type: null,
        biller: null,
        bill_account: null,
        recharge_type: null,
        operator: null,
        number: null,
        vehicle_number: null,
        tag_id: null
      };
    },
    async confirmTransaction() {
      if (!this.otp || this.otp.length !== 6 || !this.transactionPassword) {
        this.otpMessage = "Please enter a valid 6-digit OTP and transaction password";
        this.otpMessageType = "error";
        return;
      }

      this.isConfirming = true;
      this.otpMessage = "";

      const payload = {
        session_id: this.otpModalData.session_id,
        customer_id: this.otpModalData.customer_id,
        amount: this.otpModalData.amount,
        otp: this.otp,
        transaction_password: this.transactionPassword
      };

      let url = "";
      switch (this.otpModalData.type) {
        case "pay-bill":
          url = "http://127.0.0.1:5000/customer/confirm-pay-bill";
          payload.bill_type = this.otpModalData.bill_type;
          payload.biller = this.otpModalData.biller;
          payload.bill_account = this.otpModalData.bill_account;
          break;
        case "recharge":
          url = "http://127.0.0.1:5000/customer/confirm-recharge";
          payload.recharge_type = this.otpModalData.recharge_type;
          payload.operator = this.otpModalData.operator;
          payload.number = this.otpModalData.number;
          break;
        case "fastag":
          url = "http://127.0.0.1:5000/customer/confirm-fastag";
          payload.vehicle_number = this.otpModalData.vehicle_number;
          payload.tag_id = this.otpModalData.tag_id;
          break;
        default:
          this.otpMessage = "Invalid transaction type";
          this.otpMessageType = "error";
          this.isConfirming = false;
          return;
      }

      try {
        const res = await axios.post(url, payload);
        this.otpMessage = res.data.message || "Transaction successful";
        this.otpMessageType = "success";
        
        // Close modal and refresh after 2 seconds
        setTimeout(() => {
          this.closeOTPModal();
          // Reset forms
          this.bill = { bill_type: "", biller: "", bill_account: "", amount: "" };
          this.rechargeData = { recharge_type: "", operator: "", number: "", amount: "" };
          this.fastag = { vehicle_number: "", tag_id: "", amount: "" };
        }, 2000);
      } catch (err) {
        this.otpMessage = err.response?.data?.message || "Transaction failed. Please try again.";
        this.otpMessageType = "error";
      } finally {
        this.isConfirming = false;
      }
    },
  },
  mounted() {
    this.fetchBillOptions();
  },
};
</script>

<style scoped>
.font-sans {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.logo-box {
  width: 48px;
  height: 48px;
}

.avatar {
  width: 40px;
  height: 40px;
}

.btn-ghost-dark {
  background: transparent;
  border: none;
}

.btn-ghost-dark:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white !important;
}

.hover-text-white:hover {
  color: white !important;
}

.hover-bg-light:hover {
  background-color: #f8f9fa !important;
}

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-3px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
}

.transition-all {
  transition: all 0.2s ease-in-out;
}

.bg-primary-subtle {
  background-color: rgba(13, 110, 253, 0.1);
}

.bg-success-subtle {
  background-color: rgba(25, 135, 84, 0.1);
}

.bg-warning-subtle {
    background-color: rgba(255, 193, 7, 0.1);
}

.text-primary {
  color: #0d6efd !important;
}

.text-success {
  color: #198754 !important;
}

.text-warning {
    color: #ffc107 !important;
}

.logout-btn {
  background: #fff;
  border: 1px solid rgba(220, 53, 69, 0.35);
  color: #dc3545;
  border-radius: 12px;
  transition: all 0.25s ease-in-out;
  box-shadow: 0 2px 6px rgba(255, 0, 0, 0.06);
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 0.08);
  border-color: rgba(220, 53, 69, 0.7);
  box-shadow: 0 4px 10px rgba(220, 53, 69, 0.15);
  transform: translateY(-2px);
}

.logout-btn:active {
  transform: scale(0.98);
  background: rgba(220, 53, 69, 0.16);
}

.cursor-pointer {
  cursor: pointer;
}

/* Spinner animation */
.spinner {
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Modal backdrop */
.modal.show {
  display: block;
}

/* Custom dropdown styling */
.dropdown-toggle::after {
  display: none;
}

.dropdown-menu {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid rgba(0,0,0,0.1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.dropdown-item {
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item img {
  flex-shrink: 0;
}

.hover-bg-light-transition {
  transition: background-color 0.2s ease;
}

.hover-bg-light-transition:hover {
  background-color: rgba(255,255,255,0.1) !important;
}

.modal-backdrop {
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
