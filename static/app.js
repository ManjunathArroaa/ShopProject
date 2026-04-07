// Configuration
const API_BASE = '';
let authToken = localStorage.getItem('authToken');
let currentCustomerId = null;
let currentFilter = 'all';
let currentMonthFilter = 'current';
let allPaymentsCache = [];

// Utility Functions
function showLoading() {
    document.getElementById('loadingOverlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
    
    // Load data when showing certain screens
    if (screenId === 'dashboardScreen') {
        loadDashboard();
    } else if (screenId === 'customersScreen') {
        loadCustomers();
    } else if (screenId === 'paymentsScreen') {
        loadPayments();
    } else if (screenId === 'collectionsScreen') {
        loadCollections();
    }
}

function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
    setTimeout(() => {
        errorEl.classList.add('hidden');
    }, 5000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0
    }).format(amount);
}

// Reminder Tracking Functions
function getTodayDateKey() {
    const today = new Date();
    return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
}

function wasReminderSentToday(customerId) {
    const todayKey = getTodayDateKey();
    const sentReminders = JSON.parse(localStorage.getItem('sentReminders') || '{}');
    return sentReminders[customerId] === todayKey;
}

function markReminderAsSent(customerId) {
    const todayKey = getTodayDateKey();
    const sentReminders = JSON.parse(localStorage.getItem('sentReminders') || '{}');
    sentReminders[customerId] = todayKey;
    localStorage.setItem('sentReminders', JSON.stringify(sentReminders));
}

// API Functions
async function apiCall(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    const fetchOptions = {
        method: options.method || 'GET',
        headers,
    };
    
    if (options.body) {
        fetchOptions.body = JSON.stringify(options.body);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, fetchOptions);
        
        // Handle 204 No Content response (like DELETE)
        if (response.status === 204) {
            return null;
        }
        
        const responseData = await response.json();
        
        if (!response.ok) {
            throw new Error(responseData.detail || 'An error occurred');
        }
        
        return responseData;
    } catch (error) {
        throw error;
    }
}

// Authentication Functions
function showLoginTab() {
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
    document.querySelectorAll('.tab-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', idx === 0);
    });
}

function showRegisterTab() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
    document.querySelectorAll('.tab-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', idx === 1);
    });
}

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }
        
        authToken = data.access_token;
        localStorage.setItem('authToken', authToken);
        
        showScreen('dashboardScreen');
        document.getElementById('loginForm').reset();
    } catch (error) {
        showError('loginError', error.message);
    } finally {
        hideLoading();
    }
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();
    
    const userData = {
        username: document.getElementById('registerUsername').value,
        email: document.getElementById('registerEmail').value,
        password: document.getElementById('registerPassword').value,
        shop_name: document.getElementById('registerShopName').value || null
    };
    
    try {
        await apiCall('/api/auth/register', { method: 'POST', body: userData });
        alert('Registration successful! Please login.');
        showLoginTab();
        document.getElementById('registerForm').reset();
    } catch (error) {
        showError('registerError', error.message);
    } finally {
        hideLoading();
    }
});

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        authToken = null;
        localStorage.removeItem('authToken');
        showScreen('loginScreen');
    }
}

