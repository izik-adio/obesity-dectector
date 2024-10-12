const form = document.getElementById('obesityForm');
const resultsSection = document.getElementById('results');
const obesityCategory = document.getElementById('obesityCategory');
const formSection = document.getElementById('formSection')
const medicalAdvice = document.getElementById('medicalAdvice');
const reference = document.getElementById('reference');
const innerLink = document.getElementById('reference_link');


console.log(innerLink)

// Function to populate the results section
function populateResults(response) {
    // Update the obesity category
    obesityCategory.innerHTML = response.obesityCategory;
    
    // Update the medical advice
    medicalAdvice.innerText = response.advice;

    const urlRegex = /(?:https?:\/\/)?[\w.-]+(?:\.[\w.-]+)*\/[\w&\?\-\+\.#\/=]*$/;
    const text = response.reference
    const match = urlRegex.exec(text);
    const contentBeforeLink = text.substring(0, match.index);
    const link = match[0];
    // Update the reference link
    reference.innerText = contentBeforeLink;
    innerLink.href = link;
    innerLink.innerText = link;
    
    // Make the results section visible
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
    .then(response => response.json())  // Expecting JSON response from Flask
    .then(data => {
        populateResults(data);
        formSection.classList.add('hidden')
    }).catch(error => console.error('Error:', error));
});
