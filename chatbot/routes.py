import datetime
import random
from functools import wraps
import jwt
import pandas as pd
from flask import request, jsonify, make_response, redirect, render_template, url_for, \
	flash, session, send_from_directory
from sklearn.preprocessing import normalize
from werkzeug.security import generate_password_hash, check_password_hash
from chatbot import app, bot, data_loader, helper_methods as helpers
from chatbot.logregform import LoginForm
from chatbot.models import db, chatbot_users, chatbot_logs, error_message, user_roles, \
	RLS_COLUMNS_FILTER_CHOICE
from custom_exceptions import *
import os


# Solution for favicon.ico used as icon on tabs in browser
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
	if 'username' in session:
		return redirect(url_for('home'))

	form = LoginForm()

	if form.validate_on_submit():
		user = chatbot_users.query.filter_by(username=form.username.data).first()
		if not user:
			flash('Login Unsuccessful. Username not found!', 'danger')

		if check_password_hash(user.password_hash, form.password.data):
			token = jwt.encode({
				'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
				app.config['SECRET_KEY'])
			# role = user_roles.query.filter_by(username=user.username).first()
			role = user.role
			session['username'] = form.username.data
			session['role'] = role
			session['token'] = token.decode('UTF-8')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')

	return render_template('login/login.html', title='Login', form=form)


# Logout
@app.route("/logout")
def logout():
	session.pop('username', None)
	return redirect('/')


# Page containing all the existing packages of the user logged in !
@app.route('/home', methods=["GET", "POST"])
def home():
	if 'username' in session:
		username = session['username']
		role = session['role']
		token = session['token']
		return render_template('index.html', username=username, role=role, token=token)

	return redirect(url_for('login'))


# create wt-forms for new users and also a disabled access json form that will be invisible
@app.route('/CreateUser', methods=["GET", "POST"])
def CreateUser():
	if 'username' in session:
		username = session['username']
		current_role = session['role']
		token = session['token']
		if current_role != 'admin':
			return render_template("notAuthorized.html")

		roles = user_roles.query.all()
		role_output = []
		for roles in roles:
			role_data = {'role': roles.role, 'access_json': eval(
				roles.access_json)}
			role_output.append(role_data)

		for col in RLS_COLUMNS_FILTER_CHOICE:
			if 'in' in col['operator_choice'].keys():
				col['value_choice'] = data_loader.get_unique_dim_value(col['col_name'])

		users = chatbot_users.query.all()
		user_output = []
		for user in users:
			user_output.append({'username': user.username, 'role': user.role})

		return render_template('CreateUserNew.html', username=username, role=current_role, token=token,
							   existing_roles=role_output, rls_filters=RLS_COLUMNS_FILTER_CHOICE, users=user_output)
	return redirect(url_for('login'))


@app.route('/UpdateUser/<user_to_update>', methods=["GET", "POST"])
def UpdateUser(user_to_update):
	if 'username' in session:
		username = session['username']
		role = session['role']
		token = session['token']
		if role != 'admin':
			return render_template("notAuthorized.html")

		user_to_update = chatbot_users.query.filter_by(username=user_to_update).first()
		role_to_update = user_roles.query.filter_by(role=user_to_update.role).first()
		roles_data = user_roles.query.all()
		role_output = []
		for roles in roles_data:
			output = {'role': roles.role, 'access_json': eval(roles.access_json)}
			role_output.append(output)

		if user_to_update.username == username:
			return render_template("notAuthorized.html")

		for col in RLS_COLUMNS_FILTER_CHOICE:
			if 'in' in col['operator_choice'].keys():
				col['value_choice'] = data_loader.get_unique_dim_value(col['col_name'])

		user_details = {'username': user_to_update.username, 'name': user_to_update.name, 'role': user_to_update.role,
						'access_json': role_to_update.access_json}
		return render_template('UpdateUser.html', username=username, role=role, token=token, user_details=user_details,
							   user_roles=role_output, rls_filters=RLS_COLUMNS_FILTER_CHOICE)

	return redirect(url_for('login'))


@app.route('/test', methods=["GET", "POST"])
def test():
	return render_template("test.html")


@app.route('/view_user', methods=["GET", "POST"])
def view_user():
	if 'username' in session:
		username = session['username']
		role = session['role']
		token = session['token']
		if role != 'admin':
			return render_template("notAuthorized.html")
		return render_template('ViewUser.html', username=username, role=role, token=token)

	return redirect(url_for('login'))


# =================================================================

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({'message': 'Token is missing'}), 401

		# noinspection PyBroadException
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = chatbot_users.query.filter_by(username=data['username']).first()
			if not current_user:
				return jsonify({'message': 'Token is invalid'}), 401
		except:
			return jsonify({'message': 'Token is invalid! Please Login again'}), 401
		return f(current_user, *args, **kwargs)

	return decorated


# ========================================
@app.route('/api/DeleteUser/<username>', methods=["GET", "POST"])
@token_required
def delete_user(current_user, username):
	# current_user_role = user_roles.query.filter_by(username=current_user.username).first()
	current_user_role = chatbot_users.query.filter_by(username=current_user.username).first()
	if current_user_role.role != 'admin':
		return jsonify({'message': 'Access Denied! You do not have permission to do that.'}), 401
	if current_user.username == username:
		return jsonify({'message': 'Access Denied! You do not have permission to delete.'}), 401
	status = chatbot_users.query.filter_by(username=username).delete()
	db.session.commit()
	if status:
		return jsonify({'message': 'User deleted successfully.'})
	return jsonify({'message': "User could not be deleted"})


@app.route('/api/UpdateUser', methods=['POST'])
@token_required
def update_user(current_user):
	# current_user_role = user_roles.query.filter_by(username=current_user.username).first()
	# current_user_role = chatbot_users.query.filter_by(username=current_user.username).first()

	if current_user.role != 'admin':
		return jsonify({'message': 'Access Denied! You do not have permission to do that.'}), 401
	data = request.get_json()
	if not data:
		return jsonify({'message': 'Cannot Find Post data'}), 401
	username = data.get('username')
	name = data.get('name')
	role = data.get('role')

	password = data.get('password')
	# update_role=data.get('update_role')
	is_new_role = data.get('is_new_role')
	if not username:
		return jsonify({'message': 'username cannot be empty!'}), 401
	if not role:
		return jsonify({'message': 'You must provide a role name for the user'}), 401
	if not password:
		return jsonify({'message': 'password can not be empty!'}), 401
	if current_user.username == username:
		return jsonify({'message': 'Access Denied! You cannot update yourself.'}), 401
	password_hash = generate_password_hash(password, method='sha256')
	try:
		user_details = chatbot_users.query.filter_by(username=username).first()
		user_details.name = name
		user_details.password_hash = password_hash
		user_details.role = role
		if is_new_role:
			access_json = data.get('access_json')
			if not access_json and access_json != []:
				return jsonify({'message': 'You must select accessible column values for the user.'}), 401
			new_user_role = user_roles(role=role, access_json=str(access_json))
			db.session.add(new_user_role)

		if not is_new_role:
			user_role = user_roles.query.filter_by(role=role).first()
			if not user_role:
				return jsonify({'message': 'Role does not exist! Contact admin for Registration.'}), 401

		db.session.commit()
	except Exception as e:
		return jsonify({'message': 'Error Occurred While Updating User!', 'Error Message': str(e)}), 400
	return jsonify({'message': 'User Updated Successfully!'})


# ========================================
@app.route('/api/login')
def apilogin():
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response('Enter Username and Password!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

	username = auth.username
	if not username:
		return make_response('Username not found!', 404, {'WWW-Authenticate': 'Basic realm="Login Required"'})

	user = chatbot_users.query.filter_by(username=username).first()
	if not user:
		return make_response('Username does not exist! Contact admin for Registration.', 401,
							 {'WWW-Authenticate': 'Basic realm="Login Required"'})

	if check_password_hash(user.password_hash, auth.password):
		token = jwt.encode({
			'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
			app.config['SECRET_KEY'])
		# role = user_roles.query.filter_by(username=user.username).first()
		role = user.role
		return jsonify({'token': token.decode('UTF-8'), 'role': role})
	return make_response('Username or Password is Incorrect!', 401,
						 {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/api/get_users', methods=['GET', 'POST'])
@token_required
def get_users(current_user):
	if current_user.role != 'admin':
		return jsonify({'message': 'Access Denied! You do not have permission to do that.'}), 401
	if request.method == 'GET':
		users = chatbot_users.query.all()
		user_output = []
		for user in users:
			role = user_roles.query.filter_by(role=user.role).first()
			user_data = {'username': user.username, 'name': user.name, 'role': role.role, 'access_json': eval(
				role.access_json)}
			user_output.append(user_data)
		return jsonify(user_output)
	elif request.method == 'POST':
		json = request.get_json()
		if 'username' not in json:
			return jsonify({'message': 'No username found on post data!'}), 201
		username = json['username']
		user = chatbot_users.query.filter_by(username=username).first()
		if not user:
			return jsonify({'message': 'No user found'})
		role = user_roles.query.filter_by(role=user.role).first()
		# role=user.role
		user_data = {'username': user.username, 'name': user.name, 'role': role.role, 'access_json': role.access_json}
		return jsonify(user_data)


@app.route('/api/get_roles', methods=['GET', 'POST'])
@token_required
def get_roles(current_user):
	if current_user.role != 'admin':
		return jsonify({'message': 'Access Denied! You do not have permission to do that.'}), 401
	if request.method == 'GET':
		roles = user_roles.query.all()
		role_output = []
		for roles in roles:
			role = user_roles.query.filter_by(role=roles.role).first()
			role_data = {'role': role.role, 'access_json': eval(
				role.access_json)}
			role_output.append(role_data)
		return jsonify(role_output)
	elif request.method == 'POST':
		json = request.get_json()
		if 'role' not in json:
			return jsonify({'message': 'No user role found on post data!'}), 201
		role = json['role']

		role = user_roles.query.filter_by(role=role).first()
		if not role:
			return jsonify({'message': 'No role found'})
		# role=user.role
		role_data = {'role': role.role, 'access_json': role.access_json}
		return jsonify(role_data)


@app.route('/api/get_rls_filters', methods=['GET'])
@token_required
def get_rls_filters(current_user):
	# current_user_role = user_roles.query.filter_by(username=current_user.username).first()
	if current_user.role != 'admin':
		return jsonify({'message': 'Access Denied! You do not have permission to do that.'}), 401
	for col in RLS_COLUMNS_FILTER_CHOICE:
		if 'in' in col['operator_choice'].keys():
			col['value_choice'] = data_loader.get_unique_dim_value(col['col_name'])

	return jsonify(RLS_COLUMNS_FILTER_CHOICE)


@app.route('/api/create_user', methods=['POST'])
@token_required
def create_user(current_user):
	# current_user_role = user_roles.query.filter_by(username=current_user.username).first()
	if current_user.role != 'admin':
		return jsonify({'message': 'Access Denied! You do not have permission to do that.'}), 401
	data = request.get_json()
	if not data:
		return jsonify({'message': 'Cannot Find Post data'}), 401
	username = data.get('username')
	name = data.get('name')
	role = data.get('role')

	password = data.get('password')
	existing_role = data.get('existing_role')
	if not username:
		return jsonify({'message': 'username cannot be empty!'}), 401
	if not role:
		return jsonify({'message': 'You must provide a role name for the user'}), 401
	if not password:
		return jsonify({'message': 'password can not be empty!'}), 401

	password_hash = generate_password_hash(password, method='sha256')
	try:
		if existing_role:
			user_role = user_roles.query.filter_by(role=role).first()
			if not user_role:
				return jsonify({'message': 'Role does not exist! Create Role First!'}), 401

		new_user = chatbot_users(
			username=username, name=name, password_hash=password_hash, role=role)
		db.session.add(new_user)
		if not existing_role:
			access_json = data.get('access_json')
			if not access_json and access_json != []:
				return jsonify({'message': 'You must select accessible column values for the user.'}), 401
			new_user_role = user_roles(role=role, access_json=str(access_json))
			db.session.add(new_user_role)

		db.session.commit()
	except Exception as e:
		return jsonify({'message': 'Error Occurred While Creating User!', 'Error Message': str(e)}), 400
	return jsonify({'message': 'User Created Successfully!'})


# @app.route('/api')
# def index():
# 	return redirect(GUI_ADDRESS)


@app.route('/api/get_popular_queries')
@token_required
def get_popular_queries(current_user):
	number = request.args.get('queries')
	if not number:
		return jsonify({'message': 'Bad Request! \'queries\' not specified'}), 400
	try:
		number = int(number)
	except ValueError:
		return jsonify({'message': 'Bad Request! \'queries\' not valid!'}), 400

	# Popular queries algorithm
	logs_df = pd.read_sql(db.session.query(chatbot_logs.user_query, chatbot_logs.query_parameters,
										   chatbot_logs.query_response, chatbot_logs.create_time).filter_by(
		username=current_user.username, status='SUCCESS').statement, db.session.bind)

	if logs_df.empty:
		return jsonify([])

	# Get parameters without date_condition in it
	logs_df['parameter_no_date'] = logs_df['query_parameters'].apply(
		lambda x: x[0:x.find("date_condition") - 5] if x.find("date_condition") > -1 else x)

	# Group by parameters no date
	logs_df = logs_df.groupby('parameter_no_date').agg({'user_query': ['max', 'count'],
														'create_time': 'max'})
	logs_df.columns = ['user_query', 'frequency', 'create_time']
	logs_df['recency'] = -(logs_df['create_time'].max() - logs_df['create_time']).dt.total_seconds()

	# Get new response based on the recency of the query
	logs_df['query_response'] = logs_df.apply(
		lambda x: get_query_response(x.user_query, current_user, logging=False)[0], axis=1)

	norm = normalize(logs_df[['recency', 'frequency']], axis=0)
	logs_df['score'] = norm[:, 0] + norm[:, 1]
	logs_df = logs_df[['user_query', 'query_response', 'score']].sort_values(
		'score', ascending=False).iloc[0: number]
	response = logs_df.to_dict('records')

	return jsonify(response)


def get_query_response(user_query, current_user, logging=True):
	security_access_string = user_roles.query.filter_by(role=current_user.role).first().access_json
	try:
		query_response, entities = bot.get_json_from_query(user_query, security_access_string)
		query_parameters = str(entities)
		status = 'SUCCESS'
		error_name = None
		error_msg = None

	except DialogFlowDataError as e:
		error_messages = error_message.query.filter_by(error_name='DialogFlowDataError').all()
		r = random.randrange(0, len(error_messages))
		query_response = {'message': error_messages[r].message}
		query_parameters = None
		status = 'FAIL'
		error_name = 'DialogFlowDataError'
		error_msg = str(e)

	except NoFactError as e:
		error_messages = error_message.query.filter_by(error_name='NoFactError').all()
		r = random.randrange(0, len(error_messages))
		query_response = {'message': error_messages[r].message}
		query_parameters = None
		status = 'FAIL'
		error_name = 'NoFactError'
		error_msg = str(e)

	except ConditionNotDefined as e:
		error_messages = error_message.query.filter_by(error_name='ConditionNotDefined').all()
		r = random.randrange(0, len(error_messages))
		query_response = {'message': error_messages[r].message}
		query_parameters = None
		status = 'FAIL'
		error_name = 'ConditionNotDefined'
		error_msg = str(e)

	except NoFactInOperand as e:
		error_messages = error_message.query.filter_by(error_name='NoFactInOperand').all()
		r = random.randrange(0, len(error_messages))
		query_response = {'message': error_messages[r].message}
		query_parameters = None
		status = 'FAIL'
		error_name = 'NoFactInOperand'
		error_msg = str(e)
	except NoLeftOperandInPercentage as e:
		error_messages = error_message.query.filter_by(error_name='NoLeftOperandInPercentage').all()
		r = random.randrange(0, len(error_messages))
		query_response = {'message': error_messages[r].message}
		query_parameters = None
		status = 'FAIL'
		error_name = 'NoLeftOperandInPercentage'
		error_msg = str(e)

	except TimeoutError as e:
		error_messages = error_message.query.filter_by(error_name='TimeoutError').all()
		r = random.randrange(0, len(error_messages))
		query_response = {'message': error_messages[r].message}
		query_parameters = None
		status = 'FAIL'
		error_name = 'TimeoutError'
		error_msg = str(e)

	except ConnectionError as e:
		error_messages = error_message.query.filter_by(error_name='ConnectionError').all()
		r = random.randrange(0, len(error_messages))
		query_response = {'message': error_messages[r].message}
		query_parameters = None
		status = 'FAIL'
		error_name = 'ConnectionError'
		error_msg = str(e)

	except Exception as e:
		error_messages = error_message.query.filter_by(error_name='Default').all()
		r = random.randrange(0, len(error_messages))
		query_response = {'message': error_messages[r].message}
		query_parameters = None
		status = 'FAIL'
		error_name = 'Default'
		error_msg = str(e)

	if logging:
		new_log = chatbot_logs(username=current_user.username, user_query=user_query, query_parameters=query_parameters,
							   query_response=str(query_response), create_time=datetime.datetime.now(), status=status,
							   error_name=error_name, error_message=error_msg)
		db.session.add(new_log)
		db.session.commit()

	return query_response, status


# noinspection PyBroadException
@app.route('/api/resolve_query')
@token_required
def resolve_query(current_user):
	user_query = request.args.get('message')
	if not user_query:
		return jsonify({'message': 'could not find message in request!'}), 400

	response, status = get_query_response(user_query=user_query, current_user=current_user)

	if status == 'FAIL':
		return jsonify(response), 400
	return jsonify(response)
