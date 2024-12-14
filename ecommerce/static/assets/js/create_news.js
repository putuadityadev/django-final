document.addEventListener('DOMContentLoaded', function() {
  const imageUploadInput = document.querySelector('.image-upload-input');
  const imageUploadContainer = document.querySelector('.image-upload-container');
  const imageUploadOverlay = document.querySelector('.image-upload-overlay');
  const imagePreviewContainer = document.querySelector('.image-preview-container');
  const imagePreview = document.querySelector('.image-preview');
  const imageRemoveBtn = document.querySelector('.image-remove-btn');

  // Drag and Drop
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      imageUploadContainer.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
      imageUploadContainer.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
      imageUploadContainer.addEventListener(eventName, unhighlight, false);
  });

  function highlight() {
      imageUploadContainer.classList.add('highlight');
  }

  function unhighlight() {
      imageUploadContainer.classList.remove('highlight');
  }

  imageUploadContainer.addEventListener('drop', handleDrop, false);

  function handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      handleFiles(files);
  }

  // File input change
  imageUploadInput.addEventListener('change', function(e) {
      handleFiles(this.files);
  });

  function handleFiles(files) {
      if (files.length > 0) {
          const file = files[0];
          
          // Validate file type and size
          const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
          const maxSize = 5 * 1024 * 1024; // 5MB

          if (!validTypes.includes(file.type)) {
              alert('Please upload a valid image (JPEG, PNG, WEBP)');
              return;
          }

          if (file.size > maxSize) {
              alert('File size exceeds 5MB limit');
              return;
          }

          const reader = new FileReader();
          reader.onload = function(event) {
              imagePreview.src = event.target.result;
              imageUploadOverlay.classList.add('d-none');
              imagePreviewContainer.classList.remove('d-none');
          }
          reader.readAsDataURL(file);
      }
  }

  imageRemoveBtn.addEventListener('click', function() {
      imageUploadInput.value = '';
      imagePreview.src = '';
      imageUploadOverlay.classList.remove('d-none');
      imagePreviewContainer.classList.add('d-none');
  });
});