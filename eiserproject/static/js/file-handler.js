//Image-Preview:
function previewImage(event) {
    const fileInput = document.getElementById("photo-upload");
    const previewImage = document.getElementById("photo-preview");
    const placeholderText = document.getElementById("placeholder-text");
    const file = fileInput.files[0];
  
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        previewImage.src = e.target.result;
        previewImage.style.display = "block";
        placeholderText.textContent = file.name;
      };
      reader.readAsDataURL(file);
    }
}

// Seller-Documents:
function previewDoc(event) {
    const fileInput = event.target; // Get the input element that triggered the event
    const file = fileInput.files[0]; // Get the uploaded file
    let placeholderText;

    // Determine which input triggered the event and find the corresponding placeholder
    if (fileInput.id === "document-upload-lic") {
        placeholderText = document.getElementById("placeholder-text-lic");
    } else if (fileInput.id === "document-upload-id") {
        placeholderText = document.getElementById("placeholder-text-id");
    }

    if (file && placeholderText) {
        // Update the placeholder text with the file name
        placeholderText.textContent = file.name;
    }
}


// Trigger file input when "Edit Photo" is clicked (profile/seller-profile)
document.getElementById('change-photo-btn').addEventListener('click', function() {
    document.getElementById('profile-img-edit').click();
});

// Preview the uploaded image
document.getElementById('profile-img-edit').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-img').src = e.target.result;
            document.getElementById('delete-photo-btn').style.display = 'inline-block';
        };
        reader.readAsDataURL(file);
    }
});

// Reset to default image when "Delete Photo" is clicked
document.getElementById('delete-photo-btn').addEventListener('click', function() {
    document.getElementById('profile-img').src = "{% static 'img/default-profile.png' %}";
    document.getElementById('delete-photo-btn').style.display = 'none';
});