// gestion de la notation avec les étoiles

const container_label = document.getElementById('id_review-rating');

function updateRating() {
    let labels = container_label.querySelectorAll('label');
    let checkedInput = container_label.querySelector('input[type="radio"]:checked');
    let checkedValue = checkedInput ? parseInt(checkedInput.value) : -1;

    for (let i = 0; i < labels.length; i++) {
        let label = labels[i]
        const input = label.querySelector('input[type="radio"]');
        const val = parseInt(input.value);
        if (val <= checkedValue && checkedValue !== -1) {
            label.classList.add('rating_active');
        } else {
            label.classList.remove('rating_active');
        }
    }
}

if (container_label) {
    updateRating();
    container_label.addEventListener('change', updateRating);
}


// gestion du focus

const focusElement1 = document.getElementById('id_review-headline');
const focusElement2 = document.getElementById('id_ticket-title');
focusElement1.focus();
if (focusElement2) {
    focusElement2.focus();
}