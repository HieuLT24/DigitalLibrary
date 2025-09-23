// Tìm kiếm tự động trên navbar
class SearchAutocomplete {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.searchDropdown = document.getElementById('searchDropdown');
        this.searchResults = document.getElementById('searchResults');
        this.searchForm = document.getElementById('searchForm');
        
        this.debounceTimer = null;
        this.isSearching = false;
        
        this.init();
    }
    
    init() {
        if (!this.searchInput) return;
        
        this.searchInput.addEventListener('input', (e) => {
            this.handleInput(e.target.value);
        });
        
        this.searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.performFullSearch();
        });
        
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-container')) {
                this.hideDropdown();
            }
        });
        
    }
    
    handleInput(value) {
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        if (!value.trim()) {
            this.hideDropdown();
            return;
        }

    }
    
    async performQuickSearch(keyword) {
        if (this.isSearching) return;
        
        this.isSearching = true;
        this.showLoading();
        
        try {
            const result = await apiClient.searchBooks(keyword, null, null, 1, 5);
            
            if (result.success) {
                this.displayQuickResults(result.data.books);
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            console.error('Search error:', error);
            this.showError('Có lỗi xảy ra khi tìm kiếm: ' + error.message);
        } finally {
            this.isSearching = false;
        }
    }
    
    displayQuickResults(books) {
        if (!books || books.length === 0) {
            this.showNoResults();
            return;
        }
        
        this.searchResults.innerHTML = '';
        
        books.forEach(book => {
            const resultItem = this.createResultItem(book);
            this.searchResults.appendChild(resultItem);
        });
        
        this.showDropdown();
    }
    
    createResultItem(book) {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        item.onclick = () => this.selectBook(book);
        
        // Tạo hình ảnh placeholder
        const imageHtml = this.createBookImage(book);
        
        const title = this.highlightKeyword(book.title, this.searchInput.value);
        const author = book.author_name || 'Chưa có tác giả';
        const status = book.status === 'available' ? 'available' : 'borrowed';
        const statusText = book.status === 'available' ? 'Có sẵn' : 'Đã mượn';
        
        item.innerHTML = `
            ${imageHtml}
            <div class="search-result-content">
                <div class="search-result-title">${title}</div>
                <div class="search-result-meta">${author}</div>
            </div>
            <span class="search-result-status ${status}">${statusText}</span>
        `;
        
        return item;
    }
    
    createBookImage(book) {
        if (book.image) {
            return `
                <div class="search-result-image">
                    <img src="${book.image}" alt="${book.title}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 4px;">
                </div>
            `;
        }
        
        const firstLetter = book.title.charAt(0).toUpperCase();
        const colors = ['#e3f2fd', '#f3e5f5', '#e8f5e8', '#fff3e0', '#fce4ec'];
        const colorIndex = book.book_id % colors.length;
        
        return `
            <div class="search-result-image" style="background-color: ${colors[colorIndex]}">
                ${firstLetter}
            </div>
        `;
    }
    
    highlightKeyword(text, keyword) {
        if (!keyword) return text;
        
        const regex = new RegExp(`(${keyword})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    selectBook(book) {
        window.location.href = `/book/${book.book_id}`;
    }
    
    async performFullSearch() {
        const keyword = this.searchInput.value.trim();
        if (!keyword) return;
        
        window.location.href = `/search?q=${encodeURIComponent(keyword)}`;
    }
    
    showLoading() {
        this.searchResults.innerHTML = `
            <div class="search-loading">
                <i class="fas fa-spinner fa-spin"></i> Đang tìm kiếm...
            </div>
        `;
        this.showDropdown();
    }
    
    showError(message) {
        this.searchResults.innerHTML = `
            <div class="search-no-results">
                <i class="fas fa-exclamation-triangle"></i><br>
                ${message}
            </div>
        `;
        this.showDropdown();
    }
    
    showNoResults() {
        this.searchResults.innerHTML = `
            <div class="search-no-results">
                <i class="fas fa-search"></i><br>
                Không tìm thấy sách nào
            </div>
        `;
        this.showDropdown();
    }
    
    showDropdown() {
        this.searchDropdown.classList.remove('d-none');
    }
    
    hideDropdown() {
        this.searchDropdown.classList.add('d-none');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    new SearchAutocomplete();
});
