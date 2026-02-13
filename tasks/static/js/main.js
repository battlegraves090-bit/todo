/**
 * Main JavaScript file for Todo Application
 * 
 * Handles:
 * - Task interactions (toggle complete, delete)
 * - Form submissions
 * - Dynamic UI updates
 * - AJAX requests
 * - Notifications and messages
 * - Animations and transitions
 */

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Get CSRF token from DOM or cookies
 * @returns {string} CSRF token
 */
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    // Try to get from meta tag if not in cookies
    if (!cookieValue) {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        if (token) {
            cookieValue = token.value;
        }
    }
    return cookieValue;
}

/**
 * Show notification message with animation
 * @param {string} message - Message text
 * @param {string} type - Message type (success, error, info, warning)
 * @param {number} duration - Duration in milliseconds (default 4000)
 */
function showNotification(message, type = 'info', duration = 4000) {
    const container = document.getElementById('notifications') || createNotificationContainer();
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} animate-slide-in`;
    alertDiv.innerHTML = `
        <div class="alert-content">
            <span>${message}</span>
            <button type="button" class="alert-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    container.appendChild(alertDiv);
    
    // Auto-remove with animation
    setTimeout(() => {
        alertDiv.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => alertDiv.remove(), 300);
    }, duration);
}

/**
 * Create notification container if it doesn't exist
 */
function createNotificationContainer() {
    let container = document.getElementById('notifications');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notifications';
        container.className = 'notification-container';
        document.body.insertBefore(container, document.body.firstChild);
    }
    return container;
}

/**
 * Format date to readable format
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', options);
}

/**
 * Calculate days remaining until due date
 * @param {string} dueDate - ISO date string
 * @returns {number} Days remaining
 */
function daysUntilDue(dueDate) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const due = new Date(dueDate);
    due.setHours(0, 0, 0, 0);
    
    const diffTime = due - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays;
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============================================================================
// PROFILE DROPDOWN
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    const profileBtn = document.getElementById('profile-btn');
    const dropdownMenu = document.getElementById('dropdown-menu');
    
    if (profileBtn && dropdownMenu) {
        profileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdownMenu.classList.toggle('active');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!profileBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.remove('active');
            }
        });
    }
});

// ============================================================================
// TASK MANAGEMENT
// ============================================================================

/**
 * Toggle task completion status via AJAX
 * @param {number} taskId - Task ID
 * @param {HTMLElement} checkbox - Checkbox element
 */
function toggleTaskStatus(taskId, checkbox) {
    const csrfToken = getCsrfToken();
    const taskItem = checkbox.closest('.task-item');
    
    fetch(`/api/tasks/${taskId}/toggle/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update UI
            if (data.completed) {
                taskItem.classList.add('completed');
            } else {
                taskItem.classList.remove('completed');
            }
            
            // Update completion percentage if it exists
            updateCompletionStats();
            
            showNotification('Task status updated!', 'success', 2000);
        } else {
            checkbox.checked = !checkbox.checked;
            showNotification('Error updating task', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        checkbox.checked = !checkbox.checked;
        showNotification('Error updating task', 'error');
    });
}

/**
 * Delete task via AJAX
 * @param {number} taskId - Task ID
 */
function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    const csrfToken = getCsrfToken();
    const taskItem = document.querySelector(`[data-task-id="${taskId}"]`);
    
    fetch(`/api/tasks/${taskId}/delete/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Animate removal
            taskItem.style.opacity = '0';
            taskItem.style.transition = 'opacity 0.3s ease';
            
            setTimeout(() => {
                taskItem.remove();
                
                // Update stats
                updateCompletionStats();
                
                // Show empty state if no tasks remain
                const taskList = document.querySelector('.task-list');
                if (taskList?.children.length === 0) {
                    showEmptyState();
                }
                
                showNotification('Task deleted successfully!', 'success', 2000);
            }, 300);
        } else {
            showNotification('Error deleting task', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error deleting task', 'error');
    });
}

/**
 * Quick add task from input
 * @param {HTMLFormElement} form - Form element
 */
function quickAddTask(form) {
    const titleInput = form.querySelector('input[name="title"]');
    const title = titleInput?.value.trim();
    
    if (!title) {
        showNotification('Please enter a task title', 'warning');
        return;
    }
    
    const csrfToken = getCsrfToken();
    
    fetch('/api/tasks/quick-add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ title: title })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Clear input
            titleInput.value = '';
            
            // Refresh task list or add new task to UI
            location.reload(); // Simple reload for now
            
            showNotification('Task added successfully!', 'success', 2000);
        } else {
            showNotification(data.message || 'Error adding task', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding task', 'error');
    });
    
    return false;
}

// ============================================================================
// TASK FILTERING
// ============================================================================

/**
 * Apply task filters
 */
function applyTaskFilters() {
    const statusFilter = document.getElementById('status-filter')?.value || 'all';
    const priorityFilter = document.getElementById('priority-filter')?.value || '';
    const searchInput = document.getElementById('search-input')?.value || '';
    
    const params = new URLSearchParams();
    if (statusFilter !== 'all') {
        params.append('status', statusFilter);
    }
    if (priorityFilter) {
        params.append('priority', priorityFilter);
    }
    if (searchInput) {
        params.append('search', searchInput);
    }
    
    const queryString = params.toString();
    const url = queryString ? `/tasks/?${queryString}` : '/tasks/';
    
    window.location.href = url;
}

/**
 * Setup filter change listeners
 */
