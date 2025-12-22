<template>
  <div>
    <!-- Top Header -->
    <header 
      class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center sticky-top shadow-sm bg-white border-light"
    >
      <div>
        <h4 class="fw-bold text-dark mb-0">Create & Assign Task</h4>
        <p class="text-muted mb-0 small">Create new tasks and assign them to your team members.</p>
      </div>
    </header>

    <!-- Content -->
    <div class="p-4">
      <div class="create-task-container">
        <div class="form-card">
          <div class="form-header">
            <h5 class="form-title">Task Details</h5>
            <p class="form-subtitle">Fill in the information below to create and assign a new task</p>
          </div>

          <form @submit.prevent="createTask" class="task-form">
            <div class="form-row">
              <div class="form-group">
                <label for="title">
                  <FileText :size="18" class="label-icon" />
                  Task Title <span class="required">*</span>
                </label>
                <input 
                  id="title" 
                  v-model="newTask.title" 
                  type="text"
                  placeholder="e.g., Process payment dispute" 
                  required
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="customer">
                  <User :size="18" class="label-icon" />
                  Customer ID <span class="required">*</span>
                </label>
                <input 
                  id="customer" 
                  type="number"
                  v-model="newTask.customer_id" 
                  placeholder="Enter customer ID" 
                  required
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label for="assignedTo">
                  <Briefcase :size="18" class="label-icon" />
                  Employee ID <span class="required">*</span>
                </label>
                <input 
                  id="assignedTo" 
                  type="number"
                  v-model="newTask.employee_id" 
                  placeholder="Enter employee ID" 
                  required
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="priority">
                  <AlertCircle :size="18" class="label-icon" />
                  Priority <span class="required">*</span>
                </label>
                <select id="priority" v-model="newTask.priority" required class="form-input">
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>

              <div class="form-group">
                <label for="due">
                  <Calendar :size="18" class="label-icon" />
                  Due Date <span class="required">*</span>
                </label>
                <input 
                  id="due" 
                  type="date" 
                  v-model="newTask.due" 
                  required
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="description">
                <FileText :size="18" class="label-icon" />
                Task Description
              </label>
              <textarea 
                id="description" 
                v-model="newTask.description" 
                placeholder="Brief description of the required action..."
                rows="4"
                class="form-input"
              ></textarea>
            </div>

            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="resetForm">
                <X :size="18" />
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                <PlusCircle :size="18" />
                {{ submitting ? 'Creating...' : 'Create & Assign Task' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Success Message -->
        <div v-if="showSuccess" class="success-message">
          <CheckCircle :size="24" />
          <div>
            <h6>Task Created Successfully!</h6>
            <p>The task has been assigned to the employee.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { 
  FileText, 
  User, 
  Briefcase, 
  AlertCircle, 
  Calendar, 
  X, 
  PlusCircle, 
  CheckCircle 
} from 'lucide-vue-next';

const router = useRouter();
const BASE = 'http://127.0.0.1:5000';

const newTask = ref({
  title: '',
  customer_id: '',
  employee_id: '',
  priority: 'medium',
  due: '',
  description: ''
});

const submitting = ref(false);
const showSuccess = ref(false);

const resetForm = () => {
  newTask.value = {
    title: '',
    customer_id: '',
    employee_id: '',
    priority: 'medium',
    due: '',
    description: ''
  };
  showSuccess.value = false;
};

const createTask = async () => {
  if (!newTask.value.title || !newTask.value.customer_id || !newTask.value.employee_id || !newTask.value.due) {
    alert('Please fill in all required fields');
    return;
  }

  submitting.value = true;
  showSuccess.value = false;

  try {
    const payload = {
      name: newTask.value.title,
      employee_id: parseInt(newTask.value.employee_id),
      customer_id: parseInt(newTask.value.customer_id),
      due_date: newTask.value.due,
      priority: newTask.value.priority.charAt(0).toUpperCase() + newTask.value.priority.slice(1),
      description: newTask.value.description
    };

    const response = await fetch(`${BASE}/api/task/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error('Failed to create task');
    }

    showSuccess.value = true;
    setTimeout(() => {
      resetForm();
    }, 3000);
  } catch (error) {
    console.error('Error creating task:', error);
    alert('Failed to create task. Please try again.');
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.create-task-container {
  max-width: 900px;
  margin: 0 auto;
}

.form-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.form-header {
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.form-subtitle {
  font-size: 0.95rem;
  color: #7f8c8d;
  margin: 0;
}

.task-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-weight: 600;
  font-size: 0.95rem;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

.label-icon {
  color: #4a90e2;
}

.required {
  color: #e74c3c;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #ffffff;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
  line-height: 1.6;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
  padding-top: 24px;
  border-top: 2px solid #f0f0f0;
}

.btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #4a90e2, #357abd);
  color: white;
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #357abd, #2a5f8f);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4);
}

.btn-secondary {
  background: #f8f9fa;
  color: #6c757d;
  border: 2px solid #e0e0e0;
}

.btn-secondary:hover {
  background: #e9ecef;
  border-color: #d0d0d0;
}

.success-message {
  margin-top: 24px;
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
  border: 2px solid #28a745;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-message svg {
  color: #28a745;
  flex-shrink: 0;
}

.success-message h6 {
  margin: 0 0 4px 0;
  color: #155724;
  font-weight: 700;
}

.success-message p {
  margin: 0;
  color: #155724;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>



