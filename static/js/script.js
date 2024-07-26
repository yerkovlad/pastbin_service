function copyToClipboard() {
    const urlField = document.getElementById('message-url');
    urlField.select();
    document.execCommand('copy');

    // Show notification
    const notification = document.getElementById('notification');
    notification.classList.add('show');

    // Hide notification after 2 seconds
    setTimeout(() => {
        notification.classList.remove('show');
    }, 2000);
}