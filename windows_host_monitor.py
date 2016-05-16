from __future__ import division
from email.mime.text import MIMEText
import psutil
import smtplib
import socket
'''
    This script is used to monitor the usage rate of machine disk memory in window system.
'''
localip=socket.gethostbyname(socket.gethostname())

def get_disk_info():
	
	_disk=psutil.disk_partitions()
	# print _disk
	_usage=0
	for diskpart in _disk:
	    if diskpart[3] != 'cdrom':
	        _part=diskpart[0]
	        _totaldisk=psutil.disk_usage(_part)[0]/1024/1024/1024
	        _freedisk=psutil.disk_usage(_part)[2]/1024/1024/1024
	        _usage=psutil.disk_usage(_part)[3]
	        _usmassage='{0} Disk percent used {1}%'.format(_part,_usage)
	        if int(_usage)>80:
	        	_waninginfo='Waring Waring Waring \n\n Host_IP:{0} \n Total:{1}G \n Free:{2}G \n {3}'.format(localip,int(_totaldisk),int(_freedisk),_usmassage)
	        	Sendmail(content=_waninginfo,subject="Disk will be full").send()
            else:
        	    pass


def get_memory_info():
	total= int(psutil.virtual_memory().total/1024/1024)
	free=int(psutil.virtual_memory().free/1024/1024)
	used= "Memory percent used {0}%".format(int(psutil.virtual_memory().percent))
	if used>90:
		_waninginfo='Waring Waring Waring \n\n Host_IP:{0} \n Total:{1}M \n Free:{2}M \n {3}'.format(localip,int(total),int(free),used)
		Sendmail(content=_waninginfo,subject="Memory usage rate is high").send()
	else:
		pass




class Sendmail:
    def __init__(self,to="",cc="",content="",subject=""):
        self.host="smtp.126.com"
        self.user='xxxx@126.com'
        self.pwd='xxxxx'
        self.to=to or ['xxx9@foxmail.com']#,'xiaoshuzhen@chinasoftinc.com']
        self.content= content or 'This is a mail from monitor server'
 #       self.cc= cc or ['']
        self.subject= subject or "mysql warning"
    def send(self):
        msg=MIMEText(self.content)
        msg['From']=self.user
        msg['Subject']=self.subject
        msg['To']=','.join(self.to)
  #      msg['Cc']=','.join(self.cc)
        try:
            s=smtplib.SMTP()
            s.connect(self.host)
            s.login(self.user,self.pwd)
            _to=self.to
            s.sendmail(self.user,_to,msg.as_string())
        except Exception,e:
            print e

if __name__=='__main__':
	get_disk_info()
	get_memory_info()

    
        
