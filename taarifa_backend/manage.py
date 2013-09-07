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
@manager.option("-e", "--email", dest="email")
@manager.option("-c", "--clean", dest="clean", action="store_true", default=False)
def setup(email, clean):
    if clean:
        clear_database()

    if email is None:
        print "Please provide a valid email address for the admin"

    role = Role(name="admin", description="Tarrifa Admin")
    role.save()

    user = User()
    user.email = email
    user.roles = [role]
    user.save()

if __name__ == "__main__":
    manager.run()
