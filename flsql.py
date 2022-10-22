'''
Database sql helper
'''

import psycopg2.extras
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
        except:
            print('Ошибка чтения из БД')
        return []
