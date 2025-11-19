// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let currentState = {
    balance: 10000,
    transactions: [],
    pendingTransaction: null
};

// DOM Elements - will be initialized after DOM loads
let elements = {};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing application...');
    
    // CRITICAL FIX: Force hide fraud modal on page load
    const fraudModal = document.getElementById('fraud-alert-modal');
    if (fraudModal) {
        fraudModal.classList.add('hidden');
        fraudModal.style.display = 'none';
        console.log('Fraud modal forcefully hidden on page load');
    }
    
    // Initialize DOM elements
    initializeElements();
    
    // Emergency: Hide loading spinner after 8 seconds no matter what
    setTimeout(() => {
        const spinner = document.getElementById('loading-spinner');
        if (spinner && !spinner.classList.contains('hidden')) {
            console.log('Emergency: Hiding spinner after timeout');
            hideLoading();
        }
    }, 8000);

    initializeNavigation();
    loadInitialData();
    setupEventListeners();
});

// Initialize DOM elements
function initializeElements() {
    elements = {
        navLinks: document.querySelectorAll('.nav-link'),
        contentSections: document.querySelectorAll('.content-section'),
        currentBalance: document.getElementById('current-balance'),
        transactionsList: document.getElementById('transactions-list'),
        fullTransactionsTable: document.getElementById('full-transactions-table')
    };
    
    console.log('DOM elements initialized:', {
        currentBalance: !!elements.currentBalance,
        transactionsList: !!elements.transactionsList,
        fullTransactionsTable: !!elements.fullTransactionsTable,
        navLinks: elements.navLinks.length,
        contentSections: elements.contentSections.length
    });
}

// Navigation
function initializeNavigation() {
    if (!elements.navLinks || elements.navLinks.length === 0) {
        console.warn('No navigation links found');
        return;
    }

    elements.navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.getAttribute('href')?.substring(1);
            if (!targetSection) return;
            
            // Update active nav link
            elements.navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Show target section
            elements.contentSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection) {
                    section.classList.add('active');
                }
            });
            
            // Load section-specific data
            switch(targetSection) {
                case 'transactions':
                    loadFullTransactionHistory();
                    break;
                case 'security':
                    loadSecurityStats();
                    break;
            }
        });
    });
}

// Load initial data
async function loadInitialData() {
    console.log('Starting to load initial data...');
    
    try {
        // Test API connection first with timeout
        const healthPromise = fetch(`${API_BASE_URL}/health`);
        const timeoutPromise = new Promise((_, reject) => 
            setTimeout(() => reject(new Error('API timeout')), 5000)
        );

        const healthResponse = await Promise.race([healthPromise, timeoutPromise]);
        
        if (!healthResponse.ok) {
            throw new Error(`API server error: ${healthResponse.status}`);
        }

        const healthData = await healthResponse.json();
        console.log('API Health:', healthData);

        // Load all data in parallel with timeouts
        const [balanceRes, transactionsRes, statsRes] = await Promise.all([
            fetchWithTimeout(`${API_BASE_URL}/balance`, 5000),
            fetchWithTimeout(`${API_BASE_URL}/transactions`, 5000),
            fetchWithTimeout(`${API_BASE_URL}/stats`, 5000)
        ]);

        console.log('API responses received:', {
            balance: balanceRes.ok,
            transactions: transactionsRes.ok, 
            stats: statsRes.ok
        });

        // Process balance data
        if (balanceRes.ok) {
            const balanceData = await balanceRes.json();
            currentState.balance = balanceData.balance;
            updateBalanceDisplay(balanceData);
            console.log('Balance data loaded successfully');
        } else {
            console.warn('Failed to load balance data, using default');
            updateBalanceDisplay({ balance: 10000 });
        }

        // Process transactions data
        if (transactionsRes.ok) {
            const transactionsData = await transactionsRes.json();
            currentState.transactions = Array.isArray(transactionsData) ? transactionsData : [];
            updateRecentTransactions();
            console.log('Transactions data loaded:', currentState.transactions.length, 'transactions');
        } else {
            console.warn('Failed to load transactions data, using empty array');
            currentState.transactions = [];
            updateRecentTransactions();
        }

        // Process stats data
        if (statsRes.ok) {
            const statsData = await statsRes.json();
            updateQuickStats(statsData);
            console.log('Stats data loaded successfully');
        } else {
            console.warn('Failed to load stats data, using defaults');
            updateQuickStats({
                approved_transactions: 0,
                fraud_detected: 0,
                blocked_transactions: 0
            });
        }
        
        console.log('Initial data loading completed successfully');
        
    } catch (error) {
        console.error('Error loading initial data:', error);
        
        // Show user-friendly error message
        if (error.message.includes('timeout') || error.message.includes('Failed to fetch')) {
            showError('Cannot connect to server. Please make sure the backend is running on localhost:5000');
        } else {
            showError('Failed to load application data: ' + error.message);
        }
        
        // Set default data on error
        updateBalanceDisplay({ balance: 10000 });
        currentState.transactions = [];
        updateRecentTransactions();
        updateQuickStats({
            approved_transactions: 0,
            fraud_detected: 0,
            blocked_transactions: 0
        });
    } finally {
        // Always hide loading spinner
        hideLoading();
        console.log('Initial data loading process finished');
    }
}

