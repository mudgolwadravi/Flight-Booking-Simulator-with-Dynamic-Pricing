// document.getElementById('flightSearchForm').addEventListener('submit', async (e) => {
//     e.preventDefault();

//     const source = document.getElementById('source').value;
//     const destination = document.getElementById('destination').value;
//     const date = document.getElementById('date').value;

//     const response = await fetch(`/api/flights/search/?source=${source}&destination=${destination}&date=${date}`);
//     const data = await response.json();

//     const results = document.getElementById('flightResults');
//     results.innerHTML = '';

//     if (data.length === 0) {
//         results.innerHTML = `<p style="text-align:center;">No flights found. Try another route.</p>`;
//         return;
//     }

//     data.forEach(flight => {
//         const card = document.createElement('div');
//         card.classList.add('flight-card');
//         card.innerHTML = `
//             <h3>${flight.flight_number} - ${flight.airline}</h3>
//             <p><strong>From:</strong> ${flight.source} | <strong>To:</strong> ${flight.destination}</p>
//             <p><strong>Departure:</strong> ${flight.departure_time} | <strong>Arrival:</strong> ${flight.arrival_time}</p>
//             <p><strong>Price:</strong> ₹${flight.dynamic_price}</p>
//             <button class="search-btn" onclick="bookFlight(${flight.id})">Book Now</button>
//         `;
//         results.appendChild(card);
//     });
// });

// function bookFlight(flightId) {
//     alert(`Booking initiated for Flight ID: ${flightId}`);
// // }
// document.getElementById('flightSearchForm').addEventListener('submit', async (e) => {
//     e.preventDefault();

//     const source = document.getElementById('source').value;
//     const destination = document.getElementById('destination').value;
//     const date = document.getElementById('date').value;
//     const sort = document.getElementById('sort')?.value || 'price';

//     const results = document.getElementById('flightResults');
//     results.innerHTML = `<p style="text-align:center;">Searching for flights...</p>`;

//     try {
//         const response = await fetch(`/api/flights/search/?source=${encodeURIComponent(source)}&destination=${encodeURIComponent(destination)}&date=${encodeURIComponent(date)}&sort=${encodeURIComponent(sort)}`);
        
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }

//         const data = await response.json();
//         results.innerHTML = '';

//         if (data.length === 0) {
//             results.innerHTML = `<p style="text-align:center;">No flights found. Try another route.</p>`;
//             return;
//         }

//         data.forEach(flight => {
//             const card = document.createElement('div');
//             card.classList.add('flight-card');
//             card.innerHTML = `
//                 <h3>${flight.flight_number} - ${flight.airline}</h3>
//                 <p><strong>From:</strong> ${flight.source} | <strong>To:</strong> ${flight.destination}</p>
//                 <p><strong>Departure:</strong> ${flight.departure_time} | <strong>Arrival:</strong> ${flight.arrival_time}</p>
//                 <p><strong>Price:</strong> ₹${flight.dynamic_price}</p>
//                 <button class="search-btn" onclick="bookFlight(${flight.id})">Book Now</button>
//             `;
//             results.appendChild(card);
//         });
//     } catch (error) {
//         results.innerHTML = `<p style="text-align:center; color:red;">Error fetching flights. Please try again later.</p>`;
//         console.error('Flight search error:', error);
//     }
// });

// function bookFlight(flightId) {
//     alert(`Booking initiated for Flight ID: ${flightId}`);
// // }
// document.addEventListener("DOMContentLoaded", () => {
//   const form = document.getElementById("flightSearchForm");
//   const resultsDiv = document.getElementById("results") || document.getElementById("flightResults");
//   const errorBox = document.getElementById("errorBox");

//   form.addEventListener("submit", async (e) => {
//     e.preventDefault();
//     resultsDiv.innerHTML = `<p style="text-align:center;">Searching for flights...</p>`;
//     if (errorBox) errorBox.style.display = "none";

//     const origin = document.getElementById("origin")?.value.trim() || document.getElementById("source")?.value.trim();
//     const destination = document.getElementById("destination").value.trim();
//     const date = document.getElementById("date").value;
//     const sort = document.getElementById("sort")?.value || "price";

//     try {
//       const res = await fetch(`/api/flights/search/?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}&date=${encodeURIComponent(date)}&sort=${encodeURIComponent(sort)}`);
//       const data = await res.json();

//       if (!res.ok) {
//         const errorMsg = data.errors
//           ? Object.values(data.errors).join("<br>")
//           : data.message || "Something went wrong.";
//         showError(errorMsg);
//         return;
//       }

//       renderFlights(data.flights, data.sort_by);
//     } catch (err) {
//       showError("Network error. Please try again later.");
//       console.error("Flight search error:", err);
//     }
    
//   });

//   function showError(msg) {
//     if (errorBox) {
//       errorBox.innerHTML = msg;
//       errorBox.style.display = "block";
//     } else {
//       resultsDiv.innerHTML = `<p style="color:red; text-align:center;">${msg}</p>`;
//     }
//   }

//   function renderFlights(flights, sortBy) {
//     if (flights.length === 0) {
//       resultsDiv.innerHTML = "<p style='text-align:center;'>No flights found.</p>";
//       return;
//     }

//     resultsDiv.innerHTML = `<h3 style="text-align:center;">Showing ${flights.length} results (sorted by ${sortBy})</h3>`;
//     flights.forEach(f => {
//       const card = document.createElement("div");
//       card.classList.add("flight-card");
//       card.innerHTML = `
//         <h3>${f.flight_number} — ${f.airline || f.origin + " → " + f.destination}</h3>
//         <div class="flight-details">
//           <p><strong>From:</strong> ${f.origin} | <strong>To:</strong> ${f.destination}</p>
//           <p><strong>Departure:</strong> ${new Date(f.departure_time).toLocaleString()}</p>
//           <p><strong>Arrival:</strong> ${new Date(f.arrival_time).toLocaleString()}</p>
//           <p><strong>Duration:</strong> ${f.duration_hours} hrs</p>
//           <p><strong>Price:</strong> ₹${f.dynamic_price}</p>
//           <button class="search-btn" onclick="bookFlight(${f.id})">Book Now</button>
//         </div>
//       `;
//       resultsDiv.appendChild(card);
//     });
//   }

//   window.bookFlight = function(flightId) {
//     alert(`Booking initiated for Flight ID: ${flightId}`);
//   };
// });

// ===== Offers Carousel Auto Scroll =====
const carousel = document.querySelector('.offers-carousel');
let scrollAmount = 0;
let scrollStep = 2; // pixels per interval
let scrollDelay = 20; // milliseconds

function autoScrollCarousel() {
  scrollAmount += scrollStep;
  if (scrollAmount >= carousel.scrollWidth - carousel.clientWidth) {
    scrollAmount = 0; // reset scroll to start
  }
  carousel.scrollLeft = scrollAmount;
}

// Start auto-scrolling
setInterval(autoScrollCarousel, scrollDelay);

// ===== Smooth Scroll for Navbar Links (if using anchors) =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// ===== Hover Animation for Destination Cards =====
const destinationCards = document.querySelectorAll('.destination-card');

destinationCards.forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.style.transform = 'scale(1.05)';
    card.style.transition = 'transform 0.3s';
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'scale(1)';
  });
});
