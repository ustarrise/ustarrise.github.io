---
title: Linux
date: 2023-09-03 19:46:51
tags:
---

> 这是一个引用

> 引用完之后要退出引用并且换行使用两个“Enter”

> 如果要使用web访问虚拟机的IP，可能需要关闭防火墙。

## Linux常规指令:

> 1.文件结构:

```linux
/bin        二进制文件，系统常规命令
/boot       系统启动分区，系统启动时读取的文件
/dev        设备文件
/etc        大多数配置文件
/home       普通用户的家目录
/lib        32位函数库
/lib64      64位库
/media      手动临时挂载点
/mnt        手动临时挂载点
/opt        第三方软件安装位置
/proc       进程信息及硬件信息
/root       临时设备的默认挂载点
/sbin       系统管理命令
/srv        数据
/var        数据
/sys        内核相关信息
/tmp        临时文件
/usr        用户相关设定

```

> 2.关闭/重启系统:

```
关机操作:
(1)立刻关机
  shutdown -h now 或者 poweroff
(2)两分钟后关机
  shutdown -h 2
重启操作:  
  (1)立刻重启
  shutdown -r now 或者 reboot
(2)两分钟后重启
  shutdown -r 2 

```

>命令说明

```
  ifconfig  --help     //查看 ifconfig 命令的用法
  man shutdown         //打开命令说明后，可按"q"键退出
  su yao               //切换为用户"yao",输入后回车需要输入该用户的密码
  exit                 //退出当前用户
```

## 目录操作:

1. ### 切换目录(cd)

2. ### 查看目录(ls):

   ```
     ls                   //查看当前目录下的所有目录和文件
     ls -a                //查看当前目录下的所有目录和文件（包括隐藏的文件）
     ls -l                //列表查看当前目录下的所有目录和文件（列表查看，显示更多信息），与命令"ll"效果一样
     ls /bin              //查看指定目录下的所有目录和文件 
   ```

   

3. ### 创建目录（mkdir）/ 删除目录(rm) /修改目录(mv) /拷贝目录(cp):

   ```
     mkdir tools          //在当前目录下创建一个名为tools的目录
     mkdir /bin/tools     //在指定目录下创建一个名为tools的目录
   
     rm 文件名              //删除当前目录下的文件
     rm -f 文件名           //删除当前目录的的文件（不询问）
     rm -r 文件夹名         //递归删除当前目录下此名的目录
     rm -rf 文件夹名        //递归删除当前目录下此名的目录（不询问）
     rm -rf *              //将当前目录下的所有目录和文件全部删除
     rm -rf /*             //将根目录下的所有文件全部删除【慎用！相当于格式化系统】
   
     mv 当前目录名 新目录名        //修改目录名，同样适用与文件操作
     mv /usr/tmp/tool /opt       //将/usr/tmp目录下的tool目录剪切到 /opt目录下面
     mv -r /usr/tmp/tool /opt    //递归剪切目录中所有文件和文件夹
     
     cp /usr/tmp/tool /opt       //将/usr/tmp目录下的tool目录复制到 /opt目录下面
     cp -r /usr/tmp/tool /opt    //递归剪复制目录中所有文件和文件夹
   
     find /bin -name 'a*'        //查找/bin目录下的所有以a开头的文件或者目录
       find . -name "*.c"     //将目前目录及其子目录下所有延伸档名是 c 的文件列出来
     find . -type f         //将目前目录其其下子目录中所有一般文件列出
     find . -ctime -20      //将目前目录及其子目录下所有最近 20 天内更新过的文件列出
     find /var/log -type f -mtime +7 -ok rm {} \;     //查找/var/log目录中更改时间在7日以前的普通文件，并在删除之前询问它们
     find . -type f -perm 644 -exec ls -l {} \;       //查找前目录中文件属主具有读、写权限，并且文件所属组的用户和其他用户具有读权限的文件
     find / -type f -size 0 -exec ls -l {} \;         //为了查找系统中所有文件长度为0的普通文件，并列出它们的完整路径
   
   
     pwd                         //显示当前位置路径
   
      touch  a.txt         //在当前目录下创建名为a的txt文件（文件不存在），如果文件存在，将文件时间属性修改为当前系统时间
   ```

   

## 编辑文件（vi、vim）

