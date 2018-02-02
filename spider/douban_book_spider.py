# coding=utf8

import re

import pymongo
import requests
from bs4 import BeautifulSoup

from data import douban_book

# 激活一次与页面的链接，'Connection': 'keep-alive'保持活力，那么之后不需要cookie也能进入了
def activate_cookie(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control':   'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'bid=EjVfNuCFCCc; __yadk_uid=p7eO16BlyhEZGRS5OFrIZLONj1oQIFfJ; gr_user_id=9f9ee961-658f-4d94-9064-6456ddc74420; ll="118159"; _vwo_uuid_v2=6F188EB37C02AF8DC97FD5D1A469D383|c652b51c9b96af699095d2f2d5378abe; ps=y; __utma=30149280.185030239.1505136888.1514481776.1517553762.19; __utmc=30149280; __utmz=30149280.1517553762.19.16.utmcsr=open.weixin.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/connect/qrconnect; push_noty_num=0; push_doumail_num=0; gr_cs1_0d411a4f-9fb6-4843-8b80-83a66830df18=user_id%3A1; ap=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1517555178%2C%22https%3A%2F%2Fbook.douban.com%2Fsubject%2F2230208%2F%22%5D; _pk_ses.100001.8cb4=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=a42eeb1e-0dd3-4ba2-a089-7b0b769cfbb7; gr_cs1_a42eeb1e-0dd3-4ba2-a089-7b0b769cfbb7=user_id%3A0; __utmt_douban=1; viewed="26957760_26986954_26871657_25831096_2131426_1082334_20428302_25862578_2044626_24697776"; ue="junnorgan@sohu.com"; dbcl2="173425388:SCTdvt66y20"; ck=LI5z; _pk_id.100001.8cb4=cb1c59d8ae794cd9.1492239201.22.1517556092.1514481774.; __utmt=1; __utmv=30149280.17342; __utmb=30149280.12.10.1517553762'
    }):
    html = requests.get(url, headers=headers)
    return html

# 根据url获取页面对象,如果要获得html文档,就需要加一个text属性,html.text
def get_html(url, headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }):
    # cookie = 'bid=EjVfNuCFCCc; __yadk_uid=p7eO16BlyhEZGRS5OFrIZLONj1oQIFfJ; gr_user_id=9f9ee961-658f-4d94-9064-6456ddc74420; ll="118159"; _vwo_uuid_v2=6F188EB37C02AF8DC97FD5D1A469D383|c652b51c9b96af699095d2f2d5378abe; ps=y; __utma=30149280.185030239.1505136888.1514481776.1517553762.19; __utmc=30149280; __utmz=30149280.1517553762.19.16.utmcsr=open.weixin.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/connect/qrconnect; push_noty_num=0; push_doumail_num=0; gr_cs1_0d411a4f-9fb6-4843-8b80-83a66830df18=user_id%3A1; ap=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1517555178%2C%22https%3A%2F%2Fbook.douban.com%2Fsubject%2F2230208%2F%22%5D; _pk_ses.100001.8cb4=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=a42eeb1e-0dd3-4ba2-a089-7b0b769cfbb7; gr_cs1_a42eeb1e-0dd3-4ba2-a089-7b0b769cfbb7=user_id%3A0; __utmt_douban=1; viewed="26957760_26986954_26871657_25831096_2131426_1082334_20428302_25862578_2044626_24697776"; ue="junnorgan@sohu.com"; dbcl2="173425388:SCTdvt66y20"; ck=LI5z; _pk_id.100001.8cb4=cb1c59d8ae794cd9.1492239201.22.1517556092.1514481774.; __utmt=1; __utmv=30149280.17342; __utmb=30149280.12.10.1517553762'
    # headers['Cookie'] = cookie
    print url
    html = requests.get(url, headers=headers)
    return html


# 从文学类书单列表的html中找到每一本书的链接,返回链接的列表
def get_book_list(html):
    book_list = []
    soup = BeautifulSoup(html.text, 'lxml')
    # select用于获得一个节点元素,这里获得了对应每本书链接<a></a>标签的元素,我们所需要的每本书的界面链接就保存在当中book['href']
    print soup
    books = soup.select('.pic > .nbg')
    for book in books:
        # print book['href']
        book_list.append(book['href'])
    return book_list


