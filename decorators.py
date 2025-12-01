from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login')) # Updated to blueprint endpoint
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session:
                return redirect(url_for('auth.login'))
            if session['user_role'] not in allowed_roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.index')) # Updated to blueprint endpoint
            return f(*args, **kwargs)
        return decorated_function
    return decorator
