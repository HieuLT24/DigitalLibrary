

class APIClient {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Có lỗi xảy ra');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async getBooks(page = 1, perPage = 10) {
        return this.request(`/books?page=${page}&per_page=${perPage}`);
    }

    async searchBooks(keyword = '', page = 1, perPage = 16) {
        let url = `/books/search?q=${encodeURIComponent(keyword)}&page=${page}&per_page=${perPage}`;
        return this.request(url);
    }

    async getBookById(bookId) {
        return this.request(`/books/${bookId}`);
    }



    async getCategories() {
        return this.request('/categories');
    }

    async getAuthors() {
        return this.request('/authors');
    }


    
}

const apiClient = new APIClient();

window.apiClient = apiClient;
