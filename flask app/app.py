# --- Flask Backend Skeleton with Comments and Integration Points ---
from flask import Flask, render_template, request, redirect, url_for, session
import os
from loginsystem import login_system
from main import clone

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a strong secret key for session management
# Delete chat history for a clone (POST)
@app.route('/delete_chat/<clone_name>', methods=['POST'])
def delete_chat(clone_name):
	username = session.get('username')
	if not username:
		return redirect(url_for('signin_get'))
	chat_file = os.path.join('users', username, clone_name, 'chat_history.json')
	if os.path.exists(chat_file):
		with open(chat_file, 'w', encoding='utf-8') as f:
			f.write('[]')
	return redirect(url_for('chat_clone', clone_name=clone_name))

# Delete a clone (POST)
@app.route('/delete_clone/<clone_name>', methods=['POST'])
def delete_clone(clone_name):
	username = session.get('username')
	if not username:
		return redirect(url_for('signin_get'))
	user_folder = os.path.join('users', username, clone_name)
	import shutil
	try:
		shutil.rmtree(user_folder)
		# Also remove from static if exists
		static_folder = os.path.join('flask app', 'static', 'users', username, clone_name)
		if os.path.exists(static_folder):
			shutil.rmtree(static_folder)
		return redirect(url_for('dashboard'))
	except Exception as e:
		return f"Error deleting clone: {e}", 

# Rename a clone (POST)
@app.route('/rename_clone/<clone_name>', methods=['POST'])
def rename_clone(clone_name):
	username = session.get('username')
	if not username:
		return redirect(url_for('signin_get'))
	new_name = request.form.get('new_name', '').strip()
	if not new_name:
		return "New name required", 400
	old_folder = os.path.join('users', username, clone_name)
	new_folder = os.path.join('users', username, new_name)
	import shutil
	try:
		shutil.move(old_folder, new_folder)
		# Also move static folder if exists
		static_old = os.path.join('flask app', 'static', 'users', username, clone_name)
		static_new = os.path.join('flask app', 'static', 'users', username, new_name)
		if os.path.exists(static_old):
			shutil.move(static_old, static_new)
		return redirect(url_for('chat_clone', clone_name=new_name))
	except Exception as e:
		return f"Error renaming clone: {e}", 500

# Optional: Set chat background (per session or query param)
@app.route('/set_chat_bg', methods=['POST'])
def set_chat_bg():
	bg = request.form.get('chat_bg', '').strip()
	if bg:
		session['chat_bg'] = bg
	return ('', 204)
# Home route: always show sign-in form
@app.route('/')
def home():
	# Renders the login/signup page. Toggle form with JS or template logic.
	return render_template('index.html', form='signin', message=None, bg_file='login_bg.jpg')

# GET: Show sign-in form
@app.route('/signin', methods=['GET'])
def signin_get():
	message = request.args.get('message')
	return render_template('index.html', form='signin', message=message, bg_file='login_bg.jpg')

# POST: Handle sign-in (calls backend logic)
@app.route('/signin', methods=['POST'])
def signin():
	username = request.form.get('username')
	password = request.form.get('password')
	user = login_system()
	output, message = user.signin(username, password)
	if output:
		session['username'] = username
		return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('signin_get', message=message))

# GET: Show sign-up 
@app.route('/signup', methods=['GET'])
def signup_get():
	message = request.args.get('message')
	return render_template('index.html', form='signup', message=message, bg_file='login_bg.jpg')

# POST: Handle sign-up (calls backend logic)
@app.route('/signup', methods=['POST'])
def signup():
	username = request.form.get('reg_username')
	password = request.form.get('reg_password')
	user = login_system()
	output, message = user.signup(username, password)
	if output:
		session['username'] = username
		return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('signup_get', message=message))

# Dashboard route: main landing page after login
@app.route('/dashboard')
def dashboard():
	# Require login
	username = session.get('username')
	if not username:
		return redirect(url_for('signin_get'))
	# Fetch user's clones from backend (list folders in users/<username>)
	user_folder = os.path.join('users', username)
	
	clones = []
	clone_pics = {}
	if os.path.exists(user_folder):
		for clone in os.listdir(user_folder):
			clones.append(clone)
			# Optionally, check for a profile pic for each clone
			pic_path = os.path.join(user_folder, clone, 'profile.jpg')
			if os.path.exists(pic_path):
				clone_pics[clone] = f'users/{username}/{clone}/profile.jpg'
	# Optionally, set user profile pic
	profile_pic = None
	user_pic_path = os.path.join(user_folder, 'profile.jpg')
	if os.path.exists(user_pic_path):
		profile_pic = f'users/{username}/profile.jpg'
	return render_template('dashboard.html', username=username, clones=clones, clone_pics=clone_pics, profile_pic=profile_pic)

# --- ADD THIS NEW SECTION TO app.py ---


