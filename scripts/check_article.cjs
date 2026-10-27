/* Actual rendered Quarto HTML: guided game, source-backed views and offline fallbacks. */
const playwright=require('playwright');
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),out=path.join(root,'artifacts/local');
const engine=process.env.MG_BROWSER||'chromium';
const prefix=engine==='chromium'?'':engine+'-';
const study=JSON.parse(fs.readFileSync(path.join(root,'data/generated/study.json'),'utf8'));
const pct=x=>(100*x).toFixed(1)+'%';
(async()=>{
  const browser=await playwright[engine].launch({headless:true,timeout:30000,
    ...(process.env.MG_BROWSER_EXE?{executablePath:process.env.MG_BROWSER_EXE}:{})});
  try {
    const report={engine,browser:browser.version(),viewports:[],checks:[]};
    const errors=[],external=[];
    const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
    await context.route(/^https?:/,r=>{external.push(r.request().url());r.abort();});
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
    const url=pathToFileURL(path.join(root,'_output/index.html')).href;
    await page.goto(url);await page.locator('#duel-game').waitFor({state:'visible'});
    assert.equal((await page.locator('h1.bs-title').innerText()).replace(/\s+/g,' '),'MANUFACTURING GENIUS');
    assert.ok(await page.locator('#title-block-header').isHidden(),'only the masthead title is visible');
    await page.evaluate(()=>document.fonts.ready);
    assert.ok(await page.evaluate(()=>document.fonts.check('400 24px "Ultra"')&&document.fonts.check('400 24px "League Gothic"')&&document.fonts.check('400 18px "Old Standard"')),'embedded broadside fonts loaded');
    const text=await page.locator('main').innerText();
    assert.ok(!text.includes('·'),'separator dots removed');
    assert.ok(/one decision, one round, one prize/i.test(await page.locator('.bs-folio').innerText()),'masthead folio present');
    for(const [target,panel] of [['derivation','derivation-panel'],['selection-grid','selection-grid-panel'],['evaluation-grid','evaluation-grid-panel'],['results-ledger','results-ledger-panel'],['reproduction','reproduction-panel']]) {
      const link=page.locator('#TOC a[href="#'+target+'"]');
      assert.equal(await link.count(),1,'subsection appears in desktop contents');
      await link.click();assert.equal(await page.locator('#'+panel).evaluate(el=>el.open),true,'contents link reveals evidence');
      await page.locator('#'+panel+' > summary').click();
    }
    assert.ok(await page.locator('summary').evaluateAll(els=>els.every(el=>getComputedStyle(el).listStyleType==='none')),'native disclosure arrows removed');
    const shortcuts=await page.locator('.reading-shortcuts a').evaluateAll(els=>els.map(el=>({size:parseFloat(getComputedStyle(el).fontSize),shadow:getComputedStyle(el).boxShadow,height:el.getBoundingClientRect().height})));
    assert.ok(shortcuts.every(s=>s.size>=18&&s.shadow!=='none'&&s.height>=44),'large inked shortcuts with a press shadow');
    await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(150);
    assert.equal(await page.locator('#TOC a.active').getAttribute('href'),'#duel','contents active state returns to the first section');
    assert.equal(await page.locator('#TOC a.active').evaluate(el=>getComputedStyle(el).color),'rgb(28, 23, 18)','active contents is inked, not red');
    assert.equal(await page.locator('#quarto-appendix').evaluate(el=>getComputedStyle(el).backgroundColor),'rgba(0, 0, 0, 0)','appendix shows the newsprint ground');
    assert.ok(!text.includes('{python}')&&!text.includes('incentives over repeated play'));
    assert.ok(text.includes('played once')&&text.includes('75.0%')&&text.includes('66.7%'));
    assert.ok(await page.locator('#free-controls').isHidden());
    assert.equal(await page.locator('#opponent').inputValue(),'safe');
    for(const width of [1440,390]){
      await page.setViewportSize({width,height:1000});
      await page.locator('#duel-game').screenshot({path:path.join(out,prefix+`guided-safe-${width}.png`)});
    }
    await page.locator('[data-action="0"]').focus();await page.keyboard.press('Enter');
    assert.match(await page.locator('#exact-choice').innerText(),/100%/);
    assert.match(await page.locator('#best-response').innerText(),/Safe is a best response/);
    assert.ok(await page.locator('#mixed-solution').isHidden(),'mixing not introduced in first fixed rule');
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(()=>document.activeElement.dataset.action),'1');
    await page.keyboard.press('Space');
    assert.match(await page.locator('#exact-choice').innerText(),/50%/);
    assert.match(await page.locator('#sample').innerText(),/One random play: you chose risky/);
    await page.locator('#guide-next').click();
    assert.equal(await page.locator('#opponent').inputValue(),'risky');
    await page.locator('[data-action="0"]').click();
    assert.match(await page.locator('#exact-choice').innerText(),/50%/);
    await page.locator('[data-action="1"]').click();
    assert.match(await page.locator('#exact-choice').innerText(),/100%/);
    assert.match(await page.locator('#best-response').innerText(),/Risky is a best response/);
    assert.ok(await page.locator('#mixed-solution').isHidden(),'mixing not introduced in second fixed rule');
    await page.locator('#guide-next').click();
    assert.ok(await page.locator('#free-controls').isVisible());
    assert.equal(await page.locator('#opponent').inputValue(),'equilibrium');
    assert.match(await page.locator('#equilibrium-text').innerText(),/75%/);
    assert.equal(await page.evaluate(()=>document.activeElement.id),'gap');
    await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#gap').inputValue(),'6');
    await page.locator('#rho').focus();await page.keyboard.press('ArrowLeft');
    assert.equal(await page.locator('#rho').inputValue(),'0.9');
    for(const gap of [-25,-20,-10,-5,0,5,10,20,25])for(const rho of [-1,0,1]){
      await page.locator('#gap').fill(String(gap));await page.locator('#rho').fill(String(rho));
      const value=await page.evaluate(()=>MGDuel.equilibrium(MGDuel.matrix(+document.getElementById('gap').value,10,+document.getElementById('rho').value)).value);
      assert.ok((await page.locator('#equilibrium-text').innerText()).includes((100*value).toLocaleString('en',{maximumFractionDigits:1})+'%'));
    }
    await page.locator('#gap').fill('5');await page.locator('#rho').fill('1');
    for(const [rule,expectation] of [['safe','100%'],['risky','50%']]){
      await page.locator('#opponent').selectOption(rule);await page.locator('[data-action="0"]').click();
      assert.ok((await page.locator('#exact-choice').innerText()).includes(expectation));
      assert.match(await page.locator('#opponent-note').innerText(),/Prescribed opponent rule/);
    }
    await page.locator('#opponent').selectOption('equilibrium');
    await page.locator('#guide-restart').click();
    assert.ok(await page.locator('#free-controls').isHidden());
    await page.locator('#guide-skip').click();
    assert.equal(await page.evaluate(()=>document.activeElement.id),'gap');
    assert.ok(await page.locator('#free-controls').isVisible());
    report.checks.push('guided fixed-safe -> fixed-risky -> one-shot equilibrium; keyboard activation/focus; exact best responses; 27 boundary displays; free exploration');
    for(const c of study.cells.filter(c=>c.delta===.75&&c.risk_size===1.5&&[0,1].includes(c.correlation))){
      const panel=page.locator(`#reversal-example [data-rho="${c.correlation}"]`);
      const alt=await panel.locator('img').getAttribute('alt');
      for(const value of Object.values(c.exact_accuracy))assert.ok(alt.includes(pct(value)));
      const delta=100*(c.exact_accuracy.equilibrium-c.exact_accuracy.risky);
      assert.ok((await panel.innerText()).replace(/−/g,'-').includes((delta>=0?'+':'')+delta.toFixed(2)));
      for(const key of ['mean','low','high'])assert.ok((await panel.innerText()).replace(/−/g,'-').includes((100*c.paired['equilibrium-risky'].accuracy[key]).toFixed(2)));
    }
    await page.locator('#assumption-explorer summary').click();
    assert.equal(await page.locator('.study-view').count(),study.cells.length);
    for(const c of study.cells){
      for(const key of ['delta','risk_size','correlation'])await page.locator('#study-'+key).selectOption(String(c[key]));
      const selected=page.locator('.study-view:visible');assert.equal(await selected.count(),1);
      const t=(await selected.innerText()).replace(/−/g,'-');
      if(c.delta===0)assert.match(t,/undefined at equal ability/);
      else {
        for(const value of Object.values(c.exact_accuracy))assert.ok(t.includes(pct(value)));
        for(const p of ['equilibrium','safe','risky'])for(const key of ['mean','low','high'])assert.ok(t.includes((100*c.policies[p].accuracy[key]).toFixed(2)));
        for(const p of ['safe','risky'])for(const key of ['mean','low','high'])assert.ok(t.includes((100*c.paired['equilibrium-'+p].accuracy[key]).toFixed(2)));
      }
    }
    await page.locator('#assumption-explorer summary').click();
    report.checks.push('both reversal panels match exact/paired saved outputs; all 48 selectable cells match saved accuracy and Wilson intervals, including equal-ability and zero-risk controls');
    report.contrast=await page.evaluate(()=>{
      const rgb=s=>s.match(/[\d.]+/g).slice(0,3).map(Number);
      const luminance=v=>v.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4;}).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);
      const selectors=['body','.game-guide p','.game-note','.sample','.mx-row','.comparison-panel h4','.paired-interval','.figure-key','.focus-evidence figcaption','.reading-shortcuts a','#refs .csl-entry','#refs a','#quarto-bibliography h2'];
      return selectors.map(selector=>{
        const el=document.querySelector(selector),style=getComputedStyle(el);
        let node=el,bg;
        do {bg=getComputedStyle(node).backgroundColor;node=node.parentElement;}while(bg==='rgba(0, 0, 0, 0)'&&node);
        const a=luminance(rgb(style.color)),b=luminance(rgb(bg));
        return {selector,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
      });
    });
    assert.ok(report.contrast.every(c=>c.ratio>=4.5),'new reading/UI text contrast');
    for(const width of [1440,1280,768,414,390,375,320,1920]){
      await page.setViewportSize({width,height:1000});
      const info=await page.evaluate(()=>({width:innerWidth,pageWidth:document.documentElement.scrollWidth,
        primaryWidths:[...document.querySelectorAll('.focus-evidence')].map(el=>({width:el.clientWidth,scrollWidth:el.scrollWidth})),
        stacked:document.querySelector('#reversal-example .comparison-panels').getBoundingClientRect().height>document.querySelector('#reversal-example .comparison-panel').getBoundingClientRect().height*1.8}));
      assert.ok(info.pageWidth<=width+1,`page overflow at ${width}`);
      assert.ok(info.primaryWidths.every(v=>v.scrollWidth<=v.width+1),`primary figure overflow at ${width}`);
      if(width<=900)assert.ok(info.stacked);
      report.viewports.push(info);
      if([1440,390,320].includes(width)){
        await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(100);await page.screenshot({path:path.join(out,prefix+`opening-${width}.png`)});
        for(const id of ['duel-game','reversal-example','fresh-example'])await page.locator('#'+id).screenshot({path:path.join(out,prefix+id+`-${width}.png`)});
      }
    }
    for(const width of [320,390,1280]) {
      await page.setViewportSize({width,height:1000});
      await page.evaluate(()=>{document.documentElement.style.fontSize='200%';document.querySelectorAll('details').forEach(d=>d.open=true);});
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`200% text reflow at ${width}`);
      if(width===320) {
        const matrix=page.locator('.matrix-scroll');
        await matrix.focus();await page.keyboard.press('ArrowRight');await page.waitForTimeout(150);
        assert.ok(await matrix.evaluate(el=>el.scrollLeft)>0,'enlarged payoff matrix scrolls by keyboard');
        await page.evaluate(()=>scrollTo(0,0));
        await page.screenshot({path:path.join(out,prefix+'polish-text-200-320.png')});
      }
      await page.evaluate(()=>{document.documentElement.style.fontSize='';document.querySelectorAll('details').forEach(d=>d.open=false);});
    }
    assert.equal(await page.locator('#fresh-example h3').count(),2,'fresh panels use the next heading level');
    assert.ok(await page.locator('input[type="range"],.reading-shortcuts a').evaluateAll(els=>els.every(e=>e.getBoundingClientRect().height>=44)),'standalone touch targets');
    report.checks.push('200% text resize at 320/390/1280 with all evidence expanded; keyboard scrolling of enlarged matrix; 44px sliders/shortcuts; fresh panel heading hierarchy');
    await page.setViewportSize({width:390,height:1000});
    await page.locator('#reader-contents > summary').click();
    await page.locator('#reader-contents a[href="#derivation"]').click();
    assert.equal(await page.locator('#derivation-panel').evaluate(el=>el.open),true,'mobile contents reveals derivation');
    assert.equal(await page.locator('#reader-contents').evaluate(el=>el.open),false,'mobile contents closes after navigation');
    await page.locator('#derivation-panel > summary').click();
    await page.locator('#quarto-bibliography').screenshot({path:path.join(out,prefix+'references-390.png')});
    await page.locator('#selection-grid summary').click();
    const plot=page.locator('.plot-scroll').first();await plot.focus();await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(200);assert.ok(await plot.evaluate(el=>el.scrollLeft)>0,'keyboard scroll full evidence grid');
    await page.locator('#evaluation-grid summary').click();
    assert.equal(await page.locator('.plot-scroll img').count(),4);
    await page.locator('#results-ledger summary').click();
    assert.equal(await page.locator('#results-ledger tbody tr').count(),240);
    assert.match(await page.locator('#results-ledger').innerText(),/Undefined/);
    assert.ok(await page.locator('figure img').evaluateAll(imgs=>imgs.length===9&&imgs.every(i=>i.alt.length>40&&i.complete&&i.naturalWidth>0)));
    const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    await nojs.route(/^https?:/,r=>{external.push(r.request().url());r.abort();});
    const fallback=await nojs.newPage();await fallback.goto(url);
    assert.ok(await fallback.locator('#duel-game').isHidden());
    assert.ok(await fallback.locator('.static-benchmark').innerText().then(t=>t.includes('100%')&&t.includes('50%')));
    assert.equal(await fallback.locator('#reversal-example .comparison-panel:visible').count(),2);
    await fallback.locator('#selection-grid summary').focus();await fallback.keyboard.press('Enter');
    assert.ok(await fallback.locator('#fig-selection').isVisible());
    await fallback.setViewportSize({width:320,height:844});
    await fallback.evaluate(()=>document.documentElement.style.fontSize='200%');
    assert.ok(await fallback.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'no-JavaScript enlarged-text reflow');
    report.checks.push('primary figures stack without horizontal scrolling; 4 expandable grids and 240 ledger rows; keyboard evidence scrolling; native details/no-JavaScript explanation; embedded proportional fonts; reference contrast; desktop/mobile subsection contents; bold rounded shortcuts; no disclosure arrows or separator dots; no external requests/errors');
    assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
    report.errors=errors;report.externalRequests=external;
    fs.writeFileSync(path.join(out,prefix+'browser-validation.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify(report,null,2));
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
