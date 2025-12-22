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

    <!-- Main Content -->
    <div class="flex-grow-1 overflow-auto" style="margin-left: 280px;">
      <!-- Top Header -->
      <header 
        class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center sticky-top shadow-sm"
        :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'"
        :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''"
      >
        <div>
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Management & Oversight Hub</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">High-level performance metrics and task assignments.</p>
        </div>
      </header>

      <!-- Top Header -->
      <header 
        class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center sticky-top shadow-sm"
        :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'"
        :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''"
      >
        <div>
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Management & Oversight Hub</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">High-level performance metrics and task assignments.</p>
        </div>
      </header>

      <!-- Dashboard Content -->
      <div class="p-4" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
        <section class="stats-grid">
          <div class="stat-card team-members">
            <div class="icon-box">👥</div>
            <div class="stat-content">
              <span class="stat-label">Team Members</span>
              <span class="stat-value">12</span>
            </div>
          </div>
          <div class="stat-card completed-tasks">
            <div class="icon-box">✓</div>
            <div class="stat-content">
              <span class="stat-label">Tasks Completed</span>
              <span class="stat-value">176</span>
            </div>
          </div>
          <div class="stat-card pending-tasks">
            <div class="icon-box">⏰</div>
            <div class="stat-content">
              <span class="stat-label">Pending Tasks</span>
              <span class="stat-value">34</span>
            </div>
          </div>
          <div class="stat-card efficiency">
            <div class="icon-box">⚡</div>
            <div class="stat-content">
              <span class="stat-label">Avg Efficiency</span>
              <span class="stat-value">87%</span>
            </div>
          </div>
        </section>

        <section class="charts-section">
          <div class="chart-panel small-chart">
            <h4 class="chart-title">Task Performance (Weekly)</h4>
            <canvas ref="barChart"></canvas>
          </div>

          <div class="chart-panel small-chart">
            <h4 class="chart-title">Verification Statistics</h4>
            <canvas ref="pieChart"></canvas>
          </div>
        </section>

        <div class="chart-panel full-chart">
          <h4 class="chart-title">Task Completion Rate – Monthly Trend</h4>
          <canvas ref="lineChart"></canvas>
        </div>

        <div class="row-panels">
          <div class="panel active-tasks-panel">
            <h3>Active Tasks ({{ tasks.length }})</h3>
            <div class="task-list">
              <div v-for="(task, index) in tasks" :key="index" :class="['task-item', task.priority]">
                <div class="task-header">
                  <strong class="task-title">{{ task.title }}</strong>
                  <span :class="['priority-tag', task.priority]">{{ task.priority.toUpperCase() }}</span>
                </div>
                <p class="task-meta">Customer: <strong>{{ task.customer }}</strong></p>
                <p class="task-meta">Assigned To: <strong>{{ task.assignedTo }}</strong></p>
                <p class="task-due">Due: {{ task.due }}</p>
              </div>
            </div>
          </div>

          <div class="panel create-task-panel">
            <h3>Create & Assign Task</h3>
            <div class="task-form">
              <div class="form-group">
                <label for="title">Task Title</label>
                <input 
                  id="title" 
                  v-model="newTask.title" 
                  placeholder="e.g., Process payment dispute" 
                />
              </div>

              <div class="form-group">
                <label for="customer">Customer ID</label>
                <input 
                  id="customer" 
                  type="number"
                  v-model="newTask.customer_id" 
                  placeholder="Enter customer ID" 
                />
              </div>

              <div class="form-group">
                <label for="assignedTo">Employee ID</label>
                <input 
                  id="assignedTo" 
                  type="number"
                  v-model="newTask.employee_id" 
                  placeholder="Enter employee ID" 
                />
              </div>

              <div class="d-flex-split">
                <div class="form-group half-width">
                  <label for="priority">Priority</label>
                  <select id="priority" v-model="newTask.priority">
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>
                <div class="form-group half-width">
                  <label for="due">Due Date</label>
                  <input 
                    id="due" 
                    type="date" 
                    v-model="newTask.due" 
                  />
                </div>
              </div>

              <div class="form-group">
                <label for="description">Task Description</label>
                <textarea 
                  id="description" 
                  v-model="newTask.description" 
                  placeholder="Brief description of the required action..."
                ></textarea>
              </div>

              <div class="actions">
                <button class="btn-secondary" @click="resetForm">Cancel</button>
                <button class="btn-primary" @click="createTask">Create & Assign Task</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import { LogOut, LayoutDashboard, Moon, Sun } from 'lucide-vue-next';
