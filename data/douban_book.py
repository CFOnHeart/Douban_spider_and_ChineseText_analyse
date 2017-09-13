# coding=utf8

from db import mongodb


class Douban_book:

    def __init__(self, author, publisher, book_name, publish_date, price, ISBN, content, comment):
        self.author = author
        self.publisher = publisher
        self.book_name = book_name
        self.publish_date = publish_date
        self.price = price
        self.ISBN = int(ISBN)
        self.content = content
        self.comment = comment


# 将book保存到对应的mongodb的表对象中
def write_douban_books_to_mongodb(book, collection):
    mongo = mongodb.Mongodb('localhost', 27017)
    collection = mongo.get_collection("douban", "book")

    info = {
        'author': book.author,
        'publisher': book.publisher,
        'book_name': book.book_name,
        'publish_date': book.publish_date,
        'price': book.price,
        'ISBN': book.ISBN,
        'content': book.content,
        'comment': book.comment
    }
    # 判断此书是否已经存在于数据库中,如果已经存在相同的,则不再插入
    ret = mongo.insert_data(collection, info)
    if ret == 1:
        collection.insert_one(info)
        print u"Logging: 书名为: " + book.book_name + u" 的书成功存入mongodb"
    elif ret == 0:
        print u"Warning: 书名为: " + book.book_name + u" 未能存入mongodb,因为有相同ISBN的书存在"

# 在douban数据库bookcollection,读取满足data字典的所有数据信息,得到的是一个字典的列表
# 函数返回一个Douban_book对象的列表
def read_douban_books_from_mongodb(collection, data={}):
    mongo = mongodb.Mongodb('localhost', 27017)
    collection = mongo.get_collection("douban", "book")
    data_list = mongo.get_datainfo(collection, data)
    book_list = []
    for item in data_list:
        author = item['author']
        publisher = item['publisher']
        book_name = item['book_name']
        publish_date = item['publish_date']
        price = item['price']
        ISBN = item['ISBN']
        content = item['content']
        comment = item['comment']
        book = Douban_book(author, publisher, book_name, publish_date, price, ISBN, content, comment)
        book_list.append(book)
    return book_list


