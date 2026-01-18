from flask import Blueprint, jsonify, request
from . import db
from .models import User, Task

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Flask API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Username and email are required'}), 400
    
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('user_id'):
        return jsonify({'error': 'Title and user_id are required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        user_id=data['user_id']
    )
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@bp.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    """Mark task as completed"""
    task = Task.query.get_or_404(task_id)
    task.status = 'completed'
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(task.to_dict()), 200