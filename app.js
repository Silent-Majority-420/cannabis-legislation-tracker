// Cannabis Legislation Tracker - Frontend Application

let allBills = [];
let filteredBills = [];

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    loadBillsData();
    setupEventListeners();
});

// Load bills data from JSON file
async function loadBillsData() {
    try {
        const response = await fetch('bills.json');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        allBills = data.bills || [];
        filteredBills = [...allBills];
        
        updateLastUpdated(data.last_updated);
        updateStats();
        renderBills();
        
    } catch (error) {
        console.error('Error loading bills data:', error);
        showError('Failed to load legislation data. Please try again later.');
    }
}

// Setup event listeners for filters and search
function setupEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const sortOrder = document.getElementById('sortOrder');
    
    searchInput.addEventListener('input', applyFilters);
    statusFilter.addEventListener('change', applyFilters);
    sortOrder.addEventListener('change', applyFilters);
}

// Apply filters and sorting
function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    const sortOrder = document.getElementById('sortOrder').value;
    
    // Filter bills
    filteredBills = allBills.filter(bill => {
        const matchesSearch = 
            bill.title.toLowerCase().includes(searchTerm) ||
            bill.description.toLowerCase().includes(searchTerm) ||
            bill.bill_number.toLowerCase().includes(searchTerm);
        
        const matchesStatus = 
            statusFilter === 'all' || 
            bill.status.toLowerCase().includes(statusFilter);
        
        return matchesSearch && matchesStatus;
    });
    
    // Sort bills
    switch (sortOrder) {
        case 'recent':
            filteredBills.sort((a, b) => 
                new Date(b.last_action_date) - new Date(a.last_action_date)
            );
            break;
        case 'oldest':
            filteredBills.sort((a, b) => 
                new Date(a.last_action_date) - new Date(b.last_action_date)
            );
            break;
        case 'alphabetical':
            filteredBills.sort((a, b) => 
                a.bill_number.localeCompare(b.bill_number)
            );
            break;
    }
    
    renderBills();
}

// Update statistics
function updateStats() {
    const totalBills = allBills.length;
    const activeBills = allBills.filter(bill => 
        !bill.status.toLowerCase().includes('enacted') && 
        !bill.status.toLowerCase().includes('vetoed') &&
        !bill.status.toLowerCase().includes('failed')
    ).length;
    const analyzedBills = allBills.filter(bill => bill.analysis_url).length;
    
    document.getElementById('totalBills').textContent = totalBills;
    document.getElementById('activeBills').textContent = activeBills;
    document.getElementById('analyzedBills').textContent = analyzedBills;
}

// Update last updated timestamp
function updateLastUpdated(timestamp) {
    const date = new Date(timestamp);
    const formatted = date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    document.getElementById('lastUpdated').textContent = formatted;
}

// Render bills to the DOM
function renderBills() {
    const container = document.getElementById('billsContainer');
    
    if (filteredBills.length === 0) {
        container.innerHTML = `
            <div class="no-results">
                <p>No bills found matching your criteria.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = filteredBills.map(bill => createBillCard(bill)).join('');
}

// Create HTML for a single bill card
function createBillCard(bill) {
    const statusClass = getStatusClass(bill.status);
    const sponsors = bill.sponsors.slice(0, 3); // Show first 3 sponsors
    const hasMoreSponsors = bill.sponsors.length > 3;
    
    const lastActionDate = new Date(bill.last_action_date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    return `
        <div class="bill-card">
            <div class="bill-header">
                <div class="bill-title">
                    <div class="bill-number">${bill.bill_number}</div>
                    <h4>${bill.title}</h4>
                </div>
                <div class="bill-status ${statusClass}">
                    ${bill.status}
                </div>
            </div>
            
            <div class="bill-description">
                ${bill.description}
            </div>
            
            <div class="bill-meta">
                <div class="bill-meta-item">
                    <strong>Last Action:</strong> ${lastActionDate}
                </div>
            </div>
            
            ${sponsors.length > 0 ? `
                <div class="bill-sponsors">
                    <strong>Sponsors:</strong>
                    <div class="sponsor-list">
                        ${sponsors.map(sponsor => `
                            <span class="sponsor-tag">
                                ${sponsor.name} (${sponsor.party})
                            </span>
                        `).join('')}
                        ${hasMoreSponsors ? `
                            <span class="sponsor-tag">
                                +${bill.sponsors.length - 3} more
                            </span>
                        ` : ''}
                    </div>
                </div>
            ` : ''}
            
            <div class="bill-actions">
                <a href="${bill.url}" target="_blank" class="btn btn-secondary">
                    View on LegiScan
                </a>
                ${bill.analysis_url ? `
                    <a href="${bill.analysis_url}" target="_blank" class="btn btn-analysis">
                        Read CBDT Analysis
                    </a>
                ` : `
                    <span class="btn btn-disabled" title="Analysis coming soon">
                        Analysis Pending
                    </span>
                `}
            </div>
        </div>
    `;
}

// Get CSS class for bill status
function getStatusClass(status) {
    const statusLower = status.toLowerCase();
    
    if (statusLower.includes('introduced')) return 'status-introduced';
    if (statusLower.includes('committee')) return 'status-committee';
    if (statusLower.includes('passed')) return 'status-passed';
    if (statusLower.includes('enacted')) return 'status-enacted';
    
    return 'status-introduced'; // default
}

// Show error message
function showError(message) {
    const container = document.getElementById('billsContainer');
    container.innerHTML = `
        <div class="no-results">
            <p style="color: var(--accent-color);">${message}</p>
        </div>
    `;
}
