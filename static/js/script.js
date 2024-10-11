const form = document.getElementById('obesityForm');
const resultsSection = document.getElementById('results');
const obesityCategory = document.getElementById('obesityCategory');

const medicalAdvice = document.getElementById('medicalAdvice');

form.addEventListener('submit', function (event) {
    event.preventDefault();

    // Simulating model response
    const randomCategory = ['Normal Weight', 'Overweight Level I', 'Obesity Type I'][Math.floor(Math.random() * 3)];
    const advice = {
        'Normal Weight': 'Maintain a balanced diet and regular exercise to keep your weight in check.',
        'Overweight Level I': 'Consider reducing caloric intake and increasing physical activity.',
        'Obesity Type I': 'Seek professional medical advice to manage your weight effectively.'
    };

    // Display the results
    obesityCategory.textContent = `You fall into the category of: ${randomCategory}`;
    medicalAdvice.textContent = `Medical advice: ${advice[randomCategory]}`;
    resultsSection.classList.remove('hidden');
});