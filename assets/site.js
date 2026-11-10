// The attract mode plays while it is in sight, and never for those who
// asked their system for less motion (they get its first picture and the
// controls to start it themselves). A click, Enter or Space holds it or
// plays it on, and then it stays as chosen.
const video = document.querySelector(".attract");
if (video) {
  const still = matchMedia("(prefers-reduced-motion: reduce)");
  if (still.matches) {
    video.controls = true;
  } else {
    let held = false;
    const toggle = () => {
      held = !video.paused;
      if (held) video.pause();
      else video.play().catch(() => { video.controls = true; });
    };
    video.addEventListener("click", toggle);
    video.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
    });
    new IntersectionObserver(([seen]) => {
      if (seen.isIntersecting && !held) video.play().catch(() => { video.controls = true; });
      else video.pause();
    }, { threshold: 0.25 }).observe(video);
  }
}
