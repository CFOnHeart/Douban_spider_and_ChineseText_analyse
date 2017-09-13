# coding=utf-8

import jieba
import jieba.posseg as pseg
from jieba import analyse
import codecs
import os

# 读取文章内容
def read_article(filename):
    f_in = codecs.open(filename, 'r', 'utf-8')
    lines = f_in.readlines()
    comments = u""
    for line in lines:
        comments += line
    return comments

# 对input_file进行分词,将中文分词好的内容输出到output_file中
def text_participle(input_file, output_file):
    f_in = codecs.open(input_file, 'r', 'utf-8')
    f_out = codecs.open(output_file, 'w', 'utf-8')
    lines = f_in.readlines()
    comments = u""
    for line in lines:
        comments += line

    # 精确模式
    seg_list = jieba.cut(comments, cut_all=False)
    f_out.write(" ".join(seg_list))

    f_in.close()
    f_out.close()

# 对text文本内容提取前topk个关键词
def text_keywords_extract(text, topk):
     #获取关键词
    tags = analyse.extract_tags(text, topK=topk)
    return tags

# 载入词典,增加的词典文件均放在resource/word_dictionary文件下
def add_dictionary(dic):
    if os.path.exists(dic) == False:
        print "需要加载的字典文件: "+dic+" 不存在"
    else:
        jieba.load_userdict(dic)
        print "需要加载的字典文件: "+dic+" 已经成功加载"

# 对text词性标注
def part_of_speech(text):
    words = pseg.cut(text, HMM=True)
    # 每一个元素中包含了词语word和词性flag两个量
    # for word, flag in words:
    #     print('%s %s' % (word, flag))
    return words

# 下方是对本脚本的测试代码,完成了对豆瓣评论文件的分词操作后保存
if __name__ == "__main__":
    add_dictionary('resource/word_dictionary/comment_dic.txt')
    text_participle('resource/initial_text/douban_comments.txt', 'resource/participal_text/douban_comments_participal.txt')

