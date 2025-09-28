from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only for demo)."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Simple admin check
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    users = User.query.all()
    users_data = []
    
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat()
        })
    
    return jsonify({'users': users_data})


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user."""
    current_user_id = get_jwt_identity()
    
    # Users can only see their own profile or admin can see all
    if current_user_id != user_id:
        current_user = User.query.get(current_user_id)
        if not current_user.is_admin:
            return jsonify({'error': 'Access denied'}), 403
    
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        }
    })