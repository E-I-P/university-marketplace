// Flash message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(function(message) {
        // Auto-hide success and info messages after 5 seconds
        if (message.classList.contains('flash-success') || message.classList.contains('flash-info')) {
            setTimeout(function() {
                message.style.opacity = '0';
                setTimeout(function() {
                    message.remove();
                }, 300);
            }, 5000);
        }
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            field.style.borderColor = '#ddd';
        }
    });
    
    return isValid;
}

// Registration number formatting
document.addEventListener('DOMContentLoaded', function() {
    const regNumberInput = document.getElementById('reg_number');
    if (regNumberInput) {
        regNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.toUpperCase();
            // Remove any non-alphanumeric characters
            value = value.replace(/[^A-Z0-9]/g, '');
            
            // Format as H000000A
            if (value.length > 0) {
                if (value.length <= 1) {
                    // First character should be a letter
                    value = value.replace(/[^A-Z]/g, '');
                } else if (value.length <= 7) {
                    // Characters 2-7 should be numbers
                    const firstChar = value.charAt(0);
                    const numbers = value.substring(1).replace(/[^0-9]/g, '');
                    value = firstChar + numbers;
                } else {
                    // Last character should be a letter
                    const firstChar = value.charAt(0);
                    const numbers = value.substring(1, 7).replace(/[^0-9]/g, '');
                    const lastChar = value.charAt(7).replace(/[^A-Z]/g, '');
                    value = firstChar + numbers + lastChar;
                }
            }
            
            e.target.value = value;
        });
    }
});

// Price input validation
document.addEventListener('DOMContentLoaded', function() {
    const priceInput = document.getElementById('price');
    if (priceInput) {
        priceInput.addEventListener('input', function(e) {
            let value = e.target.value;
            
            // Remove any non-numeric characters except decimal point
            value = value.replace(/[^0-9.]/g, '');
            
            // Ensure only one decimal point
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            
            // Limit to 2 decimal places
            if (parts[1] && parts[1].length > 2) {
                value = parts[0] + '.' + parts[1].substring(0, 2);
            }
            
            e.target.value = value;
        });
    }
});

// Search form enhancement
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('.search-input');
        const categorySelect = searchForm.querySelector('.category-select');
        
        // Auto-submit on category change
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                searchForm.submit();
            });
        }
        
        // Clear search functionality
        if (searchInput) {
            searchInput.addEventListener('keyup', function(e) {
                if (e.key === 'Escape') {
                    searchInput.value = '';
                    searchForm.submit();
                }
            });
        }
    }
});

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Image loading error handling
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    
    images.forEach(function(img) {
        img.addEventListener('error', function() {
            this.src = '/broken-image-icon.png';
            this.alt = 'Image not available';
        });
    });
});

// Mobile menu toggle (if needed for responsive design)
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.classList.toggle('mobile-active');
    }
}

// Confirmation dialogs for important actions
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?');
}

// Local storage for user preferences
function saveUserPreference(key, value) {
    try {
        localStorage.setItem('smp_' + key, JSON.stringify(value));
    } catch (e) {
        console.warn('Could not save user preference:', e);
    }
}

function getUserPreference(key, defaultValue) {
    try {
        const stored = localStorage.getItem('smp_' + key);
        return stored ? JSON.parse(stored) : defaultValue;
    } catch (e) {
        console.warn('Could not load user preference:', e);
        return defaultValue;
    }
}

// Initialize user preferences
document.addEventListener('DOMContentLoaded', function() {
    // Remember search preferences
    const searchInput = document.querySelector('.search-input');
    const categorySelect = document.querySelector('.category-select');
    
    if (searchInput && !searchInput.value) {
        const savedSearch = getUserPreference('lastSearch', '');
        if (savedSearch) {
            searchInput.value = savedSearch;
        }
    }
    
    // Save search on form submit
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            if (searchInput) {
                saveUserPreference('lastSearch', searchInput.value);
            }
        });
    }
});
