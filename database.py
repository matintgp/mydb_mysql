import mysql.connector

class DB:
    #       database base method and settings

    def __init__(self, host, user, password, database):
        self.mydb = None
        self.host = host
        self.user = user
        self.passwd = password
        self.dbname = database
        
        try:
            self.mydb = mysql.connector.connect(
                host= self.host,
                user= self.user,
                passwd= self.passwd,
                database= self.dbname
            )
            
        except mysql.connector.Error as e:
            with open('db_errors.log', 'a') as f:
                f.write(e)
            print(f'Error: {e}')
            
            self.mydb = mysql.connector.connect(
                host= self.host,
                user= self.user,
                passwd= self.passwd,
                database= self.dbname
            )
        self.mycursor = self.mydb.cursor()

    def _reconnect_to_db(self):
        self.mydb = None
        self.mydb = mysql.connector.connect(
            host= self.host,
            user= self.user,
            passwd= self.passwd,
            database= self.dbname
        )
        self.mycursor = self.mydb.cursor()


    def __close_connection__(self):
        if self.mycursor:
            self.mycursor.close()

        if self.mydb and self.mydb.is_connected():
            self.mydb.close()


    def _save(self, sql, val=None):
        self._reconnect_to_db()
        try:
            if val:
                self.mycursor.execute(sql, val)
            else:
                self.mycursor.execute(sql)
            self.mydb.commit()
            return True

        except mysql.connector.Error as e:
            with open('db_errors.log', 'a') as f:
                f.write(str(e))
            print(f'Error: {str(e)}')

        finally:
            self.__close_connection__()

    def _get_one(self, sql, val=None):
        self._reconnect_to_db()
        try:
            if val:
                self.mycursor.execute(sql, val)
            else:
                self.mycursor.execute(sql)
            res = self.mycursor.fetchall()
            if res is not None and len(res) > 0:
                return res[0]

        except mysql.connector.Error as e:
            with open('db_errors.log', 'a') as f:
                f.write(str(e))
            print(f'Error: {str(e)}')

        finally:
            self.__close_connection__()

    def _get_all(self, sql, val=None):
        self._reconnect_to_db()
        try:
            if val:
                self.mycursor.execute(sql, val)
            else:
                self.mycursor.execute(sql)
            return self.mycursor.fetchall()

        except mysql.connector.Error as e:
            with open('db_errors.log', 'a') as f:
                f.write(str(e))
            print(f'Error: {str(e)}')

        finally:
            self.__close_connection__()
