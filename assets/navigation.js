/* Keep contents links useful when the target evidence is in a closed disclosure. */
(function () {
  'use strict';
  const panels={derivation:'derivation-panel',assumptions:'assumption-explorer',
    'selection-grid':'selection-grid-panel','evaluation-grid':'evaluation-grid-panel',
    'results-ledger':'results-ledger-panel',reproduction:'reproduction-panel'};
  function reveal(hash) {
    let id;try{id=decodeURIComponent(hash.replace(/^#/,''));}catch{return;}
    const target=document.getElementById(id);if(!target)return;
    const panel=document.getElementById(panels[id]);if(panel)panel.open=true;
    for(let node=target;node;node=node.parentElement)if(node.tagName==='DETAILS')node.open=true;
  }
  // Quarto retains the last active link above its first heading's 200px margin.
  // Treat that title/intro area as the opening instead of leaving a stale link.
  function highlightOpening() {
    const links=[...document.querySelectorAll('#TOC a[data-scroll-target]')];
    const first=links[0];if(!first)return;
    const heading=document.getElementById(first.getAttribute('data-scroll-target').slice(1));
    if(heading&&scrollY<Math.max(0,heading.getBoundingClientRect().top+scrollY-200)) {
      links.forEach(link=>link.classList.toggle('active',link===first));
    }
  }
  document.addEventListener('scroll',highlightOpening,{passive:true});
  window.addEventListener('resize',highlightOpening);
  document.addEventListener('click',event=>{
    const link=event.target.closest?.('a[href^="#"]');if(!link)return;
    reveal(link.getAttribute('href'));
    if(link.closest('#reader-contents'))document.getElementById('reader-contents').open=false;
  });
  window.addEventListener('hashchange',()=>reveal(location.hash));
  function init(){reveal(location.hash);highlightOpening();document.fonts?.ready.then(highlightOpening);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
