# coding=utf-8
import douban_book
import mongodb
import codecs
# 将douban图书的评论信息保存到文件中,用作语料库
def write_douban_comment(filename):
    file = codecs.open(filename, "w" , 'utf-8')
    mongo = mongodb.Mongodb("localhost", 27017);
    book_list = douban_book.read_douban_books_from_mongodb(mongo.get_collection("douban", "book"))
    for book in book_list:
        file.write(book.comment+u"\n")
    mongo.close_mongodb()
    pass


write_douban_comment("douban_comments.txt")