import { useDarkMode } from "@/composables/useDarkMode";

export default {
  name: 'ManagerDashboard',
  components: {
    LogOut,
    LayoutDashboard,
    Moon,
    Sun
  },
  setup() {
    const { isDarkMode, toggleDarkMode } = useDarkMode();
    return {
      isDarkMode,
      toggleDarkMode,
      Moon,
      Sun
    };
  },
  data() {
    return {
      managerName: localStorage.getItem("manager_name") || "Manager",
      tasks: [
        { title: 'Process loan application', customer: 'John Doe', assignedTo: 'Jane', due: '2025-10-16', priority: 'high' },
        { title: 'Update customer KYC', customer: 'Alice Smith', assignedTo: 'Robert', due: '2025-10-17', priority: 'medium' },
        { title: 'Resolve complaint ticket', customer: 'Bob Johnson', assignedTo: 'Alex', due: '2025-10-15', priority: 'high' }
      ],
      newTask: {
        title: '',
        customer_id: '',
        employee_id: '',
        priority: 'medium',
        due: '',
        description: ''
      },
      navItems: [
        { id: 'dashboard', label: 'Dashboard', path: '/manager-dashboard', icon: LayoutDashboard }
      ]
    };
  },
  methods: {
    getInitials(name) {
      if (!name) return 'M';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },
    isActiveRoute(path) {
      return this.$route.path === path || this.$route.path.startsWith(path + '/');
    },
    navigate(path) {
      this.$router.push(path);
    },
    handleLogout() {
      localStorage.removeItem("manager_id");
      localStorage.removeItem("manager_name");
      localStorage.removeItem("manager_email");
      localStorage.removeItem("user_role");
      this.$router.push("/");
    },
    resetForm() {
      this.newTask = {
        title: '',
        customer_id: '',
        employee_id: '',
        priority: 'medium',
        due: '',
        description: ''
      };
    },
    async createTask() {
      // Validation
      if (!this.newTask.title || !this.newTask.customer_id || !this.newTask.employee_id || !this.newTask.due) {
        alert('Please fill in all required fields');
        return;
      }

      try {
        const payload = {
          name: this.newTask.title,
          employee_id: parseInt(this.newTask.employee_id),
          customer_id: parseInt(this.newTask.customer_id),
          due_date: this.newTask.due,
          priority: this.newTask.priority.charAt(0).toUpperCase() + this.newTask.priority.slice(1),
          description: this.newTask.description
        };

        const response = await fetch('http://127.0.0.1:5000/api/task/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          throw new Error('Failed to create task');
        }

        const result = await response.json();
        
        // Add the task to the local list for immediate UI update
        this.tasks.push({ 
          title: this.newTask.title,
          customer: `Customer ${this.newTask.customer_id}`,
          assignedTo: `Employee ${this.newTask.employee_id}`,
          due: this.newTask.due,
          priority: this.newTask.priority
        });
        
        alert('Task created & assigned successfully!');
        this.resetForm();
      } catch (error) {
        console.error('Error creating task:', error);
        alert('Failed to create task. Please try again.');
      }
    },
    initCharts() {
      const primaryColor = '#4a90e2';
      const secondaryColor = '#50e3c2';
      const highColor = '#e74c3c';

      // Bar Chart (Task Performance)
      if (this.$refs.barChart) {
        new Chart(this.$refs.barChart, {
          type: 'bar',
          data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            datasets: [{
              label: 'Tasks Completed',
              data: [12, 19, 8, 17, 14],
              backgroundColor: primaryColor,
              borderRadius: 4,
            }]
          },
          options: { 
            responsive: true, 
            maintainAspectRatio: true,
            scales: { y: { beginAtZero: true } } 
          }
        });
      }

      // Pie Chart (Verification Statistics)
      if (this.$refs.pieChart) {
        new Chart(this.$refs.pieChart, {
          type: 'doughnut',
          data: {
            labels: ['Approved', 'Pending', 'Rejected'],
            datasets: [{
              data: [63, 29, 8],
              backgroundColor: [secondaryColor, primaryColor, highColor],
            }]
          },
          options: { 
            responsive: true, 
            maintainAspectRatio: true 
          }
        });
      }

      // Line Chart (Task Completion Rate – Monthly Trend)
      if (this.$refs.lineChart) {
        new Chart(this.$refs.lineChart, {
          type: 'line',
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
              label: 'Completion Rate (%)',
              data: [40, 50, 55, 65, 70, 80],
              borderColor: primaryColor,
              backgroundColor: 'rgba(74, 144, 226, 0.1)',
              tension: 0.3,
              fill: true,
            }]
          },
          options: { 
            responsive: true, 
            maintainAspectRatio: true,
            scales: { y: { beginAtZero: true, max: 100 } } 
          }
        });
      }
    }
  },
  mounted() {
    this.initCharts();
  }
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.3s ease;
  border-left: 6px solid #ccc;
}

