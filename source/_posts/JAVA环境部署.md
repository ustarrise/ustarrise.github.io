---
title: JAVA环境部署
typora-root-url: ..
date: 2023-09-07 21:26:51
tags: 环境部署
---

## Java环境部署教程

Java是一种广泛使用的编程语言，它具有跨平台、面向对象、高性能等特点。要开发和运行Java程序，我们需要先搭建Java开发环境，主要包括两个部分：JDK和IDE。

## JDK

JDK（Java Development Kit）是Java开发工具包，它提供了开发和调试Java程序所需的各种工具，如编译器、解释器、文档生成器等。JDK是Java编程的基础，没有它就无法进行Java开发。

目前，有两种主流的JDK版本：OracleJDK和OpenJDK。OracleJDK是由Oracle公司提供的商业化JDK版本，它包含了一些专有的特性和优化，但也有一些限制和收费条款。OpenJDK是由社区维护的开源免费的JDK版本，它遵循GPL协议，功能上与OracleJDK基本一致，但可能存在一些差异和兼容性问题。

在本教程中，我们使用OpenJDK作为示例，你也可以根据自己的喜好选择其他版本的JDK。下面是OpenJDK的下载和安装步骤：

### 下载OpenJDK

首先，我们需要从官网上下载OpenJDK的安装包，根据自己的操作系统和硬件架构选择合适的版本。下载地址为：[OpenJDK](https://www.oracle.com/java/technologies/downloads/)。

以Windows 10 64位系统为例，我们选择下载openjdk-15.0.1_windows-x64_bin.zip这个压缩包文件。

### 解压OpenJDK

下载完成后，我们需要将压缩包文件解压到一个合适的位置，例如D:\Java\jdk-15.0.1。解压后的文件夹结构如下图所示：



### 配置环境变量

为了让系统能够识别和使用JDK中的工具，我们需要配置一些环境变量。具体操作如下：

- 在桌面上右击“此电脑”，点击“属性”菜单，在打开的窗口中点击左侧的“高级系统设置”菜单；
- 在打开的“系统属性”窗口中点击下方的“环境变量”按钮；
- 在打开的“环境变量”窗口中点击“系统变量”栏中的“新建”按钮；
- 在打开的“新建系统变量”窗口中输入变量名和变量值，然后点击下方的“确定”按钮。变量名为JAVA_HOME，变量值为JDK解压后的文件夹路径（本例为D:\Java\jdk-15.0.1）；
- 在“环境变量”窗口中双击“系统变量”栏中的"Path"变量，在打开的“编辑环境变量”窗口中点击右侧的“新建”按钮，在弹出的输入框中输入``%JAVA_HOME%\bin`` ``%JAVA_HOME%\bin\jre``，并按回车键确认；
- 在“环境变量”窗口中点击底部的“确定”按钮，关闭所有窗口。

### 测试JDK是否安装成功

为了验证JDK是否安装成功，我们可以在命令行中执行一些简单的命令。具体操作如下：

- 按WIN + R快捷键打开“运行”窗口，输入cmd并按回车键打开“命令提示符”窗口；
- 在打开的窗口中输入javac -version和java -version命令并按回车键执行，如果能成功看到版本信息，则证明JDK已经安装成功。



## IDE

IDE（Integrated Development Environment）是集成开发环境，是用于提供程序开发环境的软件，它一般包括代码编辑器、编译器、调试器和图形用户界面等工具，集成了代码编写、分析、编译、调试等开发所需功能。使用IDE可以提高开发效率和质量，提升编程体验。

目前，市场上有很多优秀的IDE软件，如Eclipse、IntelliJ IDEA、Visual Studio Code等。在本教程中，我们使用Eclipse作为示例，你也可以根据自己的喜好选择其他IDE软件。下面是Eclipse的下载和安装步骤：

### 下载Eclipse

首先，我们需要从官网上下载Eclipse的安装包，根据自己的开发需求和硬件架构选择合适的版本。下载地址为：[Eclipse](http://www.eclipse.org/downloads/packages/)。

以Windows 10 64位系统为例，我们选择下载eclipse-jee-2020-09-R-win32-x86_64.zip这个压缩包文件。

### 解压Eclipse

下载完成后，我们需要将压缩包文件解压到一个合适的位置，例如D:\Java\eclipse。解压后的文件夹结构如下图所示：



### 启动Eclipse

在成功解压Eclipse后，打开Eclipse解压后所在的文件夹（本例为D:\Java\eclipse），双击“eclipse.exe”这个可执行文件就可以直接启动Eclipse软件了。为了方便后续使用，可以将该文件发送到桌面快捷方式。

启动Eclipse后，会弹出一个窗口，提示设置工作空间（Workspace），工作空间就是用于存放Java项目的文件夹。我们可以点击“Browse…”按钮进行修改或保持默认，然后点击底部的“Launch”按钮。



稍等片刻即可打开Eclipse主界面，可以直接关闭欢迎（Welcome）界面。



## 写出第一个Java程序

在成功搭建好Java开发环境后，我们就可以开始编写我们的第一个Java程序了。这里我们以经典的Hello World程序为例，演示如何使用Eclipse创建、编写、运行和调试Java程序。

### 创建Java项目

在Eclipse主界面中，依次点击菜单File --> New --> Java Project，在打开的窗口中输入项目名称（Project name），例如HelloWorld，其他配置项可以保持默认，然后点击底部的“Finish”按钮。



创建成功后，在左侧的Package Explorer视图中可以看到刚刚创建的项目文件夹HelloWorld。展开该文件夹，可以看到其中包含了一个名为src的源代码文件夹和一个名为JRE System Library的系统库文件夹。



## 创建Java类

在src文件夹下右击鼠标，在弹出的菜单中选择New --> Class，在打开的窗口中输入类名（Name），例如HelloWorld，并勾选“public static void main(String[] args)”选项，然后点击底部的“Finish”按钮。



创建成功后，在src文件夹下会生成一个名为HelloWorld.java的源代码文件，并在右侧的编辑器视图中打开该文件。此时该文件已经包含了一个名为HelloWorld的类定义和一个名为main的方法定义。



