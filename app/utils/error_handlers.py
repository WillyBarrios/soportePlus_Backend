from flask import jsonify
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError


def register_error_handlers(app):
    """Register error handlers for the Flask app."""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Handle Marshmallow validation errors."""
        return jsonify({'errors': e.messages}), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle 404 errors."""
        return jsonify({
            'error': 'Resource not found',
            'message': 'The requested resource does not exist'
        }), 404
    
    @app.errorhandler(403)
    def handle_forbidden(e):
        """Handle 403 errors."""
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(401)
    def handle_unauthorized(e):
        """Handle 401 errors."""
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """Handle 500 errors."""
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle general HTTP exceptions."""
        return jsonify({
            'error': e.name,
            'message': e.description
        }), e.code