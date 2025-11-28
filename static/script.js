document.addEventListener('DOMContentLoaded', () => {
    console.log('Ain’t all Risky Bizz App Loaded');
});

function toggleGuidance(id) {
    const element = document.getElementById(id);
    if (element.classList.contains('hidden')) {
        element.classList.remove('hidden');
    } else {
        element.classList.add('hidden');
    }
}

function fillVulnerability(value) {
    const input = document.getElementById('vulnerability');
    if (input) {
        input.value = value;
    }
}
