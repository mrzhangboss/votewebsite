# coding=utf-8
from flask import Flask,session,redirect,escape,request,abort
import sys
import dbhelper
base_path=sys.path[0]
app = Flask(__name__)
app.debug=True
administrator_list={'MrZhang':'123456'}
@app.route('/')
def index():
	if 'username' in session:
		return app.send_static_file('index.html')
	else:
		abort(404)
@app.route('/login/<name>')
def login(name):
    session['username'] =escape(name)
    print session['username']
    return redirect('/')

@app.route('/admin/login',methods=['GET','POST'])
def admin_login():
	if request.method=='GET':
		return app.send_static_file('login.html')
	else:
		if valid_login(request.form['UserName'].strip()\
			,request.form['Password'].strip()):
			session['UserName']=escape(request.form['UserName'].strip())
			return app.send_static_file('update.html')
		else:
			return 'Invalid username/password'
def valid_login(UserName,Password):
	for (k, v) in zip(administrator_list.iterkeys(), administrator_list.itervalues()):
		if k==UserName and v==Password:
			return 1
	return 0

# to make only project by one designer
import my_security
@app.route('/admin/update',methods=['POST'])
def admin_update():
	if not 'UserName' in session:
		return 'operate over time'
	else:
		de_file=request.files['file']
		work_name=get_pic_name(de_file.filename.strip(),request.form['UserName'].strip())
		if dbhelper.exit_design(request.form['UserName'].strip()):
			return 'you have already update a designer'
		else:
			de_file.save(base_path+'\\static\\upfile\\'+work_name)
			dbhelper.save_design(filename=work_name,designer=request.form['UserName'].strip())
			return 'Success!'

def get_pic_name(filename,username):
	pswd=my_security.create_hash(username)
	file_type=filename.split('.')
	if not len(file_type)==2:
		raise NameError('the filename is not correct')
	return pswd+'.'+file_type[1]








@app.route('/test')
def test():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

if __name__=='__main__':
	app.secret_key='vote_system'
	app.run()