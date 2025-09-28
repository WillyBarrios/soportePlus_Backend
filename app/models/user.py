from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from app import db


class BaseModel(db.Model):
    """Base model with common fields."""
    
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def save(self):
        """Save the model to database."""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the model from database."""
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(BaseModel):
    """User model."""
    
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_tokens(self):
        """Generate JWT tokens for user."""
        return {
            'access_token': create_access_token(identity=self.id),
            'refresh_token': create_refresh_token(identity=self.id)
        }
    
    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"