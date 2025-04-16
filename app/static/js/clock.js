  // Auto-show toast
  const toastElList = [].slice.call(document.querySelectorAll('.toast'));
  toastElList.map(function (toastEl) {
    new bootstrap.Toast(toastEl).show();
  });

  // Real-Time Clock Update
  function updateClock() {
    const clock = document.getElementById('clock');
    const now = new Date();
    clock.innerText = now.toLocaleTimeString();
    console.log("Clock updated:", now.toLocaleTimeString()); // Log to console for debugging
  }
  
  setInterval(updateClock, 1000);
  updateClock();

