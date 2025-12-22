<template>
  <div class="d-flex min-vh-100 font-sans" :class="isDarkMode ? 'bg-dark' : 'bg-light'" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
    <!-- Sidebar -->
    <div class="sidebar d-flex flex-column shadow-sm" style="width: 280px; position: fixed; height: 100vh; overflow-y: auto; z-index: 1000; background-color: #1e293b;">
      <!-- Logo/Header -->
      <div class="p-4 mb-2">
        <div class="d-flex align-items-center gap-3 mb-4">
          <div>
            <h5 class="fw-bold text-white mb-0">GIROBANK</h5>
            <small class="text-white-50">Management Dashboard</small>
          </div>
        </div>
        
        <div 
          class="user-profile p-3 rounded-3 d-flex align-items-center gap-3" 
          style="background-color: rgba(255,255,255,0.05);"
        >
          <div class="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center fw-bold">
            {{ getInitials(managerName) }}
          </div>
          <div class="overflow-hidden">
            <h6 class="text-white mb-0 text-truncate">{{ managerName }}</h6>
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
              isActiveRoute(item.path)
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

    <!-- Main Content Area -->
    <div class="flex-grow-1 overflow-auto" style="margin-left: 280px;">
      <!-- Router View for Nested Routes -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { LogOut, LayoutDashboard, ClipboardList, PlusCircle, Moon, Sun } from "lucide-vue-next";
import { useDarkMode } from "@/composables/useDarkMode";

const router = useRouter();
const route = useRoute();
const { isDarkMode, toggleDarkMode } = useDarkMode();
const managerName = ref(localStorage.getItem("manager_name") || "Manager");

const getInitials = (name) => {
  if (!name) return 'M';
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
};

const navItems = [
  { id: 'dashboard', label: 'Dashboard', path: '/manager-dashboard', icon: LayoutDashboard },
  { id: 'active-tasks', label: 'Active Tasks', path: '/manager-dashboard/active-tasks', icon: ClipboardList },
  { id: 'create-task', label: 'Create Task', path: '/manager-dashboard/create-task', icon: PlusCircle }
];

const isActiveRoute = (path) => {
  if (path === '/manager-dashboard') {
    return route.path === '/manager-dashboard' || route.path === '/manager-dashboard/';
  }
  return route.path === path || route.path.startsWith(path + '/');
};

const navigate = (path) => {
  router.push(path);
};

const handleLogout = () => {
  localStorage.removeItem("manager_id");
  localStorage.removeItem("manager_name");
  localStorage.removeItem("manager_email");
  localStorage.removeItem("user_role");
  router.push("/");
};
</script>

<style scoped>
.sidebar {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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

.transition-all {
  transition: all 0.2s ease-in-out;
}

.logo-box {
  width: 48px;
  height: 48px;
}

.user-profile {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.user-profile:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.avatar {
  width: 40px;
  height: 40px;
  font-size: 0.9rem;
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
</style>