// Helper function for fetch with timeout
async function fetchWithTimeout(url, timeout = 5000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        throw error;
    }
}

// Update UI functions
function updateBalanceDisplay(balanceData) {
    console.log('Updating balance display:', balanceData);
    if (elements.currentBalance) {
        elements.currentBalance.textContent = `$${balanceData.balance.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        })}`;
        console.log('Balance updated to:', elements.currentBalance.textContent);
    } else {
        console.error('currentBalance element not found');
        // Try to find it again
        elements.currentBalance = document.getElementById('current-balance');
        if (elements.currentBalance) {
            elements.currentBalance.textContent = `$${balanceData.balance.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })}`;
        }
    }
}

function updateRecentTransactions() {
    console.log('Updating recent transactions:', currentState.transactions);
    const container = elements.transactionsList || document.getElementById('transactions-list');
    
    if (!container) {
        console.error('Transactions list container not found');
        return;
    }

    const recentTransactions = currentState.transactions.slice(-5).reverse();

    if (recentTransactions.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-receipt"></i>
                <p>No transactions yet</p>
            </div>
        `;
        console.log('Displayed empty transactions state');
        return;
    }

    container.innerHTML = recentTransactions.map(transaction => `
        <div class="transaction-item">
            <div class="transaction-info">
                <div class="transaction-icon">
                    <i class="fas fa-shopping-bag"></i>
                </div>
                <div class="transaction-details">
                    <h4>${escapeHtml(transaction.merchant || 'Unknown')}</h4>
                    <p>${formatDateTime(transaction.time)}</p>
                </div>
            </div>
            <div class="transaction-amount">
                $${parseFloat(transaction.amount || 0).toFixed(2)}
            </div>
            <div class="transaction-status ${getStatusClass(transaction.status)}">
                ${getStatusText(transaction.status)}
            </div>
        </div>
    `).join('');
    
    console.log('Updated transactions list with', recentTransactions.length, 'transactions');
}

function updateQuickStats(stats) {
    console.log('Updating quick stats:', stats);
    
    // Try multiple ways to find elements
    const successEl = document.getElementById('success-tx') || document.querySelector('[id="success-tx"]');
    const flaggedEl = document.getElementById('flagged-tx') || document.querySelector('[id="flagged-tx"]');
    const blockedEl = document.getElementById('blocked-tx') || document.querySelector('[id="blocked-tx"]');
    
    console.log('Stats elements found:', {
        success: !!successEl,
        flagged: !!flaggedEl,
        blocked: !!blockedEl
    });
    
    if (successEl) {
        successEl.textContent = stats.approved_transactions || 0;
        console.log('Set success-tx to:', stats.approved_transactions || 0);
    }
    if (flaggedEl) {
        flaggedEl.textContent = stats.fraud_detected || 0;
        console.log('Set flagged-tx to:', stats.fraud_detected || 0);
    }
    if (blockedEl) {
        blockedEl.textContent = stats.blocked_transactions || 0;
        console.log('Set blocked-tx to:', stats.blocked_transactions || 0);
    }
}

function getStatusClass(status) {
    const statusMap = {
        'completed': 'status-completed',
        'completed_override': 'status-completed',
        'cancelled_fraud': 'status-blocked',
        'failed_insufficient_funds': 'status-blocked',
        'failed_error': 'status-blocked',
        'pending': 'status-flagged'
    };
    return statusMap[status] || 'status-completed';
}

function getStatusText(status) {
    const statusMap = {
        'completed': 'Completed',
        'completed_override': 'Approved',
        'cancelled_fraud': 'Blocked',
        'failed_insufficient_funds': 'Failed',
        'failed_error': 'Error',
        'pending': 'Pending'
    };
    return statusMap[status] || 'Completed';
}

function formatDateTime(dateTimeStr) {
    if (!dateTimeStr) return 'Just now';
    try {
        // Handle different date formats
        if (dateTimeStr.includes('-')) {
            const [datePart, timePart] = dateTimeStr.split(' ');
            const [day, month, year] = datePart.split('-');
            const date = new Date(`${month}-${day}-${year} ${timePart}`);
            if (!isNaN(date.getTime())) {
                return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
            }
        }
        
        // Try direct parsing
        const date = new Date(dateTimeStr);
        if (!isNaN(date.getTime())) {
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
        }
        
        return dateTimeStr;
    } catch (e) {
        return dateTimeStr;
    }
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Setup event listeners
function setupEventListeners() {
    console.log('Setting up event listeners...');
    
    // Merchant other input
    const merchantSelect = document.getElementById('merchant');
    const merchantOther = document.getElementById('merchant-other');
    
    if (merchantSelect && merchantOther) {
        merchantSelect.addEventListener('change', function() {
            if (this.value === 'other') {
                merchantOther.classList.remove('hidden');
                merchantOther.required = true;
            } else {
                merchantOther.classList.add('hidden');
                merchantOther.required = false;
            }
        });
        console.log('Merchant select listener added');
    } else {
        console.warn('Merchant select elements not found');
    }

    // Location other input
    const locationSelect = document.getElementById('location');
    const locationOther = document.getElementById('location-other');
    
    if (locationSelect && locationOther) {
        locationSelect.addEventListener('change', function() {
            if (this.value === 'other') {
                locationOther.classList.remove('hidden');
                locationOther.required = true;
            } else {
                locationOther.classList.add('hidden');
                locationOther.required = false;
            }
        });
        console.log('Location select listener added');
    } else {
        console.warn('Location select elements not found');
    }

    // Transaction form - Remove the default submit handler since transaction.js will handle it
    const transactionForm = document.getElementById('transaction-form');
    if (transactionForm) {
        // Remove any existing submit listeners to prevent duplicates
        transactionForm.replaceWith(transactionForm.cloneNode(true));
        console.log('Transaction form prepared for transaction.js handling');
    } else {
        console.warn('Transaction form not found');
    }

    // Close modals when clicking outside
    document.addEventListener('click', function(e) {
        const modal = document.getElementById('fraud-alert-modal');
        if (modal && e.target === modal) {
            modal.classList.add('hidden');
            console.log('Fraud modal closed by clicking outside');
        }
    });

    // Escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('fraud-alert-modal');
            if (modal && !modal.classList.contains('hidden')) {
                modal.classList.add('hidden');
                console.log('Fraud modal closed with Escape key');
            }
        }
    });
    
    console.log('Event listeners setup completed');
}

// Utility functions
function showLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.remove('hidden');
        spinner.style.display = 'flex';
        console.log('Loading spinner shown');
    } else {
        console.warn('Loading spinner element not found');
    }
}

function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.add('hidden');
        spinner.style.display = 'none';
        console.log('Loading spinner hidden');
    }
}

function showSuccess(message) {
    console.log('Showing success message:', message);
    const notification = document.getElementById('success-notification');
    const messageEl = document.getElementById('success-message');
    
    if (notification && messageEl) {
        messageEl.textContent = message;
        notification.classList.remove('hidden');
        
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 5000);
    } else {
        console.warn('Success notification elements not found');
    }
}

function showError(message) {
    console.log('Showing error message:', message);
    const notification = document.getElementById('error-notification');
    const messageEl = document.getElementById('error-message');
    
    if (notification && messageEl) {
        messageEl.textContent = message;
        notification.classList.remove('hidden');
        
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 5000);
    } else {
        console.warn('Error notification elements not found');
    }
}

// Export for use in other files
window.app = {
    currentState,
    API_BASE_URL,
    showLoading,
    hideLoading,
    showSuccess,
    showError,
    updateBalanceDisplay,
    loadInitialData,
    fetchWithTimeout
};

// Make functions globally available for other scripts
window.loadFullTransactionHistory = async function() {
    console.log('Loading full transaction history...');
    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/transactions`, 5000);
        
        if (response.ok) {
            const transactions = await response.json();
            updateFullTransactionTable(transactions);
            console.log('Full transaction history loaded');
        } else {
            console.error('Failed to load transaction history');
            showError('Failed to load transaction history');
        }
    } catch (error) {
        console.error('Error loading transaction history:', error);
        showError('Failed to load transaction history');
    }
};

