# coding=utf-8
import codecs

from data import douban_book
from db import mongodb


# 将douban图书的评论信息保存到文件中,用作语料库
def write_douban_comment(filename):
    file = codecs.open(filename, "w", 'utf-8')
    mongo = mongodb.Mongodb("localhost", 27017);
    book_list = douban_book.read_douban_books_from_mongodb(mongo.get_collection("douban", "book"))
    for book in book_list:
        file.write(book.comment+u"\n")
    mongo.close_mongodb()
    pass

# 下方完成了将豆瓣评论信息从数据库加载到对应文件中
if __name__ == "__main__":
    write_douban_comment("douban_comments.txt")
