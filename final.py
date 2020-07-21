from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
import hashlib

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='9820587794'
app.config['MYSQL_DB']='TODO'

mysql=MySQL(app)

@app.route('/app/agent', methods=['GET', 'POST'])
def register():
	password = request.args.get('password')
	username = request.args.get('agent_id')
	temp2=hashlib.md5(password.encode())
	b=temp2.hexdigest()
	cur=mysql.connection.cursor()
	try:
		cur.execute("INSERT INTO agents(agentid,agentpw) VALUES(%s,%s)",(username,b))
		mysql.connection.commit()
		cur.close()
		return jsonify({'status':'account created','status_code':'200'})
	except Exception as e:
		print("Hello")

@app.route('/app/agent/auth',methods=["GET","POST"])
def verify():
	username = request.args.get('agent_id')
	password = request.args.get('password')
	temp2=hashlib.md5(password.encode())
	b=temp2.hexdigest()
	cur=mysql.connection.cursor()
	try:
		cur.execute("SELECT * FROM agents WHERE agentid=%s",(username,))
		res=cur.fetchall()
		pwd=list(res)[0][1]
		print(b)
		print(pwd)
		if b==pwd:
			return jsonify({'status':'success','agent_id':username,'status_code':'200'})
		else:
			return jsonify({'status':'failure','status_code':'401'})
	except Exception as e:
		return jsonify({'status':'failure','status_code':'401'})
		
@app.route('/app/sites', methods=["POST","GET"])
def inserttask():
	a=request.args.get('agent')
	b=request.args.get('title')
	c=request.args.get('description')
	d=request.args.get('category')	
	e=request.args.get('date')
	cur=mysql.connection.cursor()
	try:
		cur.execute("INSERT INTO list(title,description,category,due,agentid) VALUES(%s,%s,%s,%s,%s)",(b,c,d,e,a))
		mysql.connection.commit()
		cur.close()
		return jsonify({'status':'success','status_code':'200'})
	except Exception as e:
		print("Hello")
		
@app.route('/app/sites/list',methods=["POST","GET"])
def showtask():
	a=request.args.get('agent')
	cur=mysql.connection.cursor()
	try:
		cur.execute("SELECT * FROM list WHERE agentid=%s",(a,))
		res=cur.fetchall()
		return str(list(res))
	except Exception as e:
		return "Nothing Found"
		
		
	
if __name__ == '__main__':
	app.run(debug=True)
