# coding=utf-8
import pymongo

class Mongodb:

    def __init__(self, ip_address='localhost', port=27017):
        self.client = pymongo.MongoClient(ip_address, port)

    # def __init__(self, database_name, collection_name, ip_address='localhost', port=27017):
    #     self.client = pymongo.MongoClient(ip_address, port)
    #     self.database = self.client[database_name]
    #     self.collection = self.database[collection_name]

    def close_mongodb(self):
        self.client.close()

    def get_database(self, database_name):
        return self.client[database_name]


    def get_collection(self, database_name, collection_name):
        return self.client[database_name][collection_name]


    def query_data(self, collection, query_data):
        return collection.find(query_data)

    # data是一个字典,每一个key值表示每一个数据的属性名,每一个value,就是对应数据属性的value,这个value的type决定了在mongodb中的对象类型
    # 返回1表示数据插入成功
    # 返回0表示当前数据在collection已经存在
    def insert_data(self, collection, data):
        if not self.query_data(collection, data):
            collection.insert_one(data)
            return 1
        else:
            return 0


    # 根据collection对于data的询问,返回一组数据,返回列表,列表中每个元素都是一个数据对应的字典
    def get_datainfo(self, collection, data):
        dics = []
        query = self.query_data(collection, data)
        for item in query:
            dics.append(item)
            # 注释中的方法也可以,只不过是逐条添加数据,这里item就是一个字典对象
            # dic = {}
            # for key in item.keys():
            #     dic[key] = item[key]
        return dics
