// Check if already logged in
if (isLoggedIn() && window.location.pathname.includes('index.html')) {
    window.location.href = 'dashboard.html';
}

// Login Form Handler
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const loginBtn = document.getElementById('loginBtn');
            
            // Store original button text
            loginBtn.dataset.originalText = loginBtn.innerHTML;
            
            // Set loading state
            setLoading(loginBtn, true);
            
            try {
                const response = await fetch(API_CONFIG.BASE_URL + API_CONFIG.ENDPOINTS.LOGIN, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email,
                        mat_khau: password
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Save user data
                    saveUser(data.data);
                    
                    // Show success message
                    showAlert('Đăng nhập thành công! Đang chuyển hướng...', 'success');
                    
                    // Redirect to dashboard
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 1000);
                } else {
                    showAlert(data.message || 'Email hoặc mật khẩu không đúng!');
                    setLoading(loginBtn, false);
                }
            } catch (error) {
                console.error('Login error:', error);
                showAlert('Lỗi kết nối đến server! Vui lòng kiểm tra server đang chạy.');
                setLoading(loginBtn, false);
            }
        });
    }
});