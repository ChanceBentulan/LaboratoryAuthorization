from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models.models import User, CourseSchedule, Course, UserAdmin, UserCourseSchedule


class CourseScheduleView(ModelView):
    column_list = ('id', 'course_id', 'days', 'start_time', 'end_time', 'room')


class UserAdminView(ModelView):
        column_list = ['username', 'password', 'user']


def setup_admin(app, db):
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Course, db.session))
    admin.add_view(CourseScheduleView(CourseSchedule, db.session))
    admin.add_view(ModelView(UserCourseSchedule, db.session))
    admin.add_view(UserAdminView(UserAdmin, db.session))
