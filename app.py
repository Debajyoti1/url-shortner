from flask import Flask, render_template, url_for, request, session, redirect, g, jsonify
import sqlite3
import random
import string

app = Flask(__name__)
app.secret_key='Hellothere'

@app.route('/')
def index():
    return render_template('index.html')
def c(u):
    try:
        conn = sqlite3.connect('serv.db')
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(5)))
        st='''insert into urls values('{}','{}');'''.format(result_str,u)
        print(st)
        conn.execute(st)
        conn.commit()
        conn.close()
        return result_str
    except:
        return 1

@app.route('/create',methods=['GET','POST'])
def create():
    if request.method== 'GET':
        u=request.args['url']
        ret=c(u)
        if ret!=1:
            return render_template('done.html',val=ret,ur=u)
    else:
        return '<h1>Something went wrong!!!</h1>'
@app.route('/go',methods=['GET','POST'])
def go():
    if request.method== 'GET':
        u=request.args['url']
        conn = sqlite3.connect('serv.db')
        st='''select * from urls where value='{}';'''.format(u)
        cursor = conn.execute(st)
        curl=list(cursor)
        conn.close()
        if len(curl)<1:
            return '<h1>No url found</h1>'
        else:
            print(curl[0][1])
            if 'http'==curl[0][1][:4]:
                print(curl[0][1])
                return redirect(curl[0][1],code=302)
            else:
                print('http://'+curl[0][1])
                return redirect('http://'+curl[0][1],code=302)
@app.route('/data',methods=['GET','POST'])
def data():
    conn = sqlite3.connect('serv.db')
    st='''select * from urls;'''
    cursor = conn.execute(st)
    strr=''
    for i in cursor:
        strr+=str(i)+'\n'
    return strr
if __name__ == '__main__':
    app.run(debug=True)