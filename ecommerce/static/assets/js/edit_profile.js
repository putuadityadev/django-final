document.addEventListener('DOMContentLoaded', function() {
  const profilePictureInput = document.querySelector('.profile-picture-upload-input');
  const currentProfilePicture = document.querySelector('.current-profile-picture');
  const imagePreviewContainer = document.querySelector('.image-preview-container');
  const imagePreview = document.querySelector('.image-preview');
  const imageRemoveBtn = document.querySelector('.image-remove-btn');

  profilePictureInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
          const reader = new FileReader();
          reader.onload = function(event) {
              imagePreview.src = event.target.result;
              imagePreviewContainer.class .remove('d-none');
              currentProfilePicture.src = event.target.result; // Update current profile picture
          }
          reader.readAsDataURL(file);
      }
  });

  imageRemoveBtn.addEventListener('click', function() {
      profilePictureInput.value = '';
      imagePreview.src = '';
      currentProfilePicture.src = "{{ request.user.profile.profile_picture.url }}"; // Reset to current picture
      imagePreviewContainer.classList.add('d-none');
  });
});