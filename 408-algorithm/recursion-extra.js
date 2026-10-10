/* 408 递归树补充训练：11—15 题，保留原有 10 题 */
window.RT_EXTRA_QUESTIONS=[
{
id:11,title:"规模减二 + 二重循环",level:"进阶 · 非单位步长",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) x++;\n    f(n - 2);\n}",
opts:["Θ(n²)","Θ(n³)","Θ(n² log n)","Θ(2ⁿ)"],answer:1,
recur:"T(n) = T(n − 2) + Θ(n²)",
why:"两个嵌套循环共执行 n×n=n² 次，形成当前节点的 Θ(n²) 代价；只有一次 f(n−2) 递归，因此递归时间是 T(n−2)。",
layer:"递归树是一条链，Nₖ=1，规模 sₖ=n−2k，故第 k 层自身代价 Wₖ=Θ((n−2k)²)（非终止层）。",
height:"n−2h≤1，所以 h=⌈(n−1)/2⌉=Θ(n)。最底层基本情况另计 Θ(1)。",
total:"T(n) = Θ(1 + ∑ₖ₌₀ʰ⁻¹(n−2k)²)\n     = Θ(n²+(n−2)²+(n−4)²+⋯)\n     = Θ(n³)",
mistake:"要累加第 k 层循环次数的平方，而不是把 n−2k 直接相加。",
general:"第 k 层：1 × (n−2k)²；最后是平方数之和",
layers:[{vals:[["n","n²"]],w:"n²"},{vals:[["n−2","(n−2)²"]],w:"(n−2)²"},{vals:[["n−4","(n−4)²"]],w:"(n−4)²"}]
},
{
id:12,title:"减半递归 + 倍增循环",level:"进阶 · 对数代价",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 1; i < n; i *= 2) x++;\n    f(n / 2);\n}",
opts:["Θ(n)","Θ(log n)","Θ(n log n)","Θ((log n)²)"],answer:3,
recur:"T(n) = T(n/2) + Θ(log n)",
why:"i 每次乘 2，因此循环执行 Θ(log₂n) 次，而不是 n 次；只有一次 f(n/2)，故递归部分为 T(n/2)。",
layer:"第 k 层只有 1 个节点，规模 n/2ᵏ，非递归工作 Θ(log₂(n/2ᵏ))。若 n=2ʰ，则 Wₖ=Θ(h−k)。",
height:"n/2ʰ=1，所以 h=log₂n。",
total:"T(n) = Θ(1 + ∑ₖ₌₀ʰ⁻¹(h−k))\n     = Θ(1+h+(h−1)+⋯+1)\n     = Θ(h²)\n     = Θ((log n)²)",
mistake:"f(n)=log n 时，第 k 层要代入当前规模：log(n/2ᵏ)=log n−k，不能写成 n/2ᵏ。",
general:"第 k 层：1 × (log₂n−k)；共 h=log₂n 层",
layers:[{vals:[["n","log₂n"]],w:"log₂n"},{vals:[["n/2","log₂n−1"]],w:"log₂n−1"},{vals:[["n/4","log₂n−2"]],w:"log₂n−2"}]
},
{
id:13,title:"双分支减半 + 倍增循环",level:"进阶 · 和第12题对照",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 1; i < n; i *= 2) x++;\n    f(n / 2);\n    f(n / 2);\n}",
opts:["Θ(n)","Θ(n log n)","Θ((log n)²)","Θ(n²)"],answer:0,
recur:"T(n) = 2T(n/2) + Θ(log n)",
why:"本层倍增循环为 Θ(log n)；两次 f(n/2) 都执行，所以递归部分是 2T(n/2)。",
layer:"令 n=2ʰ。第 k 层有 2ᵏ 个节点；每个非叶节点自身代价 Θ(h−k)，故 Wₖ=Θ(2ᵏ(h−k))；第 h 层有 2ʰ 个常数代价叶节点。",
height:"n/2ʰ=1，故 h=log₂n。",
total:"T(n) = Θ(2ʰ + ∑ₖ₌₀ʰ⁻¹2ᵏ(h−k))\n     = Θ(n + 2ʰ∑ⱼ₌₁ʰj/2ʲ)\n     = Θ(n)，因为 ∑ⱼ₌₁∞j/2ʲ=2。",
mistake:"与第12题只有一次递归调用之差，但这一题的同层节点数是 2ᵏ，复杂度改变很大。",
general:"第 k 层：2ᵏ × (log₂n−k)；叶层 n 个节点",
layers:[{vals:[["n","log₂n"]],w:"log₂n"},{vals:[["n/2","log₂n−1"],["n/2","log₂n−1"]],w:"2(log₂n−1)"},{vals:[["n/4","log₂n−2"],["n/4","log₂n−2"],["n/4","log₂n−2"],["n/4","log₂n−2"]],w:"4(log₂n−2)"}]
},
{
id:14,title:"不等规模：减半与四分之一",level:"进阶 · 非对称递归",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 0; i < n; i++) x++;\n    f(n / 2);\n    f(n / 4);\n}",
opts:["Θ(log n)","Θ(n log n)","Θ(n)","Θ(n²)"],answer:2,
recur:"T(n) = T(n/2) + T(n/4) + Θ(n)",
why:"一重循环执行 n 次。随后两个递归调用分别处理 n/2 和 n/4 规模，不能写成 2T(n/2)。",
layer:"根节点代价为 n；第 1 层规模和 n/2+n/4=3n/4；第 2 层规模和 n/4+n/8+n/8+n/16=9n/16。后续非终止层的规模总和不超过 n(3/4)ᵏ。",
height:"最长路径始终选 n/2，故最大深度 Θ(log₂n)；较小分支先终止。",
total:"T(n) ≥ c n（根节点）。\n所有非终止节点的代价和 ≤ Cn∑ₖ₌₀∞(3/4)ᵏ=4Cn。\n因每个内部节点生成两子节点、且有至少常数代价，叶子总代价也是 O(n)。\n因此 T(n)=Θ(n)。",
mistake:"不能把这道题当成 2T(n/2)+n，否则会误判为 n log n。规模之和每层至多缩为 3/4。",
general:"第 k 层规模代价和 ≤ n(3/4)ᵏ",
layers:[{vals:[["n","n"]],w:"n"},{vals:[["n/2","n/2"],["n/4","n/4"]],w:"3n/4"},{vals:[["n/4","n/4"],["n/8","n/8"],["n/8","n/8"],["n/16","n/16"]],w:"9n/16"}]
},
{
id:15,title:"三分支折半递归",level:"进阶 · 非整数指数",
code:"void f(int n) {\n    if (n <= 1) return;\n    for (int i = 0; i < n; i++) x++;\n    for (int j = 0; j < 3; j++) f(n / 2);\n}",
opts:["Θ(n)","Θ(n log n)","Θ(n²)","Θ(n^(log₂3))"],answer:3,
recur:"T(n) = 3T(n/2) + Θ(n)",
why:"第一个循环是本次调用的 n 次操作；第二个循环固定执行 3 次，每次发起一次规模为 n/2 的递归，因此有 3 个子节点。",
layer:"第 k 层有 3ᵏ 个节点，每节点规模 n/2ᵏ，代价 Θ(n/2ᵏ)，故 Wₖ=Θ(n(3/2)ᵏ)，层代价逐渐增长。",
height:"问题规模每次减半：n/2ʰ=1，所以 h=log₂n。",
total:"T(n) = Θ(n∑ₖ₌₀ˡᵒᵍ²ⁿ(3/2)ᵏ)\n     = Θ(n(3/2)^(log₂n))\n     = Θ(n^(log₂3))。",
mistake:"3 决定每层节点数 3ᵏ，2 决定递归深度 log₂n；结果约为 n^1.585，并非 3ⁿ。",
general:"第 k 层：3ᵏ × (n/2ᵏ) = n(3/2)ᵏ",
layers:[{vals:[["n","n"]],w:"n"},{vals:[["n/2","n/2"],["n/2","n/2"],["n/2","n/2"]],w:"3n/2"},{vals:[["n/4 ×3","每组 3n/4"],["n/4 ×3","每组 3n/4"],["n/4 ×3","每组 3n/4"]],w:"9n/4",group:true,groupLabel:"第 2 层按 3 个节点一组折叠，共 9 个节点。"}]
}
];
