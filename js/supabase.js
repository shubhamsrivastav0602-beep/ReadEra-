// ============================================
// READERA - SUPABASE CLIENT CONFIGURATION
// ============================================

// ⚠️ IMPORTANT: Replace these with your own Supabase credentials
// Go to: Your Supabase Project → Settings → API

const SUPABASE_URL = 'https://rjyzblqxpzhirsdctvpq.supabase.co';  // 👈 Replace this
const SUPABASE_ANON_KEY = 'sb_publishable_MPqGLh4Zi5HdLuTRQ81SzA_Ssm9nSQo';              // 👈 Replace this

// Initialize Supabase client
const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// ============================================
// AUTHENTICATION FUNCTIONS
// ============================================

const AuthService = {
    // Sign up new user
    async signUp(email, password, fullName) {
        try {
            const { data, error } = await supabaseClient.auth.signUp({
                email: email,
                password: password,
                options: {
                    data: {
                        full_name: fullName
                    }
                }
            });

            if (error) throw error;

            // Show success message
            showToast('Account created successfully! Please verify your email.', 'success');
            return { success: true, data };
        } catch (error) {
            showToast(error.message, 'error');
            return { success: false, error: error.message };
        }
    },

    // Sign in existing user
    async signIn(email, password) {
        try {
            const { data, error } = await supabaseClient.auth.signInWithPassword({
                email: email,
                password: password
            });

            if (error) throw error;

            // Save session to localStorage
            localStorage.setItem('token', data.session.access_token);
            localStorage.setItem('refresh_token', data.session.refresh_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.setItem('token_expiry', Date.now() + (data.session.expires_in * 1000));

            showToast('Welcome back!', 'success');

            // Start token refresh timer
            this.startTokenRefreshTimer();

            // Redirect to home page
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1000);

            return { success: true, data };
        } catch (error) {
            showToast(error.message, 'error');
            return { success: false, error: error.message };
        }
    },

    // Refresh token before it expires
    async refreshTokenIfNeeded() {
        try {
            const tokenExpiry = localStorage.getItem('token_expiry');
            const now = Date.now();
            
            // If token expires in less than 5 minutes, refresh it
            if (tokenExpiry && (parseInt(tokenExpiry) - now) < 5 * 60 * 1000) {
                const { data, error } = await supabaseClient.auth.refreshSession();
                
                if (error) throw error;
                
                // Update token in localStorage
                localStorage.setItem('token', data.session.access_token);
                localStorage.setItem('refresh_token', data.session.refresh_token);
                localStorage.setItem('token_expiry', Date.now() + (data.session.expires_in * 1000));
                
                console.log('Token refreshed successfully');
                return { success: true };
            }
            
            return { success: true };
        } catch (error) {
            console.error('Token refresh failed:', error);
            // If refresh fails, force logout
            this.signOut();
            return { success: false, error: error.message };
        }
    },

    // Start automatic token refresh timer
    startTokenRefreshTimer() {
        // Refresh token every 30 minutes
        if (window.tokenRefreshInterval) {
            clearInterval(window.tokenRefreshInterval);
        }
        
        window.tokenRefreshInterval = setInterval(() => {
            if (this.isAuthenticated()) {
                this.refreshTokenIfNeeded();
            }
        }, 30 * 60 * 1000);
    },

    // Stop token refresh timer
    stopTokenRefreshTimer() {
        if (window.tokenRefreshInterval) {
            clearInterval(window.tokenRefreshInterval);
        }
    },

    // Sign out user
    async signOut() {
        try {
            // Stop token refresh timer
            this.stopTokenRefreshTimer();

            const { error } = await supabaseClient.auth.signOut();
            if (error) throw error;

            // Clear localStorage
            localStorage.removeItem('token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('token_expiry');
            localStorage.removeItem('user');
            localStorage.removeItem('readera_current_user');
            localStorage.removeItem('admin_logged_in');

            showToast('Logged out successfully', 'success');

            // Redirect to login page
            setTimeout(() => {
                window.location.href = 'auth.html';
            }, 500);

            return { success: true };
        } catch (error) {
            showToast(error.message, 'error');
            return { success: false, error: error.message };
        }
    },

    // Get current user
    getCurrentUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    // Check if user is logged in
    isAuthenticated() {
        return !!localStorage.getItem('token');
    },

    // Refresh navigation based on auth state
    refreshNav() {
        const isLoggedIn = this.isAuthenticated();
        const libraryLink = document.getElementById('library-link');
        const profileLink = document.getElementById('profile-link');
        const authLink = document.getElementById('auth-link');
        const logoutLink = document.getElementById('logout-link');
        const heroLibraryCta = document.getElementById('hero-library-cta');

        if (isLoggedIn) {
            if (libraryLink) libraryLink.style.display = 'list-item';
            if (profileLink) profileLink.style.display = 'list-item';
            if (authLink) authLink.style.display = 'none';
            if (logoutLink) logoutLink.style.display = 'inline-flex';
            if (heroLibraryCta) heroLibraryCta.style.display = 'inline-flex';
        } else {
            if (libraryLink) libraryLink.style.display = 'none';
            if (profileLink) profileLink.style.display = 'none';
            if (authLink) authLink.style.display = 'inline-flex';
            if (logoutLink) logoutLink.style.display = 'none';
            if (heroLibraryCta) heroLibraryCta.style.display = 'none';
        }
    }
};

// ============================================
// BOOKS FUNCTIONS
// ============================================

const BookService = {
    // Get all books with pagination
    async getAllBooks(page = 1, limit = 20) {
        try {
            const start = (page - 1) * limit;
            const { data, error, count } = await supabaseClient
                .from('books')
                .select('*', { count: 'exact' })
                .range(start, start + limit - 1)
                .order('created_at', { ascending: false });

            if (error) throw error;

            return { success: true, books: data, total: count, page, limit };
        } catch (error) {
            console.error('Error fetching books:', error);
            return { success: false, books: [], error: error.message };
        }
    },

    // Get book by ID
    async getBookById(bookId) {
        try {
            const { data, error } = await supabaseClient
                .from('books')
                .select('*')
                .eq('id', bookId)
                .single();

            if (error) throw error;

            // Increment view count
            await this.incrementViews(bookId);

            return { success: true, book: data };
        } catch (error) {
            console.error('Error fetching book:', error);
            return { success: false, book: null, error: error.message };
        }
    },

    // Increment book views
    async incrementViews(bookId) {
        try {
            await supabaseClient.rpc('increment_book_views', { book_id: bookId });
        } catch (error) {
            console.error('Error incrementing views:', error);
        }
    },

    // Search books by title or author
    async searchBooks(query, genre = null, page = 1, limit = 20) {
        try {
            let searchQuery = supabaseClient
                .from('books')
                .select('*', { count: 'exact' });

            // Search in title or author
            if (query) {
                searchQuery = searchQuery.or(`title.ilike.%${query}%,author.ilike.%${query}%`);
            }

            // Filter by genre
            if (genre && genre !== 'all') {
                searchQuery = searchQuery.eq('genre', genre);
            }

            const start = (page - 1) * limit;
            const { data, error, count } = await searchQuery
                .range(start, start + limit - 1)
                .order('views', { ascending: false });

            if (error) throw error;

            return { success: true, books: data, total: count };
        } catch (error) {
            console.error('Error searching books:', error);
            return { success: false, books: [], error: error.message };
        }
    },

    // Get books by genre
    async getBooksByGenre(genre, page = 1, limit = 20) {
        try {
            const start = (page - 1) * limit;
            const { data, error, count } = await supabaseClient
                .from('books')
                .select('*', { count: 'exact' })
                .eq('genre', genre)
                .range(start, start + limit - 1)
                .order('views', { ascending: false });

            if (error) throw error;

            return { success: true, books: data, total: count };
        } catch (error) {
            console.error('Error fetching books by genre:', error);
            return { success: false, books: [], error: error.message };
        }
    },

    // Get featured books (most viewed)
    async getFeaturedBooks(limit = 8) {
        try {
            const { data, error } = await supabaseClient
                .from('books')
                .select('*')
                .order('views', { ascending: false })
                .limit(limit);

            if (error) throw error;

            return { success: true, books: data };
        } catch (error) {
            console.error('Error fetching featured books:', error);
            return { success: false, books: [] };
        }
    },

    // Get recent books
    async getRecentBooks(limit = 10) {
        try {
            const { data, error } = await supabaseClient
                .from('books')
                .select('*')
                .order('created_at', { ascending: false })
                .limit(limit);

            if (error) throw error;

            return { success: true, books: data };
        } catch (error) {
            console.error('Error fetching recent books:', error);
            return { success: false, books: [] };
        }
    }
};

// ============================================
// GENRE FUNCTIONS
// ============================================

const GenreService = {
    // Get all genres
    async getAllGenres() {
        try {
            const { data, error } = await supabaseClient
                .from('genres')
                .select('*')
                .order('name');

            if (error) throw error;

            return { success: true, genres: data };
        } catch (error) {
            console.error('Error fetching genres:', error);
            return { success: false, genres: [] };
        }
    },

    // Get genre by name
    async getGenreByName(name) {
        try {
            const { data, error } = await supabaseClient
                .from('genres')
                .select('*')
                .eq('name', name)
                .single();

            if (error) throw error;

            return { success: true, genre: data };
        } catch (error) {
            console.error('Error fetching genre:', error);
            return { success: false, genre: null };
        }
    }
};

// ============================================
// USER LIBRARY FUNCTIONS
// ============================================

const LibraryService = {
    // Add book to user's library
    async addToLibrary(bookId) {
        try {
            const user = AuthService.getCurrentUser();
            if (!user) {
                showToast('Please login to add books to your library', 'warning');
                return { success: false, error: 'Not authenticated' };
            }

            const { data, error } = await supabaseClient
                .from('user_library')
                .insert({
                    user_id: user.id,
                    book_id: bookId,
                    added_at: new Date()
                })
                .select();

            if (error) throw error;

            showToast('Book added to your library!', 'success');
            return { success: true, data };
        } catch (error) {
            if (error.code === '23505') {
                showToast('Book already in your library', 'info');
            } else {
                showToast(error.message, 'error');
            }
            return { success: false, error: error.message };
        }
    },

    // Remove book from library
    async removeFromLibrary(bookId) {
        try {
            const user = AuthService.getCurrentUser();
            if (!user) return { success: false, error: 'Not authenticated' };

            const { error } = await supabaseClient
                .from('user_library')
                .delete()
                .eq('user_id', user.id)
                .eq('book_id', bookId);

            if (error) throw error;

            showToast('Book removed from your library', 'success');
            return { success: true };
        } catch (error) {
            showToast(error.message, 'error');
            return { success: false, error: error.message };
        }
    },

    // Get user's library
    async getUserLibrary() {
        try {
            const user = AuthService.getCurrentUser();
            if (!user) return { success: false, books: [] };

            const { data, error } = await supabaseClient
                .from('user_library')
                .select(`
                    id,
                    last_read_page,
                    is_favorite,
                    added_at,
                    books (*)
                `)
                .eq('user_id', user.id)
                .order('added_at', { ascending: false });

            if (error) throw error;

            const books = data.map(item => ({
                ...item.books,
                library_id: item.id,
                last_read_page: item.last_read_page,
                is_favorite: item.is_favorite,
                added_at: item.added_at
            }));

            return { success: true, books };
        } catch (error) {
            console.error('Error fetching user library:', error);
            return { success: false, books: [] };
        }
    },

    // Check if book is in library
    async isInLibrary(bookId) {
        try {
            const user = AuthService.getCurrentUser();
            if (!user) return false;

            const { data, error } = await supabaseClient
                .from('user_library')
                .select('id')
                .eq('user_id', user.id)
                .eq('book_id', bookId)
                .maybeSingle();

            if (error) throw error;

            return !!data;
        } catch (error) {
            return false;
        }
    },

    // Update reading progress
    async updateProgress(bookId, pageNumber) {
        try {
            const user = AuthService.getCurrentUser();
            if (!user) return { success: false };

            const { error } = await supabaseClient
                .from('user_library')
                .update({ last_read_page: pageNumber })
                .eq('user_id', user.id)
                .eq('book_id', bookId);

            if (error) throw error;

            // Also add to reading history
            await supabaseClient
                .from('reading_history')
                .insert({
                    user_id: user.id,
                    book_id: bookId,
                    read_at: new Date()
                });

            return { success: true };
        } catch (error) {
            console.error('Error updating progress:', error);
            return { success: false };
        }
    },

    // Toggle favorite
    async toggleFavorite(bookId) {
        try {
            const user = AuthService.getCurrentUser();
            if (!user) return { success: false };

            // Get current favorite status
            const { data: current } = await supabaseClient
                .from('user_library')
                .select('is_favorite')
                .eq('user_id', user.id)
                .eq('book_id', bookId)
                .single();

            const { error } = await supabaseClient
                .from('user_library')
                .update({ is_favorite: !current?.is_favorite })
                .eq('user_id', user.id)
                .eq('book_id', bookId);

            if (error) throw error;

            showToast(current?.is_favorite ? 'Removed from favorites' : 'Added to favorites', 'success');
            return { success: true };
        } catch (error) {
            showToast(error.message, 'error');
            return { success: false };
        }
    }
};

// ============================================
// HELPER FUNCTIONS
// ============================================

// Toast notification function
function showToast(message, type = 'info') {
    // Check if toast container exists
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
        `;
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };

    toast.style.cssText = `
        background: ${colors[type] || colors.info};
        color: white;
        padding: 12px 20px;
        margin-top: 10px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
        cursor: pointer;
    `;

    toast.textContent = message;
    toastContainer.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);

    // Click to dismiss
    toast.onclick = () => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    };
}

// Add CSS animations for toast
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(toastStyles);

// ============================================
// EXPORT FUNCTIONS (make them global)
// ============================================

window.supabaseClient = supabaseClient;
window.AuthService = AuthService;
window.BookService = BookService;
window.GenreService = GenreService;
window.LibraryService = LibraryService;
window.showToast = showToast;

console.log('✅ Supabase services loaded successfully!');