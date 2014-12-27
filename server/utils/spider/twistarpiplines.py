# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#encoding=utf8
from twisted.enterprise import adbapi
from twistar.registry import Registry
from twistar.dbobject import DBObject
from scrapy.conf import settings
from ..url import parse_sql_url
from scrapy.item import Field, Item, ItemMeta

class TwistarItemMeta(ItemMeta):

    def  __new__(mcs, class_name, bases, attrs):
        cls = super(TwistartemMeta, mcs).__new__(mcs, class_name, bases, attrs)
        #cls.fields = cls.fields.copy()
        if cls.sql_model:
            cls._model_fields = []
            #cls._model_meta = cls.sqlalchemy_model._meta
            tablename = cls.sql_model.tablename()
            #attrs = {}
            if Registry.SCHEMAS.has_key(tablename):
                for name in Registry.SCHEMAS[tablename]:
                    if name not in cls.fields:
                        cls.fields[name] = Field()
                    cls._model_fields.append(name)
        return cls


class TwistarItem(Item):

    __metaclass__ = TwistarItemMeta

    #a DBObject class
    sql_model = None

    def __init__(self, *args, **kwargs):
        super(TwistarItem, self).__init__(*args, **kwargs)
        self._instance = None
        self._errors = None


    @property
    def dbobject(self):
        if self._instance is None:
            modelargs = dict((k, self.get(k)) for k in self._values
                             if k in self._model_fields)
            self._instance = self.sql_model(**modelargs)
        return self._instance

    @property
    def dbcls(self):
        return self.sql_model



#TWISTAR_DB_URL="MySQLdb://wangpan:wangpan@localhost/wangpan?charset=utf8"
class TwistarPipeline(object):

    def open_spider(self,spider):
        self.settings =  spider.settings
        sql_url = settings['TWISTAR_DB_URL']
        conn_arg = parse_sql_url(sql_url)
        drivername = conn_arg.pop("drivername")
        Registry.DBPOOL = adbapi.ConnectionPool(drivername, **conn_arg)


        

    def process_item(self, item, spider):
        if isinstance(item,TwistarItem):
            item.model
 

        return item