from flask import Blueprint, render_template, request, session, flash, redirect, url_for

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        
        if username and role:
            session['username'] = username
            session['user_role'] = role
            flash(f'Welcome, {username}! Logged in as {role}.', 'success')
            return redirect(url_for('main.index'))
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
