/* Switch among already-rendered study cells. No estimation or data requests. */
(function () {
  'use strict';
  function init() {
    const container=document.getElementById('assumption-explorer');
    if(!container)return;
    const keys=['delta','risk_size','correlation'];
    const controls=keys.map(k=>document.getElementById('study-'+k));
    const panels=[...container.querySelectorAll('.study-view')];
    function show() {
      const values=controls.map(c=>Number(c.value));
      panels.forEach(p=>{p.hidden=!keys.every((key,i)=>Number(p.getAttribute('data-'+key.replace('_','-')))===values[i]);});
      document.getElementById('study-announcement').textContent='Showing ability gap '+values[0]+', risk magnitude '+values[1]+', correlation '+values[2]+'.';
    }
    controls.forEach(c=>c.addEventListener('change',show));
    container.querySelector('.assumption-controls').hidden=false;
    show();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
