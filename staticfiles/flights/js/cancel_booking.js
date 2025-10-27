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

document.getElementById("cancel-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const pnr = document.getElementById("pnr-input").value.trim();
  const responseDiv = document.getElementById("cancel-response");
  responseDiv.innerHTML = "";

  if (!pnr) {
    responseDiv.innerHTML = `<p class="error-msg">⚠️ Please enter a valid PNR.</p>`;
    return;
  }

  fetch(`/api/bookings/${pnr}/`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((res) => res.json())
    .then((response) => {
      if (response.message) {
        responseDiv.innerHTML = `
          <div class="success-card">
            <h3>✅ Booking Cancelled Successfully</h3>
            <p><strong>PNR:</strong> ${response.cancelled_booking.pnr}</p>
            <p><strong>Flight ID:</strong> ${response.cancelled_booking.flight_id}</p>
            <p><strong>Seat No:</strong> ${response.cancelled_booking.seat_no}</p>
            <p><strong>Travel Date:</strong> ${response.cancelled_booking.travel_date}</p>
            <p class="info-msg">📩 SMS notification sent to your registered mobile number.</p>
          </div>`;
      } else {
        responseDiv.innerHTML = `<p class="error-msg">❌ ${response.detail || "Cancellation failed."}</p>`;
      }
    })
    .catch((err) => {
      console.error("Error:", err);
      responseDiv.innerHTML = `<p class="error-msg">❌ Something went wrong. Please try again later.</p>`;
    });
});
