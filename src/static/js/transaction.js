// Transaction handling
document.addEventListener('DOMContentLoaded', function() {
    const transactionForm = document.getElementById('transaction-form');
    
    if (transactionForm) {
        transactionForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Transaction form submitted');
            
            const transactionData = {
                amount: parseFloat(document.getElementById('amount').value),
                merchant: getMerchantValue(),
                merchant_category: document.getElementById('merchant-category').value,
                location: getLocationValue(),
                payment_channel: document.getElementById('payment-channel').value,
                device_used: document.getElementById('device-used').value
            };

            console.log('Transaction data:', transactionData);

            // Validate form
            if (!validateTransactionForm(transactionData)) {
                return;
            }

            await processTransaction(transactionData);
        });
    } else {
        console.error('Transaction form not found');
    }
});

function getMerchantValue() {
    const merchantSelect = document.getElementById('merchant');
    const merchantOther = document.getElementById('merchant-other');
    
    if (merchantSelect.value === 'other') {
        return merchantOther.value || 'Unknown';
    }
    return merchantSelect.value;
}

function getLocationValue() {
    const locationSelect = document.getElementById('location');
    const locationOther = document.getElementById('location-other');
    
    if (locationSelect.value === 'other') {
        return locationOther.value || 'Unknown';
    }
    return locationSelect.value;
}

function validateTransactionForm(data) {
    console.log('Validating transaction form:', data);
    
    if (!data.amount || data.amount <= 0) {
        app.showError('Please enter a valid amount');
        return false;
    }
    
    if (!data.merchant || !data.merchant_category || !data.location || 
        !data.payment_channel || !data.device_used) {
        app.showError('Please fill in all required fields');
        return false;
    }
    
    console.log('Transaction form validation passed');
    return true;
}

async function processTransaction(transactionData) {
    console.log('Processing transaction:', transactionData);
    
    try {
        app.showLoading();
        
        // Step 1: Predict fraud
        console.log('Sending prediction request...');
        const predictionResponse = await fetch(`${app.API_BASE_URL}/transaction/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(transactionData)
        });

        if (!predictionResponse.ok) {
            throw new Error(`Failed to analyze transaction: ${predictionResponse.status}`);
        }

        const predictionResult = await predictionResponse.json();
        console.log('Prediction result:', predictionResult);
        
        app.hideLoading();

        // Step 2: Handle based on prediction
        if (predictionResult.is_fraud) {
            console.log('Fraud detected, showing alert');
            showFraudAlert(predictionResult, transactionData);
        } else {
            console.log('No fraud detected, completing transaction');
            await completeTransaction(predictionResult, transactionData);
        }

    } catch (error) {
        console.error('Transaction processing error:', error);
        app.hideLoading();
        app.showError('Transaction failed: ' + error.message);
    }
}

function showFraudAlert(predictionResult, transactionData) {
    console.log('Showing fraud alert modal');
    
    const modal = document.getElementById('fraud-alert-modal');
    const fraudScore = document.getElementById('fraud-score');
    const alertAmount = document.getElementById('alert-amount');
    const alertMerchant = document.getElementById('alert-merchant');
    const alertLocation = document.getElementById('alert-location');
    const alertTime = document.getElementById('alert-time');
    const fraudReasons = document.getElementById('fraud-reasons');

    if (!modal) {
        console.error('Fraud alert modal not found');
        return;
    }

    // Update modal content
    if (fraudScore) fraudScore.textContent = `${predictionResult.fraud_probability}%`;
    if (alertAmount) alertAmount.textContent = `$${transactionData.amount.toFixed(2)}`;
    if (alertMerchant) alertMerchant.textContent = transactionData.merchant;
    if (alertLocation) alertLocation.textContent = transactionData.location;
    if (alertTime) alertTime.textContent = new Date().toLocaleString();

    // Update fraud reasons
    if (fraudReasons && predictionResult.flagged_reasons) {
        fraudReasons.innerHTML = predictionResult.flagged_reasons
            .map(reason => `<li>${reason}</li>`)
            .join('');
    }

    // Store pending transaction
    app.currentState.pendingTransaction = {
        predictionResult,
        transactionData
    };

    // Show modal
    modal.classList.remove('hidden');
    console.log('Fraud alert modal shown');

    // Setup modal actions
    setupFraudModalActions();
}

function setupFraudModalActions() {
    console.log('Setting up fraud modal actions');
    
    const approveBtn = document.getElementById('approve-transaction');
    const cancelBtn = document.getElementById('cancel-transaction');
    const modal = document.getElementById('fraud-alert-modal');

    if (!approveBtn || !cancelBtn) {
        console.error('Modal action buttons not found');
        return;
    }

    // Remove existing event listeners
    const newApproveBtn = approveBtn.cloneNode(true);
    const newCancelBtn = cancelBtn.cloneNode(true);
    approveBtn.parentNode.replaceChild(newApproveBtn, approveBtn);
    cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);

    // Add new event listeners
    newApproveBtn.addEventListener('click', async () => {
        console.log('User approved fraudulent transaction');
        modal.classList.add('hidden');
        app.showLoading();
        await completeTransaction(
            app.currentState.pendingTransaction.predictionResult,
            app.currentState.pendingTransaction.transactionData,
            true // User approved despite fraud warning
        );
    });

    newCancelBtn.addEventListener('click', () => {
        console.log('User cancelled transaction due to fraud');
        modal.classList.add('hidden');
        app.showSuccess('Transaction was cancelled due to fraud concerns.');
    });

    console.log('Fraud modal actions setup completed');
}

async function completeTransaction(predictionResult, transactionData, userApproved = false) {
    console.log('Completing transaction:', { predictionResult, transactionData, userApproved });
    
    try {
        app.showLoading();

        const processResponse = await fetch(`${app.API_BASE_URL}/transaction/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                transaction_data: predictionResult.transaction_data,
                is_fraud: predictionResult.is_fraud,
                user_approved: userApproved
            })
        });

        if (!processResponse.ok) {
            throw new Error(`Failed to process transaction: ${processResponse.status}`);
        }

        const processResult = await processResponse.json();
        console.log('Process result:', processResult);
        
        app.hideLoading();

        if (processResult.success) {
            app.showSuccess(processResult.message);
            // Reset form
            document.getElementById('transaction-form').reset();
            // Hide any "other" inputs
            document.getElementById('merchant-other').classList.add('hidden');
            document.getElementById('location-other').classList.add('hidden');
            // Reload data to update balance and transactions
            await app.loadInitialData();
        } else {
            app.showError(processResult.message);
        }

    } catch (error) {
        console.error('Transaction completion error:', error);
        app.hideLoading();
        app.showError('Transaction failed: ' + error.message);
    }
}

