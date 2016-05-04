#!/usr/bin/env python
#coding=utf-8

import sys
import os
import commands
'''
  this is kill slow query processlist scripty.
'''

def getslowqurey():
    logincommand="mysqladmin -uroot -p'xxxx' -hxxx.xxx.xxx.xxx "
    rule = '{0} {1}'.format(logincommand,'processlist')
    (_status,_qureys)=commands.getstatusoutput(rule)
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
                  commands.getstatusoutput('{0} {1} {2}'.format(logincommand,'kill',id))
               #delete slow query processlist if time > 20sec
               elif str(state) == 'Query' and int(time) > 20:
                  commands.getstatusoutput('{0} {1} {2}'.format(logincommand,'kill',id))
                             
#break
       else:
           pass
		
        
	 
if __name__=='__main__':
    getslowqurey()
