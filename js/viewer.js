/**
 * Viewer Module
 * Handles displaying elements in the UI
 */

class ElementViewer {
    constructor(apiService) {
        this.api = apiService;
        this.currentCategory = null;
        this.currentElements = [];
        this.selectedElement = null;
    }
    
    /**
     * Initialize the viewer and populate categories
     */
    init() {
        this.populateCategories();
        this.attachEventListeners();
    }
    
    /**
     * Populate the category sidebar
     */
    populateCategories() {
        const categoryList = document.getElementById('category-list');
        categoryList.innerHTML = '';
        
        ONLYWORLDS.ELEMENT_TYPES.forEach(type => {
            const categoryItem = document.createElement('div');
            categoryItem.className = 'category-item';
            categoryItem.dataset.type = type;
            
            categoryItem.innerHTML = `
                <span class="category-icon material-icons-outlined">${ONLYWORLDS.ELEMENT_ICONS[type]}</span>
                <span class="category-name">${ONLYWORLDS.ELEMENT_LABELS[type]}</span>
                <span class="category-count" id="count-${type}">-</span>
            `;
            
            categoryItem.addEventListener('click', () => this.selectCategory(type));
            categoryList.appendChild(categoryItem);
        });
        
        // Load counts for all categories
        this.updateCategoryCounts();
    }
    
    /**
     * Update element counts for each category
     */
    async updateCategoryCounts() {
        for (const type of ONLYWORLDS.ELEMENT_TYPES) {
            try {
                const elements = await this.api.getElements(type);
                const countElement = document.getElementById(`count-${type}`);
                if (countElement) {
                    countElement.textContent = elements.length;
                }
            } catch (error) {
                console.warn(`Could not get count for ${type}:`, error);
            }
        }
    }
    
