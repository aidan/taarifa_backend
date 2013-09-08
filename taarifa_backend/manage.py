# Set the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server

from taarifa_backend import app
from taarifa_backend.models import clear_database, Role, User

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)


# Setup roles and initial admin user
@manager.option("-e", "--email", dest="email", required=True,
                help="Email address (required)")
@manager.option("-c", "--clean", dest="clean", action="store_true",
                default=False, help="Clear the user and role database")
def setup(email, clean):
    """Create a new admin user with given email address."""
    if clean:
        clear_database()

    role, _ = Role.objects.get_or_create(name="admin",
                                         defaults={'description': 'Taarifa Admin'})
    User(email=email, roles=[role]).save()

if __name__ == "__main__":
    manager.run()
