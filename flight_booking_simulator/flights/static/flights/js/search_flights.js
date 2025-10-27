document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("flightSearchForm");
  const resultsDiv = document.getElementById("results");
  const errorBox = document.getElementById("errorBox");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    resultsDiv.innerHTML = "";
    errorBox.style.display = "none";

    const origin = document.getElementById("origin").value.trim();
    const destination = document.getElementById("destination").value.trim();
    const date = document.getElementById("date").value;
    const sort = document.getElementById("sort").value;

    try {
      const res = await fetch(`/api/flights/search/?origin=${origin}&destination=${destination}&date=${date}&sort=${sort}`);
      const data = await res.json();

      if (!res.ok) {
        const errorMsg = data.errors
          ? Object.values(data.errors).join("<br>")
          : data.message || "Something went wrong.";
        showError(errorMsg);
        return;
      }

      if (!Array.isArray(data.flights)) {
        showError("Invalid flight data format.");
        return;
      }

      renderFlights(data.flights, data.sort_by);
    } catch (err) {
      showError("Network error. Please try again later.");
      console.error(err);
    }
  });

  function showError(msg) {
    errorBox.innerHTML = msg;
    errorBox.style.display = "block";
  }

  function renderFlights(flights, sortBy) {
    if (flights.length === 0) {
      resultsDiv.innerHTML = "<p>No flights found.</p>";
      return;
    }

    resultsDiv.innerHTML = `<h3>Showing ${flights.length} results (sorted by ${sortBy})</h3>`;

    flights.forEach(f => {
      const flightId = f.flight_id ?? f.id ?? "N/A";

      const card = document.createElement("div");
      card.classList.add("flight-card");
      card.innerHTML = `
        <h3>Flight ID: ${flightId}— ${f.origin} → ${f.destination}</h3>
        <div class="flight-details">
          <p>Departure: ${new Date(f.departure_time).toLocaleString()}</p>
          <p>Arrival: ${new Date(f.arrival_time).toLocaleString()}</p>
          <p>Duration: ${f.duration_hours} hrs</p>
          <p><strong>₹${f.dynamic_price}</strong></p>
        </div>
        
        <a href="/bookings-page/${flightId}/" class="btn book-btn">✈️ Book Flight</a>

      `;
      resultsDiv.appendChild(card);
    });

    // Add click listeners for Book Flight buttons
    document.querySelectorAll(".book-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const flightId = e.target.dataset.id;
        if (flightId && flightId !== "N/A") {
          window.location.href = '/bookings-page/${flightId}/';
        } else {
          alert("Invalid flight ID. Cannot proceed with booking.");
        }
      });
    });
  }
});
