// Frontend Layout JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize toast notifications
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl);
    });

    // Auto-show toasts
    toastList.forEach(toast => toast.show());

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Search functionality
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            performSearch();
        });
    }

    // File upload handling
    const fileUploadAreas = document.querySelectorAll('.file-upload-area');
    fileUploadAreas.forEach(area => {
        const fileInput = area.querySelector('input[type="file"]');
        
        area.addEventListener('click', () => fileInput.click());
        
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });
        
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileUpload(files[0], area);
            }
        });
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFileUpload(e.target.files[0], area);
                }
            });
        }
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Dynamic form handling
    setupDynamicForms();
    
    // Initialize animations
    initializeAnimations();
});

// Search functionality
function performSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    const locationInput = document.querySelector('input[name="location"]');
    const categorySelect = document.querySelector('select[name="category"]');
    
    const searchParams = {
        search: searchInput ? searchInput.value : '',
        location: locationInput ? locationInput.value : '',
        category: categorySelect ? categorySelect.value : ''
    };
    
    // Show loading state
    showLoadingState();
    
    // Perform API call
    fetch('/api/jobs/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchParams)
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingState();
        displaySearchResults(data);
    })
    .catch(error => {
        hideLoadingState();
        console.error('Search error:', error);
        showToast('Search failed. Please try again.', 'error');
    });
}

// Display search results
function displaySearchResults(data) {
    const resultsContainer = document.getElementById('searchResults');
    if (!resultsContainer) return;
    
    if (data.jobs && data.jobs.length > 0) {
        let html = '';
        data.jobs.forEach(job => {
            html += createJobCard(job);
        });
        resultsContainer.innerHTML = html;
        
        // Add fade-in animation
        resultsContainer.classList.add('fade-in');
    } else {
        resultsContainer.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-search fa-3x text-muted mb-3"></i>
                <h5>No jobs found</h5>
                <p class="text-muted">Try adjusting your search criteria</p>
            </div>
        `;
    }
}

// Create job card HTML
function createJobCard(job) {
    return `
        <div class="card job-card">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <h5 class="job-title">${job.title}</h5>
                        <p class="job-company">${job.company_name}</p>
                        <p class="job-location">
                            <i class="fas fa-map-marker-alt me-1"></i>${job.location}
                        </p>
                        <div class="job-tags">
                            ${job.skills_required ? job.skills_required.split(',').map(skill => 
                                `<span class="badge bg-secondary">${skill.trim()}</span>`
                            ).join('') : ''}
                        </div>
                    </div>
                    <div class="col-md-4 text-md-end">
                        <p class="job-salary">${job.salary_min && job.salary_max ? 
                            `$${job.salary_min} - $${job.salary_max}` : 'Salary not specified'}</p>
                        <button class="btn btn-primary btn-sm" onclick="viewJob(${job.id})">
                            View Details
                        </button>
                        <button class="btn btn-outline-primary btn-sm ms-1" onclick="applyToJob(${job.id})">
                            Apply Now
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// File upload handling
function handleFileUpload(file, uploadArea) {
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    if (!allowedTypes.includes(file.type)) {
        showToast('Please upload a PDF or Word document', 'error');
        return;
    }
    
    if (file.size > maxSize) {
        showToast('File size must be less than 5MB', 'error');
        return;
    }
    
    // Show upload progress
    const progressBar = uploadArea.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = '0%';
        progressBar.parentElement.style.display = 'block';
    }
    
    // Simulate upload progress (replace with actual upload logic)
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
        
        if (progress >= 100) {
            clearInterval(interval);
            showToast('File uploaded successfully', 'success');
            updateUploadArea(uploadArea, file.name);
        }
    }, 100);
}

// Update upload area after successful upload
function updateUploadArea(uploadArea, fileName) {
    uploadArea.innerHTML = `
        <div class="text-success">
            <i class="fas fa-check-circle fa-2x mb-2"></i>
            <p class="mb-0">${fileName}</p>
            <small class="text-muted">Click to change file</small>
        </div>
    `;
}

// Toast notifications
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas fa-${getToastIcon(type)} me-2"></i>
            <strong class="me-auto">${getToastTitle(type)}</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// Get toast icon based on type
function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || icons['info'];
}

// Get toast title based on type
function getToastTitle(type) {
    const titles = {
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        'info': 'Info'
    };
    return titles[type] || titles['info'];
}

// Loading states
function showLoadingState() {
    const loadingElements = document.querySelectorAll('.loading-target');
    loadingElements.forEach(element => {
        element.innerHTML = '<div class="text-center py-3"><div class="loading-spinner"></div></div>';
    });
}

function hideLoadingState() {
    // This will be handled by the search results display
}

// Dynamic forms
function setupDynamicForms() {
    // Add skill tags
    const skillInputs = document.querySelectorAll('.skill-input');
    skillInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                addSkillTag(this);
            }
        });
    });
    
    // Remove skill tags
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-skill')) {
            e.target.closest('.skill-tag').remove();
        }
    });
}

// Add skill tag
function addSkillTag(input) {
    const value = input.value.trim();
    if (value) {
        const container = input.parentElement.querySelector('.skills-container');
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.innerHTML = `
            ${value}
            <button type="button" class="btn btn-sm remove-skill ms-1">&times;</button>
            <input type="hidden" name="skills[]" value="${value}">
        `;
        container.appendChild(tag);
        input.value = '';
    }
}

// Initialize animations
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Job-related functions (to be implemented)
function viewJob(jobId) {
    // Implement job details view
    window.location.href = `/jobs/${jobId}`;
}

function applyToJob(jobId) {
    // Implement job application
    if (!isLoggedIn()) {
        showToast('Please login to apply for jobs', 'warning');
        return;
    }
    
    // Show application modal or redirect
    window.location.href = `/jobs/${jobId}/apply`;
}

// Helper functions
function isLoggedIn() {
    // Check if user is logged in
    return document.body.dataset.userId !== undefined;
}

// API helper functions
function makeApiCall(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    };
    
    return fetch(url, { ...defaultOptions, ...options })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
}

function getCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}