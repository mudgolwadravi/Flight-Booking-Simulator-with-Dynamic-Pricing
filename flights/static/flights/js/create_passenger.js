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

document.getElementById('passenger-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    fetch('/api/passengers/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(response => {
        const messageDiv = document.getElementById('response-message');
        if (response.passenger_id) {
            messageDiv.innerHTML = `<p style="color:green;">${response.message} (ID: ${response.passenger_id})</p>`;
            e.target.reset();
        } else {
            messageDiv.innerHTML = `<p style="color:red;">${JSON.stringify(response)}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response-message').innerHTML = `<p style="color:red;">Something went wrong.</p>`;
    });
});