window.loadSecurityStats = async function() {
    console.log('Loading security stats...');
    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/stats`, 5000);
        
        if (response.ok) {
            const data = await response.json();
            const totalAnalyzed = document.getElementById('total-analyzed');
            const fraudDetected = document.getElementById('fraud-detected');
            
            if (totalAnalyzed) {
                totalAnalyzed.textContent = data.total_transactions || 0;
                console.log('Set total-analyzed to:', data.total_transactions || 0);
            }
            if (fraudDetected) {
                fraudDetected.textContent = data.fraud_detected || 0;
                console.log('Set fraud-detected to:', data.fraud_detected || 0);
            }
            console.log('Security stats loaded');
        } else {
            console.error('Failed to load security stats');
        }
    } catch (error) {
        console.error('Error loading security stats:', error);
    }
};

function updateFullTransactionTable(transactions) {
    console.log('Updating full transaction table with:', transactions);
    const tbody = document.querySelector('#full-transactions-table tbody');
    if (!tbody) {
        console.error('Full transactions table tbody not found');
        return;
    }
    
    if (!transactions || transactions.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-table">No transactions found</td>
            </tr>
        `;
        console.log('Displayed empty table state');
        return;
    }

    tbody.innerHTML = transactions.reverse().map(transaction => `
        <tr>
            <td>${formatDateTime(transaction.time)}</td>
            <td>${escapeHtml(transaction.merchant || 'Unknown')}</td>
            <td>$${parseFloat(transaction.amount || 0).toFixed(2)}</td>
            <td>${escapeHtml(transaction.location || 'Unknown')}</td>
            <td>
                <span class="transaction-status ${getStatusClass(transaction.status)}">
                    ${getStatusText(transaction.status)}
                </span>
            </td>
            <td>
                ${transaction.fraud_probability > 50 ? 
                    `<span style="color: #ef4444; font-weight: 600;">${transaction.fraud_probability}% Risk</span>` : 
                    `<span style="color: #10b981; font-weight: 600;">${transaction.fraud_probability}% Risk</span>`
                }
            </td>
        </tr>
    `).join('');
    
    console.log('Updated full transaction table with', transactions.length, 'transactions');
}

console.log('app.js loaded successfully');