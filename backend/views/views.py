from flask_restful import Resource, fields, marshal_with
from flask import request, jsonify, current_app, make_response
from models.models import *
import csv
from datetime import time, datetime
from utils.utils import preprocess_days, are_days_overlapping
from datetime import time
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import logging
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
import io

logging.basicConfig(level=logging.INFO)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing'}, 401

        token_parts = token.split(" ")
        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return {'message': 'Invalid token format'}, 401

        token = token_parts[1]

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["H2512", "HS256"])
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token'}, 401

        return f(*args, **kwargs)

    return decorated


def full_name_serializer(user):
    if isinstance(user, dict):
        return user.get('full_name')
    elif isinstance(user, User):
        return user.full_name
    else:
        return None

adminFields = {
    'id': fields.Integer,
    'username': fields.String
}

userFields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'serial': fields.String,
    'id_number': fields.Integer,
    'user_type': fields.Integer,
    'full_name': fields.String(attribute='full_name'),
    'user_type_display': fields.String(attribute='user_type_display'),
    'has_schedule': fields.Boolean(attribute='has_schedule'),
    'admin': fields.Nested(adminFields)
}

courseFields = {
    'id': fields.Integer,
    'group_number': fields.String,
    'name': fields.String,
    'course_code': fields.String,
    'has_schedule': fields.Boolean(attribute='has_schedule')
}

courseScheduleFields = {
    'id': fields.Integer,
    'course_id': fields.Integer,
    'days': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'room': fields.String,
    'course': fields.Nested(courseFields),
    'user_pks': fields.List(fields.Integer)
}


# {
#     "username": "chance",
#     "password": "chance",
#     "first_name": "Chance",
#     "last_name": "Bentulan",
#     "serial": "31231928398",
#     "id_number": "15106694",
#     "user_type": 1
# }


class UserRegistration(Resource):
    method_decorators = [token_required]

    def post(self):
        data = request.json
        # get all useradmin fields needed
        username = data.get('username')
        password = data.get('password')

        # get all user fields needed
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        serial = data.get('serial')
        id_number = data.get('id_number')
        user_type = data.get('user_type')

        user = User.query.filter_by(id_number=id_number).first()

        if user:
            return {'message': 'User already exists'}, 400
        
        new_user = User(first_name=first_name, last_name=last_name,
                        serial=serial, id_number=id_number, user_type=user_type)

        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        existing_user_admin = UserAdmin.query.filter_by(username=username).first()
        if existing_user_admin:
            return {'message': 'Username already exists'}, 400

        hashed_password = generate_password_hash(password)
        new_user_admin = UserAdmin(username=username, password=hashed_password, user=new_user)
        db.session.add(new_user_admin)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

class UserInformation(Resource):
    method_decorators = [token_required]

    @marshal_with(adminFields)
    def patch(self, pk):

        user_admin = UserAdmin.query.get(pk)
        if not user_admin:
            return jsonify({'message': 'User does not exist'}), 404

        data = request.get_json(force=True)

        if not data: 
            return jsonify({'message': 'Invalid JSON data'}), 400
        
        fields_to_update = ['username', 'password']

        try:
            for field in fields_to_update:
                if field in data:
                    if field == 'password':
                        setattr(user_admin, field, generate_password_hash(data[field]))
                    else:
                        setattr(user_admin, field, data[field])
                
            db.session.commit()

            updated_user_admin = UserAdmin.query.get(pk)

            return updated_user_admin, 200
        except Exception as e:
            db.session.rollback()

            return jsonify({'message': f'Error updating user: {str(e)}'}), 500


class UserLogin(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = UserAdmin.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'Invalid username or password'}, 401

        user_info = {
            'id': user.user.id,
            'full_name': user.user.full_name,
            'user_type': user.user.user_type_display
        }

        token = jwt.encode({'username': username}, current_app.config['SECRET_KEY'], algorithm="HS256")

        response_data = {
            'token': token,
            'user': user_info
        }
        return make_response(jsonify(response_data), 200)