# Route to show the clone creation form and handle POST
@app.route('/create_clone', methods=['GET', 'POST'])
def create_clone_view():
	if not session.get('username'):
		return redirect(url_for('signin_get'))
	message = None
	success = None
	clone_name = ''
	personality_data = ''
	if request.method == 'POST':
		username = session.get('username')
		clone_name = request.form.get('clone_name', '').strip()
		personality_data = request.form.get('personality_data', '').strip()
		personality_file=request.form.get("personality_file",'')
		user_clone = clone(username, None)
		if personality_file!=None:
			with open('try.txt','w') as f:
				f.writelines(personality_file)
			output, message = user_clone.create_clone(clone_name,personality_file)
		else: 
			output, message = user_clone.create_clone(clone_name, personality_data)
		success = output
		if output:
			# On success, redirect to dashboard with a message
			return redirect(url_for('dashboard', message=message))
		# On failure, show the form again with error
	return render_template('create_clone.html', message=message, success=success, clone_name=clone_name, personality_data=personality_data)

# --- END NEW SECTION ---

# Chat page for a clone: supports GET (show history) and POST (send message, get AI reply)
@app.route('/chat/<clone_name>', methods=['GET', 'POST'])
def chat_clone(clone_name):
    # Require login
    username = session.get('username')
    if not username:
        return redirect(url_for('signin_get'))

    from main import clone, load_chat_history
    user_clone = clone(username, None)
    chat_history = load_chat_history(username, clone_name)
    ai_response = None
    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()
        if user_message:
            success, ai_response = user_clone.chat_the_clone(clone_name, user_message)
            # Reload chat history after update
            chat_history = load_chat_history(username, clone_name)
    # Set chat background and clone profile pic (ensure static path)
    user_folder = os.path.join('users', username, clone_name)
    chat_bg = session.get('chat_bg') or 'my_anime_poster.png.webp'
    clone_pic = None
    pic_path = os.path.join('flask app', 'static', 'users', username, clone_name, 'profile.jpg')
    # If not found in static, fallback to users folder (legacy)
    if os.path.exists(pic_path):
        clone_pic = f'users/{username}/{clone_name}/profile.jpg'
    else:
        legacy_pic = os.path.join('users', username, clone_name, 'profile.jpg')
        if os.path.exists(legacy_pic):
            # Optionally, copy to static for future
            import shutil
            static_dir = os.path.join('flask app', 'static', 'users', username, clone_name)
            os.makedirs(static_dir, exist_ok=True)
            shutil.copy2(legacy_pic, os.path.join(static_dir, 'profile.jpg'))
            clone_pic = f'users/{username}/{clone_name}/profile.jpg'
    # Load clone details (optional: from clone.json)
    clone_details = None
    import json
    clone_json_path = os.path.join('users', username, clone_name, 'clone.json')
    if os.path.exists(clone_json_path):
        with open(clone_json_path, 'r', encoding='utf-8') as f:
            try:
                clone_details = json.load(f)
            except Exception:
                clone_details = None
    return render_template('chat.html', clone_name=clone_name, chat_history=chat_history, chat_bg=chat_bg, clone_pic=clone_pic, ai_response=ai_response, clone_details=clone_details, theme=session.get('theme', 'dark'))

# Theme toggle endpoint
@app.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    if 'theme' not in session or session['theme'] == 'dark':
        session['theme'] = 'light'
    else:
        session['theme'] = 'dark'
    return ('', 204)

# Settings page: change username/password, delete account, logout
@app.route('/settings', methods=['GET', 'POST'])
def settings():
	user = login_system()
	result_message = None
	result_success = None
	if request.method == 'POST':
		if 'old_username' in request.form and 'new_username' in request.form:
			# Change username logic
			old_username = request.form['old_username']
			new_username = request.form['new_username']
			ok = user.change_username(old_username, new_username)
			if ok:
				result_message = 'Username changed successfully.'
				result_success = True
				session['username'] = new_username
			else:
				result_message = 'Failed to change username. Please follow guidelines.'
				result_success = False
		elif 'old_password' in request.form and 'new_password' in request.form:
			# Change password logic
			username = session.get('username')
			old_password = request.form['old_password']
			new_password = request.form['new_password']
			ok = user.change_password(username, old_password, new_password)
			if ok:
				result_message = 'Password changed successfully.'
				result_success = True
			else:
				result_message = 'Failed to change password. Please follow guidelines.'
				result_success = False
		elif 'delete_account' in request.form:
			# Delete account logic
			username = session.get('username')
			ok = user.delete_account(username)
			if ok:
				session.clear()
				return redirect(url_for('home'))
			else:
				result_message = 'Failed to delete account.'
				result_success = False
	theme = session.get('theme', 'dark')
	return render_template('settings.html', result_message=result_message, result_success=result_success, theme=theme)

# About page
@app.route('/about')
def about():
	return render_template('about.html')

# Theme page (toggle day/night mode)
@app.route('/theme')
def theme():
	# Pass the current theme to the template
	theme = session.get('theme', 'dark')
	return render_template('theme.html', theme=theme)

# Logout route
@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))

if __name__ == '__main__':
	print("--- Starting Flask Server ---")
	app.run(debug=True)
# Backup of your original app.py before refactor
