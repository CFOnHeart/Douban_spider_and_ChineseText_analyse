# Douban_spider_and_ChineseText_analyse
## 安装python 依赖
1. pip install pymongo
2. pip install lxml
3. pip install bs4

**本项目最主要的目的是为了构建用豆瓣上的评论信息所得的数据来构建中文语料库进行分析统计**

## 本模块主要有:
1. 负责采集豆瓣书籍数据的douban_book_spider.py
2. 负责mongodb数据库操作的mongodb.py
3. 负责处理豆瓣书籍数据对象的douban_book.py
4. 负责整理评论信息的用作语料库的text_presolve.py
5. 负责利用jieba分词工具对原文本文件进行分词的participal.py
6. 用于对文本分析词向量的my_word2vec.py

## 资源(resource)模块介绍
1. initial_text放入的是初始的未经过分词的文本
2. participal_text放入的是经过分词后的中文文本
3. word2vec_model保存的是word2vec过程保存下来的一些模型,方便之后加载
4. word_dictionary保存的是自定义的一些词典(用于更精确分词)的文本

## 源文件模块
1. data模块 存储各类数据对象,比如douban_book就是豆瓣上书籍信息的对象
2. db模块 存储各类数据库相关对象,比如mongodb,mysql
3. spider模块 存储对不同类型数据进行爬取的爬虫
4. text模块 是对于各类数据文件的文本进行处理的代码块

## 具体执行流程
执行测试代码是test.py,具体用到的文件执行过程如下:
1. 运行douban_book_spider.py中的代码
2. 运行text_presolve.py中的代码
3. 运行participal.py中的代码
4. 运行my_word2vec.py中的代码
