function switchTab(tabId) {
    document.querySelectorAll('.form-tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[onclick="switchTab('${tabId}')"]`).classList.add('active');
  }

  function togglePasswordVisibility() {
    const passField = document.getElementById('loginPass');
    passField.type = passField.type === 'password' ? 'text' : 'password';
  }

  function toggleSignupPasswordVisibility() {
    const passField = document.getElementById('signupPass');
    passField.type = passField.type === 'password' ? 'text' : 'password';

  }
  function toggleConfirmPasswordVisibility() {
    const passField = document.getElementById('confirmPass');
    passField.type = passField.type === 'password' ? 'text' : 'password';
  }

  // Initialize Particles.js
  particlesJS("particles-js", {
    particles: {
      number: {
        value: 80,
        density: {
          enable: true,
          value_area: 800
        }
      },
      color: {
        value: "#0ff"
      },
      shape: {
        type: "circle",
        stroke: {
          width: 0,
          color: "#000"
        },
        polygon: {
          nb_sides: 5
        }
      },
      opacity: {
        value: 0.5,
        random: true,
        anim: {
          enable: true,
          speed: 1,
          opacity_min: 0.1,
          sync: false
        }
      },
      size: {
        value: 3,
        random: true,
        anim: {
          enable: true,
          speed: 4,
          size_min: 0.1,
          sync: false
        }
      },
      line_linked: {
        enable: true,
        distance: 150,
        color: "#0ff",
        opacity: 0.4,
        width: 1
      },
      move: {
        enable: true,
        speed: 6,
        direction: "none",
        random: false,
        straight: false,
        out_mode: "out",
        bounce: false,
        attract: {
          enable: false
        }
      }
    },
    interactivity: {
      detect_on: "canvas",
      events: {
        onhover: {
          enable: true,
          mode: "repulse"
        },
        onclick: {
          enable: true,
          mode: "push"
        }
      },
      modes: {
        repulse: {
          distance: 100,
          duration: 0.4
        },
        push: {
          particles_nb: 4
        }
      }
    },
    retina_detect: true
  });


 