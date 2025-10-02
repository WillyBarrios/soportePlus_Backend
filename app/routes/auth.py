from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError

from app import db
from app.models.soporteplus_models import Usuario  # Usar el modelo Usuario real

auth_bp = Blueprint('auth', __name__)


class RegisterSchema(Schema):
    """Schema for user registration."""
    nombre = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    ID_Rol = fields.Int(required=False, missing=2)  # Por defecto rol técnico


class LoginSchema(Schema):
    """Schema for user login."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    schema = RegisterSchema()
    
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Check if user already exists by email (more reliable than name)
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Check if name already exists (optional check)
    if Usuario.query.filter_by(Nombre=data['nombre']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # Create new user
    user = Usuario(
        Nombre=data['nombre'],
        email=data['email'],
        ID_Rol=data['ID_Rol']
    )
    user.set_password(data['password'])
    user.save()
    
    # Generate tokens
    tokens = user.get_tokens()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.ID_usuario,
            'nombre': user.Nombre,
            'email': user.email,
            'ID_Rol': user.ID_Rol
        },
        'tokens': tokens
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user."""
    schema = LoginSchema()
    
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Find user by email
    user = Usuario.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 401
    
    # Generate tokens
    tokens = user.get_tokens()
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.ID_usuario,
            'nombre': user.Nombre,
            'email': user.email,
            'ID_Rol': user.ID_Rol,
            'is_admin': user.is_admin
        },
        'tokens': tokens
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information."""
    user_id = int(get_jwt_identity())  # Convertir de string a int
    user = Usuario.query.get_or_404(user_id)
    
    return jsonify({
        'user': {
            'id': user.ID_usuario,
            'nombre': user.Nombre,
            'email': user.email,
            'ID_Rol': user.ID_Rol,
            'is_admin': user.is_admin
        }
    })