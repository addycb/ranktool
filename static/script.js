function copyLinkToClipboard() {
    const text = document.getElementById('copyText').innerText.split(': ')[1];
    navigator.clipboard.writeText(text).then(() => {
        const feedback = document.getElementById('feedback');
        feedback.style.opacity = 1;
        setTimeout(() => {
            feedback.style.opacity = 0;
        }, 2000); // Hide the feedback message after 2 seconds
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}
