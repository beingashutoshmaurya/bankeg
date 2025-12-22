<template>
  <div>
    <!-- Top Header -->
    <header 
      class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center sticky-top shadow-sm bg-white border-light"
    >
      <div>
        <h4 class="fw-bold text-dark mb-0">Active Tasks</h4>
        <p class="text-muted mb-0 small">Monitor and manage all active tasks assigned to your team.</p>
      </div>
      <button class="btn btn-primary d-flex align-items-center gap-2" @click="refreshTasks">
        <RefreshCw :size="18" :class="{ 'spinning': loading }" />
        <span>Refresh</span>
      </button>
    </header>

    <!-- Content -->
    <div class="p-4">
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p class="text-muted">Loading tasks...</p>
      </div>

      <!-- Tasks List -->
      <div v-else-if="tasks.length > 0" class="tasks-container">
        <div 
          v-for="(task, index) in sortedTasks" 
          :key="task.id || index" 
          :class="['task-card', task.priority?.toLowerCase(), task.status === 'complete' ? 'completed' : 'pending']"
        >
          <div class="task-card-header">
            <div class="task-title-section">
              <h5 class="task-title">{{ task.name || task.title }}</h5>
              <span :class="['priority-badge', task.priority?.toLowerCase()]">
                {{ task.priority?.toUpperCase() || 'MEDIUM' }}
              </span>
            </div>
            <span :class="['status-badge', task.status === 'complete' ? 'completed' : 'pending']">
              {{ task.status === 'complete' ? 'Completed' : 'Pending' }}
            </span>
          </div>

          <div class="task-card-body">
            <div class="task-info-grid">
              <div class="task-info-item">
                <span class="info-icon">
                  <User :size="16" />
                </span>
                <div class="info-content">
                  <span class="info-label">Customer</span>
                  <span class="info-value">{{ task.customer || `Customer ${task.customer_id}` }}</span>
                </div>
              </div>

              <div class="task-info-item">
                <span class="info-icon">
                  <Briefcase :size="16" />
                </span>
                <div class="info-content">
                  <span class="info-label">Assigned To</span>
                  <span class="info-value">{{ task.employee || task.assignedTo || `Employee ${task.employee_id}` }}</span>
                </div>
              </div>

              <div class="task-info-item">
                <span class="info-icon">
                  <Calendar :size="16" />
                </span>
                <div class="info-content">
                  <span class="info-label">Due Date</span>
                  <span class="info-value">{{ formatDate(task.due_date || task.due) }}</span>
                </div>
              </div>
            </div>

            <div v-if="task.description" class="task-description">
              <p>{{ task.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <ClipboardList :size="64" class="empty-icon" />
        <h5>No Active Tasks</h5>
        <p class="text-muted">All tasks have been completed. Great work!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { ClipboardList, RefreshCw, User, Briefcase, Calendar } from 'lucide-vue-next';

const tasks = ref([]);
const loading = ref(true);
const BASE = 'http://127.0.0.1:5000';

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

const fetchTasks = async () => {
  loading.value = true;
  try {
    const response = await fetch(`${BASE}/api/task/get`);
    if (!response.ok) throw new Error('Failed to fetch tasks');
    const data = await response.json();
    tasks.value = data;
  } catch (err) {
    console.error('Error fetching tasks:', err);
    alert('Failed to load tasks. Please try again.');
  } finally {
    loading.value = false;
  }
};

const refreshTasks = () => {
  fetchTasks();
};

const sortedTasks = computed(() => {
  return [...tasks.value].sort((a, b) => {
    const aIsComplete = a.status === 'complete';
    const bIsComplete = b.status === 'complete';
    if (aIsComplete && !bIsComplete) return 1;
    if (!aIsComplete && bIsComplete) return -1;
    return 0;
  });
});

onMounted(() => {
  fetchTasks();
});
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4a90e2;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spinning {
  animation: spin 1s linear infinite;
}

.tasks-container {
  display: grid;
  gap: 20px;
}

.task-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-left: 5px solid #ccc;
  transition: all 0.3s ease;
  position: relative;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

/* Color code by status - pending = orange, completed = green */
.task-card.pending {
  border-left-color: #ff9800;
  background: #fff4e6;
  border: 2px solid rgba(255, 152, 0, 0.2);
}

.task-card.completed {
  border-left-color: #4caf50;
  background: #e8f5e9;
  border: 2px solid rgba(76, 175, 80, 0.2);
}

.task-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  gap: 16px;
}

.task-title-section {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.task-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.priority-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: white;
}

.priority-badge.high {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.priority-badge.medium {
  background: linear-gradient(135deg, #f39c12, #e67e22);
}

.priority-badge.low {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.status-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  white-space: nowrap;
}

.status-badge.completed {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  color: white;
}

.status-badge.pending {
  background: linear-gradient(135deg, #f39c12, #e67e22);
  color: white;
}

.task-card-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.task-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.task-info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 10px;
}

.info-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #4a90e2, #357abd);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.info-label {
  font-size: 0.75rem;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.info-value {
  font-size: 0.95rem;
  color: #2c3e50;
  font-weight: 600;
}

.task-description {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 3px solid #4a90e2;
}

.task-description p {
  margin: 0;
  color: #555;
  line-height: 1.6;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.empty-icon {
  color: #bdc3c7;
  margin-bottom: 20px;
}

.empty-state h5 {
  color: #2c3e50;
  margin-bottom: 8px;
}
</style>

