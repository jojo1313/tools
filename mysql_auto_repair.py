#!/usr/bin/env python
# encoding=utf-8

import os
import smtplib
import json
import time

from email.mime.text import MIMEText
from email.header import Header

_sql = 'mysql -uroot -pxxx -h127.0.0.1 -e %s'


def check_repair_slave_sync():
    try:
        cmd = _sql % '"show slave status\G"|grep "Running"'
        output = os.popen(cmd)
        _str = str(output.read())
        output.close()
        if 'No' in _str:
            hostname = os.popen('hostname')
            msg = str(hostname.read()) + '\nMysql Sync error.\nStart Automatic repair...'
            sendmail(msg)

            master_pos = get_master_log_pos()
            master_file = get_master_log_file()
            print(master_pos, master_file)
            reset_sync_pos(master_file, master_pos)
        else:
            print('Mysql sync is normal.')
    except Exception as e:
        print(e)


def get_master_log_pos():  # 获取mysql log pos.
    master_pos = None
    try:
        cmd = _sql % '"show slave status\G"' + "|grep 'Read_Master_Log_Pos'|awk -F ': ' '{print $2}'"
        output = os.popen(cmd)
        master_pos = str(output.read()).strip()
    except Exception as e:
        print(e)

    return master_pos


def get_master_log_file():  # 获取mysql master binlog 文件名.
    master_file = None
    try:
        cmd = _sql % '"show slave status\G"' + "|grep 'Master_Log_File'|grep -v 'Relay'|awk -F ': ' '{print $2}'"
        output = os.popen(cmd)
        master_file = str(output.read()).strip()
    except Exception as e:
        print(e)
    return master_file


def reset_sync_pos(master_file, master_pos):
    try:
        _rule = '"stop slave;CHANGE MASTER TO %s,%s;start slave;"'
        _file = "MASTER_LOG_FILE='%s'" % master_file
        _pos = "MASTER_LOG_POS=%s" % master_pos
        if master_pos and master_file:
            _rule = _rule % (_file, _pos)
            cmd = _sql % _rule
            print(cmd)
            _ = os.popen(cmd)

            _status = _sql % '"show slave status\G"'
            print(_status)

    except Exception as e:
        print(e)


def sendmail(msg):  # 发送邮件
    msg = str(msg)
    msg = msg.replace('->', ',')
    sender = 'jxxx@126.com'
    smtpserver = 'smtp.126.com'
    username = 'jxxx'
    password = 'xxx'

    _subject = 'mysql 同步故障'
    _to = 'jxxx@xxx.net'
    _content = msg

    msg = MIMEText(_content, 'plain', 'utf-8')
    msg['Subject'] = Header(_subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = _to

    smtp = smtplib.SMTP()
    try:
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, _to.split(','), msg.as_string())
        smtp.quit()
        response = {'msg': 'Successful.', "code": 1}
    except Exception as e:
        print(e)
        smtp.quit()
        response = {'msg': 'Failure', "code": 0}

    return json.dumps(response)


if __name__ == '__main__':
    check_repair_slave_sync()