# 根据每本书的页面链接,读取每本书的信息,返回对应豆瓣书的对象
def get_book_info(url, iter=0):
    print u"当前书的url地址为: "+url
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'lxml')

    # 获取作者名
    author = soup.select('#info > a')
    if len(author) > 0:
        author = author[0].text
    else:
        author = u"暂无"
    # 去除unicode编码中的空格和换行
    author = re.sub(u'[ , \n]', u'', author)

    # 获取出版社名
    publisher = re.findall(u'<span class="pl">出版社:</span>(.*?)<br/>', html.text, re.S)
    if len(publisher) > 0:
        publisher = publisher[0]
    else:
        publisher = u"暂无"
    if len(publisher) > 0 and publisher[0]==' ':
        publisher = publisher[1:]

    # 获取书本名
    book_name = soup.select("#wrapper > h1 > span")
    if len(book_name) > 0:
        book_name = book_name[0].text
    else:
        book_name = u"暂无"
    if len(book_name) > 0 and book_name[0]==' ':
        book_name = book_name[1:]

    # 获取出版日期
    publish_date = re.findall(u'<span class="pl">出版年:</span>(.*?)<br/>', html.text, re.S)
    if len(publish_date) > 0:
        publish_date = publish_date[0]
    else:
        publish_date = u"暂无"
    if len(publish_date) > 0 and publish_date[0]==' ':
        publish_date = publish_date[1:]

    # 获取书的价格
    price = re.findall(u'<span class="pl">定价:</span>(.*?)<br/>', html.text, re.S)
    if len(price) > 0:
        price = price[0]
    else:
        price = u"暂无"
    if len(price) > 0 and price[0] == ' ':
        price = price[1:]

    # 获取ISBN序列号
    ISBN = re.findall(u'<span class="pl">ISBN:</span>(.*?)<br/>', html.text, re.S)
    if len(ISBN) > 0:
        ISBN = ISBN[0]
    else:
        ISBN = u"-1"
    if len(ISBN) > 0 and ISBN[0] == ' ':
        ISBN = ISBN[1:]

    # 获取内容简介
    content_items = soup.select('.indent > div > .intro > p')
    content = u""
    for item in content_items:
        content = content+item.text+u"\n"

    # 获取短评的部分内容,就是只显示在书单页面上的很少的一部分
    comment_items = soup.select('.comment-item > .comment > p')
    comment = u""
    for item in comment_items:
        comment = comment+item.text+u"\n"

    book = douban_book.Douban_book(author, publisher, book_name, publish_date, price, ISBN, content, comment)
    print u"书名: "+book.book_name
    print u"作者: "+book.author
    print u"出版社: "+book.publisher
    print u"出版日期"+book.publish_date
    print u"书的价格"+book.price
    print u"书的ISBN编号: "+str(book.ISBN)
    # print book.content
    # print book.comment
    if book.ISBN==-1:
        print "error:\n", html
        # 访问页面失败，重复访问，至少10次
        if iter < 10:
            get_book_info(url, iter+1)
    return book


# 下方完成了从爬取数据到存入数据库的操作
if __name__ == "__main__":

    client = pymongo.MongoClient('localhost', 27017)
    database = client['douban'] #数据库名
    collection = database['book'] #对应数据库中表的名字
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    # 这里是将标签为文学的书进行爬取的,也可以改成别的类型的,range中的数字就代表了要翻页的信息
    urls = ['https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start='+format(str(i)) for i in range(0, 20, 20)]

    activate_cookie('https://www.douban.com')
    for url in urls:
        print url+'&type=T'
        html = get_html(url+'&type=T')
        books_url = get_book_list(html)
        for book_url in books_url:
            # 获取到书的完整对象
            book = get_book_info(book_url)
            # 将书存入mongodb中
            douban_book.write_douban_books_to_mongodb(book, collection)

    print client

