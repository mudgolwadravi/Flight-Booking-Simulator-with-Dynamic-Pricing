document.addEventListener('DOMContentLoaded', () => {
    fetch(`/api/flights/${flightId}/`)
        .then(response => response.json())
        .then(flight => {
            const container = document.getElementById('flight-info');

            if (flight.error) {
                container.innerHTML = `<p style="color:red;">${flight.error}</p>`;
                return;
            }

            const departure = new Date(flight.departure_time);
            const arrival = new Date(flight.arrival_time);
            const options = {
                year: 'numeric', month: 'short', day: 'numeric',
                hour: '2-digit', minute: '2-digit', hour12: true,
                timeZone: 'Asia/Kolkata'
            };
            const formattedDeparture = departure.toLocaleString('en-IN', options);
            const formattedArrival = arrival.toLocaleString('en-IN', options);

            const durationMs = arrival - departure;
            const mins = Math.floor(durationMs / 60000);
            const hours = Math.floor(mins / 60);
            const duration = `${hours}h ${mins % 60}m`;

            container.innerHTML = `
                <p><strong>Flight ID:</strong> ${flight.flight_id}</p>
                <p><strong>Airline:</strong> ${flight.airline_name}</p>
                <p><strong>Origin:</strong> ${flight.origin}</p>
                <p><strong>Destination:</strong> ${flight.destination}</p>
                <p><strong>Departure:</strong> ${formattedDeparture}</p>
                <p><strong>Arrival:</strong> ${formattedArrival}</p>
                <p><strong>Duration:</strong> ${duration}</p>
                <p><strong>Total Seats:</strong> ${flight.total_seats}</p>
                <p><strong>Available Seats:</strong> ${flight.available_seats}</p>
                <p><strong>Base Price:</strong> ₹${flight.base_price}</p>
                <p><strong>Tier:</strong> ${flight.airline_tier}</p>
                <p><strong>Demand Level:</strong> ${flight.demand_level}</p>
            `;
        })
        .catch(error => {
            document.getElementById('flight-info').innerHTML = `<p style="color:red;">Error loading flight data.</p>`;
            console.error('Fetch error:', error);
        });
});
