(function(){
"use strict";
var root=document.getElementById("mmap");
if(!root)return;
var choices=[{addr:"0x10064",offset:100,logical:0,block:50},{addr:"0x11064",offset:4196,logical:1,block:108},{addr:"0x12064",offset:8292,logical:2,block:73}];
var choice=1,step=0;
var titles=[
 "① 进程访问一个虚拟地址",
 "② mmap 的工作：虚拟地址 → 文件偏移",
 "③ 定位文件中的逻辑块",
 "④ 文件系统的工作：逻辑块 → 磁盘块",
 "⑤ 若该页未驻留：触发缺页并装入内存",
 "⑥ 更新页表，以后可直接访问物理内存"
];
function $(id){return document.getElementById(id)}
function describe(x,k){
 var inBlock=x.offset%4096;
 return [
 "CPU 读取进程的虚拟地址 "+x.addr+"。此时并不知道数据位于哪个磁盘块；CPU 首先按通常方式进行虚拟地址转换。",
 "mmap 事先登记了：虚拟地址区间 0x10000～0x12FFF 对应文件 A.txt，映射的文件起始偏移为 0。本次文件偏移 = "+x.addr+" − 0x10000 = "+x.offset+" 字节。这是“虚拟地址区间与文件位置的关联”。",
 "按 4KB 一块计算，逻辑块号 = floor("+x.offset+" / 4096) = "+x.logical+"；逻辑块内偏移 = "+x.offset+" % 4096 = "+inBlock+" 字节。逻辑块是文件内部从 0 开始编号的块。",
 "假设 A.txt 的索引信息记录：逻辑块 0→磁盘块 50，1→108，2→73。那么本次属于磁盘块 "+x.block+"、块内偏移 "+inBlock+"。文件系统管理这层映射；mmap 本身不直接维护页表项到磁盘块号的转换。",
 "假设页表显示该页未驻留，产生缺页异常。操作系统结合文件映射与文件系统信息，取得所需文件页的数据（如果已在页缓存中，就可能无须再读磁盘），把数据关联到可用的物理页框。",
 "页表建立“该虚拟页 → 物理页框”的关系，重新执行指令并从内存取得数据。下次访问同一驻留页时，一般无需重复文件系统查块或访问磁盘。"
 ][k];
}
function render(){
 var x=choices[choice];
 document.querySelectorAll("#mmap [data-mmap-choice]").forEach(function(btn){
  var yes=Number(btn.getAttribute("data-mmap-choice"))===choice;
  btn.classList.toggle("is-active",yes);
  btn.setAttribute("aria-pressed",String(yes));
 });
 $("mmapAddr").textContent=x.addr;
 $("mmapOffset").textContent=x.offset+" 字节";
 $("mmapLogical").textContent="第 "+x.logical+" 号逻辑块";
 $("mmapDisk").textContent="磁盘块 "+x.block+" + "+(x.offset%4096)+" 字节";
 document.querySelectorAll("#mmap [data-mmap-row]").forEach(function(tr){
  tr.style.background=Number(tr.getAttribute("data-mmap-row"))===x.logical?"#e4f8ee":"";
 });
 $("mmapStepBadge").textContent=(step+1)+" / "+titles.length;
 $("mmapStepTitle").textContent=titles[step];
 $("mmapStepBody").textContent=describe(x,step);
 $("mmapProgressFill").style.width=((step+1)/titles.length*100)+"%";
 $("mmapPrevStep").disabled=step===0;
 $("mmapNextStep").textContent=step===titles.length-1?"↻ 从头推演":"下一步 →";
}
root.querySelectorAll("[data-mmap-choice]").forEach(function(btn){
 btn.addEventListener("click",function(){choice=Number(btn.getAttribute("data-mmap-choice"));step=0;render()});
});
$("mmapPrevStep").addEventListener("click",function(){if(step>0)step--;render()});
$("mmapNextStep").addEventListener("click",function(){step=(step+1)%titles.length;render()});
render();
})();
