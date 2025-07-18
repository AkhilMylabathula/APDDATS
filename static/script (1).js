function toggleMenu() {
  const navLinks = document.getElementById('navLinks');
  navLinks.classList.toggle('active');
}

function openPage() {
  window.location.href = "test.html";
}
$(document).ready(function () {
  $('.slick-images').slick({
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,  // Show one image at a time
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000
  });
});


$(document).ready(function () {
  $('.slick-slider').slick({
    autoplay: true,
    dots: true,
    arrows: false,
    infinite: true,
    speed: 500,
    fade: true,
    cssEase: 'linear'
  });

  $('.disease-slider').slick({
    dots: true,
    infinite: true,
    speed: 500,
    autoplay: true,
    autoplaySpeed: 3000,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true
  });
});

// Initialize EmailJS
(function () {
  emailjs.init("M6o8AiQIrOvQ6-A3Y"); // 🔁 Replace with your actual public key
})();

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contactForm');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    emailjs.sendForm('service_rx44rfl', 'template_44ykwpr', this)
      .then(function () {
        alert('✅ Message sent successfully!');
        form.reset();
      }, function (error) {
        alert('❌ Failed to send message. Error: ' + JSON.stringify(error));
      });
  });
});