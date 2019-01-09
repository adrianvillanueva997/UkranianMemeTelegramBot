import MySQLdb

import src.config as config


class Kalash:

    def insert_betrayal(self, betrayal):
        try:
            con = config.engine
            text = ' '.join(betrayal)
            print(text)
            if text == '':
                return 0
            else:
                con.execute('INSERT INTO kalash (traicion) values (\"' + text + '\")')
                return 1
        except MySQLdb.Error or MySQLdb.Warning as e:
            print(e)
            return 0

    def show_betrayal(self):
        try:
            con = config.engine
            query = 'select Traicion from kalash'
            results = con.execute(query)
            betrayals = ''
            for betrayal in results:
                betrayals+= str(betrayal['Traicion']) +'\n'

            return betrayals
        except Exception as e:
            print(e)
