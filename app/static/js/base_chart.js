//-- Chart.js Scripts //
// Manage User Chart
const userCtx = document.getElementById('userChart').getContext('2d');
new Chart(userCtx, {
  type: 'bar',
  data: {
    labels: ['Active Users', 'Inactive Users', 'Banned Users'],
    datasets: [{
      label: 'User Status',
      data: [70, 15, 15],
      backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// View Stats Chart
const statsCtx = document.getElementById('statsChart').getContext('2d');
new Chart(statsCtx, {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April'],
    datasets: [{
      label: 'Monthly Stats',
      data: [50, 60, 70, 80],
      backgroundColor: 'rgba(0, 123, 255, 0.2)',
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// System Configuration Chart
const configCtx = document.getElementById('configChart').getContext('2d');
new Chart(configCtx, {
  type: 'pie',
  data: {
    labels: ['Configured', 'Not Configured'],
    datasets: [{
      data: [80, 20],
      backgroundColor: ['#28a745', '#dc3545'],
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// Activity Logs Chart
const activityLogsCtx = document.getElementById('activityLogsChart').getContext('2d');
new Chart(activityLogsCtx, {
  type: 'line',
  data: {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    datasets: [{
      label: 'Activities Logged',
      data: [10, 20, 25, 30, 35],
      backgroundColor: 'rgba(255, 193, 7, 0.2)',
      borderColor: '#ffc107',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// Server Status Chart
const serverStatusCtx = document.getElementById('serverStatusChart').getContext('2d');
new Chart(serverStatusCtx, {
  type: 'doughnut',
  data: {
    labels: ['Up', 'Down'],
    datasets: [{
      data: [90, 10],
      backgroundColor: ['#28a745', '#dc3545'],
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// Recent Activity Chart
const recentActivityCtx = document.getElementById('recentActivityChart').getContext('2d');
new Chart(recentActivityCtx, {
  type: 'bar',
  data: {
    labels: ['Activity 1', 'Activity 2', 'Activity 3', 'Activity 4'],
    datasets: [{
      label: 'Recent Activities',
      data: [5, 10, 8, 7],
      backgroundColor: '#17a2b8',
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// User Analytics Chart
const userAnalyticsCtx = document.getElementById('userAnalyticsChart').getContext('2d');
new Chart(userAnalyticsCtx, {
  type: 'line',
  data: {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [{
      label: 'User Analytics',
      data: [10, 25, 30, 45],
      backgroundColor: 'rgba(40, 167, 69, 0.2)',
      borderColor: '#28a745',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// Content Management Chart
const contentManagementCtx = document.getElementById('contentManagementChart').getContext('2d');
new Chart(contentManagementCtx, {
  type: 'pie',
  data: {
    labels: ['Published', 'Unpublished'],
    datasets: [{
      data: [70, 30],
      backgroundColor: ['#17a2b8', '#ffc107'],
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// Revenue Stats Chart
const revenueStatsCtx = document.getElementById('revenueStatsChart').getContext('2d');
new Chart(revenueStatsCtx, {
  type: 'bar',
  data: {
    labels: ['January', 'February', 'March', 'April'],
    datasets: [{
      label: 'Revenue',
      data: [100, 200, 300, 400],
      backgroundColor: '#fd7e14',
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// Notifications Chart
const notificationsCtx = document.getElementById('notificationsChart').getContext('2d');
new Chart(notificationsCtx, {
  type: 'doughnut',
  data: {
    labels: ['Read', 'Unread'],
    datasets: [{
      data: [50, 50],
      backgroundColor: ['#28a745', '#dc3545'],
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// System Health Chart
const systemHealthCtx = document.getElementById('systemHealthChart').getContext('2d');
new Chart(systemHealthCtx, {
  type: 'pie',
  data: {
    labels: ['Healthy', 'Critical'],
    datasets: [{
      data: [80, 20],
      backgroundColor: ['#28a745', '#dc3545'],
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// Backup & Restore Chart
const backupRestoreCtx = document.getElementById('backupRestoreChart').getContext('2d');
new Chart(backupRestoreCtx, {
  type: 'bar',
  data: {
    labels: ['Backups Created', 'Restored Backups'],
    datasets: [{
      label: 'Backup and Restore Activity',
      data: [100, 50],
      backgroundColor: '#6c757d',
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// Security Logs Chart
const securityLogsCtx = document.getElementById('securityLogsChart').getContext('2d');
new Chart(securityLogsCtx, {
  type: 'pie',
  data: {
    labels: ['Secure', 'Insecure'],
    datasets: [{
      data: [90, 10],
      backgroundColor: ['#28a745', '#dc3545'],
      borderColor: '#007bff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});

// System Updates Chart
const systemUpdatesCtx = document.getElementById('systemUpdatesChart').getContext('2d');
new Chart(systemUpdatesCtx, {
  type: 'line',
  data: {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [{
      label: 'System Updates',
      data: [1, 2, 3, 4],
      backgroundColor: 'rgba(255, 193, 7, 0.2)',
      borderColor: '#ffc107',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#333' } }
    }
  }
});