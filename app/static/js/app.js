const API_BASE = '/api';
let currentUser = null;
let currentPage = 'login';

const app = {
    init() {
        this.checkAuth();
        this.render();
    },

    async checkAuth() {
        try {
            const response = await fetch(`${API_BASE}/auth/me`);
            if (response.ok) {
                currentUser = await response.json();
                currentPage = 'dashboard';
            }
        } catch (e) {
            currentUser = null;
            currentPage = 'login';
        }
    },

    render() {
        const appDiv = document.getElementById('app');

        if (!currentUser) {
            appDiv.innerHTML = this.renderAuth();
            this.setupAuthHandlers();
        } else {
            appDiv.innerHTML = this.renderApp();
            this.setupAppHandlers();
        }
    },

    renderAuth() {
        return `
            <div class="container">
                <div class="card" style="max-width: 400px; margin: 0 auto;">
                    <h1>Login</h1>

                    <div id="auth-tabs" class="tabs">
                        <button class="tab-button active" onclick="app.switchTab('login')">Login</button>
                        <button class="tab-button" onclick="app.switchTab('register')">Register</button>
                        <button class="tab-button" onclick="app.switchTab('guest')">Guest</button>
                    </div>

                    <div id="login-tab" class="tab-content active">
                        <form id="login-form" onsubmit="app.handleLogin(event)">
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" name="email" required>
                            </div>
                            <div class="form-group">
                                <label>Password</label>
                                <input type="password" name="password" required>
                            </div>
                            <button type="submit" style="width: 100%;">Login</button>
                        </form>
                    </div>

                    <div id="register-tab" class="tab-content">
                        <form id="register-form" onsubmit="app.handleRegister(event)">
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" name="email" required>
                            </div>
                            <div class="form-group">
                                <label>Password</label>
                                <input type="password" name="password" required>
                            </div>
                            <div class="form-group">
                                <label>Confirm Password</label>
                                <input type="password" name="confirm" required>
                            </div>
                            <button type="submit" style="width: 100%;">Register</button>
                        </form>
                    </div>

                    <div id="guest-tab" class="tab-content">
                        <p>Try the app without creating an account.</p>
                        <button onclick="app.handleGuest()" style="width: 100%; margin-top: 20px;">Continue as Guest</button>
                    </div>

                    <div id="auth-message" style="margin-top: 20px;"></div>
                </div>
            </div>
        `;
    },

    renderApp() {
        return `
            <div class="container">
                <nav class="nav">
                    <div class="logo">📊 CRUD App</div>
                    <div>
                        <div class="nav-links">
                            <button class="tab-button" onclick="app.switchPage('dashboard')">Dashboard</button>
                            <button class="tab-button" onclick="app.switchPage('records')">Records</button>
                            <button class="tab-button" onclick="app.switchPage('reports')">Reports</button>
                            <button class="tab-button" onclick="app.switchPage('jobs')">Jobs</button>
                        </div>
                        <div class="user-info">
                            <div class="user-email">${currentUser.email}</div>
                            <button class="secondary" onclick="app.handleLogout()" style="padding: 6px 12px; font-size: 12px;">Logout</button>
                        </div>
                    </div>
                </nav>

                <div id="page-content">
                </div>
            </div>
        `;
    },

    switchTab(tab) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));

        document.getElementById(`${tab}-tab`).classList.add('active');
        event.target.classList.add('active');
    },

    switchPage(page) {
        currentPage = page;
        this.render();
        this.setupAppHandlers();
    },

    async handleLogin(e) {
        e.preventDefault();
        const form = e.target;
        const email = form.email.value;
        const password = form.password.value;

        try {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                currentUser = data.user;
                currentPage = 'dashboard';
                this.render();
                this.setupAppHandlers();
            } else {
                this.showMessage(data.error, 'error', 'auth-message');
            }
        } catch (error) {
            this.showMessage('Login failed', 'error', 'auth-message');
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const form = e.target;
        const email = form.email.value;
        const password = form.password.value;
        const confirm = form.confirm.value;

        if (password !== confirm) {
            this.showMessage('Passwords do not match', 'error', 'auth-message');
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.showMessage('Registration successful! Please login.', 'success', 'auth-message');
                this.switchTab('login');
            } else {
                this.showMessage(data.error, 'error', 'auth-message');
            }
        } catch (error) {
            this.showMessage('Registration failed', 'error', 'auth-message');
        }
    },

    async handleGuest() {
        try {
            const response = await fetch(`${API_BASE}/auth/guest`, {
                method: 'POST'
            });

            const data = await response.json();

            if (response.ok) {
                currentUser = data.user;
                currentPage = 'dashboard';
                this.render();
                this.setupAppHandlers();
            } else {
                this.showMessage(data.error, 'error', 'guest-message');
            }
        } catch (error) {
            this.showMessage('Failed to create guest account', 'error', 'guest-message');
        }
    },

    async handleLogout() {
        try {
            await fetch(`${API_BASE}/auth/logout`, { method: 'POST' });
            currentUser = null;
            currentPage = 'login';
            this.render();
        } catch (error) {
            console.error('Logout failed', error);
        }
    },

    setupAuthHandlers() {
        // Already handled by onsubmit
    },

    setupAppHandlers() {
        const pageContent = document.getElementById('page-content');

        if (currentPage === 'dashboard') {
            pageContent.innerHTML = this.renderDashboard();
            this.loadDashboard();
        } else if (currentPage === 'records') {
            pageContent.innerHTML = this.renderRecords();
            this.loadRecords();
        } else if (currentPage === 'reports') {
            pageContent.innerHTML = this.renderReports();
        } else if (currentPage === 'jobs') {
            pageContent.innerHTML = this.renderJobs();
            this.loadJobs();
        }
    },

    renderDashboard() {
        return `
            <div class="card">
                <h1>📊 Dashboard</h1>
                <div id="kpi-container" class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-label">Total Records</div>
                        <div class="kpi-value" id="kpi-count">0</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">Total Value</div>
                        <div class="kpi-value" id="kpi-sum">$0.00</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">Average Value</div>
                        <div class="kpi-value" id="kpi-avg">$0.00</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">Min - Max</div>
                        <div class="kpi-value" id="kpi-range">-</div>
                    </div>
                </div>

                <div class="sidebar">
                    <h3>Filters</h3>
                    <div class="filter-group">
                        <label>Category</label>
                        <select id="filter-category" onchange="app.loadDashboard()">
                            <option value="">All Categories</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Start Date</label>
                        <input type="date" id="filter-start" onchange="app.loadDashboard()">
                    </div>
                    <div class="filter-group">
                        <label>End Date</label>
                        <input type="date" id="filter-end" onchange="app.loadDashboard()">
                    </div>
                </div>

                <div id="dashboard-content"></div>
            </div>
        `;
    },

    async loadDashboard() {
        const category = document.getElementById('filter-category')?.value || '';
        const startDate = document.getElementById('filter-start')?.value || '';
        const endDate = document.getElementById('filter-end')?.value || '';

        try {
            const params = new URLSearchParams();
            if (category) params.append('category', category);
            if (startDate) params.append('start_date', startDate);
            if (endDate) params.append('end_date', endDate);

            const response = await fetch(`${API_BASE}/records/list?${params}`);
            const data = await response.json();

            if (response.ok) {
                const records = data.records;
                this.updateCategories(records);

                const response2 = await fetch(`${API_BASE}/records/statistics?${params}`);
                const stats = await response2.json();

                document.getElementById('kpi-count').textContent = stats.count;
                document.getElementById('kpi-sum').textContent = '$' + stats.sum.toFixed(2);
                document.getElementById('kpi-avg').textContent = '$' + stats.average.toFixed(2);
                document.getElementById('kpi-range').textContent = `$${stats.min.toFixed(2)} - $${stats.max.toFixed(2)}`;

                const content = document.getElementById('dashboard-content');
                if (records.length > 0) {
                    content.innerHTML = `
                        <h2>Recent Records</h2>
                        <div class="table-responsive">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Category</th>
                                        <th>Value</th>
                                        <th>Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${records.slice(0, 10).map(r => `
                                        <tr>
                                            <td>${r.title}</td>
                                            <td>${r.category}</td>
                                            <td>$${r.value.toFixed(2)}</td>
                                            <td>${new Date(r.timestamp).toLocaleDateString()}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    `;
                } else {
                    content.innerHTML = '<div class="alert info">No records found</div>';
                }
            }
        } catch (error) {
            console.error('Error loading dashboard', error);
        }
    },

    updateCategories(records) {
        const categories = [...new Set(records.map(r => r.category))];
        const select = document.getElementById('filter-category');
        const current = select?.value || '';

        if (select && categories.length > 0) {
            const options = ['<option value="">All Categories</option>'];
            categories.forEach(cat => {
                options.push(`<option value="${cat}" ${cat === current ? 'selected' : ''}>${cat}</option>`);
            });
            select.innerHTML = options.join('');
        }
    },

    renderRecords() {
        return `
            <div class="card">
                <h1>📝 Records</h1>

                <div class="tabs">
                    <button class="tab-button active" onclick="app.switchRecordsTab('list')">View Records</button>
                    <button class="tab-button" onclick="app.switchRecordsTab('create')">Add New Record</button>
                </div>

                <div id="records-list-tab" class="tab-content active">
                    <h2>Your Records</h2>
                    <div id="records-table"></div>
                </div>

                <div id="records-create-tab" class="tab-content">
                    <h2>Create New Record</h2>
                    <form id="create-record-form" onsubmit="app.handleCreateRecord(event)">
                        <div class="form-group">
                            <label>Title</label>
                            <input type="text" name="title" required>
                        </div>
                        <div class="form-group">
                            <label>Category</label>
                            <input type="text" name="category" required>
                        </div>
                        <div class="form-group">
                            <label>Value</label>
                            <input type="number" name="value" step="0.01" required>
                        </div>
                        <div class="form-group">
                            <label>Date</label>
                            <input type="date" name="date" required>
                        </div>
                        <button type="submit">Create Record</button>
                    </form>
                    <div id="create-message"></div>
                </div>
            </div>
        `;
    },

    switchRecordsTab(tab) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));

        if (tab === 'list') {
            document.getElementById('records-list-tab').classList.add('active');
            event.target.classList.add('active');
            this.loadRecords();
        } else {
            document.getElementById('records-create-tab').classList.add('active');
            event.target.classList.add('active');
        }
    },

    async loadRecords() {
        try {
            const response = await fetch(`${API_BASE}/records/list`);
            const data = await response.json();

            if (response.ok) {
                const records = data.records;
                const table = document.getElementById('records-table');

                if (records.length > 0) {
                    table.innerHTML = `
                        <div class="table-responsive">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Category</th>
                                        <th>Value</th>
                                        <th>Date</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${records.map(r => `
                                        <tr>
                                            <td>${r.title}</td>
                                            <td>${r.category}</td>
                                            <td>$${r.value.toFixed(2)}</td>
                                            <td>${new Date(r.timestamp).toLocaleDateString()}</td>
                                            <td>
                                                <button onclick="app.deleteRecord('${r.id}')" class="danger" style="padding: 6px 12px; font-size: 12px;">Delete</button>
                                            </td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    `;
                } else {
                    table.innerHTML = '<div class="alert info">No records found</div>';
                }
            }
        } catch (error) {
            console.error('Error loading records', error);
        }
    },

    async handleCreateRecord(e) {
        e.preventDefault();
        const form = e.target;
        const title = form.title.value;
        const category = form.category.value;
        const value = parseFloat(form.value.value);
        const date = form.date.value;

        try {
            const response = await fetch(`${API_BASE}/records/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title,
                    category,
                    value,
                    timestamp: new Date(date).toISOString()
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.showMessage('Record created successfully!', 'success', 'create-message');
                form.reset();
                setTimeout(() => this.switchRecordsTab('list'), 1000);
            } else {
                this.showMessage(data.error, 'error', 'create-message');
            }
        } catch (error) {
            this.showMessage('Failed to create record', 'error', 'create-message');
        }
    },

    async deleteRecord(recordId) {
        if (!confirm('Are you sure?')) return;

        try {
            const response = await fetch(`${API_BASE}/records/${recordId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.loadRecords();
            }
        } catch (error) {
            console.error('Error deleting record', error);
        }
    },

    renderReports() {
        return `
            <div class="card">
                <h1>📊 Reports</h1>

                <h2>Export Options</h2>
                <div class="grid-2">
                    <div>
                        <h3>CSV Export</h3>
                        <button onclick="app.downloadReport('csv')">Download CSV</button>
                    </div>
                    <div>
                        <h3>Excel Export</h3>
                        <button onclick="app.downloadReport('excel')">Download Excel</button>
                    </div>
                    <div>
                        <h3>PDF Export</h3>
                        <button onclick="app.downloadReport('pdf')">Download PDF</button>
                    </div>
                    <div>
                        <h3>Summary</h3>
                        <button onclick="app.loadReportSummary()">View Summary</button>
                    </div>
                </div>

                <div id="report-summary" style="margin-top: 30px;"></div>
            </div>
        `;
    },

    async downloadReport(format) {
        try {
            window.location.href = `${API_BASE}/reports/${format}`;
        } catch (error) {
            console.error('Error downloading report', error);
        }
    },

    async loadReportSummary() {
        try {
            const response = await fetch(`${API_BASE}/reports/summary`);
            const data = await response.json();

            if (response.ok) {
                const stats = data.statistics;
                const summary = document.getElementById('report-summary');
                summary.innerHTML = `
                    <div class="kpi-grid">
                        <div class="kpi-card">
                            <div class="kpi-label">Total Records</div>
                            <div class="kpi-value">${stats.count}</div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-label">Total Value</div>
                            <div class="kpi-value">$${stats.sum.toFixed(2)}</div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-label">Average Value</div>
                            <div class="kpi-value">$${stats.average.toFixed(2)}</div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-label">Value Range</div>
                            <div class="kpi-value">$${stats.min.toFixed(2)} - $${stats.max.toFixed(2)}</div>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading report summary', error);
        }
    },

    renderJobs() {
        return `
            <div class="card">
                <h1>🔄 Background Jobs</h1>

                <div class="sidebar">
                    <h3>Job Configuration</h3>
                    <div id="job-config"></div>
                </div>

                <h2>Job Control</h2>
                <button onclick="app.runJob()" type="button">Run Job Now</button>

                <h2>Last Run</h2>
                <div id="last-run"></div>

                <h2>Job History</h2>
                <div id="job-history"></div>
            </div>
        `;
    },

    async loadJobs() {
        try {
            const configResponse = await fetch(`${API_BASE}/jobs/config`);
            const config = await configResponse.json();

            if (configResponse.ok) {
                document.getElementById('job-config').innerHTML = `
                    <p><strong>API URL:</strong> ${config.external_api_url}</p>
                    <p><strong>Interval:</strong> ${config.job_interval_min} minutes</p>
                `;
            }

            const historyResponse = await fetch(`${API_BASE}/jobs/history`);
            const historyData = await historyResponse.json();

            if (historyResponse.ok) {
                const jobs = historyData.history;
                const history = document.getElementById('job-history');

                if (jobs.length > 0) {
                    history.innerHTML = `
                        <div class="table-responsive">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Date</th>
                                        <th>Status</th>
                                        <th>Message</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${jobs.slice(0, 10).map(j => `
                                        <tr>
                                            <td>${new Date(j.fetched_at).toLocaleString()}</td>
                                            <td>${j.status}</td>
                                            <td>${j.error_message || '-'}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    `;
                } else {
                    history.innerHTML = '<div class="alert info">No job history</div>';
                }
            }
        } catch (error) {
            console.error('Error loading jobs', error);
        }
    },

    async runJob() {
        try {
            const response = await fetch(`${API_BASE}/jobs/run`, { method: 'POST' });
            const data = await response.json();

            if (response.ok) {
                this.showMessage('Job executed successfully!', 'success', 'last-run');
                setTimeout(() => this.loadJobs(), 1000);
            } else {
                this.showMessage(data.message, 'error', 'last-run');
            }
        } catch (error) {
            this.showMessage('Failed to run job', 'error', 'last-run');
        }
    },

    showMessage(message, type, elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `<div class="alert ${type}">${message}</div>`;
        }
    }
};

document.addEventListener('DOMContentLoaded', () => app.init());
