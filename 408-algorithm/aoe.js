/* 408 AOE 动态推演：逐题由图自动求 ve/vl/总时差，两张表来自同一个计算结果 */
(function () {
 "use strict";
 var root=document.getElementById("aoe");
 if(!root)return;
 var $=function(id){return document.getElementById(id)};
 var questions=[],current=0,frames=[],step=0,unlocked=false,timer=null,pendingIndex=null;
 var phases=[["intro","读图"],["critical","找关键路径"],["forward","正推 ve"],["backward","反推 vl"],["activities","活动 e/l"],["gaps","补边差额"],["verify","复核结论"]];
 var phaseIndex={}; phases.forEach(function(x,i){phaseIndex[x[0]]=i});
 function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
 function stop(){if(timer){clearInterval(timer);timer=null}$("aoePlay").textContent="▶ 自动播放";}
 function solve(q) {
   var n=q.n,p=Array(n+1).fill(-Infinity),suffix=Array(n+1).fill(-Infinity),forward=Array(n+1).fill(0),backward=Array(n+1).fill(0);
   p[1]=0;
   for(var v=2;v<=n;v++){
     q.edges.filter(function(e){return e.v===v}).forEach(function(e){p[v]=Math.max(p[v],p[e.u]+e.w)});
   }
   suffix[n]=0;
   for(var u=n-1;u>=1;u--){
     q.edges.filter(function(e){return e.u===u}).forEach(function(e){suffix[u]=Math.max(suffix[u],suffix[e.v]+e.w)});
   }
   var t=p[n];
   var stats=q.edges.map(function(e){
     var early=p[e.u],late=t-suffix[e.v]-e.w,front=p[e.v]-p[e.u]-e.w,rear=t-suffix[e.v]-p[e.v];
     var slack=late-early;
     if(front<0||rear<0||slack!==front+rear||slack!==t-(p[e.u]+e.w+suffix[e.v]))throw Error("AOE 余量校验不通过："+q.id+" "+e.id);
     return Object.assign({},e,{early:early,late:late,front:front,rear:rear,slack:slack,critical:slack===0,via:p[e.u]+e.w+suffix[e.v]});
   });
   for(var i=1;i<=n;i++){forward[i]=p[i];backward[i]=t-suffix[i];}
   var paths=[];
   function dfs(v,ids,sum){
     if(v===n){if(sum===t)paths.push(ids.slice());return;}
     q.edges.filter(function(e){return e.u===v}).forEach(function(e){
       ids.push(e.id);dfs(e.v,ids,sum+e.w);ids.pop();
     });
   }
   dfs(1,[],0);
   return {T:t,p:p,suffix:suffix,ve:forward,vl:backward,stats:stats,paths:paths};
 }
 function prefix(q,d,v){
   if(v===1)return [];
   var prev=q.edges.filter(function(e){return e.v===v && d.p[e.u]+e.w===d.p[v]})[0];
   if(!prev)return [];
   return prefix(q,d,prev.u).concat(prev.id);
 }
 function tail(q,d,u){
   if(u===q.n)return [];
   var e=q.edges.filter(function(e){return e.u===u && e.w+d.suffix[e.v]===d.suffix[u]})[0];
   return e?[e.id].concat(tail(q,d,e.v)):[];
 }
 function makeFrames(q,d){
   var r=[],ve=0,vl=0,act=0,gap=0;
   function push(phase,heading,detail,vertex,edgeId){
     r.push({phase:phase,heading:heading,detail:detail,vertex:vertex||0,edgeId:edgeId||"",ve:ve,vl:vl,act:act,gap:gap});
   }
   push("intro","先读网络图","每条箭头是一项活动：字母是活动编号，括号内数字是工期。找到 V1 至 V"+q.n+" 的最紧完整路。先自己画出关键路线，再点击“查看完整解析”。");
   push("critical","第一步：先定全网工期 T","工程工期等于源点到汇点的最长路 T="+d.T+"；所有并列最长路径都要保留，不能只画一条红线。关键路径有 "+d.paths.length+" 条。");
   for(var v=1;v<=q.n;v++){
     ve=v; var prev=q.edges.filter(function(e){return e.v===v});
     var f=v===1?"源点最早发生时间规定为 0。":"入边取最大：max("+prev.map(function(e){return "ve(V"+e.u+")+"+e.w+"="+(d.ve[e.u]+e.w)}).join("，")+") = "+d.ve[v]+"。";
     push("forward","第二步：正推事件最早时间 ve(V"+v+")",f,v);
   }
   for(var u=q.n;u>=1;u--){
     vl=q.n-u+1;var next=q.edges.filter(function(e){return e.u===u});
     var b=u===q.n?"汇点最迟时间等于工程总工期 "+d.T+"。":"出边取最小：min("+next.map(function(e){return "vl(V"+e.v+")−"+e.w+"="+(d.vl[e.v]-e.w)}).join("，")+") = "+d.vl[u]+"。";
     push("backward","第三步：反推事件最迟时间 vl(V"+u+")",b,u);
   }
   d.stats.forEach(function(e,i){
     act=i+1;
     push("activities","第四步：活动 "+e.id+" 的 e、l 与总余量","e("+e.id+")=ve(V"+e.u+")="+e.early+"；l("+e.id+")=vl(V"+e.v+")−"+e.w+"="+e.late+"；l−e="+e.slack+"。",0,e.id);
   });
   d.stats.forEach(function(e,i){
     gap=i+1;
     push("gaps","第五步：给活动 "+e.id+" 补两段差额","入边差 = ve(V"+e.v+")−[ve(V"+e.u+")+"+e.w+"]="+e.front+"；后续差 = vl(V"+e.v+")−ve(V"+e.v+")="+e.rear+"。两段之和 "+e.front+"+"+e.rear+"="+e.slack+"，与 l−e 完全一致。经过此边的最严格完整路 = "+e.via+"，T−"+e.via+"="+e.slack+"。",0,e.id);
   });
   push("verify","第六步：两表交叉核对","全部 "+d.stats.length+" 项活动的“l−e”和“入边差 + 后续差”一致。余量为0的活动组成关键路径。画叉只表示未控制某次局部 ve，绝不意味着从网络删除这条边。");
   return r;
 }
 function networkSvg(q,d,f){
   var lvl=Array(q.n+1).fill(0);lvl[1]=0;
   for(var v=2;v<=q.n;v++)q.edges.forEach(function(e){if(e.v===v)lvl[v]=Math.max(lvl[v],lvl[e.u]+1);});
   var max=Math.max.apply(null,lvl.slice(1)),layers=Array.from({length:max+1},function(){return[]});
   for(var u=1;u<=q.n;u++)layers[lvl[u]].push(u);
   var rows=Math.max.apply(null,layers.map(function(a){return a.length}));
   var H=Math.max(320,Math.min(580,rows*125+100)),W=Math.max(750,(max+1)*158+60),pos={};
   layers.forEach(function(a,c){a.forEach(function(v,j){pos[v]={x:75+c*((W-150)/Math.max(1,max)),y:(j+1)*H/(a.length+1)}})});
   var result=['<svg viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AOE有向无环网络图">',
   '<defs><marker id="aoe-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#879eaa"/></marker><marker id="aoe-arr-crit" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#dc6760"/></marker><marker id="aoe-arr-focus" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#d9a342"/></marker><marker id="aoe-arr-before" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#418ab9"/></marker><marker id="aoe-arr-after" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#a183c5"/></marker></defs>'];
   var focus=d.stats.find(function(e){return e.id===f.edgeId;});
   var before=focus&&f.phase==="gaps"?prefix(q,d,focus.u):[],after=focus&&f.phase==="gaps"?tail(q,d,focus.v):[];
   q.edges.forEach(function(e,k){
     var a=pos[e.u],b=pos[e.v],dx=b.x-a.x,dy=b.y-a.y,len=Math.max(1,Math.hypot(dx,dy)),pad=23;
     var x1=a.x+pad*dx/len,y1=a.y+pad*dy/len,x2=b.x-pad*dx/len,y2=b.y-pad*dy/len;
     var bend=(k%2===0?1:-1)*Math.min(18,Math.abs(dy)*.04+5);
     var mx=(x1+x2)/2,my=(y1+y2)/2+bend;
     var path="M"+x1.toFixed(1)+" "+y1.toFixed(1)+" Q"+mx.toFixed(1)+" "+my.toFixed(1)+" "+x2.toFixed(1)+" "+y2.toFixed(1);
     var color="#8ea4ae",marker="aoe-arrow",width=2;
     if(f.phase!=="intro"&&d.stats[k].critical){color="#dc6760";marker="aoe-arr-crit";width=3;}
     if(before.indexOf(e.id)>=0){color="#418ab9";marker="aoe-arr-before";width=3.5;}
     if(after.indexOf(e.id)>=0){color="#a183c5";marker="aoe-arr-after";width=3.5;}
     if(f.edgeId===e.id){color="#d9a342";marker="aoe-arr-focus";width=4.5;}
     var tx=(x1+x2+mx*2)/4,ty=(y1+y2+my*2)/4-8+(k%2===0?-7:7);
     result.push('<path class="aoe-edge-line" d="'+path+'" fill="none" stroke="'+color+'" stroke-width="'+width+'" marker-end="url(#'+marker+')" />');
     result.push('<path class="aoe-edge-hit" data-edge-id="'+esc(e.id)+'" d="'+path+'"><title>活动 '+esc(e.id)+'：V'+e.u+' → V'+e.v+'，工期 '+e.w+'，点击分析</title></path>');
     result.push('<rect x="'+(tx-21).toFixed(1)+'" y="'+(ty-15).toFixed(1)+'" width="45" height="20" rx="6" fill="#f9fcfd" opacity=".94" pointer-events="none"/><text x="'+(tx+1).toFixed(1)+'" y="'+ty.toFixed(1)+'" text-anchor="middle" fill="'+color+'" class="aoe-edge-label">'+esc(e.id)+'('+e.w+')</text>');
   });
   for(var v=1;v<=q.n;v++){
     var p=pos[v],active=f.vertex===v;result.push('<circle class="aoe-node-circle" cx="'+p.x+'" cy="'+p.y+'" r="21"'+(active?' fill="#dff6ee" stroke="#199486" stroke-width="3"':'')+'/><text class="aoe-node-text" x="'+p.x+'" y="'+(p.y+5)+'" text-anchor="middle">'+v+'</text>');
   }
   result.push('</svg>');return result.join("");
 }
 function renderTables(q,d,f){
   var eventRows=[];for(var v=1;v<=q.n;v++){
     var showVe=unlocked&&v<=f.ve,showVl=unlocked&&v>=q.n-f.vl+1;
     eventRows.push('<tr class="'+(f.vertex===v?'is-current':'')+'"><td>V'+v+'</td><td>'+(showVe?d.ve[v]:'—')+'</td><td>'+(showVl?d.vl[v]:'—')+'</td><td>'+(showVe&&showVl?d.vl[v]-d.ve[v]:'—')+'</td></tr>');
   }
   $("aoeEventsTable").innerHTML='<thead><tr><th>事件</th><th>ve 最早</th><th>vl 最迟</th><th>时间差</th></tr></thead><tbody>'+eventRows.join("")+'</tbody>';
   $("aoeActivitiesTable").innerHTML='<thead><tr><th>活动</th><th>起点→终点</th><th>工期 w</th><th>e</th><th>l</th><th>l−e</th><th>入边差</th><th>后续差</th><th>关键？</th></tr></thead><tbody>'+
     d.stats.map(function(e,i){
       var time=unlocked&&i<f.act,gap=unlocked&&i<f.gap;
       return '<tr class="aoe-row-edge '+(f.edgeId===e.id?'is-current ':'')+(time&&e.critical?'is-critical':'')+'" data-aoe-table-edge="'+esc(e.id)+'"><td>'+esc(e.id)+'</td><td>V'+e.u+' → V'+e.v+'</td><td>'+e.w+'</td><td>'+(time?e.early:'—')+'</td><td>'+(time?e.late:'—')+'</td><td>'+(time?e.slack:'—')+'</td><td>'+(gap?e.front:'—')+'</td><td>'+(gap?e.rear:'—')+'</td><td>'+(time?(e.critical?'是':'否'):'—')+'</td></tr>';
     }).join("")+'</tbody>';
 }
 function render() {
   var q=questions[current];if(!q)return;var d=q._sol,f=frames[step]||frames[0];
   $("aoeIndex").innerHTML='<strong>'+String(current+1).padStart(2,"0")+'</strong> / '+questions.length;
   $("aoePrevQuestion").disabled=current===0;$("aoeNextQuestion").disabled=current===questions.length-1;
   $("aoeTitle").textContent=q.title;$("aoeQuestion").textContent=q.task;
   $("aoeMeta").innerHTML='<span class="aoe-tag gold">'+esc(q.level)+' · 408风格原创</span><span class="aoe-tag">'+q.n+' 个事件</span><span class="aoe-tag">'+q.edges.length+' 条活动</span>';
   $("aoeGraph").innerHTML=networkSvg(q,d,f);$("aoeStep").querySelector(".aoe-step-eyebrow").textContent="步骤 "+(step+1)+" / "+frames.length+" · "+phases[phaseIndex[f.phase]][1];
   $("aoeStepTitle").textContent=f.heading;$("aoeStepBody").textContent=f.detail;
   $("aoeProgressFill").style.width=(100*(step+1)/frames.length)+"%";
   $("aoeLocked").hidden=unlocked;$("aoeResult").hidden=!unlocked;
   $("aoeUnlock").textContent=unlocked?"✓ 已解锁完整推演":"查看完整解析与两张表 ↓";
   $("aoePrevStep").disabled=!unlocked||step===0;$("aoeNextStep").disabled=!unlocked||step===frames.length-1;
   $("aoePhaseStrip").innerHTML=phases.map(function(p){
     var selected=p[0]===f.phase;
     return '<button type="button" class="aoe-phase '+(selected?'active':'')+'" data-aoe-phase="'+p[0]+'" '+(!unlocked?'disabled ':'')+'aria-pressed="'+selected+'">'+esc(p[1])+'</button>';
   }).join("");
   renderTables(q,d,f);
   var e=d.stats.find(function(x){return x.id===f.edgeId;});
   $("aoeFormula").innerHTML=e&&unlocked?'<b>当前活动 '+esc(e.id)+'</b>：从 V'+e.u+' 到 V'+e.v+'，工期 '+e.w+'<div>① 入边差 = '+e.front+'；② 后续差 = '+e.rear+'；总余量 = '+e.front+' + '+e.rear+' = <strong>'+e.slack+'</strong>。</div><div>标准公式：e = '+e.early+'；l = '+e.late+'；l − e = <strong>'+e.slack+'</strong>。最严格经过此边的完整路长度为 '+e.via+'。</div>':
     '<b>补边法公式：</b>入边差 = ve(v) − ve(u) − w；后续差 = vl(v) − ve(v)。<br>总余量 = 入边差 + 后续差 = l − e = T − [P(u)+w+Q(v)]。';
   $("aoeCriticalPaths").innerHTML=unlocked?'<p class="aoe-table-sub">项目总工期 T = <strong>'+d.T+'</strong>，以下为全部关键路径（活动编号顺序）。</p><div class="aoe-critpaths">'+d.paths.map(function(a){return '<span class="aoe-path-pill">'+esc(a.join(' → '))+' = '+d.T+'</span>'}).join("")+'</div>':'';
 }
 function select(index,withScroll){
   stop();current=Math.max(0,Math.min(questions.length-1,index));unlocked=false;step=0;frames=makeFrames(questions[current],questions[current]._sol);render();if(!root.hidden&&/^#aoe/.test(location.hash))history.replaceState(null,"","#aoe-"+(current+1));
   if(withScroll)$("aoe").scrollIntoView({behavior:"smooth",block:"start"});
 }
 function go(s){stop();step=Math.max(0,Math.min(frames.length-1,s));render();}
 function phaseJump(phase){var i=frames.findIndex(function(f){return f.phase===phase});if(i>=0)go(i);}
 function focusEdge(id){
   var fidx=frames.findIndex(function(f){return f.phase==="gaps"&&f.edgeId===id});
   if(!unlocked){$("aoeGraphNote").textContent="已选活动 "+id+"。先点击“查看完整解析”才能看到两张表和补边步骤。";return;}
   if(fidx>=0)go(fidx);
 }
 $("aoePrevQuestion").onclick=function(){select(current-1,false)};
 $("aoeNextQuestion").onclick=function(){select(current+1,false)};
 $("aoeUnlock").onclick=function(){if(!unlocked){unlocked=true;step=1;render();$("aoeResult").scrollIntoView({behavior:"smooth",block:"nearest"});}else{$("aoeStep").scrollIntoView({behavior:"smooth",block:"nearest"});}};
 $("aoePrevStep").onclick=function(){go(step-1)};
 $("aoeNextStep").onclick=function(){go(step+1)};
 $("aoePlay").onclick=function(){
   if(timer){stop();return;}if(!unlocked){unlocked=true;step=1;render();}
   if(step>=frames.length-1)step=1;
   $("aoePlay").textContent="Ⅱ 暂停";
   timer=setInterval(function(){if(step>=frames.length-1){stop();return;}step++;render();if(step>=frames.length-1)stop();},950);
 };
 $("aoeGraph").addEventListener("click",function(e){var p=e.target.closest("[data-edge-id]");if(p)focusEdge(p.dataset.edgeId);});
 $("aoeActivitiesTable").addEventListener("click",function(e){var p=e.target.closest("[data-aoe-table-edge]");if(p)focusEdge(p.dataset.aoeTableEdge);});
 $("aoePhaseStrip").addEventListener("click",function(e){var b=e.target.closest("button[data-aoe-phase]");if(b&&unlocked)phaseJump(b.dataset.aoePhase);});
 $("aoeGraphNote").textContent="网络图可以横向滚动。点击任意活动箭头可定位到其补边验算。";
 window.AOE_LAB={activate:function(index){pendingIndex=Number.isInteger(index)?index:current;if(questions.length)select(pendingIndex,false);},count:function(){return questions.length;}};
 fetch("./aoe-lessons.json",{cache:"no-store"}).then(function(r){if(!r.ok)throw Error("HTTP "+r.status);return r.json();}).then(function(data){
   if(!Array.isArray(data)||data.length!==8)throw Error("专项题目未满8道");
   questions=data.map(function(q){q._sol=solve(q);return q;});select(Math.max(0,Math.min(questions.length-1,pendingIndex===null?0:pendingIndex)),false);
 }).catch(function(e){$("aoeTitle").textContent="AOE题库加载失败";$("aoeQuestion").textContent=String(e.message);});
})();
