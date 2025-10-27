document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/flights/')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('flight-body');
            data.forEach(flight => {
                const departure = new Date(flight.departure_time);
                const arrival = new Date(flight.arrival_time);

                // Format times to readable strings
                const options = {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: true,
                    timeZone: 'Asia/Kolkata'
                };
                const formattedDeparture = departure.toLocaleString('en-IN', options);
                const formattedArrival = arrival.toLocaleString('en-IN', options);

                // Calculate duration
                const diffMs = arrival - departure;
                const diffMins = Math.floor(diffMs / 60000);
                const hours = Math.floor(diffMins / 60);
                const minutes = diffMins % 60;
                const duration = `${hours}h ${minutes}m`;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${flight.flight_id}</td>
                    <td>${flight.origin}</td>
                    <td>${flight.destination}</td>
                    <td>${formattedDeparture}</td>
                    <td>${formattedArrival}</td>
                    <td>${duration}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching flights:', error);
        });
});
