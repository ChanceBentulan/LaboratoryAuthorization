from sqlalchemy.ext.hybrid import hybrid_property
from extensions.extensions import db
from datetime import date, datetime, timedelta
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship


class UserAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = relationship("User", back_populates="admin", uselist=False)

    def __repr__(self):
        return '<UserAdmin %r>' % self.username


class User(db.Model):
    STUDENT = 0
    ADMINISTRATOR = 1
    STAFF = 2
    FACULTY = 3

    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String, nullable=False)
    id_number = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    date_registered = db.Column(db.Date, nullable=False, default=date.today)

    admin = relationship("UserAdmin", back_populates="user", uselist=False)

    def __repr__(self):
        return self.first_name

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @hybrid_property
    def user_type_display(self):
        if self.user_type == User.FACULTY:
            return 'faculty'
        elif self.user_type == User.STAFF:
            return 'staff'
        elif self.user_type == User.ADMINISTRATOR:
            return 'administrator'
        else:
            return 'student'

    @hybrid_property
    def classes_right_now(self):
        current_time_utc = datetime.utcnow() + timedelta(hours=8)
        current_time = current_time_utc.time()
        today = current_time_utc.strftime('%a').lower()
        classes_right_now = []
        grace_period = timedelta(minutes=15)  # Define the grace period

        for user_course in self.user_course_schedules:
            if today[:-1] in user_course.course_schedule.days.split('|'):
                start_time = user_course.course_schedule.start_time
                end_time = user_course.course_schedule.end_time

                # Convert start_time to datetime and subtract the grace period
                start_datetime = datetime.combine(datetime.today(), start_time)
                start_time_with_grace = (start_datetime - grace_period).time()

                if start_time_with_grace <= current_time < end_time:
                    classes_right_now.append(user_course.course_schedule)
        return classes_right_now
    
    @hybrid_property
    def classes_today(self):
        today = datetime.now().strftime('%a').lower()
        classes_right_now = []
        for user_course in self.user_course_schedules:
            if today[:-1] in user_course.course_schedule.days.split('|'):
                classes_right_now.append(user_course.course_schedule)
        return classes_right_now

    @hybrid_property
    def has_schedule(self):
        if not self.user_course_schedules:
            return False
        return True


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_number = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(200), nullable=True)
    course_code = db.Column(db.String(100), nullable=False)

    @hybrid_property
    def has_schedule(self):
        if not self.course_schedules:
            return False
        return True


class CourseSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    days = db.Column(db.String(100), default='mo|tu|we|th|fr|sa|su')
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(100), nullable=False)

    course = db.relationship('Course', backref='course_schedules')

    __table_args__ = (
        UniqueConstraint('course_id', 'days', 'start_time', 'end_time', 'room'),
    )

    @hybrid_property
    def user_pks(self):
        return [user_course.user_id for user_course in self.user_course_schedules]


class UserCourseSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_schedule_id = db.Column(db.Integer, db.ForeignKey('course_schedule.id'), nullable=False)
    
    user = db.relationship('User', backref='user_course_schedules')
    course_schedule = db.relationship('CourseSchedule', backref='user_course_schedules')
