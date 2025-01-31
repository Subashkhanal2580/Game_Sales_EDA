/**
 * Custom JavaScript functionality for the Video Game Sales Dashboard
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    setupSidebarToggle();
    initializeResizeHandler();
    setupTableSorting();
    initializeExportButtons();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipElements.forEach(element => {
        new bootstrap.Tooltip(element);
    });
}

/**
 * Setup sidebar toggle functionality for mobile devices
 */
function setupSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            // Store sidebar state in localStorage
            localStorage.setItem('sidebarActive', sidebar.classList.contains('active'));
        });

        // Restore sidebar state from localStorage
        const sidebarActive = localStorage.getItem('sidebarActive') === 'true';
        if (sidebarActive) {
            sidebar.classList.add('active');
        }
    }
}

/**
 * Handle resize events for responsive charts
 */
function initializeResizeHandler() {
    let resizeTimer;
    const charts = document.querySelectorAll('.chart-container');

    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            charts.forEach(chart => {
                if (chart.__chart) {
                    chart.__chart.resize();
                }
            });
        }, 250);
    });
}

/**
 * Setup sortable tables functionality
 */
function setupTableSorting() {
    const tables = document.querySelectorAll('.sortable-table');
    
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        
        headers.forEach(header => {
            if (header.classList.contains('sortable')) {
                header.addEventListener('click', () => {
                    const column = header.dataset.column;
                    const currentDirection = header.dataset.direction || 'asc';
                    const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
                    
                    // Remove sorting indicators from all headers
                    headers.forEach(h => {
                        h.dataset.direction = '';
                        h.classList.remove('sort-asc', 'sort-desc');
                    });
                    
                    // Update current header
                    header.dataset.direction = newDirection;
                    header.classList.add(`sort-${newDirection}`);
                    
                    sortTable(table, column, newDirection);
                });
            }
        });
    });
}

/**
 * Sort table data
 * @param {HTMLElement} table - Table element to sort
 * @param {string} column - Column identifier
 * @param {string} direction - Sort direction ('asc' or 'desc')
 */
function sortTable(table, column, direction) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.querySelector(`td[data-column="${column}"]`).textContent;
        const bValue = b.querySelector(`td[data-column="${column}"]`).textContent;
        
        if (isNaN(aValue)) {
            return direction === 'asc' ? 
                aValue.localeCompare(bValue) : 
                bValue.localeCompare(aValue);
        } else {
            return direction === 'asc' ? 
                parseFloat(aValue) - parseFloat(bValue) : 
                parseFloat(bValue) - parseFloat(aValue);
        }
    });
    
    // Clear and append sorted rows
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}

/**
 * Initialize export functionality for charts and data
 */
function initializeExportButtons() {
    const exportButtons = document.querySelectorAll('[data-export-type]');
    
    exportButtons.forEach(button => {
        button.addEventListener('click', () => {
            const type = button.dataset.exportType;
            const target = button.dataset.exportTarget;
            
            switch (type) {
                case 'png':
                    exportChartAsPNG(target);
                    break;
                case 'csv':
                    exportDataAsCSV(target);
                    break;
                case 'excel':
                    exportDataAsExcel(target);
                    break;
            }
        });
    });
}

/**
 * Export chart as PNG
 * @param {string} chartId - ID of the chart container
 */
function exportChartAsPNG(chartId) {
    const chartContainer = document.getElementById(chartId);
    if (!chartContainer || !chartContainer.__chart) return;
    
    // Convert chart to canvas and download
    html2canvas(chartContainer).then(canvas => {
        const link = document.createElement('a');
        link.download = `${chartId}-export.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
}

/**
 * Export data as CSV
 * @param {string} dataId - ID of the data container
 */
function exportDataAsCSV(dataId) {
    const table = document.getElementById(dataId);
    if (!table) return;
    
    const rows = Array.from(table.querySelectorAll('tr'));
    const csvContent = rows.map(row => 
        Array.from(row.querySelectorAll('th, td'))
            .map(cell => `"${cell.textContent}"`)
            .join(',')
    ).join('\n');
    
    downloadFile(csvContent, `${dataId}-export.csv`, 'text/csv');
}

/**
 * Export data as Excel
 * @param {string} dataId - ID of the data container
 */
function exportDataAsExcel(dataId) {
    const table = document.getElementById(dataId);
    if (!table) return;
    
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.table_to_sheet(table);
    XLSX.utils.book_append_sheet(wb, ws, 'Data');
    
    XLSX.writeFile(wb, `${dataId}-export.xlsx`);
}

/**
 * Helper function to download files
 * @param {string} content - File content
 * @param {string} fileName - Name of the file
 * @param {string} contentType - MIME type of the file
 */
function downloadFile(content, fileName, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    link.href = url;
    link.download = fileName;
    link.click();
    
    window.URL.revokeObjectURL(url);
}

/**
 * Format number with proper separators and decimals
 * @param {number} value - Number to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted number
 */
function formatNumber(value, decimals = 2) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(value);
}

/**
 * Format percentage values
 * @param {number} value - Number to format as percentage
 * @returns {string} Formatted percentage
 */
function formatPercentage(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 1,
        maximumFractionDigits: 1
    }).format(value / 100);
}

/**
 * Debounce function for performance optimization
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Observe element visibility for lazy loading
 * @param {HTMLElement} element - Element to observe
 * @param {Function} callback - Callback when element becomes visible
 */
function observeVisibility(element, callback) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                callback();
                observer.unobserve(entry.target);
            }
        });
    });
    
    observer.observe(element);
}

// Export functions for use in other scripts
window.dashboardUtils = {
    formatNumber,
    formatPercentage,
    debounce,
    observeVisibility,
    exportChartAsPNG,
    exportDataAsCSV,
    exportDataAsExcel
};