.stat-card:hover { 
  transform: translateY(-3px); 
}

.icon-box {
  background-color: #4a90e2;
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.9rem;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #4a90e2;
}

.team-members { border-left-color: #4a90e2; }
.completed-tasks { border-left-color: #2ecc71; }
.pending-tasks { border-left-color: #e74c3c; }
.efficiency { border-left-color: #50e3c2; }

.charts-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-panel {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #eee;
}

.small-chart {
  flex: 1;
  max-height: 350px;
}

.full-chart {
  min-height: 350px;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
  border-bottom: 1px dashed #eee;
  padding-bottom: 10px;
}

.row-panels {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 20px;
}

.panel {
  background: #ffffff;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #eee;
}

.panel h3 {
  font-size: 1.5rem;
  color: #4a90e2;
  margin-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 600px;
  overflow-y: auto;
}

.task-item {
  background: #f7f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 5px solid #ccc;
}

.task-item.high { border-left-color: #e74c3c; }
.task-item.medium { border-left-color: #f39c12; }
.task-item.low { border-left-color: #2ecc71; }

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.task-title {
  font-size: 1.05rem;
}

.task-meta, .task-due {
  font-size: 0.9rem;
  color: #666;
  margin: 2px 0;
}

.task-due {
  font-weight: 500;
}

.priority-tag {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: white;
  line-height: 1;
}

.priority-tag.high { background-color: #e74c3c; }
.priority-tag.medium { background-color: #f39c12; }
.priority-tag.low { background-color: #2ecc71; }

.task-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 5px;
  font-size: 0.95rem;
  color: #333;
}

input, select, textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1em;
  width: 100%;
  box-sizing: border-box;
}

textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.d-flex-split {
  display: flex;
  gap: 15px;
}

.half-width {
  flex: 1;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-primary, .btn-secondary {
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #4a90e2;
  color: white;
}

.btn-primary:hover {
  background: #397bc7;
}

.btn-secondary {
  background: #adb5bd;
  color: white;
}

.btn-secondary:hover {
  background: #868e96;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .row-panels {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-section {
    flex-direction: column;
  }
  
  .d-flex-split {
    flex-direction: column;
  }
}
</style>
