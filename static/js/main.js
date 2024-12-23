// Toast notification function
window.showToast = function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
            ${message}
        </div>
    `;
    document.getElementById('toast-container').appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Logout confirmation
function confirmLogout(event) {
    event.preventDefault();
    if (confirm('Are you sure you want to logout?')) {
        window.showToast('Logging out...', 'info');
        setTimeout(() => {
            window.location.href = event.target.href;
        }, 1000);
    }
}

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    // Show login success message if URL has success parameter
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('login') === 'success') {
        window.showToast('Successfully logged in!', 'success');
    }

    // Add logout confirmation to logout links
    const logoutLinks = document.querySelectorAll('a[href*="logout"]');
    logoutLinks.forEach(link => {
        link.addEventListener('click', confirmLogout);
    });
});

