// Main JavaScript for TeleQueue Pro

// Global variables
let refreshInterval;
let liveUpdateInterval;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize live updates if on dashboard pages
    if (window.location.pathname.includes('dashboard')) {
        startLiveUpdates();
    }
    
    // Initialize tooltips and interactive elements
    initializeInteractiveElements();
    
    // Initialize auto-refresh for queue data
    if (window.location.pathname.includes('doctor_dashboard')) {
        startQueueRefresh();
    }
}

// Live Updates System
function startLiveUpdates() {
    // Update queue status every 10 seconds
    liveUpdateInterval = setInterval(updateQueueStatus, 10000);
    
    // Initial update
    updateQueueStatus();
}

function updateQueueStatus() {
    fetch('/api/queue_status')
        .then(response => response.json())
        .then(data => {
            updateQueueWidgets(data);
            updateLiveIndicators();
        })
        .catch(error => {
            console.error('Error updating queue status:', error);
        });
}

function updateQueueWidgets(queueData) {
    // Update department patient counts
    const deptCards = document.querySelectorAll('.dept-stat-card');
    
    queueData.forEach(dept => {
        const card = Array.from(deptCards).find(card => 
            card.querySelector('h4').textContent === dept.department
        );
        
        if (card) {
            const countElement = card.querySelector('.patient-count');
            const urgencyElement = card.querySelector('.metric-value');
            
            if (countElement) {
                countElement.textContent = `${dept.patient_count} patients`;
            }
            
            if (urgencyElement) {
                urgencyElement.textContent = dept.avg_urgency.toFixed(1);
            }
        }
    });
}

function updateLiveIndicators() {
    const indicators = document.querySelectorAll('.status-item i');
    indicators.forEach(indicator => {
        indicator.classList.remove('status-red');
        indicator.classList.add('status-green');
    });
}

// Queue Refresh for Doctor Dashboard
function startQueueRefresh() {
    // Refresh every 30 seconds
    refreshInterval = setInterval(() => {
        refreshQueueData();
    }, 30000);
}

function refreshQueueData() {
    // Show loading indicator
    showLoadingIndicator();
    
    // Simulate queue update (in production, this would fetch new data)
    setTimeout(() => {
        hideLoadingIndicator();
        updateQueuePositions();
    }, 1000);
}

function updateQueuePositions() {
    const patientCards = document.querySelectorAll('.patient-card');
    
    patientCards.forEach((card, index) => {
        const positionElement = card.querySelector('.queue-position');
        if (positionElement) {
            // Simulate position changes
            const currentPosition = parseInt(positionElement.textContent.replace('#', ''));
            const newPosition = Math.max(1, currentPosition + Math.floor(Math.random() * 3) - 1);
            positionElement.textContent = `#${newPosition}`;
        }
    });
}

// Interactive Elements
function initializeInteractiveElements() {
    // Priority color coding
    initializePriorityColors();
    
    // Estimated wait time calculations
    calculateWaitTimes();
    
    // Search and filter functionality
    initializeSearchFilters();
}

function initializePriorityColors() {
    const priorityBadges = document.querySelectorAll('.priority-badge');
    
    priorityBadges.forEach(badge => {
        const priority = badge.textContent.toLowerCase().trim();
        badge.classList.add(`priority-${priority}`);
        
        // Add animation for high priority
        if (priority === 'high') {
            badge.style.animation = 'pulse 2s infinite';
        }
    });
}

function calculateWaitTimes() {
    const patientCards = document.querySelectorAll('.patient-card');
    
    patientCards.forEach(card => {
        const priorityBadge = card.querySelector('.priority-badge');
        const queuePosition = card.querySelector('.queue-position');
        
        if (priorityBadge && queuePosition) {
            const priority = priorityBadge.textContent.toLowerCase().trim();
            const position = parseInt(queuePosition.textContent.replace('#', ''));
            
            let baseTime;
            switch (priority) {
                case 'high':
                    baseTime = 5;
                    break;
                case 'medium':
                    baseTime = 15;
                    break;
                case 'low':
                    baseTime = 30;
                    break;
                default:
                    baseTime = 20;
            }
            
            const estimatedWait = baseTime + (position - 1) * 10;
            
            // Add wait time display if it doesn't exist
            let waitTimeElement = card.querySelector('.estimated-wait');
            if (!waitTimeElement) {
                waitTimeElement = document.createElement('div');
                waitTimeElement.className = 'detail-item estimated-wait';
                waitTimeElement.innerHTML = `
                    <i class="fas fa-clock"></i>
                    <span class="detail-label">Est. Wait:</span>
                    <span class="detail-value">${estimatedWait} min</span>
                `;
                
                const detailsContainer = card.querySelector('.patient-details');
                if (detailsContainer) {
                    detailsContainer.appendChild(waitTimeElement);
                }
            }
        }
    });
}

function initializeSearchFilters() {
    // Patient search functionality
    const searchInput = document.getElementById('patientSearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(searchPatients, 300));
    }
    
    // Department filter
    const deptFilter = document.getElementById('departmentFilter');
    if (deptFilter) {
        deptFilter.addEventListener('change', filterByDepartment);
    }
    
    // Priority filter
    const priorityFilter = document.getElementById('priorityFilter');
    if (priorityFilter) {
        priorityFilter.addEventListener('change', filterPatients);
    }
}

