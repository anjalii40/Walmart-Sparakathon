let loggedIn = false;

function login() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            loggedIn = true;
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('dashboard-section').style.display = 'block';
            fetchProducts();
        } else {
            alert('Invalid credentials');
        }
    })
    .catch(() => alert('Login failed.'));
}

function logout() {
    fetch('/logout', { method: 'POST' })
        .then(() => {
            loggedIn = false;
            document.getElementById('dashboard-section').style.display = 'none';
            document.getElementById('login-section').style.display = 'block';
        });
}

function fetchProducts() {
    fetch('/api/products')
        .then(res => {
            if (res.status === 401) {
                logout();
                return { products: [] };
            }
            return res.json();
        })
        .then(data => updateTable(data.products))
        .catch(() => alert('Failed to fetch products'));
}

function updateTable(products) {
    const tbody = document.getElementById('products-table').querySelector('tbody');
    tbody.innerHTML = '';
    (products || []).forEach(prod => {
        let statusClass = '';
        if (prod.status === 'expired') statusClass = 'status-expired';
        else if (prod.status === 'near') statusClass = 'status-near';
        else statusClass = 'status-safe';
        tbody.innerHTML += `<tr class="${statusClass}">
            <td>${prod.name}</td>
            <td>${prod.expiry}</td>
            <td>${prod.status ? prod.status.charAt(0).toUpperCase() + prod.status.slice(1) : ''}</td>
            <td><button onclick="markChecked('${prod.id}')">Mark Checked</button></td>
        </tr>`;
    });
}

function markChecked(id) {
    fetch(`/api/products/${id}/check`, { method: 'POST' })
        .then(() => fetchProducts());
}

function rescanProducts() {
    fetch('/api/scan', { method: 'POST' })
        .then(() => fetchProducts());
}

function sendNotifications() {
    fetch('/api/alerts', { method: 'POST' })
        .then(() => alert('Notifications sent!'));
}
