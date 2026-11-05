// Enhance the readable stage list into an automatically activated tab interface.
const timeline = document.querySelector('.timeline');
if (timeline) {
  const stops = [...timeline.querySelectorAll('.timeline-stop')];
  const panels = stops.map(stop => document.getElementById(stop.getAttribute('aria-controls')));
  timeline.querySelector('.timeline-stops').setAttribute('role', 'tablist');
  function select(index, focus = false) {
    stops.forEach((stop, i) => {
      stop.setAttribute('aria-selected', String(i === index));
      stop.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
    if (focus) stops[index].focus();
  }
  stops.forEach((stop, index) => {
    stop.setAttribute('role', 'tab');
    panels[index].setAttribute('role', 'tabpanel');
    panels[index].tabIndex = 0;
    stop.addEventListener('click', () => select(index));
    stop.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % stops.length;
      if (event.key === 'ArrowLeft') next = (index + stops.length - 1) % stops.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = stops.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        select(next, true);
      }
    });
  });
  select(0);
}
