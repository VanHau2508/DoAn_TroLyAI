// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000',
    ENDPOINTS: {
        LOGIN: '/api/students/login',
        STUDENTS: '/api/students',
        SUBJECTS: '/api/subjects',
        SCHEDULES: '/api/schedules',
        EXAMS: '/api/exams',
        DEADLINES: '/api/deadlines'
    }
};

// Local Storage Keys
const STORAGE_KEYS = {
    USER: 'student_user',
    TOKEN: 'student_token'
};

// Helper Functions
function showAlert(message, type = 'error') {
    const alertDiv = document.getElementById('alert');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.classList.remove('hidden');
    
    setTimeout(() => {
        alertDiv.classList.add('hidden');
    }, 5000);
}

function setLoading(button, loading) {
    if (loading) {
        button.disabled = true;
        button.innerHTML = '<span class="loading"></span> Đang xử lý...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || 'Đăng nhập';
    }
}

// Check if user is logged in
function isLoggedIn() {
    return localStorage.getItem(STORAGE_KEYS.USER) !== null;
}

// Get current user
function getCurrentUser() {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER);
    return userStr ? JSON.parse(userStr) : null;
}

// Save user to localStorage
function saveUser(user) {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
}

// Logout
function logout() {
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    window.location.href = 'index.html';
}