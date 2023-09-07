---
title: Git
date: 2023-09-03 22:56:50
tags: 这是Git
typora-root-url: ..
---

## 重中之重——先拉代码

每次提交代码之前，养成良好的习惯，先 `pull` 一下代码。不 `pull` 代码万一导致代码冲突了就不美了。

```
命令： git pull
```

> 中间插一句：要会使用`git status`，嗯，对，没错，就是要会使用这个。
>
> 随时敲`git status` 随时有惊喜。

### 第一步：把更改的代码暂存起来

```
# 此命令会把所有更改的文件全部暂存起来。
git add . 

# 如果要单个来，只需要 . 替换成对应的文件名即可。
git add temp.txt
```

> 若出现 LF will be replaced by CRLF the next time Git touches it的''warning'',则是因为跨平台的问题

:point_right: [ 图片插入解决办法 ](https://www.cnblogs.com/himeka/p/16306906.html):point_left:

![image-20230904000116190](/images/Git/image-20230904000116190.png)

### 第二步：把暂存的改动提交到本地的版本库

```
# -m 参数表示可以直接输入后面的 message，简要说明这次改动。
git commit -m "xxx"

加的 -a 参数可以将所有已跟踪文件中的执行修改或删除操作的文件都提交到本地仓库，即使它们没有经过git add添加到暂存区。
如：git commit -a -m "xxx"
```

> 每次 `git commit`之后，都会在本地版本库中生成一个 哈希值，就是 `commit-id`,这个 id 在进行版本回退的时候有大用。

:smiling_imp:[点击这里了解怎么获取指定的历史版本代码](https://blog.csdn.net/s_y_w123/article/details/107087382) :innocent:

> ``git remote -v``用来获取远程仓库的名称和URL

## 【Git】如何进行分支合并

> 通常会在 Git上建立多个分支，以方便代码的管理与维护，比如【master-dev】开发模型，这种开发模型就是 master存放已完成的代码，而 dev是平常用来开发的分支，开发完成后再将 dev分支合并到 master分支，当然有的大型项目还会有 bugfix这种专门修bug的分支或者有 product等等其他分支

 :fish: **git提交到远程分支，并提出合并请求（没有的话会新建）**

```
#创建项目
git init
#暂存区
git add . ,然后 git commit -m "备注名"

git remote add 远程仓库别名 远程仓库地址

git fetch 远程仓库别名

git branch -a //查看是否关联

git push 远程仓库别名 本地分支名:远程分支名
```



 :ram:**本地分支间的合并**

> 比如，我在本地分支dev开发完一个功能后，先要把dev合并到本地的master分支，然后再推到远程仓库
> 先从dev分支切换到master分支，使用checkout命令
> ``git checkout master``
> 这样就从当前分支（也就是dev分支）分支切换到了master分支
> 现在我们已经位于master分支了，那么接下来就需要用merge命令来进行分支间的合并
> `` git merge dev``

键入这个命令后我们就成功地将本地的dev合并到了master分支上，之后再使用push ``git push <本地分支名称>``命令将本地的分支推送到远程仓库就可以啦

:goat:**远程分支合并到本地分支**

> 远程分支合并到本地分支的前提是已经将dev分支的代码提交到远程仓库，那么此时远程仓库中的dev分支就是已经开发完成的代码。然后我们直接使用checkout命令从dev分支切换到master分支，接着使用pull命令将远程仓库的代码拉到本地的master即可
> ``git pull <远程仓库名称> <远程分支名称>``
> 之后我们就可以使用push命令把本地的分支合并到远程仓库啦
> ``git push <远程仓库名> <本地分支名称>``

## github文件夹有白色箭头并且不能打开的解决方案：

> 如果源码仓库里面别人的项目，导致[github](https://github.com/)这个文件夹上显示白色箭头并且不能打开。

> 原来是因为这个文件夹里面有.git隐藏文件，github就将他视为一个子系统模块了。
>
> 解决办法就是：
>
> 1、删除文件夹里面的.git文件夹
>
> 2、``git rm --cached [文件夹名]``
>
> 3、``git add [文件夹名]``
>
> 4、``git commit -m "msg"``
>
> 5、``git push origin [branch_name] ``
