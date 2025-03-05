document.addEventListener('DOMContentLoaded', function() {
    const searchIcon = document.getElementById('search-icon');
    const searchBar = document.getElementById('search-bar');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const searchSuggestions = document.getElementById('search-suggestions');

    // Toggle search bar visibility
    searchIcon.addEventListener('click', function(event) {
        event.preventDefault();
        searchBar.style.display = searchBar.style.display === 'none' ? 'block' : 'none';
    });

    // Handle search button click
    searchButton.addEventListener('click', function() {
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = `/search/?q=${encodeURIComponent(query)}`;
        }
    });

    // Handle Enter key press in the search input
    searchInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                window.location.href = `/search/?q=${encodeURIComponent(query)}`;
            }
        }
    });

    // Fetch search suggestions as the user types
    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        if (query) {
            fetch(`/search/suggestions/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.suggestions.length > 0) {
                        const suggestionsHTML = data.suggestions.map(suggestion => 
                            `<div class="suggestion-item">${suggestion}</div>`
                        ).join('');
                        searchSuggestions.innerHTML = suggestionsHTML;
                        searchSuggestions.style.display = 'block';
                    } else {
                        searchSuggestions.innerHTML = '';
                        searchSuggestions.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error fetching search suggestions:', error);
                });
        } else {
            searchSuggestions.innerHTML = '';
            searchSuggestions.style.display = 'none';
        }
    });

    // Handle click on a suggestion
    searchSuggestions.addEventListener('click', function(event) {
        if (event.target.classList.contains('suggestion-item')) {
            searchInput.value = event.target.textContent;
            searchSuggestions.innerHTML = '';
            searchSuggestions.style.display = 'none';
            window.location.href = `/search/?q=${encodeURIComponent(event.target.textContent)}`;
        }
    });
});