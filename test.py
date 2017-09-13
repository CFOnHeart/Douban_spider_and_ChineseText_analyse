# coding=utf-8
from spider import douban_book_spider as dbspider
from text import text_presolve
from text import participal
from text import my_word2vec as mywv
import pymongo
if __name__ == "__main__":

    client = pymongo.MongoClient('localhost', 27017)
    database = client['douban'] #数据库名
    collection = database['book'] #对应数据库中表的名字
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    # 这里是将标签为文学的书进行爬取的,也可以改成别的类型的,range中的数字就代表了要翻页的信息
    urls = ['https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start='+format(str(i)) for i in range(0, 20, 20)]

    for url in urls:
        print url+'&type=T'
        html = dbspider.get_html(url+'&type=T')
        books_url = dbspider.get_book_list(html)
        for book_url in books_url:
            # 获取到书的完整对象
            book = dbspider.get_book_info(book_url)
            # 将书存入mongodb中
            dbspider.douban_book.write_douban_books_to_mongodb(book, collection)

    print client

    # 下方完成了将豆瓣评论信息从数据库加载到对应文件中
    filename = "resource/initial_text/douban_comments.txt"
    text_presolve.write_douban_comment(filename)
    print "豆瓣评论信息已经写入了文件: "+filename

    # 下方是对本脚本的测试代码,完成了对豆瓣评论文件的分词操作后保存
    dict_name = 'resource/word_dictionary/comment_dic.txt'
    participal.add_dictionary(dict_name)
    participal.text_participle('resource/initial_text/douban_comments.txt', 'resource/participal_text/douban_comments_participal.txt')

    # # 对word2vec代码的测试
    mywv.test()
