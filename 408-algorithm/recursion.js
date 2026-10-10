(function(){
"use strict";
var root=document.getElementById("recursion");
if(!root)return;
var questions=[
{
id:1,title:"阶乘递归",level:"基础 · 规模减一",
code:"int fact(int n) {\n    if (n <= 1) return 1;\n    return n * fact(n - 1);\n}",
opts:["Θ(log n)","Θ(n)","Θ(n log n)","Θ(n²)"],answer:1,
recur:"T(n) = T(n − 1) + Θ(1)",
why:"fact(n − 1) 恰好调用 1 次，递归耗时 T(n − 1)；外面只有一次乘法、条件判断和返回，均为常数时间。特别注意 n × fact(n − 1) 是数值相乘，不表示执行 n 次递归。",
layer:"Nₖ = 1；sₖ = n − k；每个节点的工作量 Θ(1)，所以 Wₖ = Θ(1)。",
height:"n − h = 1，所以 h = n − 1（从根第 0 层算起）。",
total:"T(n) = Θ(∑ₖ₌₀ⁿ⁻¹ 1)\n     = Θ(n)",
mistake:"规模 n − k 不等于代价 n − k！每次只做常数次基本运算。",
general:"第 k 层：1 个节点 × Θ(1) = Θ(1)",
layers:[{vals:[["n","1"]],w:"1"},{vals:[["n−1","1"]],w:"1"},{vals:[["n−2","1"]],w:"1"}]
},
{
id:2,title:"减一递归 + 一重循环",level:"基础 · 链式递归",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 0; i < n; i++) x++;\n    f(n - 1);\n}",
opts:["Θ(n)","Θ(n log n)","Θ(n²)","Θ(2ⁿ)"],answer:2,
recur:"T(n) = T(n − 1) + Θ(n)",
why:"f(n − 1) 只执行 1 次；for 循环从 0 到 n−1 执行 n 次，每次 x++ 为常数操作，所以当前节点自身代价 Θ(n)。",
layer:"第 k 层的输入规模是 n − k；只有 1 个节点，其循环执行 n − k 次。于是 Wₖ = Θ(n − k)。",
height:"n − h = 1，故 h = n − 1。",
total:"T(n) = Θ(∑ₖ₌₀ⁿ⁻¹ (n − k))\n     = Θ(n + (n−1) + ⋯ + 1)\n     = Θ(n(n+1)/2)\n     = Θ(n²)",
mistake:"这题才能用你常写的 ∑(n−k)，因为本层确实有 n−k 次循环，与第 1 题不同。",
general:"第 k 层：1 个节点 × (n−k) = n−k",
layers:[{vals:[["n","n"]],w:"n"},{vals:[["n−1","n−1"]],w:"n−1"},{vals:[["n−2","n−2"]],w:"n−2"}]
},
{
id:3,title:"二分查找（最坏情况）",level:"基础 · 条件分支",
code:"int search(int a[], int l, int r, int key) {\n    if (l > r) return -1;\n    int mid = l + (r - l) / 2;\n    if (a[mid] == key) return mid;\n    if (a[mid] > key)\n        return search(a, l, mid - 1, key);\n    return search(a, mid + 1, r, key);\n}",
opts:["Θ(1)","Θ(log n)","Θ(n)","Θ(n log n)"],answer:1,
recur:"T(n) = T(⌈n/2⌉) + Θ(1) （最坏情况，忽略取整）",
why:"比较后只走左半区或右半区，条件分支互斥，所以每次只发生 1 次递归，不是 2 次；比较关键字与取中点均为常数时间。",
layer:"每层只剩 1 个子问题，规模约为 n/2ᵏ；每个节点比较一次，所以 Wₖ = Θ(1)。",
height:"n/2ʰ ≈ 1，故 2ʰ ≈ n，h = Θ(log₂n)。",
total:"T(n) = Θ(∑ₖ₌₀ʰ 1)\n     = Θ(h+1)\n     = Θ(log n)",
mistake:"if/else 两分支不会同时运行。这里分析的是查找失败或一直缩小到最深层的最坏情况。",
general:"第 k 层：1 个节点 × 1 = 1；规模约 n/2ᵏ",
layers:[{vals:[["n","1"]],w:"1"},{vals:[["n/2","1"]],w:"1"},{vals:[["n/4","1"]],w:"1"}]
},
{
id:4,title:"减半递归 + n 次循环",level:"基础 · 根节点主导",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 0; i < n; i++) x++;\n    f(n / 2);\n}",
opts:["Θ(log n)","Θ(n)","Θ(n log n)","Θ(n²)"],answer:1,
recur:"T(n) = T(n/2) + Θ(n)",
why:"先完成 n 次 x++，耗时 Θ(n)；再做 1 次 f(n/2) 递归。没有第二条递归分支。",
layer:"每层只有一个节点，规模由 n 变为 n/2ᵏ，节点自身循环也只运行 n/2ᵏ 次。Wₖ = Θ(n/2ᵏ)。",
height:"n/2ʰ = 1，解得 h = log₂n。",
total:"T(n) = Θ(∑ₖ₌₀ˡᵒᵍ²ⁿ n/2ᵏ)\n     = Θ(n × (1 + 1/2 + 1/4 + ⋯))\n     = Θ(n)",
mistake:"树有 log n 层，但每层代价逐次减半；不能用 n × log n 直接当结果。",
general:"第 k 层：1 个节点 × (n/2ᵏ) = n/2ᵏ",
layers:[{vals:[["n","n"]],w:"n"},{vals:[["n/2","n/2"]],w:"n/2"},{vals:[["n/4","n/4"]],w:"n/4"}]
},
{
id:5,title:"两次折半递归（常数工作）",level:"中等 · 叶子主导",
code:"void f(int n) {\n    if (n <= 1) return;\n    f(n / 2);\n    f(n / 2);\n}",
opts:["Θ(log n)","Θ(n)","Θ(n log n)","Θ(n²)"],answer:1,
recur:"T(n) = 2T(n/2) + Θ(1)",
why:"两个 f(n/2) 在不同语句中，都会执行，因此递归时间为 2T(n/2)。本层只有判断、传参和返回，非递归代价是 Θ(1)。",
layer:"每个节点分 2 个子节点，Nₖ = 2ᵏ；每个节点自身为 Θ(1)，所以 Wₖ = Θ(2ᵏ)。",
height:"每条路径的规模 n/2ᵏ；令 n/2ʰ = 1，得 h = log₂n。",
total:"T(n) = Θ(∑ₖ₌₀ˡᵒᵍ²ⁿ 2ᵏ)\n     = Θ(2^(log₂n+1) − 1)\n     = Θ(n)",
mistake:"每层节点数逐次翻倍，不能把 log n 的深度当作时间复杂度。",
general:"第 k 层：2ᵏ 个节点 × 1 = 2ᵏ",
layers:[{vals:[["n","1"]],w:"1"},{vals:[["n/2","1"],["n/2","1"]],w:"2"},{vals:[["n/4","1"],["n/4","1"],["n/4","1"],["n/4","1"]],w:"4"}]
},
{
id:6,title:"两次折半递归 + 一重循环",level:"中等 · 每层相等",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 0; i < n; i++) x++;\n    f(n / 2);\n    f(n / 2);\n}",
opts:["Θ(n)","Θ(n log n)","Θ(n²)","Θ(2ⁿ)"],answer:1,
recur:"T(n) = 2T(n/2) + Θ(n)",
why:"循环的 n 次操作形成本层 Θ(n) 工作；随后两次递归各自处理一半规模，递归耗时之和是 2T(n/2)。",
layer:"Nₖ = 2ᵏ，sₖ = n/2ᵏ；单节点代价 Θ(n/2ᵏ)。Wₖ = Θ(2ᵏ × n/2ᵏ) = Θ(n)。",
height:"n/2ʰ = 1，得 h = log₂n。",
total:"T(n) = Θ(∑ₖ₌₀ˡᵒᵍ²ⁿ n)\n     = Θ(n(log₂n+1))\n     = Θ(n log n)",
mistake:"不能只看一条路径的 n+n/2+⋯；本题有 2ᵏ 个节点，必须把同层的所有节点都算进去。",
general:"第 k 层：2ᵏ × (n/2ᵏ) = n（各层相等）",
layers:[{vals:[["n","n"]],w:"n"},{vals:[["n/2","n/2"],["n/2","n/2"]],w:"n"},{vals:[["n/4","n/4"],["n/4","n/4"],["n/4","n/4"],["n/4","n/4"]],w:"n"}]
},
{
id:7,title:"两次折半递归 + 二重循环",level:"中等 · 根节点主导",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) x++;\n    f(n / 2);\n    f(n / 2);\n}",
opts:["Θ(n log n)","Θ(n²)","Θ(n² log n)","Θ(n³)"],answer:1,
recur:"T(n) = 2T(n/2) + Θ(n²)",
why:"嵌套循环对每个 i 执行 n 次 j 循环，共 n×n=n² 次 x++；两次 f(n/2) 均执行，所以递归部分为 2T(n/2)。",
layer:"Nₖ = 2ᵏ，sₖ = n/2ᵏ；节点有二重循环，代价 Θ((n/2ᵏ)²)。因此 Wₖ = Θ(2ᵏ × n²/4ᵏ) = Θ(n²/2ᵏ)。",
height:"n/2ʰ=1，故 h=log₂n。",
total:"T(n) = Θ(∑ₖ₌₀ˡᵒᵍ²ⁿ n²/2ᵏ)\n     = Θ(n²(1 + 1/2 + 1/4 + ⋯))\n     = Θ(n²)",
mistake:"每层代价越来越小，根主导；不是二重循环 n² 再机械乘一个 log n。",
general:"第 k 层：2ᵏ × (n/2ᵏ)² = n²/2ᵏ",
layers:[{vals:[["n","n²"]],w:"n²"},{vals:[["n/2","n²/4"],["n/2","n²/4"]],w:"n²/2"},{vals:[["n/4","n²/16"],["n/4","n²/16"],["n/4","n²/16"],["n/4","n²/16"]],w:"n²/4"}]
},
{
id:8,title:"循环里调用四次折半递归",level:"提高 · 四叉树",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 0; i < n; i++) x++;\n    for (int j = 0; j < 4; j++) f(n / 2);\n}",
opts:["Θ(n)","Θ(n log n)","Θ(n²)","Θ(n² log n)"],answer:2,
recur:"T(n) = 4T(n/2) + Θ(n)",
why:"第一重循环做 n 次 x++，是本层 Θ(n)；第二重循环只有 4 次，但每次都执行 f(n/2)，所以是 4T(n/2)，不能当作普通的 4 次常数运算。",
layer:"Nₖ = 4ᵏ，每个子问题规模 sₖ = n/2ᵏ；每节点代价 Θ(n/2ᵏ)。所以 Wₖ = Θ(4ᵏ×n/2ᵏ)=Θ(n·2ᵏ)。",
height:"规模按 2 而不是按 4 缩小。n/2ʰ=1，故 h=log₂n。",
total:"T(n) = Θ(∑ₖ₌₀ˡᵒᵍ²ⁿ n·2ᵏ)\n     = Θ(n(2^(log₂n+1)−1))\n     = Θ(n²)",
mistake:"分支数 4 用来算节点数 4ᵏ；规模除以 2 用来算树高 log₂n，两者不要混淆。图中第 2 层以每组 4 个节点折叠表示。",
general:"第 k 层：4ᵏ × (n/2ᵏ) = n·2ᵏ",
layers:[{vals:[["n","n"]],w:"n"},{vals:[["n/2","n/2"],["n/2","n/2"],["n/2","n/2"],["n/2","n/2"]],w:"2n"},{vals:[["n/4 ×4","每组 n"],["n/4 ×4","每组 n"],["n/4 ×4","每组 n"],["n/4 ×4","每组 n"]],w:"4n",group:true}]
},
{
id:9,title:"不等规模递归（修正版）",level:"提高 · 不对称分支",
code:"void f(int n) {\n    if (n <= 2) return; // n=2 时必须终止\n    for (int i = 0; i < n; i++) x++;\n    f(n / 3);\n    f(n - n / 3);\n}",
opts:["Θ(log n)","Θ(n)","Θ(n log n)","Θ(n²)"],answer:2,
recur:"T(n) = T(⌊n/3⌋) + T(n−⌊n/3⌋) + Θ(n)",
why:"两个递归语句都会执行，子问题规模分别是 ⌊n/3⌋ 和 n−⌊n/3⌋；循环 Θ(n)。原题若写 if(n<=1)，n=2 时第二次调用仍是 f(2)，造成无限递归，因此已修改为 n<=2。",
layer:"忽略取整，第一层规模分别 n/3 与 2n/3，相加仍为 n；第二层四个规模 n/9、2n/9、2n/9、4n/9，总和也为 n。尚未出现终止分支的完整层 Wₖ = Θ(n)。",
height:"最短路径 n/3ʰ≈1，深度 Θ(log₃n)；最长路径 n(2/3)ʰ≈1，深度 Θ(log₍₃⁄₂₎n)。两者都是 Θ(log n)。",
total:"前面至少 Θ(log n) 个完整层，每层 Θ(n)，故 T(n)=Ω(n log n)。\n整棵树至多 O(log n) 层，每层总代价 O(n)，故 T(n)=O(n log n)。\n上下界相等，T(n)=Θ(n log n)。",
mistake:"不能因为最长路径有 log n 层就说每层都满。要同时证明下界和上界；提前结束的分支不再产生子节点。",
general:"完整层的规模和：n/3 + 2n/3 = n；Wₖ = Θ(n)；树高 Θ(log n)",
layers:[{vals:[["n","n"]],w:"n"},{vals:[["n/3","n/3"],["2n/3","2n/3"]],w:"n"},{vals:[["n/9","n/9"],["2n/9","2n/9"],["2n/9","2n/9"],["4n/9","4n/9"]],w:"n"}]
},
{
id:10,title:"两次规模减一递归",level:"提高 · 指数时间",
code:"void f(int n) {\n    if (n <= 1) return;\n    f(n - 1);\n    f(n - 1);\n}",
opts:["Θ(n)","Θ(n²)","Θ(n log n)","Θ(2ⁿ)"],answer:3,
recur:"T(n) = 2T(n−1) + Θ(1)",
why:"两次 f(n−1) 都执行，每次子问题只比原问题小 1；本层其余工作为常数，因此是 2T(n−1)+Θ(1)。",
layer:"第 k 层节点数 Nₖ=2ᵏ；各节点的问题规模是 n−k，每个节点自身为 Θ(1)，所以 Wₖ=Θ(2ᵏ)。",
height:"n−h=1，故 h=n−1。注意不是 log n！",
total:"T(n) = Θ(∑ₖ₌₀ⁿ⁻¹ 2ᵏ)\n     = Θ(2ⁿ − 1)\n     = Θ(2ⁿ)",
mistake:"对比第 5 题：同样每次分出两个节点，但这里沿一条路径要递归 n 层，而不是 log n 层，所以总时间为指数级。",
general:"第 k 层：2ᵏ 个节点 × 1 = 2ᵏ；深度约 n",
layers:[{vals:[["n","1"]],w:"1"},{vals:[["n−1","1"],["n−1","1"]],w:"2"},{vals:[["n−2","1"],["n−2","1"],["n−2","1"],["n−2","1"]],w:"4"}]
}
];
var letters=["A","B","C","D"];var progress={};var stages={};var filter="all";
try{progress=JSON.parse(localStorage.getItem("rt408-choices")||"{}")||{};}catch(e){progress={};}
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]});}
function updateProgress(){
var count=questions.filter(function(q){return Number.isInteger(progress[q.id]);}).length;
root.querySelector("#rt-count").textContent="已作答 "+count+" / 10 题";
root.querySelector("#rt-meter-fill").style.width=(count*10)+"%";
}
function save(){try{localStorage.setItem("rt408-choices",JSON.stringify(progress))}catch(e){}updateProgress();}
function render(){
var target=root.querySelector("#rt-list");target.innerHTML=questions.map(function(q){
return '<article class="rt-card rt-unanswered" data-rt-id="'+q.id+'" data-level="'+(q.id<=4?"basic":q.id<=7?"medium":"hard")+'">'+
'<div class="rt-cardhead"><div><div class="rt-no">EXERCISE '+String(q.id).padStart(2,"0")+' / 10</div><h3>'+esc(q.title)+'</h3></div><span class="rt-difficulty">'+esc(q.level)+'</span></div>'+
'<div class="rt-cardmain"><pre class="rt-code"><code>'+esc(q.code)+'</code></pre><p class="rt-question">最坏情况下，该算法最紧的渐近时间复杂度是（ ）。</p>'+
'<div class="rt-options">'+q.opts.map(function(v,j){
return '<label class="rt-opt"><input type="radio" name="rt-q-'+q.id+'" value="'+j+'" '+(progress[q.id]===j?'checked':'')+'><span>'+letters[j]+'. '+esc(v)+'</span></label>';
}).join("")+'</div>'+
'<div class="rt-actions"><button class="rt-btn" type="button" data-rt-act="tree">🌳 查看递归树</button><button class="rt-btn alt" type="button" data-rt-act="solution">查看完整答案与解析</button></div></div>'+
'<div class="rt-reveal" data-rt-tree hidden><div class="rt-subtitle">递归树 · 逐层看节点如何分裂</div>'+
'<div class="rt-treewrap" data-rt-svg></div>'+
'<div class="rt-stage-controls"><small data-rt-stage-label>已显示第 0 层</small><div class="rt-stage-buttons"><button type="button" data-rt-act="prev">← 上一层</button><button type="button" data-rt-act="next">下一层 →</button><button type="button" data-rt-act="all">显示前三层</button></div></div>'+
'<div class="rt-rows" data-rt-rows></div><div class="rt-general">'+esc(q.general)+'</div>'+
'<div class="rt-note">树图仅画前 3 层来观察规律；后续递归按第 k 层公式继续，直至达到基本情况。框内上行是问题规模，下行是自身代价。'+(q.id===8?" 第 2 层按 4 个一组折叠展示，共 16 个节点。":"")+'</div></div>'+
'<div class="rt-reveal rt-solution" data-rt-solution hidden>'+
'<div class="rt-final"><span>正确答案：'+letters[q.answer]+' · '+esc(q.opts[q.answer])+'</span><small data-rt-verdict></small></div>'+
'<div class="rt-step"><h4>① 从 C 代码找到递推式</h4><p>'+esc(q.why)+'</p><div class="rt-math">'+esc(q.recur)+'</div></div>'+
'<div class="rt-step"><h4>② 第 k 层的节点数与总代价 Wₖ</h4><p>'+esc(q.layer)+'</p></div>'+
'<div class="rt-step"><h4>③ 根据终止条件求树高 h</h4><p>'+esc(q.height)+'</p></div>'+
'<div class="rt-step"><h4>④ 按你习惯的累加定义法求和</h4><div class="rt-math">'+esc(q.total)+'</div></div>'+
'<div class="rt-caution"><strong>易错提醒：</strong>'+esc(q.mistake)+'</div></div></article>';
}).join("");
questions.forEach(function(q){stages[q.id]=0;});
updateProgress();setFilter(filter);
}
function svgEl(tag,attrs,text){
var el=document.createElementNS("http://www.w3.org/2000/svg",tag);
Object.keys(attrs||{}).forEach(function(k){el.setAttribute(k,attrs[k])});
if(text!==undefined)el.textContent=text;return el;
}
function coords(n){
if(n===1)return [535];
if(n===2)return [300,770];
if(n===4)return [125,395,675,945];
return [535];
}
function draw(q,card){
var step=stages[q.id]||0;
var svg=svgEl("svg",{viewBox:"0 0 1070 330",role:"img","aria-label":"第 "+q.id+" 题递归树前 "+(step+1)+" 层示意图"});
var y=[50,157,264];
var prev=null;
for(var k=0;k<=step;k++){
var nodes=q.layers[k].vals,xx=coords(nodes.length);
svg.appendChild(svgEl("text",{x:14,y:y[k]+4,fill:"#65788b","font-size":14,"font-weight":700},"第"+k+"层"));
if(prev){
for(var j=0;j<nodes.length;j++){
var parent=prev.length===1?0:prev.length===2?Math.floor(j/2):j;
svg.appendChild(svgEl("path",{d:"M"+prev[parent]+" "+(y[k-1]+27)+" C"+prev[parent]+" "+(y[k-1]+54)+","+xx[j]+" "+(y[k]-55)+","+xx[j]+" "+(y[k]-29),fill:"none",stroke:"#a2b7c5","stroke-width":2}));
}
}
for(var j=0;j<nodes.length;j++){
var x=xx[j],s=nodes[j][0],cost=nodes[j][1];
var box=svgEl("rect",{x:x-85,y:y[k]-30,width:170,height:59,rx:12,fill:k===step?"#e1f4ed":"#fff",stroke:k===step?"#20a090":"#cbd9e2","stroke-width":k===step?2:1.2});
svg.appendChild(box);
svg.appendChild(svgEl("text",{x:x,y:y[k]-5,"text-anchor":"middle",fill:"#183650","font-size":17,"font-weight":700},s));
svg.appendChild(svgEl("text",{x:x,y:y[k]+16,"text-anchor":"middle",fill:"#118077","font-size":12},q.id===8&&k===2?"分组代价："+cost:"自身："+cost));
}
prev=xx;
}
if(step<2){svg.appendChild(svgEl("text",{x:535,y:314,"text-anchor":"middle",fill:"#8699aa","font-size":13},"点击「下一层」继续展开"));}else{svg.appendChild(svgEl("text",{x:535,y:319,"text-anchor":"middle",fill:"#8195a8","font-size":13},"⋮ 依照第 k 层规律继续展开直到终止"));}
card.querySelector("[data-rt-svg]").replaceChildren(svg);
card.querySelector("[data-rt-stage-label]").textContent="当前显示第 0 ～ "+step+" 层（共展示前三层）";
card.querySelector('[data-rt-act="prev"]').disabled=step===0;
card.querySelector('[data-rt-act="next"]').disabled=step===2;
card.querySelector("[data-rt-rows]").innerHTML=q.layers.slice(0,step+1).map(function(row,i){return '<div class="rt-row"><span>第 '+i+' 层'+(row.group?'（分组显示）':'')+'</span><strong>W'+["₀","₁","₂"][i]+' = '+esc(row.w)+'</strong></div>'}).join("");
}
function cardBy(btn){return btn.closest(".rt-card");}
function revealTree(card,on){
var part=card.querySelector("[data-rt-tree]");var open=typeof on==="boolean"?on:part.hidden;
part.hidden=!open;card.querySelector('[data-rt-act="tree"]').textContent=open?"收起递归树 ↑":"🌳 查看递归树";
if(open)draw(questions[Number(card.dataset.rtId)-1],card);
return open;
}
function revealAnswer(card,on){
var part=card.querySelector("[data-rt-solution]");var open=typeof on==="boolean"?on:part.hidden;
part.hidden=!open;card.querySelector('[data-rt-act="solution"]').textContent=open?"隐藏答案与解析 ↑":"查看完整答案与解析";
if(open){
var q=questions[Number(card.dataset.rtId)-1];
var verdict=card.querySelector("[data-rt-verdict]");
verdict.textContent=Number.isInteger(progress[q.id])?(progress[q.id]===q.answer?"你的作答正确 ✓":"你的作答为 "+letters[progress[q.id]]+"，请对照解析"):"尚未作答";
}
}
function setFilter(v){
filter=v;root.querySelectorAll("[data-rt-filter]").forEach(function(b){b.classList.toggle("is-active",b.dataset.rtFilter===v)});
root.querySelectorAll(".rt-card").forEach(function(card){
card.hidden=v!=="all"&&card.dataset.level!==v;
});
}
root.addEventListener("click",function(e){
var btn=e.target.closest("button[data-rt-act]");
if(btn){
var a=btn.dataset.rtAct;
if(a==="all-open"){root.querySelectorAll(".rt-card").forEach(function(c){revealTree(c,true);revealAnswer(c,true)});return;}
if(a==="all-close"){root.querySelectorAll(".rt-card").forEach(function(c){revealTree(c,false);revealAnswer(c,false)});return;}
if(a==="reset"){if(!confirm("清空本专题的 10 道题选择记录？"))return;progress={};save();render();return;}
var card=cardBy(btn);if(!card)return;
var q=questions[Number(card.dataset.rtId)-1];
if(a==="tree"){revealTree(card);return;}
if(a==="solution"){revealAnswer(card);return;}
if(a==="prev"||a==="next"||a==="all"){revealTree(card,true);stages[q.id]=a==="all"?2:Math.min(2,Math.max(0,stages[q.id]+(a==="next"?1:-1)));draw(q,card);}
return;
}
var filterBtn=e.target.closest("[data-rt-filter]");
if(filterBtn)setFilter(filterBtn.dataset.rtFilter);
});
root.addEventListener("change",function(e){
var input=e.target;
if(!input.matches('input[type="radio"][name^="rt-q-"]'))return;
var card=input.closest(".rt-card");var id=Number(card.dataset.rtId);
progress[id]=Number(input.value);card.classList.add("rt-selected");save();
if(!card.querySelector("[data-rt-solution]").hidden)revealAnswer(card,true);
});
render();
})();
