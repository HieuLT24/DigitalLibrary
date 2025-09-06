

class APIClient {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
    }

    // Helper method để gọi API
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

    // Book APIs
    async getBooks(page = 1, perPage = 10) {
        return this.request(`/books?page=${page}&per_page=${perPage}`);
    }

    async searchBooks(keyword = '', categoryId = null, authorId = null, page = 1) {
        let url = `/books/search?q=${encodeURIComponent(keyword)}&page=${page}`;
        if (categoryId) url += `&category_id=${categoryId}`;
        if (authorId) url += `&author_id=${authorId}`;
        return this.request(url);
    }

    async getBookById(bookId) {
        return this.request(`/books/${bookId}`);
    }

    async getPopularBooks(limit = 10) {
        return this.request(`/books/popular?limit=${limit}`);
    }

    async getCategories() {
        return this.request('/categories');
    }

    async getAuthors() {
        return this.request('/authors');
    }

    // User APIs
    async getUsers(page = 1, perPage = 10) {
        return this.request(`/users?page=${page}&per_page=${perPage}`);
    }

    async getUserById(userId) {
        return this.request(`/users/${userId}`);
    }

    async createUser(userData) {
        return this.request('/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async updateUser(userId, userData) {
        return this.request(`/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    }

    async deleteUser(userId) {
        return this.request(`/users/${userId}`, {
            method: 'DELETE'
        });
    }

    // Auth APIs
    async login(username, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    }

    async logout() {
        return this.request('/auth/logout', {
            method: 'POST'
        });
    }

    async register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async getProfile() {
        return this.request('/auth/profile');
    }

    async changePassword(oldPassword, newPassword) {
        return this.request('/auth/change-password', {
            method: 'POST',
            body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
        });
    }
}

// Tạo instance global
const apiClient = new APIClient();

// Export để sử dụng
window.apiClient = apiClient;
