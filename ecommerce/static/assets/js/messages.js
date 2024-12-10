document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
      var alerts = document.querySelectorAll('.messages-overlay .alert');
      alerts.forEach(function(alert) {
          var bsAlert = new bootstrap.Alert(alert);
          bsAlert.close();
      });
  }, 5000);
});