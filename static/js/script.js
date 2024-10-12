const form = document.getElementById('obesityForm');
const resultsSection = document.getElementById('results');
const obesityCategory = document.getElementById('obesityCategory');

const medicalAdvice = document.getElementById('medicalAdvice');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from refreshing the page
    
    let formData = new FormData(this);
    
    // Sending form data to Flask using fetch API (AJAX)
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())  // Expecting JSON response from Flask
    .then(data => {
        // Display the result inside the 'result' div
        document.getElementById('formdata').innerHTML = `
            <h3 class="text-xl font-semibold">Form Data Submitted</h3>
            <ul>
                ${Object.entries(data).map(([key, value]) => `<li><strong>${key}:</strong> ${value}</li>`).join('')}
            </ul>
        `;
        resultsSection.classList.toggle("hidden")
    })

    .catch(error => console.error('Error:', error));
});