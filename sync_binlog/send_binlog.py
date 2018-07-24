# encoding=utf8

import pymysql
from sync_binlog.output_log import logger as loging
import time
import sys
from sync_conf import *
from sync_binlog.Decrypt import decrypt
from sync_binlog.update_post import update_datetime

target_passwd = decrypt(target_passwd)


class Mysql(object):
    ip = target_ip
    port = 3306
    user = target_user
    password = target_passwd
    conn = pymysql.connect(host=ip, port=port, user=user, passwd=password, autocommit=True, charset='utf8')
    cur = conn.cursor()
    startup_time = int(time.time())

    def __init__(self, sql):
        self.__sql = sql

    def my_sql(self, sql):
        global startup_time
        current_time = int(time.time())
        cur = Mysql.cur
        if current_time - Mysql.startup_time >= 1200:
            try:
                startup_time = int(time.time())
                Mysql.conn.ping()
            except Exception:
                conn = Mysql.conn
                cur = conn.cursor()
            data = cur.execute(sql)
        else:
            try:
                data = cur.execute(sql)
            except Exception as e:
                loging.critical("执行SQL错误：%s" % e)
                loging.critical("--->> %s " % sql)
                sys.exit("执行SQL错误：%s" % e)
        if data == 0:
            if sql[:3] == 'use':
                loging.info(sql)
            elif sql[:6] == "insert":
                error_code = '1062'
                loging.error("执行sql影响 %d 条 Error_code: 1062; handler error HA_ERR_FOUND_DUPP_KEY; ----->> %s " %
                             (data, sql))
                if skip_err_code is None:
                    print("%s执行sql影响 %d 条 Error_code: 1062; handler error HA_ERR_FOUND_DUPP_KEY; ----->> %s " %
                          (update_datetime(), data, sql))
                    sys.exit("请确认SQL是否执行正确!")
                elif error_code in skip_err_code or 'all' in skip_err_code:
                    print("%s执行sql影响 %d 条 Error_code: 1062; handler error HA_ERR_FOUND_DUPP_KEY; ----->> %s " %
                          (update_datetime(), data, sql))
            elif sql[:6] == "update":
                error_code = '1032'
                loging.error("执行sql影响 %d 条 Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; ----->> %s " %
                             (data, sql))
                if skip_err_code is None:
                    print("%s执行sql影响 %d 条 Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; ----->> %s " %
                          (update_datetime(), data, sql))
                    sys.exit("请确认SQL是否执行正确!")
                elif error_code in skip_err_code or 'all' in skip_err_code:
                    print("%s执行sql影响 %d 条 Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; ----->> %s " %
                          (update_datetime(), data, sql))
            elif sql[:6] == "delete":
                error_code = '1032'
                loging.error("执行sql影响 %d 条 Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; ----->> %s " %
                             (data, sql))
                if skip_err_code is None:
                    print("%s执行sql影响 %d 条 Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; ----->> %s " %
                          (update_datetime(), data, sql))
                    sys.exit("请确认SQL是否执行正确!")
                elif error_code in skip_err_code or 'all' in skip_err_code:
                    print("%s执行sql影响 %d 条 Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; ----->> %s " %
                          (update_datetime(), data, sql))
            else:
                loging.info(sql)
        else:
            loging.info("执行sql影响 %d 条" % data)