document.addEventListener('DOMContentLoaded', function() {
    const filterElements = [
        document.getElementById('status-filter'),
        document.getElementById('priority-filter'),
        document.getElementById('search-input')
    ];
    
    filterElements.forEach(element => {
        if (element) {
            element.addEventListener('change', applyTaskFilters);
        }
    });
    
    // Debounce search input
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(applyTaskFilters, 500));
    }
});

// ============================================================================
// COMPLETION STATS
// ============================================================================

/**
 * Update completion statistics
 */
function updateCompletionStats() {
    const taskList = document.querySelector('.task-list');
    if (!taskList) return;
    
    const allTasks = taskList.querySelectorAll('.task-item');
    const completedTasks = taskList.querySelectorAll('.task-item.completed');
    
    const totalCount = document.getElementById('total-tasks-count');
    const completedCount = document.getElementById('completed-tasks-count');
    const pendingCount = document.getElementById('pending-tasks-count');
    const progressFill = document.getElementById('progress-fill');
    
    if (totalCount) totalCount.textContent = allTasks.length;
    if (completedCount) completedCount.textContent = completedTasks.length;
    if (pendingCount) pendingCount.textContent = allTasks.length - completedTasks.length;
    
    if (progressFill && allTasks.length > 0) {
        const percentage = (completedTasks.length / allTasks.length) * 100;
        progressFill.style.width = `${percentage}%`;
    }
}

// ============================================================================
// EMPTY STATE
// ============================================================================

/**
 * Show empty state message
 */
function showEmptyState() {
    const taskList = document.querySelector('.task-list');
    if (taskList && taskList.children.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state animate-slide-in';
        emptyState.innerHTML = `
            <div class="empty-state-icon">📋</div>
            <h3>No tasks found</h3>
            <p>Create a new task to get started!</p>
            <a href="/tasks/create/" class="btn btn-primary mt-lg">Create Task</a>
        `;
        taskList.appendChild(emptyState);
    }
}

// ============================================================================
// FORM HANDLING
// ============================================================================

/**
 * Setup form validation
 */
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                input.classList.remove('error');
                
                if (!input.value.trim()) {
                    input.classList.add('error');
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'warning');
            }
        });
    });
});

/**
 * Clear form errors when user starts typing
 */
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-input, .form-textarea, .form-select');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('error');
        });
    });
});

// ============================================================================
// PASSWORD CONFIRMATION
// ============================================================================

/**
 * Validate password confirmation matches
 */
document.addEventListener('DOMContentLoaded', function() {
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    
    if (password1 && password2) {
        password2.addEventListener('input', function() {
            if (this.value && password1.value !== this.value) {
                this.classList.add('error');
                if (!this.nextElementSibling?.classList.contains('form-error')) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'form-error';
                    errorDiv.textContent = 'Passwords do not match';
                    this.parentElement.appendChild(errorDiv);
                }
            } else {
                this.classList.remove('error');
                const errorDiv = this.parentElement.querySelector('.form-error');
                if (errorDiv) {
                    errorDiv.remove();
                }
            }
        });
    }
});

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize page functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // Update completion stats if on task list page
    updateCompletionStats();
    
    // Attach task status toggle listeners
    const taskCheckboxes = document.querySelectorAll('.task-checkbox');
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            toggleTaskStatus(taskId, this);
        });
    });
    
    // Add any initial validation
    console.log('Todo app initialized');
});

// ============================================================================
// PROFILE PASSWORD VISIBILITY TOGGLE
// ============================================================================

/**
 * Toggle password field visibility
 */
function togglePasswordVisibility(fieldId) {
    const field = document.getElementById(fieldId);
    const icon = event.target.closest('.password-toggle');
    if (field && icon) {
        field.type = field.type === 'password' ? 'text' : 'password';
        icon.classList.toggle('show');
    }
}

/**
 * Add smooth scroll to elements
 */
function smoothScroll(targetId) {
    const element = document.getElementById(targetId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Add ripple effect to buttons
 */
function addRippleEffect(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    button.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
}

/**
 * Validate form before submission
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            input.focus();
            isValid = false;
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

/**
 * Add input character counter
 */
function updateCharacterCount(inputId, counterId, maxLength) {
    const input = document.getElementById(inputId);
    const counter = document.getElementById(counterId);
    
    if (input && counter) {
        const length = input.value.length;
        counter.textContent = `${length}/${maxLength}`;
        
        if (length >= maxLength * 0.9) {
            counter.classList.add('warning');
        } else {
            counter.classList.remove('warning');
        }
    }
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

/**
 * Show tooltip
 */
function showTooltip(event) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = event.target.dataset.tooltip;
    
    document.body.appendChild(tooltip);
    
    const rect = event.target.getBoundingClientRect();
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
    tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
}

/**
 * Hide tooltip
 */
function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    tooltip?.remove();
}

// ============================================================================
// LOCAL STORAGE HELPERS
// ============================================================================

/**
 * Save preference to local storage
 */
function savePreference(key, value) {
    try {
        localStorage.setItem(`todo_${key}`, JSON.stringify(value));
    } catch (e) {
        console.error('Error saving preference:', e);
    }
}

/**
 * Get preference from local storage
 */
function getPreference(key, defaultValue) {
    try {
        const value = localStorage.getItem(`todo_${key}`);
        return value ? JSON.parse(value) : defaultValue;
    } catch (e) {
        console.error('Error getting preference:', e);
        return defaultValue;
    }
}
