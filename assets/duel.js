/* Exact static duel. Safe/risky order and degeneracy convention match Python. */
(function (root) {
  "use strict";
  function matrix(gap, size, rho) {
    if (![gap, size, rho].every(Number.isFinite) || size < 0 || Math.abs(rho) > 1) throw new Error("Invalid duel parameters");
    const shocks = [[1,1,(1+rho)/4],[1,-1,(1-rho)/4],[-1,1,(1-rho)/4],[-1,-1,(1+rho)/4]];
    return [0,1].map(a => [0,1].map(b => shocks.reduce((sum,[xa,xb,prob]) => {
      const d = gap + size*(a*xa-b*xb);
      return sum + prob*(d > 0 ? 1 : d < 0 ? 0 : .5);
    },0)));
  }
  function evaluate(m,p,q) {
    const rows = m.map(r => (1-q)*r[0]+q*r[1]);
    const cols = [0,1].map(j => (1-p)*m[0][j]+p*m[1][j]);
    const value = (1-p)*rows[0]+p*rows[1];
    const rowGain = Math.max(0, ...rows.map(v => v-value));
    const columnGain = Math.max(0, ...cols.map(v => value-v));
    return {value, row_deviation_gain:rowGain, column_deviation_gain:columnGain,
      exploitability:rowGain+columnGain, max_deviation_gain:Math.max(rowGain,columnGain)};
  }
  function equilibrium(m) {
    let p, q;
    outer: for(let i=0;i<2;i++) for(let j=0;j<2;j++) {
      if(m[i][j] >= Math.max(m[0][j],m[1][j])-1e-12 && m[i][j] <= Math.min(...m[i])+1e-12) {p=i;q=j;break outer;}
    }
    if(p === undefined) {
      const [[a,b],[c,d]] = m, den=a-b-c+d;
      p=Math.min(1,Math.max(0,(a-b)/den)); q=Math.min(1,Math.max(0,(a-c)/den));
    }
    const audit=evaluate(m,p,q);
    if(audit.max_deviation_gain > 4e-12) throw new Error("Equilibrium failed deviation check");
    return {row_risky_probability:p, column_risky_probability:q, ...audit};
  }
  function play(gap,size,rho,a,q,random=Math.random) {
    const b = random() < q ? 1 : 0;
    const xa = random() < .5 ? 1 : -1;
    const xb = xa*(random() < (1+rho)/2 ? 1 : -1);
    const scoreA=100+gap+size*a*xa, scoreB=100+size*b*xb;
    return {b,scoreA,scoreB,share:scoreA>scoreB?1:scoreA<scoreB?0:.5};
  }
  const api = {matrix,equilibrium,evaluate,play};
  if(typeof module !== "undefined" && module.exports) module.exports=api;
  root.MGDuel=api;
  if(typeof document === "undefined") return;
  function init() {
    const game=document.getElementById("duel-game");
    if(!game) return;
    game.hidden=false;
    document.getElementById("game-guide").hidden=false;
    document.getElementById("duel-play").hidden=false;
    document.documentElement.classList.add("mg-js");
    const $=id=>document.getElementById(id);
    const pct=x=>(100*x).toLocaleString("en",{maximumFractionDigits:1})+"%";
    let choice=null, stage=0;
    function state() {
      const gap=Number($("gap").value),rho=Number($("rho").value),m=matrix(gap,10,rho),eq=equilibrium(m);
      const opponent=$("opponent").value;
      const q=opponent==="safe"?0:opponent==="risky"?1:eq.column_risky_probability;
      return {gap,rho,m,eq,q};
    }
    function refresh() {
      const {gap,rho,m,eq,q}=state();
      const expectations=m.map(row=>(1-q)*row[0]+q*row[1]);
      const best=expectations[0]>expectations[1]+1e-12?"Safe":expectations[1]>expectations[0]+1e-12?"Risky":"Either action";
      $("gap-value").textContent=(gap>0?"+":"")+gap+" points";
      $("rho-value").textContent=rho.toFixed(1);
      $("gap").setAttribute("aria-valuetext",(gap>0?"A leads by ":gap<0?"A trails by ":"Tied at ")+Math.abs(gap)+" points");
      $("rho").setAttribute("aria-valuetext","Correlation "+rho.toFixed(1));
      $("score-a").textContent=100+gap; $("score-b").textContent=100;
      $("position").textContent=gap>0?"You lead.":gap<0?"You trail.":"You are tied.";
      $("opponent-note").textContent=($("opponent").value==="equilibrium"?"Equilibrium opponent: ":"Prescribed opponent rule: ")+"B chooses risky with probability "+pct(q)+". Choices are simultaneous.";
      $("best-response").textContent=choice===null?"": "Exact expectations against this rule: safe "+pct(expectations[0])+"; risky "+pct(expectations[1])+". "+best+" is a best response."+
        (stage===0?" A safe rival leaves the lead untouched, so staying safe preserves it. Taking risk can give it away.":stage===1?" With a shared shock, matching a risky rival preserves the gap. Staying safe lets the rival’s positive shock pass you.":" These are expectations for one simultaneous game, not guarantees about this draw.");
      $("sample").textContent="Choose an action to play one random round.";
      $("exact-choice").textContent="";
      const shown=stage===2||choice!==null;
      [0,1].forEach(i=>{
        [0,1].forEach(j=>{
          const cell=game.querySelector('[data-cell="'+i+'-'+j+'"]');
          cell.textContent=shown?pct(m[i][j]):"?";
          cell.classList.toggle("is-chosen",choice===i);
          cell.classList.remove("is-hit");
        });
        const net=game.querySelector('[data-net="'+i+'"]');
        net.textContent=shown?pct(expectations[i]):"?";
        net.classList.toggle("is-chosen",choice===i);
        net.classList.toggle("is-best",shown&&expectations[i]>expectations[1-i]+1e-12);
      });
      [0,1].forEach(j=>{
        const weight=j?q:1-q;
        game.querySelector('[data-col="'+j+'"]').classList.toggle("is-rival",weight>1e-12);
        game.querySelector('[data-weight="'+j+'"]').textContent=weight>1-1e-12?"every time":weight<1e-12?"never":pct(weight)+" of the time";
      });
      $("equilibrium-text").textContent="One checked equilibrium: A chooses risky "+pct(eq.row_risky_probability)+
        "; B chooses risky "+pct(eq.column_risky_probability)+". A’s expected prize share is "+pct(eq.value)+
        ". Neither player gains by deviating alone.";
      $("degenerate-note").textContent=(gap===0 || Math.abs(gap)>=10 || rho===-1)
        ? "Some settings have multiple equilibria. This is one solution under the stated tie and solver convention; it is not a uniqueness claim."
        : "Both players randomize their actions independently in this one-shot simultaneous game. Expected prize share averages over actions and shocks; one realized play can differ.";
      if(choice!==null) $("exact-choice").textContent="With your chosen action, A’s exact expected prize share against this B rule is "+pct((1-q)*m[choice][0]+q*m[choice][1])+".";
    }
    function choose(a) {
      choice=a;
      document.querySelectorAll("[data-action]").forEach(b=>b.setAttribute("aria-pressed",Number(b.dataset.action)===a?"true":"false"));
      refresh();
      const {gap,rho,q}=state(), draw=play(gap,10,rho,a,q);
      $("sample").textContent="One random play: you chose "+(a?"risky":"safe")+", B chose "+(draw.b?"risky":"safe")+
        ". Final score: A "+draw.scoreA+", B "+draw.scoreB+". "+(draw.share===1?"A wins.":draw.share===0?"B wins.":"A tie splits the prize.")+" This draw is not an estimate of the exact expectation.";
      game.querySelector('[data-cell="'+a+'-'+draw.b+'"]').classList.add("is-hit");
    }
    document.querySelectorAll("[data-action]").forEach(b=>b.addEventListener("click",()=>choose(Number(b.dataset.action))));
    function setStage(next) {
      stage=next; choice=null;
      $("gap").value="5"; $("rho").value="1";
      $("opponent").value=stage===0?"safe":stage===1?"risky":"equilibrium";
      $("guide-progress").textContent=["Rule 1 of 3","Rule 2 of 3","Rule 3 of 3: free play"][stage];
      $("guide-title").textContent=["The rival always stays safe.","Now the rival always takes risk.","Neither player commits to a fixed action."][stage];
      $("guide-copy").textContent=stage<2?"Your rival is stuck with a fixed rule here. Which row gives you the bigger expected share of the prize?":"When you both choose at the same time, any predictable move can be exploited, so the equilibrium mixes safe and risky. At the starting setting, that mix leaves both of your rows paying the same. Move the lead, the correlation or the rule below and see what changes.";
      $("free-controls").hidden=stage<2;
      $("guide-next").hidden=stage===2;
      $("guide-next").textContent=stage===0?"Next: rival always risky":"Next: equilibrium";
      $("guide-skip").hidden=stage===2;
      document.querySelector(".guide-navigation").hidden=stage===2;
      $("guide-restart").hidden=stage<2;
      $("mixed-solution").hidden=stage<2;
      document.querySelectorAll("[data-action]").forEach(b=>b.setAttribute("aria-pressed","false"));
      refresh();
    }
    $("guide-next").addEventListener("click",()=>{setStage(Math.min(2,stage+1));if(stage===2)$("gap").focus();});
    $("guide-skip").addEventListener("click",()=>{setStage(2);$("gap").focus();});
    $("guide-restart").addEventListener("click",()=>{setStage(0);document.querySelector('[data-action="0"]').focus();});
    ["gap","rho","opponent"].forEach(id=>$(id).addEventListener("input",refresh));
    setStage(0);
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",init); else init();
})(typeof globalThis !== "undefined" ? globalThis : this);
