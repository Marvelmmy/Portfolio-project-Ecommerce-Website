// heroes section script
const heroBanner = document.getElementById("hero-banner");
const heroContent = document.getElementById("hero-content");

const images = [
  "static/images/hero1.jpg",
  "static/images/hero2.webp",
  "static/images/hero3.jpeg",
"static/images/hero4.avif",
  "static/images/hero5.webp"
];
let currentIndex = 0;

function changeHeroContent() {
    currentIndex = (currentIndex + 1) % images.length;
    heroBanner.style.backgroundImage = `url('${images[currentIndex]}')`;
    heroContent.classList.add("fade-in");
}

setInterval(changeHeroContent, 5000);
    
    const popup = document.getElementById("popup-meesage");
      if (popup) {
        setTimeout(() => {
          popup.style.opacity = "0";
          setTimeout(() => {
            popup.remove();
          }, 500);
        });
      }