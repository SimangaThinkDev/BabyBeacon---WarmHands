// Show different pages
function showLoginPage() {
    document.getElementById('login-page').style.display = 'flex';
    document.getElementById('user-page').style.display = 'none';
    document.getElementById('admin-page').style.display = 'none';
    document.getElementById('payment-page').style.display = 'none';
    document.getElementById('profile-page').style.display = 'none';
}

function showUserPage() {
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('user-page').style.display = 'flex';
    document.getElementById('admin-page').style.display = 'none';
    document.getElementById('payment-page').style.display = 'none';
    document.getElementById('profile-page').style.display = 'none';
}

function showAdminPage() {
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('user-page').style.display = 'none';
    document.getElementById('admin-page').style.display = 'flex';
    document.getElementById('payment-page').style.display = 'none';
    document.getElementById('profile-page').style.display = 'none';
}

function showPaymentPage() {
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('user-page').style.display = 'none';
    document.getElementById('admin-page').style.display = 'none';
    document.getElementById('payment-page').style.display = 'flex';
    document.getElementById('profile-page').style.display = 'none';
}

function showProfilePage() {
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('user-page').style.display = 'none';
    document.getElementById('admin-page').style.display = 'none';
    document.getElementById('payment-page').style.display = 'none';
    document.getElementById('profile-page').style.display = 'flex';
}

function showUsersPage() {
    // In a real app, this would navigate to a users management page
    alert('Users page would be displayed here');
}

function showReportsPage() {
    // In a real app, this would navigate to reports page
    alert('Reports page would be displayed here');
}

function backToDashboard() {
    showUserPage();
}

// Login functionality
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Simple validation
    if (username && password) {
        // Simulate login success
        if (username === 'admin' && password === 'admin123') {
            showAdminPage();
            document.getElementById('admin-name').textContent = username;
        } else {
            showUserPage();
            document.getElementById('user-name').textContent = username;
            document.getElementById('welcome-message').textContent = `Hello, ${username}`;
            document.getElementById('payment-user-name').textContent = username;
            document.getElementById('profile-user-name').textContent = username;
            document.getElementById('profile-full-name').textContent = `${username} User`;
            document.getElementById('profile-email').textContent = `${username.toLowerCase()}@moremove.com`;
            document.getElementById('profile-role').textContent = 'Regular User';
        }
    } else {
        alert('Please enter both username and password');
    }
});

// Forgot password button
document.querySelector('.fgt').addEventListener('click', function() {
    alert('Password reset instructions have been sent to your email.');
});

// Social login functions
function googleLogin() {
    alert('Redirecting to Google login...');
}

function facebookLogin() {
    alert('Redirecting to MoMo login...');
}

// Logout function
function logout() {
    showLoginPage();
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
}

// Payment processing
function processPayment() {
    const amount = parseFloat(document.getElementById('amount').value);
    const cardNumber = document.getElementById('card-number').value;
    
    // Validate inputs
    if (!cardNumber || !amount || amount <= 0) {
        showResponse('Please fill in all fields correctly.', 'error');
        return;
    }
    
    // Simulate payment processing
    showResponse('Processing payment...', 'info');
    
    setTimeout(() => {
        if (Math.random() > 0.2) { // 80% success rate
            showResponse(`Payment of $${amount.toFixed(2)} processed successfully!`, 'success');
        } else {
            showResponse('Payment failed. Please try again.', 'error');
        }
    }, 2000);
}

function showResponse(message, type) {
    const responseDiv = document.getElementById('payment-response');
    responseDiv.textContent = message;
    responseDiv.className = 'payment-response';
    responseDiv.classList.add(type);
    responseDiv.style.display = 'block';
    
    // Hide after 5 seconds for success/error messages
    if (type !== 'info') {
        setTimeout(() => {
            responseDiv.style.display = 'none';
        }, 5000);
    }
}

// Admin functions
function addUser() {
    document.getElementById('add-user-modal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

document.getElementById('add-user-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('new-username').value;
    const email = document.getElementById('new-email').value;
    const role = document.getElementById('new-role').value;
    
    alert(`User ${username} created successfully with role: ${role}`);
    closeModal('add-user-modal');
    this.reset();
});

// Payment method selection
document.querySelectorAll('.payment-option').forEach(option => {
    option.addEventListener('click', function() {
        document.querySelectorAll('.payment-option').forEach(opt => {
            opt.classList.remove('active');
        });
        this.classList.add('active');
    });
});

// Edit profile function
function editProfile() {
    alert('Edit profile functionality would go here.');
}

// Generate report function
function generateReport() {
    alert('Generating report...');
}

// Initialize page
window.onload = function() {
    showLoginPage();
};