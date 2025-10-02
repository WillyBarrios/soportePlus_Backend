import os
from flask_migrate import upgrade
from app import create_app, db
from app.models import User

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
    admin = User(
        username='admin',
        email='admin@soporteplus.com',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    admin.set_password('admin123')
    
    try:
        admin.save()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
    except Exception as e:
        print(f"Error creating admin user: {e}")


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell."""
    return {'db': db, 'User': User}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

    