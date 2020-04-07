# R3K_KBQA
## 简介

![问答系统GUI界面](pics/gui.png)

一个基于模板的三国演义KBQA系统，能够简单的回答给定模板的问题。

本项目完成了从建立知识库、处理数据生成三元组到搭建问答系统（命令行和图形化）的一系列过程。此外，KBQA系统还具有一定的异常处理的功能设计。

这是一个课程的作业，作业任务在[这里](https://github.com/nju-websoft/NJU_KEPractice)。完整的作业报告为“[基于知识库的问答实践说明文档.pdf](基于知识库的问答实践说明文档.pdf)”，里面包括各部分的详细解释。

如果对你有帮助，麻烦**点个小星星🤣**！

## 运行说明

KBQA问答系统位于`R3K-KBQA`文件夹中，运行问答系统，请按照以下步骤操作：

1. 将三元组导入Virtuoso数据库

   Graph的名称设为“R3K”。你也可以命名为其他名称，只需在“config.py”文件中做相应的修改。具体操作略。

2. 安装Python所需要的库

   本工程所需要的库为包括：REfO、SPARQLWrapper、Flask，可以使用以下命令进行安装：

   ```bash
   pip install refo sparqlwrapper flask
   ```

3. 运行程序

   图形界面：

   ```bash
   python gui_app.py
   ```

   命令行界面：

   ```bash
   python cli_app.py
   ```

## 文件说明

- KB_Construction：生成三元组数据的代码，和生成的三元组数据。
- R3K-KBQA：KBQA问答系统。

## 参与和贡献者

我和WYX同学。