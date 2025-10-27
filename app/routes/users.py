from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.soporteplus_models import Usuario

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users."""
    current_user_id = get_jwt_identity()
    current_user = Usuario.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user is admin (ID_Rol = 1)
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    users = Usuario.query.all()
    users_data = []
    
    for user in users:
        users_data.append({
            'id': user.ID_usuario,
            'email': user.email,
            'nombre': user.Nombre,
            'rol_id': user.ID_Rol,
            'is_admin': user.is_admin
        })
    
    return jsonify({'users': users_data})


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user."""
    current_user_id = get_jwt_identity()
    
    # Users can only see their own profile or admin can see all
    if int(current_user_id) != user_id:
        current_user = Usuario.query.get(current_user_id)
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Access denied'}), 403
    
    user = Usuario.query.get_or_404(user_id)
    
    return jsonify({
        'user': {
            'id': user.ID_usuario,
            'email': user.email,
            'nombre': user.Nombre,
            'rol_id': user.ID_Rol,
            'is_admin': user.is_admin
        }
    })