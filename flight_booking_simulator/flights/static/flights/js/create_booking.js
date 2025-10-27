// Get CSRF Token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Toggle seat map visibility
document.getElementById("toggle-seat-map").addEventListener("click", () => {
  const seatMap = document.getElementById("seat-map");
  const isHidden = seatMap.hasAttribute("hidden");
  if (isHidden) {
    seatMap.removeAttribute("hidden");
    loadBookedSeats();
  } else {
    seatMap.setAttribute("hidden", true);
  }
});

// Load booked seats from backend
function loadBookedSeats() {
  const flightId = document.querySelector('input[name="flight_id"]').value;
  const travelDate = document.querySelector('input[name="travel_date"]').value;

  if (!flightId || !travelDate) return;

  fetch(`/api/booked-seats/?flight_id=${flightId}&travel_date=${travelDate}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        data.booked_seats.forEach((seat) => {
          const seatDiv = document.querySelector(`.seat[data-seat="${seat}"]`);
          if (seatDiv) {
            seatDiv.classList.add("unavailable");
            seatDiv.setAttribute("title", "Already booked");
          }
        });
      }
    })
    .catch((err) => console.error("Failed to load booked seats:", err));
}

// Seat selection logic
document.addEventListener("click", (event) => {
  const seat = event.target.closest(".seat");
  if (!seat || seat.classList.contains("unavailable") || seat.classList.contains("space")) return;

  document.querySelectorAll(".seat").forEach((s) => s.classList.remove("selected"));
  seat.classList.add("selected");
  document.getElementById("selected-seat").value = seat.dataset.seat;
});

// Submit booking form
document.getElementById("booking-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const selectedSeat = document.getElementById("selected-seat").value;
  if (!selectedSeat) {
    alert("Please select a seat before booking.");
    return;
  }

  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  fetch("/api/bookings/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((response) => {
      console.log(response);
      const messageDiv = document.getElementById("response-message");
      if (response.status === "success") {
        // Show booking details + download receipt button
        messageDiv.innerHTML = `
          <p style="color:lightgreen;">
            ${response.message}<br>
            PNR: ${response.pnr}<br>
            Price: ₹${response.final_price}
          </p>
          <a href="/booking/${response.booking_id}/receipt/" 
             target="_blank" 
             class="submit-btn" 
             style="margin-top:10px; display:inline-block;">
             📄 Download Receipt
          </a>
        `;
        e.target.reset();
        document.querySelectorAll(".seat").forEach((s) => s.classList.remove("selected"));
        document.getElementById("seat-map").setAttribute("hidden", true);
      } else {
        messageDiv.innerHTML = `<p style="color:red;">${response.message || JSON.stringify(response)}</p>`;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("response-message").innerHTML = `<p style="color:red;">Something went wrong.</p>`;
    });
});
