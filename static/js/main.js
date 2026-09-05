/**
 * Harborlight Multispecialty Hospital
 * Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Harborlight Multispecialty Hospital website loaded successfully.');

    // Auto-dismiss alerts if present
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
});

