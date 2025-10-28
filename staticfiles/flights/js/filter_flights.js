document.getElementById('filter-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const form = e.target;
    const maxPrice = form.max_price.value;
    const directOnly = form.direct_only.checked;
    const airlineName = form.airline_name.value;

    const query = new URLSearchParams({
        max_price: maxPrice,
        direct_only: directOnly,
        airline_name: airlineName
    });

    fetch(`/api/flights/filter/?${query}`)
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('results-body');
            tbody.innerHTML = '';

            const filters = data.filters_applied;
            document.getElementById('filters-applied').innerHTML = `
                <p><strong>Filters Applied:</strong> Max Price = ₹${filters.max_price}, Direct Only = ${filters.direct_only}, Airline = ${filters.airline_name}</p>
            `;

            data.results.forEach(flight => {
                const dep = new Date(flight.departure_time);
                const arr = new Date(flight.arrival_time);
                const durationMs = arr - dep;
                const mins = Math.floor(durationMs / 60000);
                const hours = Math.floor(mins / 60);
                const duration = `${hours}h ${mins % 60}m`;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${flight.flight_id}</td>
                    <td>${flight.airline_name}</td>
                    <td>${flight.origin}</td>
                    <td>${flight.destination}</td>
                    <td>${dep.toLocaleString('en-IN', { hour: '2-digit', minute: '2-digit', day: 'numeric', month: 'short', year: 'numeric', hour12: true, timeZone: 'Asia/Kolkata' })}</td>
                    <td>${arr.toLocaleString('en-IN', { hour: '2-digit', minute: '2-digit', day: 'numeric', month: 'short', year: 'numeric', hour12: true, timeZone: 'Asia/Kolkata' })}</td>
                    <td>${duration}</td>
                    <td>₹${flight.base_price}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(err => {
            console.error('Error fetching filtered flights:', err);
        });
});
