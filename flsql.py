'''
Database sql helper
'''
class Flsql:
    '''
    Create Flask SQL class for sql query
    '''
    def __init__(self, cur_db):
        self.__my_db = cur_db
        self.__cur = cur_db.cursor()

    def get_menu(self):
        '''
        Function putting main menu links
        '''
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Ошибка чтения из БД')
        return []
