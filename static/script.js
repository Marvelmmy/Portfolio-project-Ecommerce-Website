// heroes section script
const heroImage = document.getElementById("hero-image");

const images = [
  "static/images/hero1.jpg",
  "static/images/hero2.webp",
  "static/images/hero3.jpeg",
  "static/images/hero4.avif",
  "static/images/hero5.webp",
];

let current = 0;

function changeHeroImage() {
  heroImage.classList.add("fade-out");

  setTimeout(() => {
    current = (current + 1) % images.length;
    heroImage.src = images[current];
    heroImage.classList.remove("fade-out");
  }, 1000); 
}

setInterval(changeHeroImage, 5000);

// brands logos section script 
function goToBrand(brandName) {
    window.location.href = `/brand/${brandName}`;
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