// Function to fetch the latest events from the API
function fetchLatestEvents() {
    fetch('/api/v1/latest-events')  // API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();  // Parse the JSON data
        })
        .then(data => {
            // Clear the current events list
            const eventsList = document.getElementById('eventsList');
            eventsList.innerHTML = '';  // Empty the current content

            // If there are no events, display a message
            if (Array.isArray(data.messages)) {
                if (data.messages.length === 0) {
                    eventsList.innerHTML = '<div class="event-row">No events found.</div>';
                } else {
                    // Display each event as a row
                    data.messages.forEach(function (message) {
                        const row = document.createElement('div');
                        row.classList.add('event-row');
                        row.textContent = message;
                        eventsList.appendChild(row);
                    });
                }
            } else {
                // Display error message if no messages returned
                eventsList.innerHTML = '<div class="event-row">Error fetching events. Please try again later.</div>';
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Handle error (e.g., network failure)
            const eventsList = document.getElementById('eventsList');
            eventsList.innerHTML = '<div class="event-row">Error fetching events. Please try again later.</div>';
        });
}

// Fetch the latest events immediately when the page loads
fetchLatestEvents();

// Set interval to fetch the latest events every 15 seconds (15000 ms)
setInterval(fetchLatestEvents, 15000);
