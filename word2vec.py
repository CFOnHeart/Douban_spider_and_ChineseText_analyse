#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models import word2vec
import logging

# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus(u"亚马逊书评.txt")  # 加载语料
print sentences
model = word2vec.Word2Vec(sentences, size=200)  # 默认window=5
# 计算某个词的相关词列表
y2 = model.most_similar(u"创业", topn=2)  # 2个最相关的
print u"和【创业】最相关的词有：\n"
for item in y2:
    print item[0], item[1]
print "--------\n"
# 计算两个词的相似度/相关程度
y1 = model.similarity(u"创业", u"时代")
print u"【创业】和【时代】的相似度为：", y1

# 将模型保存下来,方便以后直接加载
model.save(u"书评.model")
