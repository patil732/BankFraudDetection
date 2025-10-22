// UI utility functions
document.addEventListener('DOMContentLoaded', function() {
    // Close modal when clicking outside
    const modal = document.getElementById('fraud-alert-modal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    }

    // Escape key to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('fraud-alert-modal');
            if (modal && !modal.classList.contains('hidden')) {
                modal.classList.add('hidden');
            }
        }
    });

    // Form input formatting
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        amountInput.addEventListener('input', function(e) {
            // Format as user types
            let value = e.target.value.replace(/[^\d.]/g, '');
            let parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            e.target.value = value;
        });
    }
});

// Additional UI helpers
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatTime(date) {
    return new Date(date).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// UI utility functions
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing UI...');
    
    // Emergency: Hide loading spinner after 10 seconds no matter what
    setTimeout(() => {
        const spinner = document.getElementById('loading-spinner');
        if (spinner && !spinner.classList.contains('hidden')) {
            console.log('Emergency spinner hide after timeout');
            spinner.classList.add('hidden');
            spinner.style.display = 'none';
        }
    }, 10000);

    // Close modal when clicking outside
    const modal = document.getElementById('fraud-alert-modal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    }

    // Escape key to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('fraud-alert-modal');
            if (modal && !modal.classList.contains('hidden')) {
                modal.classList.add('hidden');
            }
        }
    });

    // Form input formatting
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        amountInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/[^\d.]/g, '');
            let parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            e.target.value = value;
        });
    }
});