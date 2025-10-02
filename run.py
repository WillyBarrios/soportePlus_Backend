import os
from flask_migrate import upgrade
from app import create_app, db
from app.models import Usuario

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")


@app.cli.command()
def create_admin():
    """Create an admin user."""
    # Note: The database already has admin users
    # Use: jadmin@gmail.com / secret123 or madmin@gmail.com / secret123
    print("Admin users already exist in the remote database:")
    print("Email: jadmin@gmail.com | Password: secret123")
    print("Email: madmin@gmail.com | Password: secret123")
    print("Email: padmin@test.com | Password: secret123") 
    print("Email: aadmin@test.com | Password: secret123")


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell."""
    return {'db': db, 'Usuario': Usuario}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

    