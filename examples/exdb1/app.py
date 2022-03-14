import time
import apitest

SYS_DBG_MODE = 1

def sys_dbg_print(s):
    if SYS_DBG_MODE:
        print(s)

if __name__ == "__main__":
    sys_dbg_print("exdb1.py")

    mydb = apitest.ApiDB()
    mydb.test_insert_param(10, 20, 40.75, 30.25)
    mydb.test_insert_param(10, 20, 40.75, 30.25)
    mydb.test_insert_param(10, 20, 40.75, 30.25)
    mydb.test_insert_param(10, 20, 40.75, 30.25)
    mydb.test_insert_param(10, 20, 40.75, 30.25)

    mydb.test_update_uploaded(1, 1)
    mydb.test_update_uploaded(2, 1)

    r, n = mydb.test_get_all()

    if n:
        for i in range(n):
            print(r[i])
    
    r, n = mydb.test_get_num(5, 0)
    if n:
        for i in range(n):
            print(r[i])
    
    r, n = mydb.test_get_num(3, 1)
    if n:
        for i in range(n):
            print(r[i])
