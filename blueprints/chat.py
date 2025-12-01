from flask import Blueprint, render_template, request, session, url_for, flash, redirect
from decorators import login_required, role_required
from chat_logic import ChatSession
from risk_logic import persist_assessment

chat_bp = Blueprint('chat', __name__, url_prefix='/assessment/chat')

@chat_bp.route('/')
@login_required
@role_required(['Analyst', 'Admin'])
def assessment_chat():
    if 'chat_session' not in session:
        session['chat_session'] = {}
    return render_template('chat_assessment.html')

@chat_bp.route('/history')
@login_required
def chat_history():
    cs = ChatSession(session.get('chat_session'))
    return {'history': cs.history}

@chat_bp.route('/message', methods=['POST'])
@login_required
def chat_message():
    data = request.get_json()
    user_text = data.get('message')
    
    cs = ChatSession(session.get('chat_session'))
    
    if user_text == 'START_SESSION' and not cs.history:
        response_text, options = cs.generate_response()
        cs.add_message('bot', response_text, options)
    else:
        response_text, options = cs.handle_input(user_text)
        cs.add_message('bot', response_text, options)
    
    session['chat_session'] = cs.to_dict()
    
    if cs.step == 'COMPLETED':
        session['assessment_data'] = cs.data
        return {'text': response_text, 'options': options, 'redirect': url_for('chat.save_chat_assessment')}
        
    return {'text': response_text, 'options': options}

@chat_bp.route('/save')
@login_required
def save_chat_assessment():
    data = session.get('assessment_data')
    if not data:
        return redirect(url_for('main.index'))
        
    persist_assessment(data, session.get('username'))
    
    session.pop('assessment_data', None)
    session.pop('chat_session', None)
    
    flash('Assessment completed via Chat!', 'success')
    return redirect(url_for('main.dashboard'))
