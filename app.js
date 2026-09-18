const player = document.querySelector('#player');
const frame = document.querySelector('#player-frame');
let trigger;
function stopVideo() { frame.replaceChildren(); trigger?.focus(); }
function closeVideo() { player.close(); }
document.querySelectorAll('[data-video]').forEach(link => {
  link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || typeof player.showModal !== 'function') return;
    event.preventDefault();
    trigger = link;
    document.querySelector('#player-title').textContent = link.dataset.title;
    document.querySelector('#youtube-fallback').href = link.href;
    const iframe = document.createElement('iframe');
    iframe.title = link.dataset.title;
    iframe.src = `https://www.youtube-nocookie.com/embed/${link.dataset.video}?autoplay=1&rel=0`;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.replaceChildren(iframe);
    player.showModal();
  });
});
document.querySelector('#close-player').addEventListener('click', closeVideo);
player.addEventListener('close', stopVideo);
player.addEventListener('click', event => {
  const r = player.getBoundingClientRect();
  if (event.target === player && (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)) closeVideo();
});