    /**
     * Select a category and load its elements
     * @param {string} type - Element type to select
     */
    async selectCategory(type) {
        // Update UI to show selected category
        document.querySelectorAll('.category-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-type="${type}"]`)?.classList.add('active');
        
        this.currentCategory = type;
        
        // Update list title
        document.getElementById('list-title').textContent = ONLYWORLDS.ELEMENT_LABELS[type];
        
        // Show search input
        document.getElementById('search-input').classList.remove('hidden');
        
        // Load elements
        await this.loadElements(type);
    }
    
    /**
     * Load elements for a category
     * @param {string} type - Element type to load
     */
    async loadElements(type) {
        const elementList = document.getElementById('element-list');
        
        // Show loading state
        elementList.innerHTML = '<p class="loading-text">Loading...</p>';
        
        try {
            const elements = await this.api.getElements(type);
            this.currentElements = elements;
            
            if (elements.length === 0) {
                elementList.innerHTML = `<p class="empty-state">No ${ONLYWORLDS.ELEMENT_LABELS[type].toLowerCase()} found</p>`;
                return;
            }
            
            // Display elements
            this.displayElements(elements);
            
        } catch (error) {
            elementList.innerHTML = `<p class="error-text">Error loading ${type}s: ${error.message}</p>`;
            console.error('Error loading elements:', error);
        }
    }
    
    /**
     * Display a list of elements
     * @param {Array} elements - Elements to display
     */
    displayElements(elements) {
        const elementList = document.getElementById('element-list');
        elementList.innerHTML = '';
        
        elements.forEach(element => {
            const elementCard = document.createElement('div');
            elementCard.className = 'element-card';
            elementCard.dataset.id = element.id;
            
            // Create element display
            const icon = ONLYWORLDS.ELEMENT_ICONS[this.currentCategory] || 'category';
            const supertype = element.supertype ? `<span class="element-supertype">${element.supertype}</span>` : '';
            
            // Use a fallback for elements without names
            const displayName = element.name || element.title || `Unnamed ${this.currentCategory}`;
            
            elementCard.innerHTML = `
                <div class="element-header">
                    <span class="element-icon material-icons-outlined">${icon}</span>
                    <div class="element-info">
                        <h3 class="element-name">${this.escapeHtml(displayName)}</h3>
                        ${supertype}
                    </div>
                </div>
                <p class="element-description">${this.escapeHtml(element.description || 'No description')}</p>
            `;
            
            elementCard.addEventListener('click', () => this.selectElement(element));
            elementList.appendChild(elementCard);
        });
    }
    
    /**
     * Select and display an element's details
     * @param {Object} element - Element to display
     */
    async selectElement(element) {
        // Update UI to show selected element
        document.querySelectorAll('.element-card').forEach(card => {
            card.classList.remove('selected');
        });
        document.querySelector(`[data-id="${element.id}"]`)?.classList.add('selected');
        
        this.selectedElement = element;
        
        // Display element details
        await this.displayElementDetails(element);
    }
    
    /**
     * Display detailed view of an element
     * @param {Object} element - Element to display in detail
     */
    async displayElementDetails(element) {
        const detailContainer = document.getElementById('element-detail');
        
        // Use a fallback for elements without names
        const displayName = element.name || element.title || `Unnamed ${this.currentCategory}`;
        
        // Build detail view
        let html = `
            <div class="detail-header">
                <h2>${this.escapeHtml(displayName)}</h2>
                <div class="detail-actions">
                    <button class="btn btn-small" onclick="elementEditor.editElement('${this.currentCategory}', '${element.id}')">Edit</button>
                    <button class="btn btn-small btn-danger" onclick="elementViewer.deleteElement('${this.currentCategory}', '${element.id}')">Delete</button>
                </div>
            </div>
        `;
        
        // Add base fields
        html += '<div class="detail-section">';
        html += '<h3>Basic Information</h3>';
        html += '<table class="detail-table">';
        
        // Display base fields
        const baseFieldsToShow = ['name', 'description', 'supertype', 'subtype', 'image_url'];
        baseFieldsToShow.forEach(field => {
            if (element[field]) {
                const label = field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                const value = field === 'image_url' 
                    ? `<a href="${element[field]}" target="_blank">View Image</a>`
                    : this.escapeHtml(element[field]);
                html += `
                    <tr>
                        <td class="field-label">${label}:</td>
                        <td class="field-value">${value}</td>
                    </tr>
                `;
            }
        });
        
        html += '</table>';
        html += '</div>';
        
        // Add custom fields (fields not in base fields)
        const customFields = Object.keys(element).filter(field => 
            !ONLYWORLDS.BASE_FIELDS.includes(field)
        );
        
        if (customFields.length > 0) {
            html += '<div class="detail-section">';
            html += '<h3>Additional Fields</h3>';
            html += '<table class="detail-table">';
            
            for (const field of customFields) {
                const value = element[field];
                if (value !== null && value !== undefined) {
                    const label = field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                    
                    // Handle different value types
                    let displayValue;
                    if (Array.isArray(value)) {
                        displayValue = value.length > 0 ? value.join(', ') : '<em>Empty list</em>';
                    } else if (typeof value === 'object') {
                        displayValue = '<pre>' + JSON.stringify(value, null, 2) + '</pre>';
                    } else if (typeof value === 'boolean') {
                        displayValue = value ? 'Yes' : 'No';
                    } else {
                        displayValue = this.escapeHtml(String(value));
                    }
                    
                    html += `
                        <tr>
                            <td class="field-label">${label}:</td>
                            <td class="field-value">${displayValue}</td>
                        </tr>
                    `;
                }
            }
            
            html += '</table>';
            html += '</div>';
        }
        
        // Add metadata
        html += '<div class="detail-section">';
        html += '<h3>Metadata</h3>';
        html += '<table class="detail-table">';
        html += `
            <tr>
                <td class="field-label">ID:</td>
                <td class="field-value"><code>${element.id}</code></td>
            </tr>
            <tr>
                <td class="field-label">Created:</td>
                <td class="field-value">${this.formatDate(element.created_at)}</td>
            </tr>
            <tr>
                <td class="field-label">Updated:</td>
                <td class="field-value">${this.formatDate(element.updated_at)}</td>
            </tr>
        `;
        html += '</table>';
        html += '</div>';
        
        detailContainer.innerHTML = html;
    }
    
    /**
     * Delete an element after confirmation
     * @param {string} type - Element type
     * @param {string} id - Element ID
     */
    async deleteElement(type, id) {
        if (!confirm('Are you sure you want to delete this element? This cannot be undone.')) {
            return;
        }
        
        try {
            await this.api.deleteElement(type, id);
            
            // Refresh the list
            await this.loadElements(type);
            
            // Clear detail view
            document.getElementById('element-detail').innerHTML = '<p class="empty-state">Select an element to view details</p>';
            
            // Update count
            const countElement = document.getElementById(`count-${type}`);
            if (countElement) {
                countElement.textContent = this.currentElements.length;
            }
            
            alert('Element deleted successfully');
            
        } catch (error) {
            alert(`Error deleting element: ${error.message}`);
            console.error('Error deleting element:', error);
        }
    }
    
    /**
     * Search elements in the current category
     * @param {string} searchTerm - Search term
     */
    async searchElements(searchTerm) {
        if (!this.currentCategory) return;
        
        if (!searchTerm) {
            // If search is empty, reload all elements
            await this.loadElements(this.currentCategory);
            return;
        }
        
        // Filter current elements locally for quick response
        const filtered = this.currentElements.filter(element => 
            element.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            element.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            element.supertype?.toLowerCase().includes(searchTerm.toLowerCase())
        );
        
        this.displayElements(filtered);
    }
    
    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Search input
        const searchInput = document.getElementById('search-input');
        let searchTimeout;
        
        searchInput?.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.searchElements(e.target.value);
            }, 300);
        });
    }
    
    /**
     * Escape HTML to prevent XSS
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
     */
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    /**
     * Format date for display
     * @param {string} dateString - ISO date string
     * @returns {string} Formatted date
     */
    formatDate(dateString) {
        if (!dateString) return 'Unknown';
        try {
            const date = new Date(dateString);
            return date.toLocaleString();
        } catch {
            return dateString;
        }
    }
}

// Create global instance (will be initialized after API is ready)
window.elementViewer = null;