# coding=utf-8

import sys
import gensim
import sklearn
import numpy as np

from gensim.models.doc2vec import Doc2Vec, LabeledSentence

TaggededDocument = gensim.models.doc2vec.TaggedDocument

# 返回文档的gensim.models.doc2vec.TaggedDocument对象列表
def get_datasest():
    # 这里要打开一个分好词的文件,中文文件因为编码原因打开的话需要codecs库codecs.open(filename, op, 'utf-8')
    with open("../resource/aclImdb/Readme", 'r') as cf:
        docs = cf.readlines()
        print len(docs)

    x_train = []
    #y = np.concatenate(np.ones(len(docs)))
    for i, text in enumerate(docs):
        print i, text
        word_list = text.split(' ')
        l = len(word_list)
        word_list[l-1] = word_list[l-1].strip()
        print "word_list: ", word_list, [i]
        # word_list是内容每一行分词后的数组
        document = TaggededDocument(word_list, tags=[i])
        print "document: ", document
        x_train.append(document)

    return x_train

def getVecs(model, corpus, size):
    vecs = [np.array(model.docvecs[z.tags[0]].reshape(1, size)) for z in corpus]
    return np.concatenate(vecs)

# x_train是加载数据得到的gensim.models.doc2vec.TaggedDocument对象列表
def train(x_train, size=200, epoch_num=1):
    model_dm = Doc2Vec(x_train, min_count=1, window=3, size=size, sample=1e-3, negative=5, workers=4)
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=70)
    model_dm.save('../resource/model/aclImdb_Readme.model')

    return model_dm

def test():
    model_dm = Doc2Vec.load("../resource/model/aclImdb_Readme.model")
    test_text = ['There', 'are', 'so' 'many', 'reviews']
    inferred_vector_dm = model_dm.infer_vector(test_text)
    # inferred_vector_dm就是对应文本得到的向量.
    print "check the text vector: ",inferred_vector_dm
    # model_dm.docvecs.most_similar函数是对对应地文本向量找到相近的前topn个文本
    sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=10)
    return sims

if __name__ == '__main__':
    x_train = get_datasest()
    model_dm = train(x_train)

    sims = test()
    for count, sim in sims:
        sentence = x_train[count]
        words = ''
        for word in sentence[0]:
            words = words + word + ' '
        print words, sim, len(sentence[0])

