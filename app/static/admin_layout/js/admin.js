// Admin Layout JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize admin dashboard
    initializeAdminDashboard();
    
    // Initialize data tables
    initializeDataTables();
    
    // Initialize charts
    initializeCharts();
    
    // Initialize tooltips and popovers
    initializeBootstrapComponents();
    
    // Handle sidebar toggle
    setupSidebarToggle();
    
    // Handle theme switcher
    setupThemeSwitcher();
    
    // Setup form handling
    setupFormHandling();
    
    // Setup bulk actions
    setupBulkActions();
    
    // Setup notification system
    setupNotifications();
});

// Initialize admin dashboard
function initializeAdminDashboard() {
    // Load dashboard stats
    loadDashboardStats();
    
    // Setup real-time updates
    setupRealTimeUpdates();
    
    // Handle dashboard card interactions
    setupDashboardCards();
}

// Initialize DataTables
function initializeDataTables() {
    const tables = document.querySelectorAll('.data-table');
    
    tables.forEach(table => {
        if ($.fn.DataTable.isDataTable(table)) {
            $(table).DataTable().destroy();
        }
        
        $(table).DataTable({
            responsive: true,
            pageLength: 25,
            lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
            order: [[0, 'desc']],
            dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
                 '<"row"<"col-sm-12"tr>>' +
                 '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
            language: {
                search: "Search:",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ entries",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "Next",
                    previous: "Previous"
                }
            },
            drawCallback: function() {
                // Reinitialize tooltips after table draw
                $('[data-bs-toggle="tooltip"]').tooltip();
            }
        });
    });
}

// Initialize charts
function initializeCharts() {
    // User registration chart
    const userChartCtx = document.getElementById('userRegistrationChart');
    if (userChartCtx) {
        createUserRegistrationChart(userChartCtx);
    }
    
    // Job applications chart
    const jobChartCtx = document.getElementById('jobApplicationsChart');
    if (jobChartCtx) {
        createJobApplicationsChart(jobChartCtx);
    }
    
    // Revenue chart
    const revenueChartCtx = document.getElementById('revenueChart');
    if (revenueChartCtx) {
        createRevenueChart(revenueChartCtx);
    }
    
    // Activity chart
    const activityChartCtx = document.getElementById('activityChart');
    if (activityChartCtx) {
        createActivityChart(activityChartCtx);
    }
}

// Create user registration chart
function createUserRegistrationChart(ctx) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Job Seekers',
                data: [120, 150, 180, 220, 260, 290],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.4
            }, {
                label: 'Consultancies',
                data: [20, 25, 30, 35, 45, 52],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Create job applications chart
function createJobApplicationsChart(ctx) {
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Pending', 'Under Review', 'Accepted', 'Rejected'],
            datasets: [{
                data: [45, 30, 15, 10],
                backgroundColor: [
                    '#ffc107',
                    '#17a2b8',
                    '#28a745',
                    '#dc3545'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Create revenue chart
function createRevenueChart(ctx) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Q1', 'Q2', 'Q3', 'Q4'],
            datasets: [{
                label: 'Revenue ($)',
                data: [15000, 25000, 35000, 45000],
                backgroundColor: 'rgba(0, 123, 255, 0.8)',
                borderColor: '#007bff',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// Create activity chart
function createActivityChart(ctx) {
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Job Posts', 'Applications', 'Interviews', 'Hires', 'Reviews'],
            datasets: [{
                label: 'This Month',
                data: [85, 90, 70, 60, 80],
                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                borderColor: '#007bff',
                pointBackgroundColor: '#007bff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Initialize Bootstrap components
function initializeBootstrapComponents() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Initialize modals
    var modalElements = document.querySelectorAll('.modal');
    modalElements.forEach(function(modal) {
        new bootstrap.Modal(modal);
    });
}

// Setup sidebar toggle
function setupSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            if (mainContent) {
                mainContent.classList.toggle('expanded');
            }
            
            // Save state to localStorage
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
        
        // Restore sidebar state
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
            if (mainContent) {
                mainContent.classList.add('expanded');
            }
        }
    }
}

// Setup theme switcher
function setupThemeSwitcher() {
    const themeToggle = document.getElementById('themeToggle');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            
            // Save theme preference
            const isDark = document.body.classList.contains('dark-theme');
            localStorage.setItem('darkTheme', isDark);
            
            // Update icon
            const icon = themeToggle.querySelector('i');
            if (isDark) {
                icon.className = 'fas fa-sun';
            } else {
                icon.className = 'fas fa-moon';
            }
        });
        
        // Restore theme preference
        const isDark = localStorage.getItem('darkTheme') === 'true';
        if (isDark) {
            document.body.classList.add('dark-theme');
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = 'fas fa-sun';
            }
        }
    }
}

// Setup form handling
function setupFormHandling() {
    // Handle AJAX form submissions
    const ajaxForms = document.querySelectorAll('form[data-ajax="true"]');
    ajaxForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleAjaxFormSubmission(this);
        });
    });
    
    // Handle file uploads
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            handleFilePreview(this);
        });
    });
    
    // Handle form validation
    const validationForms = document.querySelectorAll('.needs-validation');
    validationForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Handle AJAX form submission
