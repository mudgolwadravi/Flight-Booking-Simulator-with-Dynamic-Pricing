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

    // Show loading spinner
    const loader = document.createElement("div");
    loader.className = "loader";
    loader.innerHTML = "<p>🔄 Searching flights...</p>";
    resultsDiv.appendChild(loader);

    try {
      const res = await fetch(
        `/api/flights/search/?origin=${origin}&destination=${destination}&date=${date}&sort=${sort}`
      );
      const data = await res.json();
      loader.remove();

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
      loader.remove();
      showError("Network error. Please try again later.");
      console.error(err);
    }
  });

  function showError(msg) {
    errorBox.innerHTML = `<strong>Error:</strong> ${msg} <button onclick="this.parentElement.style.display='none'">✖</button>`;
    errorBox.style.display = "block";
  }

  function renderFlights(flights, sortBy) {
    if (flights.length === 0) {
      resultsDiv.innerHTML = "<p>No flights found.</p>";
      return;
    }

    resultsDiv.innerHTML = `<h3>Showing ${flights.length} results (sorted by ${sortBy})</h3>`;

    const cheapest = Math.min(...flights.map(f => f.dynamic_price));

    flights.forEach((f) => {
      const flightId = f.flight_id ?? f.id ?? "N/A";
      const isCheapest = f.dynamic_price === cheapest;
      const badge = isCheapest ? `<span class="badge">Best Price</span>` : "";

      const card = document.createElement("div");
      card.classList.add("flight-card");

      card.innerHTML = `
        <h3>Flight ID: ${flightId} — ${f.origin} → ${f.destination} ${badge}</h3>
        <div class="flight-details">
          <p>⏱ Departure: ${new Date(f.departure_time).toLocaleString()}</p>
          <p>⏱ Arrival: ${new Date(f.arrival_time).toLocaleString()}</p>
          <p>⏱ Duration: ${f.duration_hours} hrs</p>
          <p>💰 Total Fare: <strong>₹${f.dynamic_price}</strong></p>
        </div>
        <a href="#" class="btn book-btn" data-id="${flightId}">✈️ Book Flight</a>
      `;

      resultsDiv.appendChild(card);
    });

    document.querySelectorAll(".book-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const button = e.target.closest(".book-btn");
        const flightId = button?.dataset?.id;

        if (flightId && flightId !== "N/A") {
          window.location.href = `/bookings-page/${flightId}/`;
        } else {
          alert("Invalid flight ID. Cannot proceed with booking.");
        }
      });
    });
  }
});