```
  vi 文件名              //打开需要编辑的文件
  --进入后，操作界面有三种模式：命令模式（command mode）、插入模式（Insert mode）和底行模式（last line mode）
  命令模式
  -刚进入文件就是命令模式，通过方向键控制光标位置，
  -使用命令"dd"删除当前整行
  -使用命令"/字段"进行查找
  -按"i"在光标所在字符前开始插入
  -按"a"在光标所在字符后开始插入
  -按"o"在光标所在行的下面另起一新行插入
  -按"："进入底行模式
  插入模式
  -此时可以对文件内容进行编辑，左下角会显示 "-- 插入 --""
  -按"ESC"进入底行模式
  底行模式
  -退出编辑：      :q
  -强制退出：      :q!
  -保存并退出：    :wq
  ## 操作步骤示例 ##
  1.保存文件：按"ESC" -> 输入":" -> 输入"wq",回车     //保存并退出编辑
  2.取消操作：按"ESC" -> 输入":" -> 输入"q!",回车     //撤销本次修改并退出编辑
  ## 补充 ##
  vim +10 filename.txt                   //打开文件并跳到第10行
  vim -R /etc/passwd                     //以只读模式打开文件

```

## 查看文件

```
  cat a.txt          //查看文件最后一屏内容
  less a.txt         //PgUp向上翻页，PgDn向下翻页，"q"退出查看
  more a.txt         //显示百分比，回车查看下一行，空格查看下一页，"q"退出查看
  tail -100 a.txt    //查看文件的后100行，"Ctrl+C"退出查看

```

## 文件权限

```
  文件权限简介：'r' 代表可读（4），'w' 代表可写（2），'x' 代表执行权限（1），括号内代表"8421法"
  ##文件权限信息示例：-rwxrw-r--
  -第一位：'-'就代表是文件，'d'代表是文件夹
  -第一组三位：拥有者的权限
  -第二组三位：拥有者所在的组，组员的权限
  -第三组三位：代表的是其他用户的权限

  普通授权    chmod +x a.txt    
  8421法     chmod 777 a.txt     //1+2+4=7，"7"说明授予所有权限

  .zip、.rar        //windows系统中压缩文件的扩展名
  .tar              //Linux中打包文件的扩展名
  .gz               //Linux中压缩文件的扩展名
  .tar.gz           //Linux中打包并压缩文件的扩展名

```

## 打包与解压

```
  .zip、.rar        //windows系统中压缩文件的扩展名
  .tar              //Linux中打包文件的扩展名
  .gz               //Linux中压缩文件的扩展名
  .tar.gz           //Linux中打包并压缩文件的扩展名

  tar -zcvf 打包压缩后的文件名 要打包的文件
  参数说明：z：调用gzip压缩命令进行压缩; c：打包文件; v：显示运行过程; f：指定文件名;
  示例：
  tar -zcvf a.tar file1 file2,...      //多个文件压缩打包

  tar -zxvf a.tar                      //解包至当前目录
  tar -zxvf a.tar -C /usr------        //指定解压的位置
  unzip test.zip             //解压*.zip文件 
  unzip -l test.zip          //查看*.zip文件的内容 

```

>   whereis ls             //将和ls文件相关的文件都查找出来
>
>   说明：which指令会在环境变量$PATH设置的目录里查找符合条件的文件。
>   which bash             //查看指令"bash"的绝对路径
>
>   grep -i "the" demo_file              //在文件中查找字符串(不区分大小写)
>   grep -A 3 -i "example" demo_text     //输出成功匹配的行，以及该行之后的三行
>   grep -r "ramesh" *                   //在一个文件夹中递归查询包含指定字符串的文件

## server ,free :

```
  说明：service命令用于运行System V init脚本，这些脚本一般位于/etc/init.d文件下，这个命令可以直接运行这个文件夹里面的脚本，而不用加上路径
  service ssh status      //查看服务状态 
  service --status-all    //查看所有服务状态 
  service ssh restart     //重启服务 

  说明：这个命令用于显示系统当前内存的使用情况，包括已用内存、可用内存和交换内存的情况 
  free -g            //以G为单位输出内存的使用量，-g为GB，-m为MB，-k为KB，-b为字节 
  free -t            //查看所有内存的汇总

```

## top,df ,mount:

```
  top               //显示当前系统中占用资源最多的一些进程, shift+m 按照内存大小查看

  说明：显示文件系统的磁盘使用情况
  df -h            //一种易看的显示

  mount /dev/sdb1 /u01              //挂载一个文件系统，需要先创建一个目录，然后将这个文件系统挂载到这个目录上
  dev/sdb1 /u01 ext2 defaults 0 2   //添加到fstab中进行自动挂载，这样任何时候系统重启的时候，文件系统都会被加载 

```

>   说明：uname可以显示一些重要的系统信息，例如内核名称、主机名、内核版本号、处理器类型之类的信息 
>   uname -a

