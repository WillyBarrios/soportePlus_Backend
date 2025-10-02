from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import Usuario

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users."""
    current_user_id = get_jwt_identity()
    current_user = Usuario.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user is admin (tipo_usuario = 'Administrador')
    if current_user.tipo_usuario != 'Administrador':
        return jsonify({'error': 'Admin access required'}), 403
    
    users = Usuario.query.all()
    users_data = []
    
    for user in users:
        users_data.append({
            'id': user.id,
            'email': user.email,
            'nombre': user.nombre,
            'apellido': user.apellido,
            'tipo_usuario': user.tipo_usuario,
            'fecha_creacion': user.fecha_creacion.isoformat() if user.fecha_creacion else None
        })
    
    return jsonify({'users': users_data})


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user."""
    current_user_id = get_jwt_identity()
    
    # Users can only see their own profile or admin can see all
    if current_user_id != user_id:
        current_user = Usuario.query.get(current_user_id)
        if not current_user or current_user.tipo_usuario != 'Administrador':
            return jsonify({'error': 'Access denied'}), 403
    
    user = Usuario.query.get_or_404(user_id)
    
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'nombre': user.nombre,
            'apellido': user.apellido,
            'tipo_usuario': user.tipo_usuario,
            'fecha_creacion': user.fecha_creacion.isoformat() if user.fecha_creacion else None
        }
    })