class Users(Resource):
    method_decorators = [token_required]

    @marshal_with(userFields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        data = request.json
        first_name = data['first_name']
        last_name = data['last_name']
        serial = data['serial']
        id_number = data['id_number']
        user_type = data['user_type']

        user = User(
            first_name=first_name, 
            last_name=last_name, 
            serial=str(int(serial)),
            id_number=id_number,
            user_type=user_type)

        db.session.add(user)
        db.session.commit()

        created_user = User.query.get(user.id)

        return created_user

class SpecificUser(Resource):
    method_decorators = [token_required]

    @marshal_with(userFields)
    def get(self, user_id):
        user = User.query.get(user_id)
        if  not user:
            return jsonify({'message': 'User not found'}), 404
        return user, 200

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return {'message': 'User not Found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200

    @marshal_with(userFields)
    def patch(self, user_id):
        user = User.query.get(user_id)
        if  not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json(force=True)
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        fields_to_update = ['id_number', 'serial', 'first_name', 'last_name', 'user_type']

        try:
            for field in fields_to_update:
                if field in data:
                    setattr(user, field, data[field])

            db.session.commit()

            updated_user = User.query.get(user_id)

            return updated_user
        
        except Exception as e:
            db.session.rollback()

            return jsonify({'message': f'Error updating user: {str(e)}'}), 500


class Courses(Resource):
    method_decorators = [token_required]

    @marshal_with(courseFields)
    def get(self):
        courses = Course.query.all()
        return courses

    @marshal_with(courseFields)
    def post(self):
        data = request.json
        group_number = data['group_number']
        name = data['name']
        course_code = data['course_code']

        course = Course(name=name,
                        course_code=course_code,
                        group_number=group_number)

        db.session.add(course)
        db.session.commit()

        created_course = Course.query.get(course.id)

        return created_course


class SpecificCourse(Resource):
    method_decorators = [token_required]

    @marshal_with(courseFields)
    def get(self, course_id):
        course = Course.query.get(course_id)
        if  not course:
            return jsonify({'message': 'Course not found'}), 404
        return course

    def delete(self, course_id):
        course = Course.query.filter_by(id=course_id).first()

        if not course:
            return {'message': 'Course not found'}, 404

        db.session.delete(course)
        db.session.commit()

        return {'message': 'Course deleted successfully'}, 200


    @marshal_with(courseFields)
    def patch(self, course_id):
        course = Course.query.get(course_id)

        if not course_id:
            return {'message': 'Course not found'}, 404

        data = request.get_json(force=True)
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        fields_to_update = ['name', 'group_number', 'course_code']

        try:
            for field in fields_to_update:
                if field in data:
                    setattr(course, field, data[field])

            db.session.commit()

            updated_course = Course.query.get(course_id)

            return updated_course

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error updating Course: {str(e)}'}), 500


class uploadCSV(Resource):
    def post(self):
        try:
            file = request.files['file']
            if file and file.filename.endswith('.csv'):
                csv_reader = csv.reader(io.TextIOWrapper(file, 'utf-8'))


                student_list = []
                faculty_assigned = []
                schedule = []

                for row in csv_reader:
                    value2 = row[1]
                    value4 = row[4]
                    value5 = row[5]
                    value6 = row[9]

                    student_list.append(value2 + value5)
                    faculty_assigned.append(value4)
                    schedule.append(value6)

                course_information = faculty_assigned[3]
                schedule_information = schedule[3]
                faculty_assigned = faculty_assigned[2]
                student_list = student_list[5:]

                db.session.begin()

                split_course_information = course_information.split()
                course_group = split_course_information[1]
                course_code = " ".join(split_course_information[2:])
                split_schedule_information = schedule_information.split('-')
                days = split_schedule_information[0].strip()
                start_time = split_schedule_information[1].strip()
                end_time_and_room = split_schedule_information[2].strip()
                split_end_time_and_room = end_time_and_room.split()
                room = split_end_time_and_room[-1]
                end_time = " ".join(split_end_time_and_room[:-1])

                convert_start_time_to_military = datetime.strptime(start_time, "%I:%M %p").strftime("%H:%M")
                convert_end_time_to_military = datetime.strptime(end_time, "%I:%M %p").strftime("%H:%M")
                start_time_hour, start_time_minute = convert_start_time_to_military.split(':')
                start_time_hour = int(start_time_hour)
                start_time_minute = int(start_time_minute)
                end_time_hour, end_time_minute = convert_end_time_to_military.split(':')
                end_time_hour = int(end_time_hour)
                end_time_minute = int(end_time_minute)
                start_time_str = "{:02d}:{:02d}:00".format(start_time_hour, start_time_minute)
                end_time_str = "{:02d}:{:02d}:00".format(end_time_hour, end_time_minute)
                days = preprocess_days(days)

                query_course = Course.query.filter_by(course_code=course_code).first()



                if not query_course:
                    # create course, CourseSchedule and then add students

                    new_course = Course(course_code=course_code,
                                        group_number=course_group)
                    db.session.add(new_course)
                    db.session.commit()
                    new_course_schedule = CourseSchedule(course_id=new_course.id,
                                                         days=days,
                                                         start_time=start_time_str,
                                                         end_time=end_time_str,
                                                         room=room)
                    
                    
                    db.session.add(new_course_schedule)
                    db.session.commit()
                    # loop students id number first
                    for student in student_list:
                        id_number = student.split()[0]
                        
                        user = User.query.filter_by(id_number=id_number).first()

                        if user:
                            new_user_schedule=UserCourseSchedule(user_id=user.id,
                                               course_schedule_id=new_course_schedule.id)
                            db.session.add(new_user_schedule)
                else:
                    query_schedule = CourseSchedule.query.filter(
                                    and_(
                                        # are_days_overlapping(CourseSchedule.days, days),
                                        CourseSchedule.course_id == query_course.id,
                                        CourseSchedule.room == room,
                                        CourseSchedule.start_time == (start_time_hour, start_time_minute),
                                        CourseSchedule.end_time == (end_time_hour, end_time_minute)
                                    )
                                )
                    if query_schedule:
                    # add students that are not added to schedule.
                        for student in student_list:
                            id_number = student.split()[0]

                            user = User.query.filter_by(id_number=id_number).first()

                            if user:
                                student_schedule_exist = UserCourseSchedule.query.filter_by(
                                    user_id=user.id,
                                    course_schedule_id=query_schedule.id
                                )

                                if not student_schedule_exist:
                                    new_user_schedule = UserCourseSchedule(
                                        user_id=user.id,
                                        course_schedule_id=query_schedule.id
                                    )
                                    db.session.add(new_user_schedule)
                    else:
                        new_course_schedule = CourseSchedule(course=new_course,
                                                            days=days,
                                                            start_time=(start_time_hour, start_time_minute),
                                                            end_time=(end_time_hour, end_time_minute),
                                                            room=room)
                        db.session.add(new_course_schedule)
                        db.session.commit()
                        for student in student_list:
                            id_number = student.split()[0]
                            
                            user = User.query.filter_by(id_number=id_number).first()

                            if user:
                                UserCourseSchedule(user_id=user.id,
                                                   course_schedule_id=new_course_schedule.id)
            db.session.commit()
            return {'message': 'Automation successful'}, 200
        except Exception as e:
            db.session.rollback()

            return {'message': f'Error running automation: {str(e)}'}, 500
        

class CourseSchedules(Resource):
    method_decorators = [token_required]

    @marshal_with(courseScheduleFields)
    def get(self):
        courses = CourseSchedule.query.options(joinedload(CourseSchedule.course)).all()
        return courses

    @marshal_with(courseScheduleFields)
    def post(self):
        data = request.json
        course_id = data['course_id']
        days = data['days']
        start_time = json.loads(data['start_time'])
        end_time = json.loads(data['end_time'])
        room = data['room']

        converted_start_time = time(start_time[0], start_time[1])
        converted_end_time = time(end_time[0], end_time[1])

        course_schedule = CourseSchedule(
            course_id=course_id,
            days=days,
            start_time=converted_start_time,
            end_time=converted_end_time,
            room=room)

        db.session.add(course_schedule)
        db.session.commit()

        created_course_schedule = CourseSchedule.query.get(course_schedule.id)

        return created_course_schedule


class SpecificCourseSchedule(Resource):
    method_decorators = [token_required]

    @marshal_with(courseScheduleFields)
    def get(self, course_schedule_id):
        course_schedule = CourseSchedule.query.get(course_schedule_id)
        if  not course_schedule:
            return jsonify({'message': 'Course Schedule not found'}), 404
        return course_schedule

    def delete(self, course_schedule_id):
        course_schedule = CourseSchedule.query.filter_by(id=course_schedule_id).first()

        if not course_schedule:
            return {'message': 'Course Schedule not found'}, 404

        db.session.delete(course_schedule)
        db.session.commit()

        return {'message': 'Course Schedule deleted successfully'}, 200


    @marshal_with(courseScheduleFields)
    def patch(self, course_schedule_id):
        course_schedule = CourseSchedule.query.get(course_schedule_id)

        if not course_schedule_id:
            return {'message': 'Course Schedule not found'}, 404

        data = request.get_json(force=True)
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        fields_to_update = [
            'days',
            'start_time',
            'end_time',
            'room']
        
        start_time = json.loads(data['start_time'])
        end_time = json.loads(data['end_time'])

        converted_start_time = time(start_time[0], start_time[1])
        converted_end_time = time(end_time[0], end_time[1])

        data['start_time'] = converted_start_time
        data['end_time'] = converted_end_time

        try:
            for field in fields_to_update:
                if field in data:
                    setattr(course_schedule, field, data[field])

            db.session.commit()

            updated_course = CourseSchedule.query.get(course_schedule_id)

            return updated_course

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error updating Course Schedule: {str(e)}'}), 500

class UserCourseSchedules(Resource):
  method_decorators = [token_required]

  def patch(self, course_schedule_id):
      data = request.json
      new_user_ids = data['user_ids']
      course_schedule = CourseSchedule.query.get(course_schedule_id)
      old_user_ids = course_schedule.user_pks

      added_user_ids = [user_id for user_id in new_user_ids if user_id not in old_user_ids]
      removed_user_ids = [user_id for user_id in old_user_ids if user_id not in new_user_ids]

      for user_id in added_user_ids:

          new_user_course_schedule = UserCourseSchedule(user_id=user_id, course_schedule_id=course_schedule_id)
          db.session.add(new_user_course_schedule)

      for user_id in removed_user_ids:

          user_course_schedule_to_delete = UserCourseSchedule.query.filter_by(user_id=user_id, course_schedule_id=course_schedule_id).first()

          if user_course_schedule_to_delete:
              db.session.delete(user_course_schedule_to_delete)

      db.session.commit()

      return { 'message': 'Successful!' }, 200


class ScheduleToday(Resource):
    method_decorators = [token_required]

    def get(self):
        today = datetime.now().strftime('%a').lower()
        today = today[:2]
        course_schedules = CourseSchedule.query.filter(CourseSchedule.days.like(f'%{today}%')).all()
        full_date_today = datetime.now().strftime('%A')
        schedules_data = []

        for schedule in course_schedules:
            schedules_data.append({
                'id': schedule.id,
                'course_id': schedule.course_id,
                'days': schedule.days,
                'start_time': str(schedule.start_time),
                'end_time': str(schedule.end_time),
                'room': schedule.room,
                'course': schedule.course.course_code,
                'user_pks': schedule.user_pks
            })

        return {
            'course_schedules': schedules_data,
            'full_date_today': full_date_today
        }, 200

class UsersInSchedule(Resource):
  method_decorators = [token_required]

  def get(self, course_schedule_id):
    course_schedule = CourseSchedule.query.get(course_schedule_id)

    if not course_schedule:
        return {'message': 'Course schedule not found'}, 404

    user_ids = course_schedule.user_pks

    users_in_schedule = User.query.filter(User.id.in_(user_ids)).all()
    users_not_in_schedule = User.query.filter(User.id.notin_(user_ids)).all()
    user_data_in_schedule = []
    user_data_not_in_schedule = []

    for user in users_in_schedule:
        user_data_in_schedule.append({
            'id': user.id,
            'full_name': user.full_name
        })

    for user in users_not_in_schedule:
         user_data_not_in_schedule.append({
            'id': user.id,
            'full_name': user.full_name
        })

    return {'users_in_schedule': user_data_in_schedule,
            'user_not_in_schedule': user_data_not_in_schedule}, 200
