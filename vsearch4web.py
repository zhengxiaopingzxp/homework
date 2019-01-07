#-*- coding=utf-8 -*-#
from flask import Flask, render_template, request, escape,flash
from zhougong import request1,request2,request3
import json, urllib
from urllib import parse


app = Flask(__name__)
appKey="a6e4ba9c7b179bc9fce32fdd92a44114"
app.secret_key = '520'

@app.route('/search4', methods=['POST'])
def do_search():
    """Extract the posted data; perform the search; return results."""
    phrase = request.form['phrase']
    print(phrase)
    title = 'Here are your results:'
    if not parse:
        return None
    results = request2(appKey,phrase,"GET")
    print(results)
    content = []
    if results:
        for i in results:
            content.append(i)
    titles = ('id地址','主要内容','详细信息')
    return render_template('view.html',
                           the_title=u'    哒哒哒~周公为你分析的结果如下',
                           the_row_titles=titles,
                           the_data=content)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login',methods =['POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash("username empty")
            return  render_template('login.html')
        if not password:
            flash('password empty')
            return render_template('login.html')

        account =[];
        with open('user.txt','r') as r:
            data = r.readlines()

        if not data:
            flash('user empty')
            return  render_template('register.html')
        print(account)
        for i in data:
            account.append(i.strip('\n').strip('\r\n'))
        flag =False
        if not account:
            flash('user empty')
            return render_template('register.html')
        for i in account:

            splitData= i.split(':')
            print(splitData)
            print(splitData[0])
            print('username')
            print(username)
            if  splitData:
                if username == splitData[0] and password ==splitData[1]:
                    print('xxx')
                    flag=True
                    break

        print(flag)
        print('flag')
        if  not flag:
            flash('username or password error')
            return render_template('login.html')

        return render_template('lists.html')

@app.route('/register',methods =['GET','POST'])
def register():
    if request.method =='GET':
        return render_template('register.html')
    elif request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash("username empty")
            return render_template('register.html')
        if not password:
            flash('password empty')
            return render_template('register.html')

        with open('user.txt','a+') as f:
            f.write(username+":"+password+"\n")
        return render_template('login.html')

@app.route('/viewlog',methods=['GET','POST'])
def view_the_log():
    """Display the contents of the log file as a HTML table."""
    contents = []
    with open('content.txt.log','r', encoding='UTF-8') as f:
        result =f.readlines()
    if not result:
        result=request1(appKey,'GET')
        print(result)
        if result:
            with open('content.txt','a+') as f :
                for i in result:
                    f.write(i.get('name')+'\n')
    if result:
        for line in result:
            line=line.strip('\n').strip('\r\n')
            contents.append(line)
    titles = ('fid', 'id', 'name')
    return render_template('viewlog.html',
                           the_title='周公解梦--为你剖析梦境中的那景那物那人那事',
                           the_title2='type',
                           the_row_titles=titles,
                           the_data=contents,)
@app.route('/detail')
def detail():
    parems = request.args
    print(parems.get('id'))
    id = parems.get('id')
    result= request3(appKey,id,"GET")
    data =None
    if result:
        data=result
    return render_template('detail.html',data=data)

if __name__ == '__main__':
    app.run(debug=True,port=5001)