## yum,rpm,wget:

```
  说明：安装插件命令
  yum install httpd      //使用yum安装apache 
  yum update httpd       //更新apache 
  yum remove httpd       //卸载/删除apache 

  说明：插件安装命令
  rpm -ivh httpd-2.2.3-22.0.1.el5.i386.rpm      //使用rpm文件安装apache 
  rpm -uvh httpd-2.2.3-22.0.1.el5.i386.rpm      //使用rpm更新apache 
  rpm -ev httpd                                 //卸载/删除apache 

  说明：使用wget从网上下载软件、音乐、视频 
  示例：wget http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.2.1.tar.gz
  //下载文件并以指定的文件名保存文件
  wget -O nagios.tar.gz http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.2.1.tar.gz

```

>    ftp IP/hostname    //访问ftp服务器
>    mls *.html -       //显示远程主机上文件列表
>
>    ​	scp /opt/data.txt  192.168.1.101:/opt/    //将本地opt目录下的data文件发送到192.168.1.101服务器的opt目录下

## 系统管理:

1. ## 防火墙:

   ```
     service iptables status      //查看iptables服务的状态
     service iptables start       //开启iptables服务
     service iptables stop        //停止iptables服务
     service iptables restart     //重启iptables服务
     chkconfig iptables off       //关闭iptables服务的开机自启动
     chkconfig iptables on        //开启iptables服务的开机自启动
     ##centos7 防火墙操作
     systemctl status firewalld.service     //查看防火墙状态
     systemctl stop firewalld.service       //关闭运行的防火墙
     systemctl disable firewalld.service    //永久禁止防火墙服务
   ```

2. ## 修改主机名（CentOS 7）:

   > ```
   > hostnamectl set-hostname 主机名
   > 
   > ifconfig      //查看网络
   > ```

   

3. ## 修改IP:

```
  修改网络配置文件，文件地址：/etc/sysconfig/network-scripts/ifcfg-eth0
  ------------------------------------------------
  主要修改以下配置：  
  TYPE=Ethernet               //网络类型
  BOOTPROTO=static            //静态IP
  DEVICE=ens00                //网卡名
  IPADDR=192.168.1.100        //设置的IP
  NETMASK=255.255.255.0       //子网掩码
  GATEWAY=192.168.1.1         //网关
  DNS1=192.168.1.1            //DNS
  DNS2=8.8.8.8                //备用DNS
  ONBOOT=yes                  //系统启动时启动此设置
  -------------------------------------------------
  修改保存以后使用命令重启网卡：service network restart

```

## 配置映射:

```
  修改文件： vi /etc/hosts
  在文件最后添加映射地址，示例如下：
   192.168.1.101  node1
   192.168.1.102  node2
   192.168.1.103  node3
  配置好以后保存退出，输入命令：ping node1 ，可见实际 ping 的是 192.168.1.101。

```

## 查看进程,结束进程:

```
  ps -ef         //查看所有正在运行的进程
  kill pid       //杀死该pid的进程
  kill -9 pid    //强制杀死该进程   
```

>   ping IP        //查看与此IP地址的连接情况
>   netstat -an    //查看当前系统端口
>   netstat -an | grep 8080     //查看指定端口



## 重定向符：

> 重定向“>”会自动创建新的文件，不需要提前touch；
>
> 重定向“>”会覆盖文件原本的内容。

```
ls > /home/test/output.txt

#那么，以上指令就会把ls在屏幕上输出的内容写到/home/test/output.txt（如果文件不存在会自动创建，但目录必须存在）文件中，屏幕上不会存在输出。
```

> 假设不存在/bin/usr目录

```
“2>”
ls /bin/usr 2> ls-error.txt
文件描述符“2”紧放在重定向符之前，将标准错误重定向到ls-error.txt文件中。  ---作用是列出 /bin/usr 目录下的文件，并把标准错误重定向到 ls-error.txt 文件中。如果 /bin/usr 目录不存在，那么这个命令会产生一个错误信息，比如：

ls: cannot access ‘/bin/usr’: No such file or directory

这个错误信息就是标准错误，它是一种输出流，用来显示程序运行过程中的异常或者问题。标准错误的文件描述符是 2，也就是说，它是第二个打开的文件。文件描述符是一个整数，用来标识一个打开的文件。


“2>&1”
ls /bin/usr > ls-output.txt 2>&1
执行两个重定向操作，首先重定向标准输出到ls- output.txt文件中，然后使用标记符2>&1把文件描述符2（标准错误）重 定向到文件描述符1（标准输出）中。

"&>"
ls /bin/usr &> ls-output.txt
表示把标准输出和标准错误都重 定向到了ls-output.txt文件中。
```

