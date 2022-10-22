"""
Database sql helper
"""

import psycopg2
import psycopg2.extras
from datetime import datetime
import math
class Flsql:
    """
    Create Flask SQL class for sql query
    """
    def __init__(self, cur_db):
        self.__my_db = cur_db
        self.__cur = cur_db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    def get_menu(self):
        """
        Function putting main menu links
        """
        sql = '''SELECT * FROM mainmenu ORDER BY ID;'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except psycopg2.OperationalError as err:
            print('Ошибка чтения из БД', str(err) )
        return []


    def add_post(self, title, text):
        """
        Method for adding post at site
        """
        try:
            cur_time = datetime.now()
            self.__cur.execute('''INSERT INTO posts (title, posttext, posttime) VALUES (%s, %s, %s);''', (title, text, cur_time))
            self.__my_db.commit()
        except psycopg2.OperationalError as err:
            print('Ошибка добавления статьи в БД: ', str(err))
            return False
        return True


    def get_post(self, postId):
        """
        This method get post by id
        """
        try:
            self.__cur.execute(f"SELECT title, posttext FROM posts WHERE id = {postId} LIMIT 1;")
            res = self.__cur.fetchone()
            if res:
                return res
        except psycopg2.OperationalError as err:
            print('Ошибка добавления статьи в БД: ', str(err))

        return {'title': False, 'posttext': False}


    def get_posts_announcement(self):
        """
        Return announcement of the posts
        """
        try:
            self.__cur.execute("SELECT id, title, posttext FROM posts ORDER BY time DESC;")
            res = self.__cur.fetchall()
            if res:
                return res
        except psycopg2.OperationalError as err:
            print('Ошибка добавления статьи в БД: ', str(err))
        return {}
