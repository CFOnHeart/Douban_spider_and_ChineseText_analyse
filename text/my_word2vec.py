#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models import word2vec
import logging
import os

def init_loginfo():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 加载语料文件,返回语料模型
def load_corpus(filename, size=200):
    if os.path.exists(filename) == False:
        print "Error: 你要加载的语料文件 "+filename+" 不存在"
    sentences = word2vec.Text8Corpus(filename)  # 加载语料
    model = word2vec.Word2Vec(sentences, size=size)  # 默认window=5
    return model

# 保存语料模型
def save_model(model, model_name):
    if os.path.exists('resource/word2vec_model/'+model_name) == True:
        print "Warnning: 你要加载的语料模型 "+model_name+" 已经存在"
        while True:
            print "输入Y/N(Y表示覆盖此模型文件,N表示不保存当前模型),按回车结束: "
            val = raw_input()
            if val[0] == 'Y' and len(val) == 1:
                model.save('resource/word2vec_model/'+model_name)
                print "Logging: 你要保存的语料模型 "+model_name+" 已经成功覆盖"
                break
            elif val[0] == 'N' and len(val) == 1:
                print "Logging: 你已经取消保存语料模型 "+model_name
                break
    else:
        model.save('resource/word2vec_model/'+model_name)
        print "Logging: 你要保存的语料模型 "+model_name+" 已经成功保存"

# 加载语料模型
def load_model(model_name):
    if os.path.exists('resource/word2vec_model/'+model_name) == False:
        print "Error: 你要加载的语料模型 "+model_name+" 不存在"
    return word2vec.load('resource/word2vec_model/'+model_name)


def test():
    model = load_corpus("resource/participal_text/douban_comments_participal.txt")
    # 计算某个词的相关词列表
    y2 = model.most_similar(u"重要", topn=10)  # 2个最相关的
    print u"和【重要】最相关的词有：\n"
    for item in y2:
        print item[0], item[1]
    print "--------\n"
    # 计算两个词的相似度/相关程度
    y1 = model.similarity(u"故事", u"小说")
    print u"【故事】和【小说】的相似度为：", y1

    # 将模型保存下来,方便以后直接加载
    save_model(model, 'douban_book_comments.model')