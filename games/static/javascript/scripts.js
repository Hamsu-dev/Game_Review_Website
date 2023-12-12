document.addEventListener("DOMContentLoaded", function() {
  const dropdownButton = document.querySelector(".dropdown-btn");
  const dropdownContent = document.querySelector(".dropdown-content");
  const container = document.querySelector(".navbar"); // Parent container of the navbar

  dropdownButton.addEventListener("click", function() {
      container.classList.toggle("active");
  });

  document.addEventListener("click", function(event) {
      if (!dropdownButton.contains(event.target)) {
          container.classList.remove("active");
      }
  });
});

function openImageUpload() {
  document.getElementById('image-upload').click();
}

function displayImage(input) {
  const file = input.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
      document.getElementById('banner-image').src = e.target.result;
  };

  reader.readAsDataURL(file);
}

function openBioEditor() {
  const bioContent = document.getElementById('bio-content').innerHTML;
  const bioEditor = document.getElementById('bio-editor');
  const saveButton = document.getElementById('save-bio-button');

  bioEditor.style.display = 'block';
  bioEditor.value = bioContent;
  saveButton.style.display = 'block';
}

function saveBio() {
  const newBioContent = document.getElementById('bio-editor').value;
  const bioContent = document.getElementById('bio-content');

  // Update the displayed bio content
  bioContent.innerHTML = `<p>${newBioContent}</p>`;

  // Hide the bio editor and save button
  document.getElementById('bio-editor').style.display = 'none';
  document.getElementById('save-bio-button').style.display = 'none';
}