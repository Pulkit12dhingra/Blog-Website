function loadContent(page) {
    fetch(`/${page}`)  // Calls Flask route dynamically
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => console.error('Error loading the page:', error));
}

// Load default content when page loads
window.onload = function() {
    loadContent('home'); // Loads home.html by default
};
