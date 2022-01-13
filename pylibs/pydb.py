import sys
import pymysql
import pymysql.cursors
import logging

class MySQL:
    """Database connection class."""

#__init__
    def __init__(self, host='127.0.0.1', user='root', pwd='root', dbname='test', port=3306, chrset='utf8'):
        self.__host = host #"DATABASE_HOST"
        self.__username = user #"DATABASE_USERNAME"
        self.__password = pwd #"DATABASE_PASSWORD"
        self.__dbname = dbname #"DATABASE_NAME"
        self.__port = port #8000
        self.__charset = chrset #options: utf8, utf8mb4
        self.__conn = None

    def set_host(self, host):
        self.__host = host

    def set_username(self, user):
        self.__username = user

    def set_password(self, pwd):
        self.__password = pwd
    
    def set_dbname(self, dbname):
        self.__dbname = dbname

    def set_port(self, port):
        self.__port = port
    
    def set_charset(self, chrset):
        self.__charset = chrset

    def debug_class(self):
        print(self.__host, self.__username, self.__password, self.__dbname, self.__port, self.__charset)

#open_connection
    def open_connection(self):
        result = False
        """Connect to MySQL Database."""
        try:
            if self.__conn is None:
                self.__conn = pymysql.connect(host=self.__host,
                                            user=self.__username,
                                            passwd=self.__password,
                                            db=self.__dbname,
                                            charset=self.__charset,
                                            cursorclass=pymysql.cursors.DictCursor, #new added
                                            connect_timeout=5)
            result = True
        except pymysql.MySQLError as e:
            logging.error(e)
            self.__conn = None
            #result = False
            #sys.exit()
        finally:
            if result == True:
                logging.debug('Connection opened successfully.')
            else:
                logging.debug('open_connection() failed')

            return result

#close_connection
    def close_connection(self):
        result = False
        if self.__conn:
            self.__conn.close()
            self.__conn = None
            result = True
            logging.info('Database connection closed.')
            #print('Database connection closed.')
        return result

#isConnected()
    def isConnected(self):
        if self.__conn:
            return True
        return False

#insert() - Create
    def insert(self, query, values):
        result = False
        print("db.insert")
        try:
            with self.__conn.cursor() as cur:
                cur.execute(query, values)
            self.__conn.commit()
            cur.close()
            result = True
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            return result

#consult() - Read
    def consult(self, query):
        print("db.consult")
        rows_raw = None
        rows_count = 0
        try:
            with self.__conn.cursor() as cur:
                rows_count = cur.execute(query)
                if rows_count > 0:
                    rows_raw = cur.fetchall()
            cur.close()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            return rows_raw, rows_count

#update() - Update
    def update(self, query):
        result = False
        print("db.update")
        try:
            with self.__conn.cursor() as cur:
                cur.execute(query)
            self.__conn.commit()
            cur.close()
            result = True
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            return result

#delete() - Delete
    def delete(self, query):
        result = False
        print("db.delete")
        try:
            with self.__conn.cursor() as cur:
                cur.execute(query)
            self.__conn.commit()
            cur.close()
            result = True
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            return result
