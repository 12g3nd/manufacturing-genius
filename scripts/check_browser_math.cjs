/* Node checks the exact same file embedded into the rendered article. */
const fs=require('node:fs'), assert=require('node:assert/strict');
const duel=require('../assets/duel.js');
const reference=JSON.parse(fs.readFileSync('data/reference/duel_benchmark.json','utf8'));
let checks=0;
function close(a,b) {assert.ok(Math.abs(a-b)<1e-11,`${a} differs from ${b}`);checks++;}
for(const row of reference.scenarios) {
  const p=row.parameters,m=duel.matrix(p.initial_gap,p.shock_size,p.correlation),eq=duel.equilibrium(m);
  m.forEach((r,i)=>r.forEach((v,j)=>close(v,row.payoff_matrix[i][j])));
  Object.entries(row.equilibrium).forEach(([k,v])=>close(eq[k],v));
}
// Force ties and the two extreme shock laws with deterministic random draws.
let draws=[.9,.9,.1], d=duel.play(10,10,1,1,0,()=>draws.shift());
close(d.scoreA,100);close(d.scoreB,100);close(d.share,.5);
draws=[.1,.1,.1];d=duel.play(5,10,-1,1,1,()=>draws.shift());
close(d.scoreA,115);close(d.scoreB,90);
assert.throws(()=>duel.matrix(0,-1,0));assert.throws(()=>duel.matrix(0,1,2));
console.log(`${reference.scenarios.length} Python/browser states; ${checks} numerical assertions passed.`);
