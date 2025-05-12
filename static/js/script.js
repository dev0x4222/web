function LoginWithReplit() {
    window.addEventListener("message", authComplete);
    var h = 500;
    var w = 350;
    var left = screen.width / 2 - w / 2;
    var top = screen.height / 2 - h / 2;

    var authWindow = window.open(
        "https://replit.com/auth_with_repl_site?domain=" + location.host,
        "_blank",
        "modal=yes, toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=" +
        w +
        ", height=" +
        h +
        ", top=" +
        top +
        ", left=" +
        left
    );

    function authComplete(e) {
        if (e.data !== "auth_complete") {
            return;
        }
        window.removeEventListener("message", authComplete);
        authWindow.close();
        location.reload();
    }
}

// Main JavaScript file for Dev0x4 AOV Tool - Web Edition
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function(popoverTriggerEl) {
        new bootstrap.Popover(popoverTriggerEl);
    });

    // Theme toggle function
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            if (currentTheme === 'dark') {
                document.documentElement.setAttribute('data-bs-theme', 'light');
                themeIcon.classList.remove('bi-moon-fill');
                themeIcon.classList.add('bi-sun-fill');
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.setAttribute('data-bs-theme', 'dark');
                themeIcon.classList.remove('bi-sun-fill');
                themeIcon.classList.add('bi-moon-fill');
                localStorage.setItem('theme', 'dark');
            }
        });
    }

    // Apply saved theme on page load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
        if (themeIcon) {
            if (savedTheme === 'light') {
                themeIcon.classList.remove('bi-moon-fill');
                themeIcon.classList.add('bi-sun-fill');
            } else {
                themeIcon.classList.remove('bi-sun-fill');
                themeIcon.classList.add('bi-moon-fill');
            }
        }
    }

    // Auto-dismiss flash messages after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-dismissible)');
        alerts.forEach(function(alert) {
            if (alert && bootstrap.Alert.getInstance(alert)) {
                bootstrap.Alert.getInstance(alert).close();
            }
        });
    }, 5000);

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Scroll to active nav item
    const activeNavItem = document.querySelector('.nav-link.active');
    if (activeNavItem) {
        activeNavItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // Display current time in the footer
    const currentTimeElement = document.getElementById('currentTime');
    if (currentTimeElement) {
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleTimeString();
            currentTimeElement.textContent = timeString;
        }
        
        updateTime();
        setInterval(updateTime, 1000);
    }

    // Handle login button click
    var loginButtons = document.querySelectorAll('[onclick="LoginWithReplit()"]');
    loginButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            LoginWithReplit();
        });
    });
});

// Handle download with loading animation
function handleDownload(event, button) {
    event.preventDefault();
    const downloadUrl = button.href;
    const downloadContent = button.querySelector('.download-content');
    const progressContainer = button.querySelector('.progress-bar-container');
    const progressBar = button.querySelector('.progress-bar');
    
    // Show loading animation
    downloadContent.style.opacity = '0.5';
    button.classList.add('disabled');
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    
    // Animate progress bar
    setTimeout(() => {
        progressBar.style.width = '100%';
    }, 100);
    
    // Start download after animation
    setTimeout(() => {
        window.location.href = downloadUrl;
        
        // Reset button state
        setTimeout(() => {
            downloadContent.style.opacity = '1';
            button.classList.remove('disabled');
            progressContainer.style.display = 'none';
            progressBar.style.width = '0%';
        }, 500);
    }, 3000);
}