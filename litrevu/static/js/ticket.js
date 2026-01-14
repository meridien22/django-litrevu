// gestion de l'aperçu de l'image quand on la met à jour

const inputImage = document.getElementById('id_image');
const previewImage = document.querySelector('img')

function updatePreviewImage() {
    if (this.files && this.files[0]) {
        const urlTemporaire = URL.createObjectURL(this.files[0]);
        previewImage.src = urlTemporaire;
    }
}

if (inputImage) {
    inputImage.addEventListener('change', updatePreviewImage);
}

// gestion du focus

const focusElement = document.getElementById('id_title');
focusElement.focus();