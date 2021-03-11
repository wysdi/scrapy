# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from google.cloud import firestore
from google.oauth2 import service_account
from urllib.parse import urlparse
class FirestorePipeline:

    collection_name = 'items'

    def __init__(self, credentials):
        self.credentials = credentials

    @classmethod
    def from_crawler(cls, crawler):
        credentials = service_account.Credentials.from_service_account_file(
            crawler.settings.get('GOOGLE_APPLICATION_CREDENTIALS'), scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        return cls(
           credentials=credentials
        )

    def open_spider(self, spider):
        self.db = firestore.Client(credentials=self.credentials)

    # def close_spider(self, spider):
    #     self.db.close()

    def process_item(self, item, spider):
        path = item['link'].rsplit('/', 1)[-1]
        print(('path', path))
        data = ItemAdapter(item).asdict()
        doc_ref = self.db.collection(u'course').document(u'{}'.format(spider.name))
        event_ref = doc_ref.collection(u'{}'.format(self.collection_name)).document(u'{}'.format(path))
        event_ref.set(data)
        return item
