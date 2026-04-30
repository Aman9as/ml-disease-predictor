document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const predictBtn = document.getElementById('predict-btn');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('result-container');
    const predictionText = document.getElementById('prediction-text');
    const errorContainer = document.getElementById('error-container');
    const errorText = document.getElementById('error-text');
    const resetBtn = document.getElementById('reset-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Collect selected symptoms
        const selectedSymptoms = Array.from(document.querySelectorAll('input[name="symptoms"]:checked'))
                                      .map(cb => cb.value);

        // 2. Validation: Check if at least one symptom is selected
        if (selectedSymptoms.length === 0) {
            showError('Please select at least one symptom.');
            return;
        }

        // 3. Prepare UI for loading
        hideError();
        resultContainer.classList.add('hidden');
        loader.classList.remove('hidden');
        predictBtn.disabled = true;

        try {
            // 4. Send POST request to backend
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms: selectedSymptoms }),
            });

            const data = await response.json();

            if (response.ok) {
                // 5. Success: Display prediction
                predictionText.textContent = data.prediction;
                resultContainer.classList.remove('hidden');
                // Scroll to result
                resultContainer.scrollIntoView({ behavior: 'smooth' });
            } else {
                // 6. Backend error
                showError(data.error || 'Something went wrong on the server.');
            }
        } catch (error) {
            // 7. Network/Client error
            showError('Unable to connect to the server. Please try again later.');
            console.error('Prediction Error:', error);
        } finally {
            // 8. Cleanup UI
            loader.classList.add('hidden');
            predictBtn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        form.reset();
        resultContainer.classList.add('hidden');
        hideError();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    function showError(message) {
        errorText.textContent = message;
        errorContainer.classList.remove('hidden');
        errorContainer.scrollIntoView({ behavior: 'smooth' });
    }

    function hideError() {
        errorContainer.classList.add('hidden');
    }
});