// Dashboard Functions
async function loadDashboard() {
    showLoading();
    
    try {
        const stats = await apiCall('/api/dashboard/stats');
        const pending = await apiCall('/api/dashboard/pending-today');
        
        // Update stats
        document.getElementById('totalCustomers').textContent = stats.total_customers;
        document.getElementById('paidThisMonth').textContent = stats.paid_this_month;
        document.getElementById('pendingThisMonth').textContent = stats.pending_this_month;
        document.getElementById('totalCollection').textContent = formatCurrency(stats.total_collection_this_month);
        
        // Update pending list
        const pendingList = document.getElementById('pendingList');
        if (pending.length === 0) {
            pendingList.innerHTML = '<p class="text-center text-gray">No pending payments</p>';
        } else {
            pendingList.innerHTML = pending.map(p => {
                const alreadySent = wasReminderSentToday(p.customer_id);
                const buttonContent = alreadySent 
                    ? '✅ Sent Today' 
                    : '&#128276; Reminder';
                const buttonDisabled = alreadySent ? 'disabled' : '';
                
                return `
                    <div class="pending-item">
                        <div class="pending-info">
                            <h4>${p.customer_name}</h4>
                            <p>📞 ${p.phone}</p>
                            <p>Amount: ${formatCurrency(p.amount)} | Due: ${formatDate(p.due_date)}</p>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div class="pending-badge">${p.days_overdue}d</div>
                            <button class="btn-reminder" onclick="sendReminderFromDashboard(${p.customer_id}, '${p.customer_name}')" ${buttonDisabled}>
                                ${buttonContent}
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    } finally {
        hideLoading();
    }
}

// Customer Functions
async function loadCustomers() {
    showLoading();
    
    try {
        const customers = await apiCall('/api/customers');
        displayCustomers(customers);
    } catch (error) {
        console.error('Error loading customers:', error);
    } finally {
        hideLoading();
    }
}

async function checkPhoneExists() {
    const phoneInput = document.getElementById('customerPhone');
    const messageEl = document.getElementById('phoneCheckMessage');
    const phone = phoneInput.value.trim();
    
    if (!phone || phone.length < 10) {
        messageEl.style.display = 'none';
        phoneInput.style.borderColor = '';
        return;
    }
    
    try {
        const customers = await apiCall('/api/customers');
        const existing = customers.filter(c => c.phone === phone);
        
        if (existing.length > 0) {
            const names = existing.map(c => c.name).join(', ');
            messageEl.textContent = `ℹ️ ${existing.length} customer(s) with this number: ${names}`;
            messageEl.style.display = 'block';
            messageEl.style.color = '#2196F3';
            phoneInput.style.borderColor = '#2196F3';
        } else {
            messageEl.textContent = '✅ New phone number';
            messageEl.style.display = 'block';
            messageEl.style.color = '#4CAF50';
            phoneInput.style.borderColor = '#4CAF50';
        }
    } catch (error) {
        console.error('Error checking phone:', error);
    }
}

function displayCustomers(customers) {
    const customersList = document.getElementById('customersList');
    
    if (customers.length === 0) {
        customersList.innerHTML = '<p class="text-center text-gray">No customers found</p>';
        return;
    }
    
    customersList.innerHTML = customers.map(c => `
        <div class="customer-card" onclick="showCustomerDetails(${c.id})">
            <h4>${c.name}</h4>
            <p>📞 ${c.phone}</p>
            <p>💰 ${formatCurrency(c.monthly_amount)}/month | ${c.duration_months} months</p>
            <p>Start: ${formatDate(c.start_date)}</p>
            <span class="customer-status ${c.is_active ? 'active' : 'inactive'}">
                ${c.is_active ? 'Active' : 'Inactive'}
            </span>
        </div>
    `).join('');
}

async function searchCustomers() {
    const query = document.getElementById('customerSearch').value;
    
    if (query.length < 2) {
        loadCustomers();
        return;
    }
    
    showLoading();
    
    try {
        const customers = await apiCall(`/api/customers/search?q=${encodeURIComponent(query)}`);
        displayCustomers(customers);
    } catch (error) {
        console.error('Error searching customers:', error);
    } finally {
        hideLoading();
    }
}

document.getElementById('addCustomerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();
    
    const customerData = {
        name: document.getElementById('customerName').value,
        phone: document.getElementById('customerPhone').value,
        monthly_amount: parseFloat(document.getElementById('customerAmount').value),
        start_date: document.getElementById('customerStartDate').value,
        duration_months: parseInt(document.getElementById('customerDuration').value)
    };
    
    try {
        await apiCall('/api/customers', { method: 'POST', body: customerData });
        alert('✅ Customer added successfully!');
        document.getElementById('addCustomerForm').reset();
        document.getElementById('phoneCheckMessage').style.display = 'none';
        document.getElementById('customerPhone').style.borderColor = '';
        showScreen('customersScreen');
    } catch (error) {
        showError('addCustomerError', '❌ ' + error.message);
    } finally {
        hideLoading();
    }
});

async function showCustomerDetails(customerId) {
    currentCustomerId = customerId;
    showLoading();
    
    try {
        const customer = await apiCall(`/api/customers/${customerId}`);
        
        // Update customer details
        document.getElementById('detailCustomerName').textContent = customer.name;
        document.getElementById('detailCustomerPhone').textContent = customer.phone;
        document.getElementById('detailCustomerAmount').textContent = customer.monthly_amount;
        document.getElementById('detailCustomerStartDate').textContent = formatDate(customer.start_date);
        document.getElementById('detailCustomerDuration').textContent = customer.duration_months;
        document.getElementById('detailTotalPaid').textContent = customer.total_paid;
        document.getElementById('detailTotalPending').textContent = customer.total_pending;
        
        // Display payment history
        const paymentHistoryList = document.getElementById('paymentHistoryList');
        if (customer.payments.length === 0) {
            paymentHistoryList.innerHTML = '<p class="text-center text-gray">No payments found</p>';
        } else {
            paymentHistoryList.innerHTML = customer.payments.map(p => `
                <div class="payment-item">
                    <div class="payment-info">
                        <p><strong>Due:</strong> ${formatDate(p.due_date)}</p>
                        <p><strong>Amount:</strong> ${formatCurrency(p.amount)}</p>
                        ${p.paid_date ? `<p><strong>Paid on:</strong> ${formatDate(p.paid_date)}</p>` : ''}
                    </div>
                    <button class="payment-status ${p.is_paid ? 'paid' : 'pending'}" 
                            onclick="togglePayment(${p.id}, ${!p.is_paid})">
                        ${p.is_paid ? '↩ Revert to Unpaid' : '✓ Mark Paid'}
                    </button>
                </div>
            `).join('');
        }
        
        showScreen('customerDetailsScreen');
    } catch (error) {
        console.error('Error loading customer details:', error);
    } finally {
        hideLoading();
    }
}

async function deleteCustomer() {
    if (!currentCustomerId) {
        showMessage('errorMessage', 'No customer selected');
        return;
    }
    
    const customerName = document.getElementById('detailCustomerName').textContent;
    const confirmation = confirm(
        `Are you sure you want to delete customer "${customerName}"?\n\n` +
        `This will deactivate the customer and their payment records.\n\n` +
        `This action cannot be undone.`
    );
    
    if (!confirmation) {
        return;
    }
    
    showLoading();
    
    try {
        await apiCall(`/api/customers/${currentCustomerId}`, {
            method: 'DELETE'
        });
        
        // Success - go back to customers list and refresh
        showScreen('customersScreen');
        loadCustomers();
        alert(`✅ Customer "${customerName}" has been deleted successfully`);
        
        // Clear the current customer ID
        currentCustomerId = null;
    } catch (error) {
        console.error('Error deleting customer:', error);
        alert(`❌ Failed to delete customer: ${error.message || 'Unknown error'}`);
    } finally {
        hideLoading();
    }
}

// Payment Functions
async function loadPayments() {
    showLoading();
    
    try {
        let endpoint = '/api/payments';
        let payments = [];
        
        // Handle month filter
        if (currentMonthFilter === 'all') {
            // Get ALL payments - fetch from pending and current endpoints
            const pendingPayments = await apiCall('/api/payments/pending');
            const today = new Date();
            const currentMonthPayments = await apiCall(`/api/payments?month=${today.getMonth() + 1}&year=${today.getFullYear()}`);
            
            // Merge and deduplicate by payment ID
            const allPaymentsMap = new Map();
            [...pendingPayments, ...currentMonthPayments].forEach(p => {
                allPaymentsMap.set(p.id, p);
            });
            payments = Array.from(allPaymentsMap.values());
        } else if (currentMonthFilter === 'current') {
            const today = new Date();
            endpoint += `?month=${today.getMonth() + 1}&year=${today.getFullYear()}`;
            payments = await apiCall(endpoint);
        } else {
            payments = await apiCall(endpoint);
        }
        
        allPaymentsCache = payments; // Cache for client-side filtering
        displayPayments(payments, currentFilter);
        
        // Populate month dropdown if needed
        populateMonthDropdown();
    } catch (error) {
        console.error('Error loading payments:', error);
    } finally {
        hideLoading();
    }
}

function populateMonthDropdown() {
    const monthSelect = document.getElementById('monthSelect');
    if (!monthSelect || monthSelect.options.length > 2) return; // Already populated
    
    const today = new Date();
    const currentYear = today.getFullYear();
    const currentMonth = today.getMonth();
    
    // Add last 12 months
    for (let i = 0; i < 12; i++) {
        const date = new Date(currentYear, currentMonth - i, 1);
        const monthName = date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
        const value = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        
        const option = document.createElement('option');
        option.value = value;
        option.textContent = monthName;
        monthSelect.appendChild(option);
    }
}

function filterPaymentsByMonth() {
    const monthSelect = document.getElementById('monthSelect').value;
    currentMonthFilter = monthSelect;
    
    if (monthSelect === 'all') {
        loadPayments();
    } else if (monthSelect === 'current') {
        loadPayments();
    } else {
        // Specific month selected
        const [year, month] = monthSelect.split('-');
        showLoading();
        
        apiCall(`/api/payments?month=${month}&year=${year}`)
            .then(payments => {
                allPaymentsCache = payments;
                displayPayments(payments, currentFilter);
            })
            .catch(error => {
                console.error('Error loading payments:', error);
            })
            .finally(() => {
                hideLoading();
            });
    }
}

function displayPayments(payments, filter) {
    const paymentsList = document.getElementById('paymentsList');
    
    let filteredPayments = payments;
    if (filter === 'paid') {
        filteredPayments = payments.filter(p => p.is_paid);
    } else if (filter === 'pending') {
        filteredPayments = payments.filter(p => !p.is_paid);
    }
    
    if (filteredPayments.length === 0) {
        paymentsList.innerHTML = '<p class="text-center text-gray">No payments found</p>';
        return;
    }
    
    paymentsList.innerHTML = filteredPayments.map(p => `
        <div class="payment-item">
            <div class="payment-info">
                <h4>${p.customer?.name || 'Unknown'}</h4>
                <p>📞 ${p.customer?.phone || 'N/A'}</p>
                <p><strong>Due:</strong> ${formatDate(p.due_date)} | <strong>Amount:</strong> ${formatCurrency(p.amount)}</p>
                ${p.paid_date ? `<p><strong>Paid on:</strong> ${formatDate(p.paid_date)}</p>` : ''}
            </div>
            <button class="payment-status ${p.is_paid ? 'paid' : 'pending'}"
                    onclick="togglePayment(${p.id}, ${!p.is_paid})"
                    ${p.is_paid ? 'disabled' : ''}>
                ${p.is_paid ? '✓ Paid' : 'Mark Paid'}
            </button>
        </div>
    `).join('');
}

function filterPayments(filter) {
    currentFilter = filter;
    
    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Use cached payments if available
    if (allPaymentsCache.length > 0) {
        displayPayments(allPaymentsCache, filter);
    } else {
        loadPayments();
    }
}

async function togglePayment(paymentId, markAsPaid) {
    const confirmMsg = markAsPaid ? 
        'Mark this payment as paid?' : 
        'Revert this payment to unpaid? This will remove the paid date.';
    
    if (!confirm(confirmMsg)) return;
    
    showLoading();
    
    try {
        if (markAsPaid) {
            await apiCall(`/api/payments/${paymentId}/mark-paid`, { method: 'POST' });
        } else {
            // Revert to unpaid
            await apiCall(`/api/payments/${paymentId}`, { method: 'PUT', body: {
                is_paid: false,
                paid_date: null
            }});
        }
        
        // Reload current screen
        if (document.getElementById('customerDetailsScreen').classList.contains('active')) {
            showCustomerDetails(currentCustomerId);
        } else if (document.getElementById('paymentsScreen').classList.contains('active')) {
            loadPayments();
        } else if (document.getElementById('dashboardScreen').classList.contains('active')) {
            loadDashboard();
        }
    } catch (error) {
        alert('Error marking payment: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Reminder Functions
async function sendReminderFromDashboard(customerId, customerName) {
    if (!confirm(`Send payment reminder to ${customerName}?`)) return;
    
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = 'Sending...';
    
    try {
        const result = await apiCall(`/api/reminders/send/${customerId}`, { method: 'POST' });
        
        // Mark reminder as sent for today
        markReminderAsSent(customerId);
        
        // Show success message
        const successMsg = document.getElementById('reminderSuccess');
        successMsg.textContent = `✅ Reminder sent to ${customerName} successfully!`;
        successMsg.classList.remove('hidden');
        
        setTimeout(() => {
            successMsg.classList.add('hidden');
        }, 5000);
        
        // Keep button showing 'Sent Today' for entire day
        btn.innerHTML = '✅ Sent Today';
    } catch (error) {
        alert('Error sending reminder: ' + error.message);
        btn.innerHTML = '&#128276; Reminder';
        btn.disabled = false;
    }
}

async function sendCustomerReminder() {
    if (!currentCustomerId) return;
    
    const customerName = document.getElementById('detailCustomerName').textContent;
    if (!confirm(`Send payment reminder to ${customerName}?`)) return;
    
    const btn = document.getElementById('sendReminderBtn');
    const msgDiv = document.getElementById('reminderMessage');
    
    btn.disabled = true;
    btn.textContent = 'Sending Reminder...';
    
    try {
        const result = await apiCall(`/api/reminders/send/${currentCustomerId}`, { method: 'POST' });
        
        msgDiv.textContent = `✅ ${result.message || 'Reminder sent successfully!'}`;
        msgDiv.classList.remove('hidden');
        msgDiv.classList.add('success');
        
        btn.textContent = '✅ Reminder Sent';
        
        setTimeout(() => {
            msgDiv.classList.add('hidden');
            btn.textContent = '📧 Send Payment Reminder';
            btn.disabled = false;
        }, 5000);
    } catch (error) {
        msgDiv.textContent = `❌ Error: ${error.message}`;
        msgDiv.classList.remove('hidden', 'success');
        
        btn.textContent = '📧 Send Payment Reminder';
        btn.disabled = false;
    }
}

// Collections Functions
async function loadCollections() {
    showLoading();
    
    try {
        const data = await apiCall('/api/dashboard/monthly-collections');
        
        // Update grand total
        document.getElementById('collectionsTotal').textContent = `Total: ${formatCurrency(data.grand_total)}`;
        
        // Display collections list
        const collectionsList = document.getElementById('collectionsList');
        if (data.collections.length === 0) {
            collectionsList.innerHTML = '<p class="text-center text-gray">No collections found</p>';
        } else {
            collectionsList.innerHTML = data.collections.map(c => `
                <div class="collection-card">
                    <div class="collection-month">${c.month_year}</div>
                    <div class="collection-details">
                        <div class="collection-amount">${formatCurrency(c.total_amount)}</div>
                        <div class="collection-stats">
                            ${c.payment_count} payments • ${c.customer_count} customers
                        </div>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading collections:', error);
        document.getElementById('collectionsList').innerHTML = 
            '<p class="text-center" style="color: red;">Error loading collections</p>';
    } finally {
        hideLoading();
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set default start date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('customerStartDate').value = today;
    
    // Check if user is logged in
    if (authToken) {
        showScreen('dashboardScreen');
    } else {
        showScreen('loginScreen');
    }
});
