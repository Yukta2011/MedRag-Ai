const API_BASE_URL = 'http://localhost:8000/api';
const TOKEN_KEY = 'medrag_token';
const USER_KEY = 'medrag_user';

async function handleLogin(e) {
    e.preventDefault();
    clearErrors();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const submitBtn = document.getElementById('submitBtn');
    
    if (!username) return showFieldError('username', 'Required');
    if (!password) return showFieldError('password', 'Required');
    
    setLoading(submitBtn, true);
    
    try {
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Login failed');
        
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem(TOKEN_KEY + '_expires', Date.now() + data.expires_in * 1000);
        await fetchUserInfo();
        window.location.href = 'index.html'; // or your main app page
        
    } catch (err) {
        showAlert(err.message);
    } finally {
        setLoading(submitBtn, false);
    }
}

async function handleSignup(e) {
    e.preventDefault();
    clearErrors();
    
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirm = document.getElementById('confirmPassword').value;
    const submitBtn = document.getElementById('submitBtn');
    
    if (!username || username.length < 3) return showFieldError('username', 'Min 3 chars');
    if (!email || !email.includes('@')) return showFieldError('email', 'Invalid email');
    if (!password || password.length < 8) return showFieldError('password', 'Min 8 chars');
    if (password !== confirm) return showFieldError('confirmPassword', 'Mismatch');
    
    setLoading(submitBtn, true);
    
    try {
        const res = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Signup failed');
        
        showAlert('Account created! Redirecting...', 'success');
        setTimeout(() => window.location.href = 'login.html', 1500);
        
    } catch (err) {
        showAlert(err.message);
    } finally {
        setLoading(submitBtn, false);
    }
}

async function fetchUserInfo() {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) return null;
    const res = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) { logout(); return null; }
    const user = await res.json();
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    return user;
}

async function checkAuth() {
    const token = localStorage.getItem(TOKEN_KEY);
    const expires = localStorage.getItem(TOKEN_KEY + '_expires');
    if (!token || (expires && Date.now() > parseInt(expires))) {
        logout(); throw new Error('Not authenticated');
    }
    const cached = localStorage.getItem(USER_KEY);
    if (cached) return JSON.parse(cached);
    return await fetchUserInfo();
}

function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(TOKEN_KEY + '_expires');
    localStorage.removeItem(USER_KEY);
    window.location.href = 'login.html';
}

async function apiRequest(endpoint, opts = {}) {
    const token = localStorage.getItem(TOKEN_KEY);
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...opts.headers
        },
        ...opts
    });
    if (res.status === 401) { logout(); throw new Error('Session expired'); }
    return res;
}

// UI helpers
function showFieldError(id, msg) {
    const el = document.getElementById(id + 'Error');
    if (el) { el.textContent = msg; el.style.display = 'block'; }
    const input = document.getElementById(id);
    if (input) input.style.borderColor = '#e74c3c';
}

function clearErrors() {
    document.querySelectorAll('[id$="Error"]').forEach(e => { e.textContent = ''; e.style.display = 'none'; });
    document.querySelectorAll('input').forEach(i => i.style.borderColor = '');
    const alert = document.getElementById('alert');
    if (alert) alert.style.display = 'none';
}

function showAlert(msg, type = 'error') {
    const alert = document.getElementById('alert');
    if (!alert) return;
    alert.textContent = msg;
    alert.style.display = 'block';
    alert.style.background = type === 'success' ? '#def7ec' : '#fde8e8';
    alert.style.color = type === 'success' ? '#046c4e' : '#c81e1e';
}

function setLoading(btn, loading) {
    btn.disabled = loading;
    btn.dataset.original = btn.dataset.original || btn.textContent;
    btn.textContent = loading ? 'Please wait...' : btn.dataset.original;
}

// Auto-redirect if logged in on login/signup pages
if (document.body.classList.contains('auth-page')) {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) checkAuth().then(() => window.location.href = 'index.html').catch(() => {});
}