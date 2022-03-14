from datetime import datetime
import pydb

class ApiDB():
    def __create_query(self, tn, keys_sql):

        alen = len(keys_sql)
        sql = "INSERT INTO "
        sql += tn
        sql += " ("
        for i in range(alen):
            #sql += "'"
            sql += keys_sql[i]
            #sql += "'"
            if i < (alen-1):
                sql += ", "

        sql += ") VALUES ("
        for i in range(alen):
            sql += "%s"
            if i < (alen-1):
                sql += ", "

        sql += ")"

        return sql

    def test_insert_param(self, var1, var2, var3, var4):
        print("test_set_param")
        _err = 1
        _values_sql_arr = (["", "", "", "", "", ""])
        _keys_sql_arr = ([
                "var1",
                "var2",
                "var3",
                "var4",
                "uploaded",
                "created_at",
            ])
        _query = self.__create_query(self.__db_table, _keys_sql_arr)
        _query = _query + ';'

        _conn = pydb.MySQL(self.__db_host, self.__db_user, self.__db_pass, self.__db_name, self.__db_port)
        if _conn.open_connection():
            _now = datetime.now()
            _values_sql_arr[0] = var1
            _values_sql_arr[1] = var2
            _values_sql_arr[2] = var3
            _values_sql_arr[3] = var4
            _values_sql_arr[4] = 0
            _values_sql_arr[5] = _now.strftime('%Y-%m-%d %H:%M:%S')
            #insert
            if _conn.insert(_query, _values_sql_arr): #ok?
                _err = 0
            #close conn db
            _conn.close_connection()

        return _err

    def test_get_all(self):
        print("test_get_all_param")
        _rows = None
        _qty = 0
        _conn = pydb.MySQL(self.__db_host, self.__db_user, self.__db_pass, self.__db_name, self.__db_port)
        if _conn.open_connection():
            _query = "SELECT * FROM " + self.__db_table + ";"
            _rows, _qty = _conn.consult(_query)
            _conn.close_connection()

        return _rows, _qty

    def test_get_num(self, n, uploaded=0):
        print("test_get_num_param")
        _rows = None
        _qty = 0
        if n > 0:
            _conn = pydb.MySQL(self.__db_host, self.__db_user, self.__db_pass, self.__db_name, self.__db_port)
            if _conn.open_connection():
                _query = "SELECT * FROM " + self.__db_table + " WHERE uploaded=" + str(uploaded) + " LIMIT " + str(n) + ";"
                _rows, _qty = _conn.consult(_query)
                _conn.close_connection()

        return _rows, _qty

    def test_update_uploaded(self, id, upl):
        print("test_update_uploaded")
        _err = 1
        _now = datetime.now()
        _updated_at = _now.strftime('%Y-%m-%d %H:%M:%S')
        _query = "UPDATE " + self.__db_table + " SET uploaded=" + str(upl) + ", updated_at='" + _updated_at + "' WHERE id=" + str(id) + ";"
        _conn = pydb.MySQL(self.__db_host, self.__db_user, self.__db_pass, self.__db_name, self.__db_port)
        if _conn.open_connection():
            if _conn.update(_query):
                _err = 0
            _conn.close_connection()

        return _err

    def db_set_host(self, s):
        self.__db_host = s

    def db_set_name(self, s):
        self.__db_name = s

    def db_set_user(self, s):
        self.__db_user = s

    def db_set_pass(self, s):
        self.__db_pass = s

    def db_set_port(self, p):
        self.__db_port = p
    
    def db_set_table(self, s):
        self.__db_table = s

    def db_get_host(self):
        return self.__db_host

    def db_get_name(self):
        return self.__db_name

    def db_get_user(self):
        return self.__db_user

    def db_get_pass(self):
        return self.__db_pass

    def db_get_port(self):
        return self.__db_port

    def db_get_table(self):
        return self.__db_table

    def __init__(self, *args, **kwargs):
        self.__error = 0
        #DB Credentials
        self.__db_host = "127.0.0.1"
        self.__db_name = "test_db"
        self.__db_user = "pi"
        self.__db_pass = "123456789"
        self.__db_port = 3306
        self.__db_table = "test_log_param"
