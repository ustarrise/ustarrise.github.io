# 408 Algorithm Lab

这是独立于个人博客的考研 408 数据结构算法学习站，网页入口为 `408-algorithm/index.html`。

## GitHub Pages

此目录放在仓库 `ustarrise/ustarrise.github.io` 的 `master` 分支下。若 GitHub Pages 选择 **Deploy from a branch → master → /(root)**，预计访问地址为：

https://ustarrise.github.io/408-algorithm/

注意：仓库提交成功不等于 Pages 已启用；部署状态请在仓库 Settings → Pages 查看。

## 每日更新

- 网页框架：`index.html`（无需每天修改）
- 题库内容：`lessons.json`（JSON 数组，旧题保留，追加新题）
- 唯一题目键：`id`；`date` 用于排序
- 每题包含：`brute` / `optimal` 的完整 C 程序、中文注释与解析；`variation` 含巩固题和参考答案
- `animation.brute`、`animation.optimal` 是帧数组。每帧提供 `text` 解释和 `array`、`rows` 或 `diagram` 之一。链表演示可设置 `animation.layout=chains` 和 `animation.rows` 的基础数据。

网站所有新题均应满足 408 考纲。来源不确定时明确注明原创类题，而不虚构年份或题号。

原有博客文件未修改。