// Search and Filter Functions
function searchPatients() {
    const searchTerm = document.getElementById('patientSearch').value.toLowerCase();
    const rows = document.querySelectorAll('#patientsTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const isVisible = text.includes(searchTerm);
        row.style.display = isVisible ? '' : 'none';
        
        // Highlight matching text
        if (searchTerm && isVisible) {
            highlightSearchTerm(row, searchTerm);
        }
    });
}

function highlightSearchTerm(row, term) {
    const cells = row.querySelectorAll('td');
    cells.forEach(cell => {
        const text = cell.textContent;
        if (text.toLowerCase().includes(term)) {
            const regex = new RegExp(`(${term})`, 'gi');
            cell.innerHTML = text.replace(regex, '<mark>$1</mark>');
        }
    });
}

function filterByDepartment() {
    const department = document.getElementById('departmentFilter').value;
    const rows = document.querySelectorAll('#patientsTable tbody tr');
    
    rows.forEach(row => {
        const rowDept = row.getAttribute('data-department');
        row.style.display = (department === '' || rowDept === department) ? '' : 'none';
    });
}

function filterPatients() {
    const filter = document.getElementById('priorityFilter').value;
    const patientCards = document.querySelectorAll('.patient-card');
    
    patientCards.forEach(card => {
        const priority = card.getAttribute('data-priority');
        const isVisible = filter === '' || priority === filter;
        
        if (isVisible) {
            card.style.display = 'block';
            card.style.animation = 'fadeIn 0.3s ease-in';
        } else {
            card.style.display = 'none';
        }
    });
}

// Utility Functions
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

function showLoadingIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'loadingIndicator';
    indicator.className = 'loading-indicator';
    indicator.innerHTML = `
        <div class="spinner-small"></div>
        <span>Updating queue...</span>
    `;
    
    const header = document.querySelector('.queue-header');
    if (header) {
        header.appendChild(indicator);
    }
}

function hideLoadingIndicator() {
    const indicator = document.getElementById('loadingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success':
            return 'check-circle';
        case 'error':
            return 'exclamation-triangle';
        case 'warning':
            return 'exclamation-circle';
        default:
            return 'info-circle';
    }
}

// Queue Optimization Functions
function optimizeQueue(department) {
    showNotification(`Optimizing ${department} queue...`, 'info');
    
    // Simulate optimization process
    setTimeout(() => {
        showNotification(`${department} queue optimized successfully!`, 'success');
        
        // Refresh the page to show updated queue
        if (confirm('Queue optimized! Refresh page to see changes?')) {
            location.reload();
        }
    }, 2000);
}

function optimizeAllQueues() {
    showNotification('Optimizing all department queues...', 'info');
    
    // Simulate optimization process
    setTimeout(() => {
        showNotification('All queues optimized successfully!', 'success');
        
        // Refresh the page to show updated queues
        if (confirm('All queues optimized! Refresh page to see changes?')) {
            location.reload();
        }
    }, 3000);
}

// Emergency Alert System
function checkForEmergencies() {
    const highPriorityCards = document.querySelectorAll('.patient-card[data-priority="High"]');
    
    highPriorityCards.forEach(card => {
        const urgencyScore = parseFloat(card.querySelector('.urgency-score').textContent);
        
        if (urgencyScore > 85) {
            card.classList.add('emergency-alert');
            
            // Add pulsing animation
            card.style.animation = 'emergencyPulse 1.5s infinite';
            
            // Show emergency notification
            const patientName = card.querySelector('.patient-info h3').textContent;
            showNotification(`EMERGENCY: ${patientName} requires immediate attention!`, 'error');
        }
    });
}

// Real-time Updates Simulation
function simulateRealTimeUpdates() {
    setInterval(() => {
        // Simulate new patient arrivals
        if (Math.random() > 0.8) {
            showNotification('New patient registered in queue', 'info');
        }
        
        // Check for emergencies
        checkForEmergencies();
        
        // Update wait times
        calculateWaitTimes();
        
    }, 15000); // Every 15 seconds
}

// Cleanup function
function cleanup() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
    
    if (liveUpdateInterval) {
        clearInterval(liveUpdateInterval);
    }
}

// Handle page unload
window.addEventListener('beforeunload', cleanup);

// CSS Animations (added via JavaScript)
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes emergencyPulse {
        0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(231, 76, 60, 0); }
        100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
    }
    
    .loading-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #3498db;
        font-size: 0.9rem;
    }
    
    .spinner-small {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(52, 152, 219, 0.3);
        border-top: 2px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 2000;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
    }
    
    .notification-success {
        border-left: 4px solid #2ecc71;
        color: #27ae60;
    }
    
    .notification-error {
        border-left: 4px solid #e74c3c;
        color: #c0392b;
    }
    
    .notification-warning {
        border-left: 4px solid #f39c12;
        color: #e67e22;
    }
    
    .notification-info {
        border-left: 4px solid #3498db;
        color: #2980b9;
    }
    
    .notification-close {
        background: none;
        border: none;
        cursor: pointer;
        margin-left: auto;
        color: #999;
    }
    
    .notification-close:hover {
        color: #333;
    }
    
    .emergency-alert {
        border: 2px solid #e74c3c !important;
        background: linear-gradient(135deg, #fee, #fdd) !important;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    mark {
        background: #fff3cd;
        padding: 0.1rem 0.2rem;
        border-radius: 3px;
    }
`;

document.head.appendChild(style);

// Initialize real-time updates simulation
if (window.location.pathname.includes('dashboard')) {
    simulateRealTimeUpdates();
}