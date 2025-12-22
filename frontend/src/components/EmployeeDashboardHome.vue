<template>
  <div class="dashboard-container p-4">
    <!-- Motivational Alert Bar -->
    <div class="motivational-alert-bar">
      <div class="scroll-text">
        <p>
          **Congratulations!** You're doing great! | **Team Goal:** Complete all pending tasks | Stay productive and focused!
        </p>
      </div>
    </div>
    
    <!-- Header -->
    <header class="dashboard-header">
      <h1>Employee Productivity Hub</h1>
    </header>

    <!-- Stats Grid -->
    <section class="stats-grid">
      <div class="stat-card pending">
        <div class="stat-icon-wrapper pending-icon">
          <Clock :size="28" class="stat-icon" />
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ pendingTasksCount }}</span>
          <span class="stat-label">Pending Tasks</span>
        </div>
      </div>
      <div class="stat-card completed">
        <div class="stat-icon-wrapper completed-icon">
          <CheckCircle :size="28" class="stat-icon" />
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ completedTasksCount }}</span>
          <span class="stat-label">Completed Tasks</span>
        </div>
      </div>
      <div class="stat-card total">
        <div class="stat-icon-wrapper total-icon">
          <ClipboardList :size="28" class="stat-icon" />
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ tasks.length }}</span>
          <span class="stat-label">Total Tasks</span>
        </div>
      </div>
      <div class="stat-card priority">
        <div class="stat-icon-wrapper priority-icon">
          <AlertCircle :size="28" class="stat-icon" />
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ highPriorityCount }}</span>
          <span class="stat-label">High Priority</span>
        </div>
      </div>
    </section>

    <!-- Content Section -->
    <main class="content-section">
      <h2>My Tasks</h2>
      
      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading tasks...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error">
        <p>Error: {{ error }}</p>
        <button @click="fetchTasks" class="retry-btn">Retry</button>
      </div>

      <!-- Empty State -->
      <div v-else-if="tasks.length === 0" class="empty-state">
        <p>No tasks found. Great job!</p>
      </div>

      <!-- Task List -->
      <div v-else class="task-list">
        <div
          class="task-item"
          :class="[getTaskStatusClass(task.status), task.priority.toLowerCase()]"
          v-for="task in sortedTasks"
          :key="task.id"
        >
          <div class="task-content">
            <div class="task-header">
              <p class="task-title">
                {{ task.name }}
              </p>
              <span :class="['priority-bubble', task.priority.toLowerCase()]">
                {{ task.priority.toUpperCase() }}
              </span>
            </div>
            
            <div class="task-info">
              <div class="task-info-row">
                <span class="info-label">Customer:</span>
                <span class="info-value">{{ task.customer }}</span>
              </div>
              <div class="task-info-row">
                <span class="info-label">Employee:</span>
                <span class="info-value">{{ task.employee }}</span>
              </div>
              <div class="task-info-row">
                <span class="info-label">Due Date:</span>
                <span class="info-value">{{ formatDate(task.due_date) }}</span>
              </div>
            </div>
          </div>
          
          <div class="task-footer">
            <span :class="['status-badge', task.status === 'complete' ? 'completed' : 'pending']">
              {{ task.status === 'complete' ? 'Completed' : 'Pending' }}
            </span>
            <button 
              v-if="task.status !== 'complete'" 
              class="complete-btn"
              @click="handleCompleteTask(task.id)"
            >
              Mark Complete
            </button>
          </div>
        </div>
      </div>
    </main>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Clock, CheckCircle, ClipboardList, AlertCircle } from "lucide-vue-next";

const tasks = ref([]);
const loading = ref(true);
const error = ref(null);

// Backend base URL
const BASE = 'http://127.0.0.1:5000';

// Fetch tasks from backend
const fetchTasks = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await fetch(`${BASE}/api/task/get`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch tasks');
    }
    
    const data = await response.json();
    tasks.value = data;
  } catch (err) {
    error.value = err.message;
    console.error('Error fetching tasks:', err);
  } finally {
    loading.value = false;
  }
};

