// DOM Elements
const generateBtn = document.getElementById('generate-btn');
const productDetails = document.getElementById('product-details');
const scriptSize = document.getElementById('script-size');
const loading = document.getElementById('loading');
const loadingMessage = document.getElementById('loading-message');
const scriptsOutput = document.getElementById('scripts-output');
const scriptTitle = document.getElementById('script-title');
const selectedScript = document.getElementById('selected-script');
const copyBtn = document.querySelector('.copy-btn');
const regenerateBtn = document.getElementById('regenerate-btn');
const starRating = document.querySelector('.star-rating');

// Event Listeners
generateBtn.addEventListener('click', handleGenerate);
copyBtn.addEventListener('click', handleCopy);
regenerateBtn.addEventListener('click', handleGenerate); // Reuse handleGenerate for regeneration
starRating.querySelectorAll('.star').forEach(star => star.addEventListener('click', handleStarRating));

// Generate Scripts
async function handleGenerate() {
    const details = productDetails.value.trim();
    const size = scriptSize.value;
    if (!details) {
        alert('Please enter product details.');
        return;
    }

    // Show loading state with quotes
    loading.classList.remove('hidden');
    scriptsOutput.classList.add('hidden');
    regenerateBtn.classList.add('hidden'); // Hide regenerate during loading

    const quotes = [
        'Creativity is intelligence having fun. – Albert Einstein',
        'Good things come to those who wait.',
        'The best scripts are worth the wait!',
        'Inspiration is on its way...'
    ];
    let quoteIndex = 0;
    loadingMessage.textContent = quotes[quoteIndex];
    const quoteInterval = setInterval(() => {
        quoteIndex = (quoteIndex + 1) % quotes.length;
        loadingMessage.textContent = quotes[quoteIndex];
    }, 2000);

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ details, size })
        });

        if (!response.ok) throw new Error('Failed to generate script');
        const data = await response.json();

        // Update UI with the selected script
        scriptTitle.textContent = `${size.charAt(0).toUpperCase() + size.slice(1)} Script (~${size === 'short' ? '120' : size === 'medium' ? '250' : '500'} words)`;
        selectedScript.textContent = data[size];
        scriptsOutput.classList.remove('hidden');
        regenerateBtn.classList.remove('hidden'); // Show regenerate button after generation
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        clearInterval(quoteInterval);
        loading.classList.add('hidden');
    }
}

// Copy to Clipboard
function handleCopy() {
    const text = selectedScript.textContent;
    navigator.clipboard.writeText(text)
        .then(() => alert('Script copied to clipboard!'))
        .catch(err => alert(`Failed to copy: ${err}`));
}

// Handle Star Rating
function handleStarRating(event) {
    const star = event.target;
    const ratingContainer = star.parentElement;
    const stars = ratingContainer.querySelectorAll('.star');
    const ratingValue = star.dataset.value;
    const scriptType = scriptSize.value; // Use selected size as script type

    // Fill stars up to the clicked one
    stars.forEach(s => {
        if (s.dataset.value <= ratingValue) {
            s.classList.add('active');
        } else {
            s.classList.remove('active');
        }
    });

    // Submit feedback
    fetch('/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rating: ratingValue, script_type: scriptType })
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to save feedback');
        alert('Thank you for your feedback!');
    })
    .catch(error => alert(`Error: ${error.message}`));
}