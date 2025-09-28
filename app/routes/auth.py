from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError

from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


class RegisterSchema(Schema):
    """Schema for user registration."""
    username = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


class LoginSchema(Schema):
    """Schema for user login."""
    username = fields.Str(required=True)
    password = fields.Str(required=True)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    schema = RegisterSchema()
    
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    user.set_password(data['password'])
    user.save()
    
    # Generate tokens
    tokens = user.get_tokens()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name
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
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 401
    
    # Generate tokens
    tokens = user.get_tokens()
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name
        },
        'tokens': tokens
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat()
        }
    })