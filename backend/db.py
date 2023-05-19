import pymongo, os, json, datetime, random
from bson import ObjectId
from CONFIG import mongoURL, mongoDBName

database = mongoDBName

client = pymongo.MongoClient(mongoURL)
db = None


def get_db():
    global db
    if not db:
        db = client[database]
    return db


db = get_db()

data_path = './data'

def data_import():
    coll_list = db.list_collection_names()
    for collection in coll_list:
        # 删除集合
        db[collection].drop()
    for maindir, subdir, file_list in os.walk(data_path):
        for file_name in file_list:
            if file_name[file_name.rindex('.'):] == '.json':
                coll = file_name[:file_name.rindex('.')]

                with open(data_path + '/' + file_name, encoding='utf-8') as file:
                    str = file.read()
                    if str == '' or str is None:
                        continue
                    else:
                        data = []
                        data.extend(json.loads(str))
                        if coll == 'user':
                            for d in data:
                                d['_id'] = ObjectId(d['_id'])
                                d['phone'] = d['phone']
                                d['nick'] = d['nick']
                                d['point'] = d['point']
                        if coll == 'code':
                            for d in data:
                                d['_id'] = ObjectId(d['_id'])
                                d['phone'] = d['phone']
                                d['code'] = d['code']
                                d['expires_on'] = d['expires_on']
                        db[coll].insert_many(data)
