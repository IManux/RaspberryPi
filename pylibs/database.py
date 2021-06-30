import sys
import pymysql
import pymysql.cursors
import logging

class Database:
    """Database connection class."""

#__init__
    def __init__(self, config):
        self.__host = config[0] #"DATABASE_HOST"
        self.__username = config[1] #"DATABASE_USERNAME"
        self.__password = config[2] #"DATABASE_PASSWORD"
        self.__dbname = config[3] #"DATABASE_NAME"
        self.__port = config[4] #8000
        self.__conn = None

    def debug_class(self):
        print(self.__host, self.__username, self.__password, self.__dbname, self.__port)

#open_connection
    def open_connection(self):
        result = False
        """Connect to MySQL Database."""
        try:
            if self.__conn is None:
                self.__conn = pymysql.connect(self.__host,
                                            user=self.__username,
                                            passwd=self.__password,
                                            db=self.__dbname,
                                            cursorclass=pymysql.cursors.DictCursor, #new added
                                            connect_timeout=5)
            result = True
        except pymysql.MySQLError as e:
            logging.error(e)
            #result = False
            #sys.exit()
        finally:
            logging.debug('Connection opened successfully.')
            #result = True
            #print('Connection opened successfully.')
            return result
        #return result

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
            self.conn.commit()
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
        try:
            with self.__conn.cursor() as cur:
                rows_count = cur.execute(query)
                if rows_count > 0:
                    rows_raw = cur.fetchall()
            cur.close()
        except pymysql.MySQLError as e:
            logging.error(e)
            rows_count = -1
        finally:
            return rows_raw

#update() - Update
    def update(self, query):
        result = False
        print("db.update")
        try:
            with self.__conn.cursor() as cur:
                cur.execute(query)
            self.conn.commit()
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
            self.conn.commit()
            cur.close()
            result = True
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            return result