// Complete task function
const handleCompleteTask = async (taskId) => {
  try {
    const response = await fetch(`${BASE}/api/task/update/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to update task');
    }

    await fetchTasks();
    alert('Task completed successfully!');
  } catch (err) {
    alert('Error completing task: ' + err.message);
    console.error('Error completing task:', err);
  }
};

// Format date
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

// Computed properties for stats
const pendingTasksCount = computed(() => 
  tasks.value.filter(t => t.status === 'Pending').length
);

const completedTasksCount = computed(() => 
  tasks.value.filter(t => t.status === 'complete').length
);

const highPriorityCount = computed(() => 
  tasks.value.filter(t => t.priority.toLowerCase() === 'high').length
);

// Sorted tasks - pending first, completed last
const sortedTasks = computed(() => {
  return [...tasks.value].sort((a, b) => {
    const aIsComplete = a.status === 'complete';
    const bIsComplete = b.status === 'complete';
    
    // If one is complete and the other isn't, pending comes first
    if (aIsComplete && !bIsComplete) return 1;
    if (!aIsComplete && bIsComplete) return -1;
    
    // If both have same status, maintain original order
    return 0;
  });
});

// Get CSS class for task status
const getTaskStatusClass = (status) => {
  return status === 'complete' ? 'task-completed' : 'task-pending';
};

// Fetch on mount
onMounted(() => {
  fetchTasks();
});
</script>

<style scoped>
/* Design Variables */
:root {
  --primary-color: #4a90e2;
  --secondary-color: #50e3c2;
  --bg-color: #f4f7f6;
  --card-bg: #ffffff;
  --text-color: #333;
  --shadow-light: 0 4px 12px rgba(0, 0, 0, 0.08);
  --high-priority: #e74c3c;
  --medium-priority: #f39c12;
  --low-priority: #2ecc71;
}

.dashboard-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  color: var(--text-color);
}

.motivational-alert-bar {
  background-color: var(--secondary-color);
  color: var(--text-color);
  padding: 8px 0;
  margin-bottom: 25px;
  overflow: hidden;
  white-space: nowrap;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.motivational-alert-bar .scroll-text {
  display: inline-block;
  padding-left: 100%;
  animation: scroll-left 30s linear infinite;
}

.motivational-alert-bar p {
  margin: 0;
  font-weight: 600;
  color: #1f3a93;
}

@keyframes scroll-left {
  0% { transform: translateX(0%); }
  100% { transform: translateX(-100%); }
}

.dashboard-header h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--primary-color);
  border-bottom: 3px solid var(--secondary-color);
  padding-bottom: 10px;
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: #ffffff;
  padding: 28px;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
  border-left: 4px solid #ccc;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.05), transparent);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.pending-icon {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  color: white;
}

.completed-icon {
  background: linear-gradient(135deg, #4caf50, #388e3c);
  color: white;
}

.total-icon {
  background: linear-gradient(135deg, #4a90e2, #357abd);
  color: white;
}

.priority-icon {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.stat-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 6px;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #2c3e50;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #7f8c8d;
  font-weight: 600;
}

.stat-card.pending { 
  border-left-color: #ff9800;
  background: linear-gradient(to right, #fff4e6 0%, #ffffff 10%);
}

.stat-card.completed { 
  border-left-color: #4caf50;
  background: linear-gradient(to right, #e8f5e9 0%, #ffffff 10%);
}

.stat-card.total { 
  border-left-color: #4a90e2;
  background: linear-gradient(to right, #e3f2fd 0%, #ffffff 10%);
}

.stat-card.priority { 
  border-left-color: #e74c3c;
  background: linear-gradient(to right, #fff5f5 0%, #ffffff 10%);
}

.content-section h2 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: var(--shadow-light);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-color);
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

.error {
  padding: 40px;
  text-align: center;
  background: #ffeaea;
  border-radius: 12px;
  box-shadow: var(--shadow-light);
}

.retry-btn {
  background-color: var(--primary-color);
  color: white;
  padding: 10px 25px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.retry-btn:hover {
  background-color: #357abd;
}

.empty-state {
  padding: 60px;
  text-align: center;
  font-size: 1.3rem;
  color: #666;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: var(--shadow-light);
}

.task-list {
  display: grid;
  gap: 20px;
}

.task-item {
  background: var(--card-bg);
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.3s ease;
  border-left: 5px solid #ccc;
  position: relative;
  overflow: hidden;
}

.task-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.05), transparent);
}

.task-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

/* Task Status Colors */
.task-item.task-pending {
  background: #fff4e6;
  border-left-color: #ff9800;
}

.task-item.task-completed {
  background: #e8f5e9;
  border-left-color: #4caf50;
}

.task-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.task-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  color: #2c3e50;
  flex: 1;
  line-height: 1.4;
}

.priority-bubble {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: white;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.priority-bubble.high {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.priority-bubble.medium {
  background: linear-gradient(135deg, #f39c12, #e67e22);
}

.priority-bubble.low {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.task-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.task-info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.info-label {
  font-weight: 600;
  color: #555;
  min-width: 80px;
}

.info-value {
  color: #2c3e50;
  font-weight: 500;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.status-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.status-badge.completed {
  background: linear-gradient(135deg, #4caf50, #45a049);
  color: white;
}

.status-badge.pending {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  color: white;
}

.complete-btn {
  background-color: var(--primary-color);
  color: var(--card-bg);
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.complete-btn:hover {
  background-color: #357abd;
}

.kyc-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 8px;
}

.kyc-card {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-left: 5px solid var(--primary-color);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.15);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.kyc-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
}

.kyc-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(74, 144, 226, 0.25);
}

.kyc-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  gap: 16px;
}

.kyc-customer-info {
  flex: 1;
}

.kyc-customer-name {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0 0 6px 0;
  color: #1565c0;
}

.kyc-customer-id {
  font-size: 0.85rem;
  color: #1976d2;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.6);
  padding: 4px 10px;
  border-radius: 12px;
  display: inline-block;
}

.kyc-actions-top {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.kyc-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.kyc-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.kyc-btn-primary {
  background: linear-gradient(135deg, #1565c0, #0d47a1);
  color: white;
  font-weight: 700;
  box-shadow: 0 3px 8px rgba(21, 101, 192, 0.4);
}

.kyc-btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #0d47a1, #0a3d7a);
  transform: translateY(-2px);
  box-shadow: 0 5px 12px rgba(21, 101, 192, 0.5);
}

.kyc-btn-secondary {
  background: linear-gradient(135deg, #ffffff, #f5f5f5);
  color: #1565c0;
  border: 2px solid #1565c0;
  font-weight: 700;
  box-shadow: 0 3px 8px rgba(21, 101, 192, 0.2);
}

.kyc-btn-secondary:hover:not(:disabled) {
  background: linear-gradient(135deg, #1565c0, #0d47a1);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 12px rgba(21, 101, 192, 0.4);
}

.kyc-btn-success {
  background: linear-gradient(135deg, #2e7d32, #1b5e20);
  color: white;
  font-weight: 700;
  box-shadow: 0 3px 8px rgba(46, 125, 50, 0.4);
}

.kyc-btn-success:hover:not(:disabled) {
  background: linear-gradient(135deg, #1b5e20, #155017);
  transform: translateY(-2px);
  box-shadow: 0 5px 12px rgba(46, 125, 50, 0.5);
}

.kyc-btn-danger {
  background: linear-gradient(135deg, #c62828, #b71c1c);
  color: white;
  font-weight: 700;
  box-shadow: 0 3px 8px rgba(198, 40, 40, 0.4);
}

.kyc-btn-danger:hover:not(:disabled) {
  background: linear-gradient(135deg, #b71c1c, #a01515);
  transform: translateY(-2px);
  box-shadow: 0 5px 12px rgba(198, 40, 40, 0.5);
}

.kyc-card-body {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.kyc-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.kyc-info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.kyc-info-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #1976d2;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.kyc-info-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #0d47a1;
}

.kyc-documents {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}

.kyc-doc-btn {
  background: linear-gradient(135deg, var(--secondary-color), #26a69a);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(80, 227, 194, 0.3);
}

.kyc-doc-btn:hover {
  background: linear-gradient(135deg, #26a69a, #00897b);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(80, 227, 194, 0.4);
}

.kyc-doc-btn:active {
  transform: translateY(0);
}

.kyc-ai-status {
  margin-top: 12px;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 6px;
  border-left: 3px solid var(--secondary-color);
  display: flex;
  align-items: center;
  gap: 8px;
}

.kyc-ai-status-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1976d2;
}

.kyc-ai-status-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: #0d47a1;
}

.kyc-ai-result {
  margin-top: 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 16px;
  border: 2px dashed var(--primary-color);
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.kyc-ai-remarks {
  flex: 1;
  min-width: 300px;
}

.kyc-ai-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1565c0;
  margin: 0 0 10px 0;
}

.kyc-ai-text {
  white-space: pre-wrap;
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #0d47a1;
  background: rgba(227, 242, 253, 0.5);
  padding: 12px;
  border-radius: 6px;
}

.kyc-action-panel {
  width: 280px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.kyc-comment-input {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  border-radius: 6px;
  border: 2px solid rgba(25, 118, 210, 0.3);
  font-family: inherit;
  font-size: 0.9rem;
  resize: vertical;
  color: #0d47a1;
  background: white;
}

.kyc-comment-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.kyc-comment-input::placeholder {
  color: #90caf9;
}

.kyc-action-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.kyc-loading-text {
  font-size: 0.85rem;
  color: #1976d2;
  font-weight: 600;
  text-align: center;
  padding: 8px;
}

.kyc-waiting {
  margin-top: 16px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
  text-align: center;
  color: #1976d2;
  font-weight: 600;
  font-size: 0.9rem;
}

.kyc-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 20px;
}

.kyc-section-header h2 {
  margin: 0;
  flex: 1;
}

.kyc-refresh-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #ff6b35, #f7931e);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(255, 107, 53, 0.4);
  white-space: nowrap;
}

.kyc-refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #f7931e, #e8851a);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 107, 53, 0.5);
}

.kyc-refresh-btn:active:not(:disabled) {
  transform: translateY(0);
}

.kyc-refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.refresh-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.kyc-empty-message {
  color: #1976d2;
  font-weight: 600;
  font-size: 0.95rem;
  padding: 8px 16px;
  background: rgba(227, 242, 253, 0.6);
  border-radius: 6px;
}

.issues-section {
  margin-top: 40px;
  padding: 20px;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: var(--shadow-light);
}

.issue-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.issue-item {
  padding: 18px;
  background: #fafafa;
  border-left: 5px solid #e67e22;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.issue-item.issue-pending {
  background: #fff4e6;
  border-left-color: #ff9800;
}

.issue-item.issue-resolved {
  background: #e8f5e9;
  border-left-color: #4caf50;
}

.issue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.issue-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  flex: 1;
}

.issue-status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.issue-status-badge.resolved {
  background-color: #4caf50;
  color: white;
}

.issue-status-badge.pending {
  background-color: #ff9800;
  color: white;
}

.issue-desc {
  margin: 5px 0;
  color: #444;
}

.issue-actions {
  margin-top: 10px;
  display: flex;
  gap: 15px;
}

.action-btn {
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.ai-btn {
  background: #3498db;
  color: white;
}

.resolve-btn {
  background: #27ae60;
  color: white;
}

.ai-output-box {
  margin-top: 15px;
  padding: 12px;
  background: #eef6ff;
  border-left: 4px solid #2980b9;
  border-radius: 6px;
}

/* Document Dialog Styles */
.document-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.document-dialog {
  background: white;
  border-radius: 12px;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.document-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--primary-color), #1565c0);
  color: white;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.document-dialog-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
}

.document-dialog-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 28px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
  padding: 0;
}

.document-dialog-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.document-dialog-body {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: auto;
  flex: 1;
  min-height: 0;
}

.document-image {
  width: 100%;
  height: 100%;
  min-height: 70%;
  max-width: 100%;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>

