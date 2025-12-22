<template>
  <div class="home-page d-flex min-vh-100 align-items-center justify-content-center font-sans" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="container py-5">
      <div class="row justify-content-center align-items-center g-5">
        <!-- Left Column - Branding and Features -->
        <div class="col-lg-7 col-xl-6 text-center text-lg-start text-white">
          <!-- Logo and Branding -->
          <div class="mb-5">
            <h1 class="display-2 fw-bold mb-3 text-white lh-1">GIROBANK</h1>
            <p class="lead fs-4 mb-0 opacity-90 fw-light">Premium Banking Experience</p>
          </div>

          <!-- Tagline -->
          <div class="mb-5">
            <h2 class="h2 fw-semibold mb-4">Welcome to Your Financial Future</h2>
            <p class="fs-5 opacity-90 mb-3 lh-lg">
              Manage your banking operations, track expenses, and stay secure — all in one place.
            </p>
            <p class="fs-6 opacity-75 mb-0 lh-lg">
              Experience modern banking with cutting-edge security and intuitive design.
            </p>
          </div>

          <!-- Features -->
          <div class="row g-4 mt-5">
            <div class="col-md-4">
              <div class="feature-card p-4 rounded-4 bg-white bg-opacity-10 backdrop-blur shadow-sm h-100 text-center text-md-start">
                <div class="mb-3">
                  <div class="bg-white bg-opacity-20 rounded-circle d-inline-flex align-items-center justify-content-center p-3" style="width: 60px; height: 60px;">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                      <path d="M2 17l10 5 10-5"></path>
                      <path d="M2 12l10 5 10-5"></path>
                    </svg>
                  </div>
                </div>
                <h5 class="fw-semibold mb-2 fs-6">AI-Powered</h5>
                <p class="small mb-0 opacity-90 lh-base">Smart financial insights</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="feature-card p-4 rounded-4 bg-white bg-opacity-10 backdrop-blur shadow-sm h-100 text-center text-md-start">
                <div class="mb-3">
                  <div class="bg-white bg-opacity-20 rounded-circle d-inline-flex align-items-center justify-content-center p-3" style="width: 60px; height: 60px;">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                  </div>
                </div>
                <h5 class="fw-semibold mb-2 fs-6">Next-Gen</h5>
                <p class="small mb-0 opacity-90 lh-base">Cutting-edge technology</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="feature-card p-4 rounded-4 bg-white bg-opacity-10 backdrop-blur shadow-sm h-100 text-center text-md-start">
                <div class="mb-3">
                  <div class="bg-white bg-opacity-20 rounded-circle d-inline-flex align-items-center justify-content-center p-3" style="width: 60px; height: 60px;">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  </div>
                </div>
                <h5 class="fw-semibold mb-2 fs-6">Intelligent</h5>
                <p class="small mb-0 opacity-90 lh-base">Personalized banking</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Action Card -->
        <div class="col-lg-5 col-xl-4">
          <div class="card shadow-lg border-0 rounded-4 overflow-hidden">
            <div class="card-header bg-primary bg-gradient text-white text-center py-5 border-0">
              <div class="d-flex flex-column align-items-center gap-3">
                <div>
                  <h4 class="fw-bold mb-1">GIROBANK</h4>
                  <small class="opacity-75">Premium Banking</small>
                </div>
              </div>
            </div>

            <div class="card-body p-5">
              <h5 class="fw-bold text-dark mb-3 text-center">Get Started</h5>
              <p class="text-muted text-center small mb-4 lh-base">
                Sign in to your account or create a new one to begin your banking journey
              </p>

              <div class="d-grid gap-3 mb-4">
                <button 
                  class="btn btn-primary btn-lg rounded-3 fw-semibold shadow-sm py-3"
                  @click="goToLogin"
                >
                  Login
                </button>

                <button 
                  class="btn btn-outline-primary btn-lg rounded-3 fw-semibold py-3"
                  @click="goToRegister"
                >
                  Register
                </button>
              </div>

              <div class="text-center pt-3 border-top">
                <small class="text-muted d-flex align-items-center justify-content-center gap-2">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                  </svg>
                  Secure & Protected
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  methods: {
    goToLogin() {
      this.$router.push('/login');
    },
    goToRegister() {
      this.$router.push('/register');
    }
  }
};
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  padding: 2rem 0;
}

.home-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
  pointer-events: none;
}

.logo-box {
  transition: transform 0.3s ease;
}

.logo-box:hover {
  transform: scale(1.05) rotate(5deg);
}

.feature-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.15);
  min-height: 180px;
  display: flex;
  flex-direction: column;
}

.feature-card:hover {
  transform: translateY(-8px);
  background: rgba(255, 255, 255, 0.18) !important;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25) !important;
  border-color: rgba(255, 255, 255, 0.3);
}

.card {
  border-radius: 24px;
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.btn-outline-primary {
  border: 2px solid #667eea;
  color: #667eea;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
  background: transparent;
}

.btn-outline-primary:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.backdrop-blur {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-card {
  animation: fadeInUp 0.6s ease-out;
}

.feature-card:nth-child(1) {
  animation-delay: 0.1s;
}

.feature-card:nth-child(2) {
  animation-delay: 0.2s;
}

.feature-card:nth-child(3) {
  animation-delay: 0.3s;
}

/* Typography improvements */
h1 {
  letter-spacing: -0.02em;
}

h2 {
  letter-spacing: -0.01em;
}

.lead {
  letter-spacing: 0.01em;
}

/* Responsive spacing */
@media (max-width: 991.98px) {
  .home-page {
    padding: 3rem 0;
  }
  
  .mb-5 {
    margin-bottom: 3rem !important;
  }
}

@media (max-width: 575.98px) {
  .display-2 {
    font-size: 2.5rem;
  }
  
  .h2 {
    font-size: 1.75rem;
  }
  
  .logo-box {
    width: 100px !important;
    height: 100px !important;
  }
  
  .logo-box span {
    font-size: 2.5rem !important;
  }
}
</style>
