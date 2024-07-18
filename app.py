from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from config.config import configure_app
from admin.admin import setup_admin
from models.models import *
from views.views import *
from extensions.extensions import db
from flask_cors import CORS
from flask_apscheduler import APScheduler
import secrets
import string


app = Flask(__name__)
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Manila'


def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


app.config['SECRET_KEY'] = generate_secret_key()


CORS(app)
configure_app(app)

db.init_app(app)

migrate = Migrate(app, db)


scheduler = APScheduler()
scheduler.init_app(app)

api = Api(app)

setup_admin(app, db)

with app.app_context():
    db.create_all()

@app.route('/api/verify/<string:id>')
def verifyID(id):
    user = User.query.filter_by(serial=str(int(id))).first()
    if not user:
        return jsonify({'result': 0})
    if user.user_type == 1 or user.classes_right_now:
        return jsonify({'result': 1})
    else:
        return jsonify({'result': 0})

api.add_resource(Users, '/api/users')
api.add_resource(SpecificUser, '/api/user/<int:user_id>')
api.add_resource(Courses, '/api/courses')
api.add_resource(SpecificCourse, '/api/course/<int:course_id>')
api.add_resource(CourseSchedules, '/api/course-schedules')
api.add_resource(SpecificCourseSchedule, '/api/course-schedule/<int:course_schedule_id>')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserRegistration, '/api/register')
api.add_resource(UserCourseSchedules, '/api/user-course-schedule/<int:course_schedule_id>')
api.add_resource(UsersInSchedule, '/api/users-schedule/<int:course_schedule_id>')
api.add_resource(uploadCSV, '/api/upload-csv')
api.add_resource(UserInformation, '/api/update-user-information/<int:pk>')
api.add_resource(ScheduleToday, '/api/schedules-today')

if __name__ == '__main__':
    from tasks.task import *
    app.run(host='0.0.0.0', port=5000)
