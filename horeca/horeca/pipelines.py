# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class horecaPipeline:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="horeca",
            user="postgres",
            password="coderslab")

        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        try:
            self.curr.execute("""INSERT INTO products (product_name, product_price, product_url) VALUES (%s, %s, %s)""", (
                item["title"][0],
                item["price"][0],
                item["url"][0]
            ))
        except Exception as e:
            print(e)
        self.conn.commit()
