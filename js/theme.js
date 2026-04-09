// ============================================
// READERA - DARK MODE THEME MANAGER
// ============================================

const ThemeManager = {
    // Keys for localStorage
    STORAGE_KEY: 'readera_theme',

    // Theme values
    THEMES: {
        LIGHT: 'light',
        DARK: 'dark'
    },

    // Initialize theme on page load
    init() {
        // Get saved theme or system preference
        const savedTheme = this.getSavedTheme();
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        // Determine initial theme
        let initialTheme = savedTheme;
        if (!initialTheme) {
            initialTheme = systemPrefersDark ? this.THEMES.DARK : this.THEMES.LIGHT;
        }

        // Apply theme
        this.applyTheme(initialTheme);

        // Setup theme toggle button
        this.setupToggleButton();

        // Listen for system theme changes (optional)
        this.listenToSystemTheme();
    },

    // Get saved theme from localStorage
    getSavedTheme() {
        return localStorage.getItem(this.STORAGE_KEY);
    },

    // Save theme to localStorage
    saveTheme(theme) {
        localStorage.setItem(this.STORAGE_KEY, theme);
    },

    // Apply theme to body
    applyTheme(theme) {
        if (theme === this.THEMES.DARK) {
            document.body.classList.add('dark-mode');
            this.updateToggleButtonIcon(true);
        } else {
            document.body.classList.remove('dark-mode');
            this.updateToggleButtonIcon(false);
        }

        // Save to localStorage
        this.saveTheme(theme);

        // Dispatch event for other components to listen
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: theme } }));
    },

    // Toggle between light and dark
    toggleTheme() {
        const isDarkMode = document.body.classList.contains('dark-mode');

        if (isDarkMode) {
            this.applyTheme(this.THEMES.LIGHT);
            this.showToast('Light mode activated', 'info');
        } else {
            this.applyTheme(this.THEMES.DARK);
            this.showToast('Dark mode activated', 'info');
        }
    },

    // Update toggle button icon based on current theme
    updateToggleButtonIcon(isDark) {
        const toggleBtn = document.getElementById('theme-toggle');
        if (!toggleBtn) return;

        if (isDark) {
            toggleBtn.innerHTML = '☀️';
            toggleBtn.setAttribute('aria-label', 'Switch to light mode');
        } else {
            toggleBtn.innerHTML = '🌙';
            toggleBtn.setAttribute('aria-label', 'Switch to dark mode');
        }
    },

    // Setup theme toggle button event listener
    setupToggleButton() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            // Remove any existing listeners
            const newToggleBtn = toggleBtn.cloneNode(true);
            toggleBtn.parentNode.replaceChild(newToggleBtn, toggleBtn);

            // Add new listener
            newToggleBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTheme();
            });

            // Update icon based on current state
            const isDark = document.body.classList.contains('dark-mode');
            this.updateToggleButtonIcon(isDark);
        } else {
            console.warn('Theme toggle button not found! Make sure element with id="theme-toggle" exists.');
        }
    },

    // Listen to system theme changes (optional feature)
    listenToSystemTheme() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        // Only listen if user hasn't manually set a preference
        mediaQuery.addEventListener('change', (e) => {
            const savedTheme = this.getSavedTheme();

            // If user never manually chose a theme, follow system
            if (!savedTheme) {
                const newTheme = e.matches ? this.THEMES.DARK : this.THEMES.LIGHT;
                this.applyTheme(newTheme);
            }
        });
    },

    // Show toast notification
    showToast(message, type = 'info') {
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

        // Auto remove after 2 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 2000);

        // Click to dismiss
        toast.onclick = () => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        };
    },

    // Get current theme
    getCurrentTheme() {
        return document.body.classList.contains('dark-mode') ? this.THEMES.DARK : this.THEMES.LIGHT;
    },

    // Preload theme before page render (to avoid flash)
    preloadTheme() {
        const savedTheme = this.getSavedTheme();
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (savedTheme === this.THEMES.DARK || (!savedTheme && systemPrefersDark)) {
            document.body.classList.add('dark-mode');
        }
    }
};

// Add CSS animations for toast (if not already added)
const toastAnimationStyles = document.createElement('style');
toastAnimationStyles.textContent = `
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

// Only add styles if they don't exist
if (!document.querySelector('#toast-animation-styles')) {
    toastAnimationStyles.id = 'toast-animation-styles';
    document.head.appendChild(toastAnimationStyles);
}

// Preload theme immediately (prevents flash of wrong theme)
ThemeManager.preloadTheme();

// Initialize theme when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
});

// Make ThemeManager globally available
window.ThemeManager = ThemeManager;

console.log('✅ Theme Manager loaded successfully!');