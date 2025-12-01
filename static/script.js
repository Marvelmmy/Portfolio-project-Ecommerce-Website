// hero slider script
document.addEventListener("DOMContentLoaded", () => {
    const slides = document.querySelectorAll(".hero-slider a");
    let current = 0;

    function showNextSlide() {
      slides[current].classList.remove("active");
      current = (current + 1) % slides.length;
      slides[current].classList.add("active");
    }

    slides[0].classList.add("active"); 
    setInterval(showNextSlide, 4000); 
  });

// brands logos section script 
function goToBrand(brandName) {
    window.location.href = `/brand/${brandName}`;
  }

// track order navigation
function goToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
}  

var header = document.getElementById("order-nav");
var btns = header.getElementsByClassName("order-nav-btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
  var current = document.getElementsByClassName("active");
  current[0].className = current[0].className.replace(" active", "");
  this.className += " active";
  });
}

// flash messages 
const popup = document.getElementById("popup-message");
if (popup) {
        setTimeout(() => {
          popup.style.opacity = "0";
          setTimeout(() => {
            popup.remove();
          }, 500);
        });
      }

// login page 
  function resetForm() {
    document.getElementById('login').reset();
    document.getElementById('register').reset();
  }

// cart page
function removeItem(productId) {
    fetch("/remove-from-cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_id: productId })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        location.reload(); 
    });
}

// profile preview 
function previewProfileImage(event) {
    const reader = new FileReader();
    reader.onload = function(){
        const output = document.getElementById('profile-preview');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}