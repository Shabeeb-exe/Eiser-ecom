document.addEventListener('DOMContentLoaded', function () {
    const searchIcon = document.getElementById('search-icon');
    const searchBar = document.getElementById('search-bar');
    const searchInput = document.getElementById('search-input');
    const searchHistory = document.getElementById('search-history');
    const searchSuggestions = document.getElementById('search-suggestions');
    const suggestionsLabel = document.getElementById('suggestions-label');
    const clearAllButton = document.getElementById('clear-all');


    // Function to check if search history is visible and has matching items
    function hasVisibleSearchHistory() {
        if (!searchHistory || searchHistory.style.display === 'none') {
            return false;
        }
        const historyItems = searchHistory.querySelectorAll('.history-item');
        return Array.from(historyItems).some(item => item.style.display !== 'none');
    }

    // Function to position search suggestions
    function positionSuggestions() {
        if (!searchSuggestions) return;

        const searchBarRect = searchBar.getBoundingClientRect();
        const inputRect = searchInput.getBoundingClientRect();

        if (hasVisibleSearchHistory()) {
            // If search history is visible, position suggestions below it
            const historyRect = searchHistory.getBoundingClientRect();
            const topOffset = historyRect.bottom - searchBarRect.top;
            searchSuggestions.style.top = `${topOffset}px`;
        } else {
            // If no search history is visible, position suggestions directly below the input bar
            const topOffset = inputRect.bottom - searchBarRect.top;
            searchSuggestions.style.top = `${topOffset}px`;
        }
    }

    // Show search history and suggestions when input is focused
    searchInput.addEventListener('focus', function () {
        if (searchHistory) searchHistory.style.display = 'block';
        if (searchSuggestions) searchSuggestions.style.display = 'none'; // Hide suggestions initially
        positionSuggestions(); // Position suggestions dynamically
    });

    // Hide search history and suggestions when input loses focus
    searchInput.addEventListener('blur', function () {
        setTimeout(() => {
            if (searchHistory) searchHistory.style.display = 'none';
            if (searchSuggestions) searchSuggestions.style.display = 'none';
        }, 500); // Delay to allow click events on suggestions/history
    });

    // Handle input changes to show suggestions and filter search history
    searchInput.addEventListener('input', function () {
        const query = searchInput.value.trim();

        // Filter search history based on user input
        if (searchHistory) {
            const historyItems = searchHistory.querySelectorAll('.history-item');
            let hasMatches = false;

            historyItems.forEach(item => {
                const historyQuery = item.getAttribute('data-query').toLowerCase();
                if (historyQuery.includes(query.toLowerCase())) {
                    item.style.display = 'block';
                    hasMatches = true;
                } else {
                    item.style.display = 'none';
                }
            });

            // Show or hide the search history div based on matches
            if (hasMatches) {
                searchHistory.style.display = 'block';
            } else {
                searchHistory.style.display = 'none';
            }
        }

        // Position suggestions dynamically
        positionSuggestions();
    });

    // Update suggestions position when search history changes
    if (searchHistory) {
        const observer = new MutationObserver(positionSuggestions);
        observer.observe(searchHistory, { childList: true, subtree: true });
    }

    // Function to perform search
    function performSearch() {
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = `/search/?q=${encodeURIComponent(query)}`;
        }
    }

    // Handle search icon click
    searchIcon.addEventListener('click', function (event) {
        event.preventDefault();
        performSearch();
    });

    // Handle Enter key press in the search input
    searchInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            performSearch();
        }
    });

    // Function to filter search history based on user input
    function filterSearchHistory(query) {
        if (!searchHistory) return;

        const historyItems = searchHistory.querySelectorAll('.history-item');
        let hasMatches = false;

        historyItems.forEach(item => {
            const historyQuery = item.getAttribute('data-query').toLowerCase();
            if (historyQuery.includes(query.toLowerCase())) {
                item.style.display = 'block';
                hasMatches = true;
            } else {
                item.style.display = 'none';
            }
        });

        // Show or hide the search history div based on matches
        if (hasMatches) {
            searchHistory.style.display = 'block';
        } else {
            searchHistory.style.display = 'none';
        }
    }

    // Fetch search suggestions as the user types
    searchInput.addEventListener('input', function () {
        const query = searchInput.value.trim();
    
        // Filter search history based on user input
        filterSearchHistory(query);
    
        if (query) {
            fetch(`/search/suggestions/?q=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.suggestions && data.suggestions.length > 0) {
                        const suggestionsHTML = data.suggestions.map(suggestion => {
                            const [type, name] = suggestion.split(': ');
                            return `
                                <div class="suggestion-item" data-query="${name}">
                                    <span class="suggestion-type">${type}:</span>
                                    <span class="suggestion-name">${name}</span>
                                </div>
                            `;
                        }).join('');
                        searchSuggestions.innerHTML = suggestionsHTML;
                        searchSuggestions.style.display = 'block';
                    } else {
                        searchSuggestions.innerHTML = '';
                        searchSuggestions.style.display = 'none'; // Hide suggestions if no data
                    }
                })
                .catch(error => {
                    console.error('Error fetching search suggestions:', error);
                    searchSuggestions.innerHTML = '';
                    searchSuggestions.style.display = 'none'; // Hide suggestions on error
                    suggestionsLabel.style.display = 'none'; // Hide suggestions label
                });
        } else {
            searchSuggestions.innerHTML = '';
            searchSuggestions.style.display = 'none'; // Hide suggestions if query is empty
            suggestionsLabel.style.display = 'none'; // Hide suggestions label
        }
    });

    // Handle click on a suggestion or history item
    searchBar.addEventListener('click', function (event) {
        if (event.target.classList.contains('suggestion-item') || event.target.closest('.suggestion-item')) {
            const suggestionItem = event.target.closest('.suggestion-item');
            const suggestionName = suggestionItem.querySelector('.suggestion-name').textContent;
            searchInput.value = suggestionName;
            searchSuggestions.innerHTML = '';
            searchSuggestions.style.display = 'none';
            suggestionsLabel.style.display = 'none'; // Hide suggestions label
            window.location.href = `/search/?q=${encodeURIComponent(suggestionName)}`;
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrfToken = getCookie('csrftoken');

    // Clear All functionality
    clearAllButton.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent event propagation
        if (confirm('Are you sure you want to clear all search history?')) {
            fetch('/clear_all_search_history/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Include CSRF token
                    'Content-Type': 'application/json'
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Clear the search history list
                        document.getElementById('search-history-list').innerHTML = '';
                        // Hide the "Clear All" button
                        clearAllButton.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error clearing search history:', error);
                });
        }
    });

    // Individual delete functionality
    document.querySelectorAll('.delete-search').forEach(function (element) {
        element.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent event from bubbling up to the parent <li>
            event.preventDefault();  // Prevent default action (if any)
            const historyId = this.getAttribute('data-history-id');
            fetch(`/delete_search_history/${historyId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Include CSRF token
                    'Content-Type': 'application/json'
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        this.parentElement.remove(); // Remove the <li> element from the DOM
                        // Hide the "Clear All" button if no history items are left
                        if (document.getElementById('search-history-list').children.length === 0) {
                            clearAllButton.style.display = 'none';
                        }
                    }
                })
                .catch(error => {
                    console.error('Error deleting search history:', error);
                });
        });
    });

    // Clicking on a search history item triggers a new search
    document.querySelectorAll('.history-item').forEach(function (element) {
        element.addEventListener('click', function (event) {
            // Prevent the event from bubbling up if the delete button is clicked
            if (event.target.classList.contains('delete-search')) {
                return;
            }
            const query = this.getAttribute('data-query');
            if (query) {
                window.location.href = `/search?q=${encodeURIComponent(query)}`;
            }
        });
    });

    // Keyboard navigation for search history and suggestions
    let selectedIndex = -1;
    const historyItems = document.querySelectorAll('.history-item');
    const suggestionItems = document.querySelectorAll('.suggestion-item');

    searchInput.addEventListener('keydown', function (event) {
        const items = searchSuggestions.style.display === 'block' ? suggestionItems : historyItems;
        if (event.key === 'ArrowDown') {
            selectedIndex = (selectedIndex + 1) % items.length;
            items[selectedIndex].focus();
        } else if (event.key === 'ArrowUp') {
            selectedIndex = (selectedIndex - 1 + items.length) % items.length;
            items[selectedIndex].focus();
        } else if (event.key === 'Enter' && selectedIndex !== -1) {
            const selectedItem = items[selectedIndex];
            const query = selectedItem.getAttribute('data-query') || selectedItem.querySelector('.suggestion-name').textContent;
            searchInput.value = query;
            window.location.href = `/search/?q=${encodeURIComponent(query)}`;
        }
    });
});