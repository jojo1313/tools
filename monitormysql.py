#!/usr/bin/env python
#coding=utf-8

import sys
import os
import commands
import smtplib
import MySQLdb.cursors
from email.mime.text import MIMEText

def killslowqurey():
    master_db="mysqladmin -uroot -p'xxx' -h211.xxx.xx.xxx "
    _command = '{0} {1}'.format(master_db,'processlist')
    (_status,_qureys)=commands.getstatusoutput(_command)
    qureyslist=_qureys.split('\n')
    for row in qureyslist:
       if '|' in row :
           _row=row.split('|')
           if len(_row) >=7:
               id    = _row[1].strip()
               user  = _row[2].strip()
               ip    = _row[3].strip()
               db    = _row[4].strip()
               state = _row[5].strip()
               time  = _row[6].strip()
               #delete sleep processlist if time > 1800sec.
               if str(state) == 'Sleep' and int(time) > 1800:
                 # _content='Kill the sleep process:\n----------------------\nid:{0}\nuser:{1}\nip:{2}\ndb:{3}\ntime:{4} \
                 #           \n\n\nThis is auto message from monitor server,please don`t response this email.\
                 #            \nthank you.'.format(id,user,ip,db,time)
                 # Sendmail(content=_content,subject="killed sleep process").send()
                  commands.getstatusoutput('{0} {1} {2}'.format(master_db,'kill',id))
               #delete slow query processlist if time > 20sec
               elif str(state) == 'Query' and int(time) > 20:
                  _content='Kill the slow query process:\n----------------------\nid:{0}\nuser:{1}\nip:{2}\ndb:{3}\ntime:{4} \ncommand:{5} \
                            \n\n\nThis is auto message from monitor server,please don`t response this email.\
                            \nthank you.'.format(id,user,ip,db,time,_row[8].strip())
                  Sendmail(content=_content,subject="killed slow query").send()
                  commands.getstatusoutput('{0} {1} {2}'.format(master_db,'kill',id))
               else:
                  pass             
       else:
           pass

def getdbsync_status():
    try:
       conn=MySQLdb.connect(host='xxx.xxx.xxx'user='root',passwd='xxx',port=3306,cursorclass=MySQLdb.cursors.DictCursor)
       cur=conn.cursor()
     
       cur.execute('show slave status')
       result=cur.fetchall()

       _IO_status = result[0]['Slave_IO_Running']
       _SQL_status = result[0]['Slave_SQL_Running']
       if _IO_status == 'Yes' or _SQL_status != 'Yes':
          _subject = "Mysql DB sync is down"
          _content = "this is test email, from jojo."#"The 96salve auto sync to 91master MysqlDB is down."         
          Sendmail(content=_content,subject=_subject).send()
       else:
          pass

       cur.close()
       conn.close()
    except MySQLdb.Error,e:
       print "error"
       print e


class Sendmail:
    def __init__(self,to="",cc="",content="",subject=""):
        self.host="smtp.126.com"
        self.user='we@126.com'
        self.pwd='xxx'
        self.to=to or ['xxx@foxmail.com','xxxxx@cxxx.com','xxxx@xxx.com','6xxxxx@qq.com']
        self.content= content or 'This is a mail from monitor server'
        self.cc= cc or ['xxxx@xxx.com']
        self.subject= subject or "mysql warning"
    def send(self):
        msg=MIMEText(self.content)
        msg['From']=self.user
        msg['Subject']=self.subject
        msg['To']=','.join(self.to)
        msg['Cc']=','.join(self.cc)
        try:
            s=smtplib.SMTP()
            s.connect(self.host)
            s.login(self.user,self.pwd)
            _to=self.to+self.cc
            s.sendmail(self.user,_to,msg.as_string())
        except Exception,e:
            print e
		
        
	 
if __name__=='__main__':
     killslowqurey()
     getdbsync_status()
