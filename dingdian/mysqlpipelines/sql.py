import pymysql
from dingdian import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

connect = pymysql.connect(host=MYSQL_HOSTS, database=MYSQL_DB, port=MYSQL_PORT,user=MYSQL_USER, password=MYSQL_PASSWORD)
cur = connect.cursor()

class Sql:

    @classmethod
    def insert_tb_novel(cls, name, author, novelurl, serialnumber, serialstatus, category, novel_id):
        sql = 'INSERT INTO tb_novel(`name`, `author`, `novelurl`, `serialnumber`, `serialstatus`, `category`, `novel_id`) ' \
              'VALUES (' \
              '%(name)s,' \
              ' %(author)s,' \
              ' %(novelurl)s,' \
              ' %(serialnumber)s,' \
              ' %(serialstatus)s,' \
              ' %(category)s,' \
              ' %(novel_id)s' \
              ');'

        values = {
            "name": name,
            "author": author,
            "novelurl": novelurl,
            "serialnumber": serialnumber,
            "serialstatus": serialstatus,
            "category": category,
            "novel_id": novel_id
        }
        cur.execute(sql, values)
        connect.commit()

    @classmethod
    def select_by_novel_id(cls, novel_id):
        # 下面占位符是%()s 不是%{}s; %()s也最好不要写成%()d, 否则老报formatError
        sql = "SELECT id FROM tb_novel WHERE novel_id = %(novel_id)s"
        value = {"novel_id": novel_id}

        cur.execute(sql, value)
        cur.fetchall()

    @classmethod
    def insert_novel_chapter(self, novel_id, chapter_name, chapter_num, chapter_url, chapter_content):
        sql = "INSERT INTO tb_novel_chapter(`novel_id`, `chapter_name`, `chapter_num`, `chapter_url`, `chapter_content`) " \
              "VALUES (%(novel_id)s, %(chapter_name)s, %(chapter_num)s, %(chapter_url)s, %(chapter_content)s);"
        value = {
            "novel_id": novel_id,
            "chapter_num": chapter_num,
            "chapter_name": chapter_name,
            "chapter_url": chapter_url,
            "chapter_content": chapter_content
        }
        cur.execute(sql, value)
        connect.commit()