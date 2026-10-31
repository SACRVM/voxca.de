// The attract mode plays while it is in sight, and never for those who
// asked their system for less motion (they get its first picture and the
// controls to start it themselves).
const video = document.querySelector(".attract");
if (video) {
  const still = matchMedia("(prefers-reduced-motion: reduce)");
  if (still.matches) {
    video.controls = true;
  } else {
    new IntersectionObserver(([seen]) => {
      if (seen.isIntersecting) video.play().catch(() => { video.controls = true; });
      else video.pause();
    }, { threshold: 0.25 }).observe(video);
  }
}
