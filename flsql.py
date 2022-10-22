'''
Database sql helper
'''

import psycopg2
import psycopg2.extras
import time
import math
class Flsql:
    '''
    Create Flask SQL class for sql query
    '''
    def __init__(self, cur_db):
        self.__my_db = cur_db
        self.__cur = cur_db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    def get_menu(self):
        '''
        Function putting main menu links
        '''
        sql = '''SELECT * FROM mainmenu ORDER BY ID'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except psycopg2.OperationalError as err:
            print('Ошибка чтения из БД', str(err) )
        return []


    def add_post(self, title, text):
        '''
        Method for adding post at site
        '''
        try:
            cur_time = math.floor(time.time())
            self.__cur.execute('''INSERT INTO posts (title, posttext, posttime) VALUES (%s, %s, %s)''', (title, text, cur_time))
            self.__my_db.commit()
        except psycopg2.OperationalError as err:
            print('Ошибка добавления статьи в БД: ', str(err))
            return False
        return True
