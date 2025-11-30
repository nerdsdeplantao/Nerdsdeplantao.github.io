document.addEventListener('DOMContentLoaded', function() {
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarCollapse && sidebar) {
        sidebarCollapse.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        document.addEventListener('click', function(e) {
            if (window.innerWidth < 992) {
                if (!sidebar.contains(e.target) && !sidebarCollapse.contains(e.target)) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }
    
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    const deleteButtons = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteButtons.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const message = form.getAttribute('onsubmit').match(/confirm\('([^']+)'\)/);
            if (message && !confirm(message[1])) {
                e.preventDefault();
            }
        });
    });
    
    const tooltips = document.querySelectorAll('[title]');
    tooltips.forEach(function(el) {
        if (el.classList.contains('btn') || el.classList.contains('btn-sm')) {
            new bootstrap.Tooltip(el);
        }
    });
});

function markVideoComplete(videoId) {
    const form = document.querySelector('.mark-complete-form');
    if (form) {
        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(new FormData(form))
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const button = form.querySelector('button');
                if (data.completed) {
                    button.classList.remove('btn-outline-success');
                    button.classList.add('btn-success');
                    button.innerHTML = '<i class="fas fa-check me-2"></i>Concluído';
                } else {
                    button.classList.remove('btn-success');
                    button.classList.add('btn-outline-success');
                    button.innerHTML = '<i class="fas fa-check me-2"></i>Marcar como Concluído';
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }
}