function handleAjaxFormSubmission(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Show loading state
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    }
    
    fetch(form.action, {
        method: form.method,
        body: formData,
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Operation completed successfully', 'success');
            
            // Handle redirect
            if (data.redirect) {
                window.location.href = data.redirect;
            }
            
            // Handle modal close
            const modal = form.closest('.modal');
            if (modal) {
                bootstrap.Modal.getInstance(modal).hide();
            }
            
            // Reload data table if needed
            if (data.reload_table) {
                const table = document.querySelector('.data-table');
                if (table && $.fn.DataTable.isDataTable(table)) {
                    $(table).DataTable().ajax.reload();
                }
            }
        } else {
            showNotification(data.message || 'Operation failed', 'error');
        }
    })
    .catch(error => {
        console.error('Form submission error:', error);
        showNotification('An error occurred. Please try again.', 'error');
    })
    .finally(() => {
        // Reset submit button
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = submitButton.dataset.originalText || 'Submit';
        }
    });
}

// Handle file preview
function handleFilePreview(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        const previewContainer = input.closest('.form-group').querySelector('.file-preview');
        
        reader.onload = function(e) {
            if (previewContainer) {
                if (file.type.startsWith('image/')) {
                    previewContainer.innerHTML = `<img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px;">`;
                } else {
                    previewContainer.innerHTML = `<p class="text-muted"><i class="fas fa-file me-2"></i>${file.name}</p>`;
                }
            }
        };
        
        reader.readAsDataURL(file);
    }
}

// Setup bulk actions
function setupBulkActions() {
    // Master checkbox
    const masterCheckbox = document.getElementById('masterCheckbox');
    if (masterCheckbox) {
        masterCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.row-checkbox');
            checkboxes.forEach(cb => {
                cb.checked = this.checked;
            });
            updateBulkActionsVisibility();
        });
    }
    
    // Row checkboxes
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    rowCheckboxes.forEach(cb => {
        cb.addEventListener('change', updateBulkActionsVisibility);
    });
    
    // Bulk action buttons
    const bulkActionButtons = document.querySelectorAll('.bulk-action');
    bulkActionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.dataset.action;
            const selectedIds = getSelectedIds();
            
            if (selectedIds.length === 0) {
                showNotification('Please select items to perform this action', 'warning');
                return;
            }
            
            performBulkAction(action, selectedIds);
        });
    });
}

// Update bulk actions visibility
function updateBulkActionsVisibility() {
    const selectedCount = document.querySelectorAll('.row-checkbox:checked').length;
    const bulkActionsBar = document.getElementById('bulkActionsBar');
    const selectedCountSpan = document.getElementById('selectedCount');
    
    if (bulkActionsBar) {
        if (selectedCount > 0) {
            bulkActionsBar.classList.remove('d-none');
            if (selectedCountSpan) {
                selectedCountSpan.textContent = selectedCount;
            }
        } else {
            bulkActionsBar.classList.add('d-none');
        }
    }
}

// Get selected IDs
function getSelectedIds() {
    const checkedBoxes = document.querySelectorAll('.row-checkbox:checked');
    return Array.from(checkedBoxes).map(cb => cb.value);
}

// Perform bulk action
function performBulkAction(action, ids) {
    if (confirm(`Are you sure you want to ${action} ${ids.length} item(s)?`)) {
        fetch(`/admin/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                action: action,
                ids: ids
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(`${action} completed successfully`, 'success');
                location.reload(); // Reload page to see changes
            } else {
                showNotification(data.message || 'Action failed', 'error');
            }
        })
        .catch(error => {
            console.error('Bulk action error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        });
    }
}

// Setup notifications
function setupNotifications() {
    // Auto-hide notifications after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notificationContainer') || createNotificationContainer();
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    notificationContainer.appendChild(notification);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Create notification container
function createNotificationContainer() {
    const container = document.createElement('div');
    container.id = 'notificationContainer';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1050';
    document.body.appendChild(container);
    return container;
}

// Load dashboard stats
function loadDashboardStats() {
    fetch('/admin/api/dashboard-stats')
        .then(response => response.json())
        .then(data => {
            updateDashboardCards(data);
        })
        .catch(error => {
            console.error('Error loading dashboard stats:', error);
        });
}

// Update dashboard cards
function updateDashboardCards(data) {
    const cards = {
        'total-users': data.total_users,
        'total-jobs': data.total_jobs,
        'total-applications': data.total_applications,
        'total-revenue': data.total_revenue
    };
    
    Object.keys(cards).forEach(cardId => {
        const card = document.getElementById(cardId);
        if (card) {
            const valueElement = card.querySelector('.card-value');
            if (valueElement) {
                valueElement.textContent = cards[cardId];
            }
        }
    });
}

// Setup dashboard cards
function setupDashboardCards() {
    const cards = document.querySelectorAll('.dashboard-card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            const url = this.dataset.url;
            if (url) {
                window.location.href = url;
            }
        });
    });
}

// Setup real-time updates
function setupRealTimeUpdates() {
    // Check for updates every 30 seconds
    setInterval(() => {
        loadDashboardStats();
    }, 30000);
}

// Utility functions
function getCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

// Export functions for external use
window.adminJS = {
    showNotification,
    loadDashboardStats,
    updateDashboardCards,
    handleAjaxFormSubmission
};