# -*- coding: cp936 -*-
from flask import Flask, jsonify, render_template,request
import types
import json
import os
import MySQLdb
import sqlite3
import string
from loc import localization

testserver=Flask(__name__)
#������֤ͨ������Ӧ�÷���ʲô
def send_ok_json(data=None):
    if not data:
        data = {}
    ok_json = {'ok':True, 'loc':data}
    return json.dumps(ok_json)

def send_fail_json():
    fail_json = {'ok':False}
    return json.dumps(fail_json)

#�����ѯλ�������ص�����
def query_ok_json(data=None):
    if not data:
        data = {}
    ok_json = {'ok':True, 'loc':data}
    return json.dumps(ok_json)

def query_fail_json():
    fail_json = {'ok':False}
    return json.dumps(fail_json)

#login����ʵ�ֵĹ���
#1������post��ʽֱ��������������û��������롢rss����ݡ�ʱ����Ϣ��
#2��stat�����ǹ��˻��ǹ���Ա,1Ϊ����Ա��0����
#3�����ͨ����֤���򷵻�λ�����ݣ�����¼������˵�λ����Ϣ������ʱ�̣�λ�ã�ָ�ƣ�
@testserver.route('/login/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        usern=request.form.get('username')
        passw=request.form.get('password')
        rss=request.form.get('rss')
        stat=request.form.get('status')
        time=request.form.get('time')
        rssv=string.atof(rss)#��������ʱ��������
        location=localization.loc(rss) #���ö�λ����������RSS���ж�λ

        #�������ݿ�
        db=MySQLdb.connect(host='localhost',user='root',passwd='wuyou',db='noyou_db') 
        cursor=db.cursor()        
        #ִ��sql���
        #�˶��û�
        sql="select * from account where username=%s and password=%s and status=%s"#�з���ͳ�Ƶ����ݼ�¼��
        exist=cursor.execute(sql,(usern, passw, stat))#����ͳ��
        #����¼���ݿ������λ����Ϣ
        insertrec="insert into locrecord (username, rss, loc, time) values(%s, %s, %s, %s)"#��λ�����ݿ�������¼����¼λ�á��û�����ʱ�䡢rss
        if exist==1:#������ڸ��û�������ȷ��������¼
            cursor.execute(insertrec, (usern, rss, location, time))        
        db.commit()
        cursor.close()
        db.close()
        logfail='account does not exist'
        logsucess='%f' %(location)#
        if exist==1:       
            return send_ok_json(logsucess)
        if exist!=1:
            return send_fail_json(logfail)
        
       
    #���������������
    if request.method=="GET":
        return render_template('login.html')


#��ѯĳ������ĳ��ʱ���λ��.
#ɾ����qexist���жϣ�
@testserver.route('/query/',methods=['GET','POST'])
def query():
     #���������������
    if request.method=="GET":
        return render_template('query.html')
    if request.method=="POST":
        usern=request.form.get('username')
        passw=request.form.get('password')
        quser=request.form.get('quser')
        stat=request.form.get('status')
        time=request.form.get('time')
        #�������ݿ�
        db=MySQLdb.connect(host='localhost',user='root',passwd='wuyou',db='noyou_db') 
        cursor=db.cursor()        
        #ִ��sql���
        #�˶��û�
        sql="select * from account where username=%s and password=%s and status=%s"#�з���ͳ�Ƶ����ݼ�¼��
        quserv="select * from locrecord where username=%s"#���ָ�Ƽ�¼�����Ƿ���ڸ��û��������Լ�һ���ڰ�count�����Ƿ�����
        query="select * from locrecord where username=%s and time=%s"#��ѯʱ���趨��û�����ôŪ
        exist=cursor.execute(sql,(usern, passw, stat))#����ͳ��
        qexist=cursor.execute(quserv,(quser))
        qtexist=cursor.execute(query,(quser, time))
        
        if exist==1 & qtexist==1:#���ͨ����֤�����ǹ���Ա,���Ҵ��ڼ�¼����¼�������ظ��ģ����޸ģ�
            cursor.execute(query,(quser, time))
            qloc=cursor.fetchone()
            loca=qloc[0]
            qresult="%s" %(loca)
            cursor.close()
            db.close()
            return query_ok_json(qresult)
        else:
            cursor.close()
            db.close()
            return query_fail_json()#�ɶ�Ӽ����ж�





if __name__=='__main__':
  
    testserver.run(host='0.0.0.0', port=5000,debug=True)
