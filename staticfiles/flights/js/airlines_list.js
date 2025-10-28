document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/flights/airlines/')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('airlines-list');
            list.innerHTML = ''; // Clear loading message

            if (data.length === 0) {
                list.innerHTML = '<li>No airlines found.</li>';
                return;
            }

            data.forEach(airline => {
                const li = document.createElement('li');
                li.textContent = `${airline.name} (Code: ${airline.flight_id})`;
                list.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching airlines:', error);
            document.getElementById('airlines-list').innerHTML = '<li>Error loading airlines.</li>';
        });
});