// Load full transaction history for transactions section
async function loadFullTransactionHistory() {
    console.log('Loading full transaction history...');
    try {
        const response = await app.fetchWithTimeout(`${app.API_BASE_URL}/transactions`, 5000);
        
        if (response.ok) {
            const transactions = await response.json();
            updateFullTransactionTable(transactions);
            console.log('Full transaction history loaded');
        } else {
            console.error('Failed to load transaction history');
        }
    } catch (error) {
        console.error('Error loading transaction history:', error);
    }
}

function updateFullTransactionTable(transactions) {
    console.log('Updating full transaction table');
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

// Load security stats
async function loadSecurityStats() {
    console.log('Loading security stats...');
    try {
        const response = await app.fetchWithTimeout(`${app.API_BASE_URL}/stats`, 5000);
        
        if (response.ok) {
            const data = await response.json();
            const totalAnalyzed = document.getElementById('total-analyzed');
            const fraudDetected = document.getElementById('fraud-detected');
            
            if (totalAnalyzed) totalAnalyzed.textContent = data.total_transactions || 0;
            if (fraudDetected) fraudDetected.textContent = data.fraud_detected || 0;
            console.log('Security stats loaded');
        } else {
            console.error('Failed to load security stats');
        }
    } catch (error) {
        console.error('Error loading security stats:', error);
    }
}

// Helper functions
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
        if (dateTimeStr.includes('-')) {
            const [datePart, timePart] = dateTimeStr.split(' ');
            const [day, month, year] = datePart.split('-');
            const date = new Date(`${month}-${day}-${year} ${timePart}`);
            if (!isNaN(date.getTime())) {
                return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
            }
        }
        
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

// Export functions for global access
window.loadFullTransactionHistory = loadFullTransactionHistory;
window.loadSecurityStats = loadSecurityStats;

console.log('transaction.js loaded successfully');