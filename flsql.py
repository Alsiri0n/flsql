"""
Database sql helper
"""
import re
from datetime import datetime
from psycopg2 import OperationalError
from flask import url_for
import psycopg2.extras

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
        sql = "SELECT * FROM mainmenu ORDER BY ID;"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except OperationalError as err:
            print("Ошибка чтения из БД", str(err))
        return []


    def add_post(self, title, text, url):
        """
        Method for adding post at site
        """
        try:
            self.__cur.execute(
                f"SELECT COUNT(*) as \"count\" FROM posts WHERE posturl LIKE '{url}';")
            res = self.__cur.fetchone()
            if res["count"] > 0:
                print("Статья с таким url уже существует.")
                return False

            cur_time = datetime.now()
            self.__cur.execute("INSERT INTO posts (title, posttext, posturl, posttime)\
                                VALUES (%s, %s, %s, %s);",
                                (title, text, url, cur_time))
            self.__my_db.commit()
        except OperationalError as err:
            print("Ошибка добавления статьи в БД: ", str(err))
            return False
        return True


    def get_post(self, alias):
        """
        This method get post by id
        """
        try:
            self.__cur.execute(f"SELECT title, posttext FROM posts WHERE posturl LIKE '{alias}' LIMIT 1;")
            res = self.__cur.fetchone()
            if res:
                base = url_for("static", filename="images")
                text  = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                "\\g<tag>" + base + "/\\g<url>>",
                res['posttext'])
                return {"title": res['title'], "posttext": text}
        except OperationalError as err:
            print("Ошибка чтения из БД: ", str(err))

        return {"title": False, "posttext": False}


    def get_posts_announcement(self):
        """
        Return announcement of the posts
        """
        try:
            self.__cur.execute("SELECT id, title, posttext, posturl FROM posts ORDER BY posttime DESC;")
            res = self.__cur.fetchall()
            if res:
                return res
        except OperationalError as err:
            print("Ошибка чтения из БД: ", str(err))
        return {}
