import sys
import pymysql
import pymysql.cursors
import logging

class MySQL:
    """Database connection class."""

#__init__
    def __init__(self, host='127.0.0.1', user='root', pwd='root', dbname='test', port=3306, chrset='utf8', dbg=False):
        self.__host = host #"DATABASE_HOST"
        self.__username = user #"DATABASE_USERNAME"
        self.__password = pwd #"DATABASE_PASSWORD"
        self.__dbname = dbname #"DATABASE_NAME"
        self.__port = port #8000
        self.__charset = chrset #options: utf8, utf8mb4
        self.__conn = None
        self.__xdebug = False

    def __dbg_print(self, s):
        if self.__xdebug:
            print(s)

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
        ret = False
        self.__dbg_print("open_connection()")
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
            ret = True
        except pymysql.MySQLError as e:
            #logging.error(e)
            self.__dbg_print(e)
            self.__conn = None
        finally:
            if ret == True:
                #logging.debug('Connection opened successfully.')
                self.__dbg_print("Success")
            else:
                #logging.debug('open_connection() failed')
                self.__dbg_print("Failed")

            return ret

#close_connection
    def close_connection(self):
        self.__dbg_print("close_connection()")
        ret = False
        if self.__conn:
            self.__conn.close()
            self.__conn = None
            ret = True
            #logging.info('Database connection closed.')
            self.__dbg_print("DB CC")
        return ret

#isConnected()
    def isConnected(self):
        if self.__conn:
            return True
        return False

#insert() - Create
    def insert(self, query, values):
        self.__dbg_print("DB insert()")
        ret = False
        try:
            with self.__conn.cursor() as cur:
                cur.execute(query, values)
            self.__conn.commit()
            cur.close()
            ret = True
        except pymysql.MySQLError as e:
            #logging.error(e)
            self.__dbg_print(e)
        finally:
            return ret

#consult() - Read
    def consult(self, query):
        self.__dbg_print("DB consult()")
        rows_raw = None
        rows_count = 0
        try:
            with self.__conn.cursor() as cur:
                rows_count = cur.execute(query)
                if rows_count > 0:
                    rows_raw = cur.fetchall()
            cur.close()
        except pymysql.MySQLError as e:
            #logging.error(e)
            self.__dbg_print(e)
        finally:
            return rows_raw, rows_count

#update() - Update
    def update(self, query):
        self.__dbg_print("DB update()")
        ret = False
        try:
            with self.__conn.cursor() as cur:
                cur.execute(query)
            self.__conn.commit()
            cur.close()
            ret = True
        except pymysql.MySQLError as e:
            #logging.error(e)
            self.__dbg_print(e)
        finally:
            return ret

#delete() - Delete
    def delete(self, query):
        self.__dbg_print("DB delete()")
        ret = False
        try:
            with self.__conn.cursor() as cur:
                cur.execute(query)
            self.__conn.commit()
            cur.close()
            ret = True
        except pymysql.MySQLError as e:
            #logging.error(e)
            self.__dbg_print(e)
        finally:
            return ret
