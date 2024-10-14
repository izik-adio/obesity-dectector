const form = document.getElementById('obesityForm');
const resultsSection = document.getElementById('results');
const obesityCategory = document.getElementById('obesityCategory');
const formSection = document.getElementById('formSection')
const medicalAdvice = document.getElementById('medicalAdvice');
const reference = document.getElementById('reference');
const innerLink = document.getElementById('reference_link');


// Function to populate the results section
function populateResults(data) {
    // Continue with updating the UI
    obesityCategory.innerHTML = data["obesityCategory"];
    medicalAdvice.innerHTML = data["advice"];
    reference.innerHTML = data["reference"];
    innerLink.href = data["reference_link"];
    innerLink.innerHTML = data["reference_link"];
    resultsSection.classList.remove('hidden');
}


form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from refreshing the page
    
    let formData = new FormData(this);
    
    // Sending form data to Flask using fetch API (AJAX)
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        populateResults(JSON.parse(data));
        formSection.classList.add('hidden')
    }).catch(error => console.error('Error:', error));
});
