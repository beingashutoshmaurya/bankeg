<template>
  <div>
    <!-- Top Header -->
    <header 
      class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center sticky-top shadow-sm bg-white border-light"
    >
      <div>
        <h4 class="fw-bold text-dark mb-0">Management & Oversight Hub</h4>
        <p class="text-muted mb-0 small">High-level performance metrics and analytics.</p>
      </div>
    </header>

    <!-- Dashboard Content -->
    <div class="p-4">
      <!-- Stats Grid -->
      <section class="stats-grid">
        <div class="stat-card team-members">
          <div class="stat-icon-wrapper">
            <Users :size="24" class="stat-icon" />
          </div>
          <div class="stat-content">
            <span class="stat-label">Team Members</span>
            <span class="stat-value">12</span>
          </div>
        </div>
        <div class="stat-card completed-tasks">
          <div class="stat-icon-wrapper">
            <CheckCircle :size="24" class="stat-icon" />
          </div>
          <div class="stat-content">
            <span class="stat-label">Tasks Completed</span>
            <span class="stat-value">176</span>
          </div>
        </div>
        <div class="stat-card pending-tasks">
          <div class="stat-icon-wrapper">
            <Clock :size="24" class="stat-icon" />
          </div>
          <div class="stat-content">
            <span class="stat-label">Pending Tasks</span>
            <span class="stat-value">34</span>
          </div>
        </div>
        <div class="stat-card efficiency">
          <div class="stat-icon-wrapper">
            <TrendingUp :size="24" class="stat-icon" />
          </div>
          <div class="stat-content">
            <span class="stat-label">Avg Efficiency</span>
            <span class="stat-value">87%</span>
          </div>
        </div>
      </section>

      <!-- Charts Section -->
      <section class="charts-section">
        <div class="chart-panel">
          <div class="chart-header">
            <h4 class="chart-title">Task Performance (Weekly)</h4>
            <span class="chart-subtitle">Tasks completed per day</span>
          </div>
          <div class="chart-container">
            <canvas ref="barChart"></canvas>
          </div>
        </div>

        <div class="chart-panel">
          <div class="chart-header">
            <h4 class="chart-title">Verification Statistics</h4>
            <span class="chart-subtitle">KYC verification status</span>
          </div>
          <div class="chart-container">
            <canvas ref="pieChart"></canvas>
          </div>
        </div>
      </section>

      <!-- Full Width Chart -->
      <div class="chart-panel full-chart">
        <div class="chart-header">
          <h4 class="chart-title">Task Completion Rate – Monthly Trend</h4>
          <span class="chart-subtitle">Performance over the last 6 months</span>
        </div>
        <div class="chart-container">
          <canvas ref="lineChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import { Users, CheckCircle, Clock, TrendingUp } from 'lucide-vue-next';

export default {
  name: 'ManagerDashboardHome',
  components: {
    Users,
    CheckCircle,
    Clock,
    TrendingUp
  },
  methods: {
    initCharts() {
      const primaryColor = '#4a90e2';
      const secondaryColor = '#50e3c2';
      const successColor = '#2ecc71';
      const dangerColor = '#e74c3c';
      const warningColor = '#f39c12';

      // Bar Chart (Task Performance)
      if (this.$refs.barChart) {
        const ctx = this.$refs.barChart.getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
              label: 'Tasks Completed',
              data: [12, 19, 8, 17, 14, 9, 11],
              backgroundColor: primaryColor,
              borderRadius: 8,
              borderSkipped: false,
            }]
          },
          options: { 
            responsive: true, 
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                titleFont: { size: 14, weight: 'bold' },
                bodyFont: { size: 13 },
                cornerRadius: 8
              }
            },
            scales: { 
              y: { 
                beginAtZero: true,
                grid: {
                  color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                  font: { size: 12 }
                }
              },
              x: {
                grid: {
                  display: false
                },
                ticks: {
                  font: { size: 12 }
                }
              }
            } 
          }
        });
      }

      // Pie Chart (Verification Statistics)
      if (this.$refs.pieChart) {
        const ctx = this.$refs.pieChart.getContext('2d');
        new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: ['Approved', 'Pending', 'Rejected'],
            datasets: [{
              data: [63, 29, 8],
              backgroundColor: [successColor, warningColor, dangerColor],
              borderWidth: 0,
            }]
          },
          options: { 
            responsive: true, 
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  padding: 15,
                  font: { size: 12 },
                  usePointStyle: true
                }
              },
              tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                cornerRadius: 8
              }
            }
          }
        });
      }

      // Line Chart (Task Completion Rate – Monthly Trend)
      if (this.$refs.lineChart) {
        const ctx = this.$refs.lineChart.getContext('2d');
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
              label: 'Completion Rate (%)',
              data: [40, 50, 55, 65, 70, 80],
              borderColor: primaryColor,
              backgroundColor: 'rgba(74, 144, 226, 0.1)',
              tension: 0.4,
              fill: true,
              pointRadius: 6,
              pointHoverRadius: 8,
              pointBackgroundColor: primaryColor,
              pointBorderColor: '#fff',
              pointBorderWidth: 2
            }]
          },
          options: { 
            responsive: true, 
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                cornerRadius: 8,
                callbacks: {
                  label: function(context) {
                    return 'Completion Rate: ' + context.parsed.y + '%';
                  }
                }
              }
            },
            scales: { 
              y: { 
                beginAtZero: true, 
                max: 100,
                grid: {
                  color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                  font: { size: 12 },
                  callback: function(value) {
                    return value + '%';
                  }
                }
              },
              x: {
                grid: {
                  display: false
                },
                ticks: {
                  font: { size: 12 }
                }
              }
            } 
          }
        });
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts();
    });
  }
};
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: #ffffff;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
  border-left: 4px solid #ccc;
}

.stat-card:hover { 
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.team-members { 
  border-left-color: #4a90e2;
}
.team-members .stat-icon-wrapper {
  background: linear-gradient(135deg, #4a90e2, #357abd);
  color: white;
}

.completed-tasks { 
  border-left-color: #2ecc71;
}
.completed-tasks .stat-icon-wrapper {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  color: white;
}

.pending-tasks { 
  border-left-color: #e74c3c;
}
.pending-tasks .stat-icon-wrapper {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.efficiency { 
  border-left-color: #50e3c2;
}
.efficiency .stat-icon-wrapper {
  background: linear-gradient(135deg, #50e3c2, #26a69a);
  color: white;
}

.stat-content {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.stat-label {
  font-size: 0.85rem;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1.2;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.chart-panel {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.chart-panel:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.chart-header {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 4px 0;
}

.chart-subtitle {
  font-size: 0.875rem;
  color: #7f8c8d;
}

.chart-container {
  position: relative;
  height: 300px;
}

.full-chart {
  margin-bottom: 24px;
}

.full-chart .chart-container {
  height: 350px;
}

@media (max-width: 1200px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>



