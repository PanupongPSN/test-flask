jQuery(document).ready(function($) {
    // Event listener for the form submission
    $('#sapForm').on('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting the traditional way

        var fileInput = $('#sapImage')[0];
        if (fileInput.files.length === 0) {
            alert('Please upload an image of the acne-affected area.');
            return;
        }

        var formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // Display the uploaded image
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#uploadedImage').attr('src', e.target.result).show();
            $('#analyzingMessage').text('Analyzing the image...');
        };
        reader.readAsDataURL(fileInput.files[0]);

        // Send AJAX request to Flask API
        $.ajax({
            url: 'http://127.0.0.1:5000/predict', // URL ของ Flask API ที่ต้องรันอยู่ใน LocalWP
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Display prediction result
                var predictedClass = response.prediction;
                var confidence = response.confidence;

                $('#analyzingMessage').text('');
                $('#result').text(`Prediction: ${predictedClass} with a confidence of ${confidence.toFixed(2)}%`);
            },
            error: function(xhr, status, error) {
                $('#analyzingMessage').text('');
                $('#result').text('Error: ' + error);
            }
        });
    });
});
