function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.getElementById('cancel-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const pnr = document.getElementById('pnr-input').value.trim();
  if (!pnr) {
    alert("Please enter a valid PNR.");
    return;
  }

  fetch(`/api/bookings/${pnr}/`, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(res => res.json())
  .then(response => {
    const div = document.getElementById('cancel-response');
    if (response.message) {
      div.innerHTML = `<p style="color:green;">${response.message}<br>Seat ${response.cancelled_booking.seat_no} on Flight ${response.cancelled_booking.flight_id} has been released.</p>`;
    } else {
      div.innerHTML = `<p style="color:red;">${response.detail || "Cancellation failed."}</p>`;
    }
  })
  .catch(err => {
    console.error('Error:', err);
    document.getElementById('cancel-response').innerHTML = `<p style="color:red;">Something went wrong.</p>`;
  });
});