| 符号                | 作用                                         |
| ------------------- | -------------------------------------------- |
| 命令 < 文件         | 将文件作为命令的标准输入                     |
| 命令 << 分界符      | 从标准输入中读入，直到遇到分界符停止         |
| 命令 < 文件1 >文件2 | 将文件1作为命令的标准输入并将标准输出到文件2 |



| 符号                             | 作用                                                 |
| -------------------------------- | ---------------------------------------------------- |
| 命令 > 文件                      | 将标准输出重定向到文件中（清除原有文件中的数据）     |
| 命令 2> 文件                     | 将错误输出重定向到文件中（清除原有文件中的数据）     |
| 命令 >> 文件                     | 将标准输出重定向到文件中（在原有的内容后追加）       |
| 命令 2>> 文件                    | 将错误输出重定向到文件中（在原有内容后面追加）       |
| 命令 >> 文件 2>&1或命令 &>> 文件 | 将标准输出和错误输出共同写入文件（在原有内容后追加） |

## 一些补充命令

### 1.alias

> 通常情况下alias命令适合下面场景：
>
> - 简化过长且过于复杂的命令
> - 记住复杂名称的命令
> - 使用你经常使用的命令节省时间

例如，设置一个别名列出所有文件包括隐藏文件，别名为la：

```linux
[root@server1 ~]# alias la='ls -al'
```

> 这时候执行``la``将相当于执行了``ls-al``

如果要永久使用，可以将该命令写入`~/.bashrc`文件里面。

```linux
[root@server1 ~]# echo "alias la='ls -al'" >> ~/.bashrc
```

使用alias命令列出系统中已设置的所有别名：

```linux
[root@server1 ~]# alias
```

**检查命令类型是否是别名**

要检查命令是否为别名，请使用`which`命令。如下实例显示的内容就是别名。

```linux
[root@server1 ~]# which la
alias la='ls -al'
/usr/bin/ls
```

**删除alias**

如果需要停用别名，则可以使用unalias命令。要使更改永久生效，就需要在`~/.bashrc`文件中删掉对应的别名。

```linux
[root@server1 ~]# unalias la
```

**使用alias来更改命令的行为**

例如，想让ping命令只请求4次，则可以使用此别名确保它仅发出四个ping请求：

```linux
[root@server1 ~]# alias ping='ping -c 4'
```









## :fish:Docker

-  **docker基本命令**

  ```
  port  	  # 查看映射端口对应的容器内部源端口
  pause	  # 暂停容器
  ps        # 猎户容器列表
  pull      # 从docker镜像源服务器拉取指定镜像或者库镜像
  push      # 推送指定镜像或者库镜像至docker源服务器
  restart   # 重启运行的容器
  rm        # 移除一个或多个容器
  rmi       # 移除一个或多个镜像 （无容器使用该镜像才可删除，否则需要删除相关容器才可继续或 -f 强制删除）
  run       # 创建一个新的容器并运行一个命令
  save      # 保存一个镜像为一个 tar 包【对应 load】
  search    # 在 docker hub 中搜索镜像
  start     # 启动容器
  stop      # 停止容器
  tag       # 给源中镜像打标签
  top       # 查看容器中运行的进程信息
  unpause   # 取消暂停容器
  version   # 查看 docker版本号
  wait      # 截取容器停止时的退出状态值
  ```

  ## :crystal_ball:Docker学习链接:cd:

- ### :santa:[Docker学习路线1：介绍Docker以及和虚拟机区别等](https://www.kuangstudy.com/bbs/1678007219134005250)

- ### :santa:[Docker学习路线2：底层技术-包括内核等](https://www.kuangstudy.com/bbs/1678730316862586882)

- ### :santa:[Docker学习路线3：Docker基础知识讲一讲dockerfile、images等概念](https://www.kuangstudy.com/bbs/1679497237430140930)

- ### :santa:[Docker学习路线4：在 Docker 中实现数据持久化-包括卷挂载等技术](https://www.kuangstudy.com/bbs/1679811291919069186)

- ### :santa:[Docker学习路线5：构建容器镜像-Dcokerfile](https://www.kuangstudy.com/bbs/1681269951371296769)

- ### :santa:[Docker学习路线6：运行容器](https://www.kuangstudy.com/bbs/1682360165967736834)

- ### :santa:[Docker学习路线7：Docker命令行-实战使用的命令几乎都在这里](https://www.kuangstudy.com/bbs/1683856723091550209)

  ## MobaxTerm
