import csv

with open("C:\\Users\\Chance\\Downloads\\attendance.csv", 'r') as file:
    csv_reader =  csv.reader(file)

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

    for student in student_list:
        id_number = student.split()[0]
        print("ID number:" , id_number)

        # db.session.begin()

        # split_course_information = course_information.split()
        # course_group = split_course_information[1]
        # course_code = " ".join[split_course_information[2:]]

        # query_course = Course.query.filter_by(course_code=course_code).first()
        
        # split_schedule_information = schedule_information.split('-')
        # days = split_schedule_information[0].strip()
        # start_time = split_schedule_information[1].strip()
        # end_time_and_room = split_schedule_information[2].strip()
        # split_end_time_and_room = end_time_and_room.split()
        # room = split_end_time_and_room[-1]
        # end_time = " ".join(split_end_time_and_room[:-1])

        # convert_start_time_to_military = datetime.strptime(start_time, "%I:%M %p").strftime("%H:%M")
        # convert_end_time_to_military = datetime.strptime(end_time, "%I:%M %p").strftime("%H:%M")
        # start_time_hour, start_time_minute = convert_start_time_to_military.split(':')
        # start_time_hour = int(start_time_hour)
        # start_time_minute = int(start_time_minute)
        # end_time_hour, end_time_minute = convert_end_time_to_military.split(':')
        # end_time_hour = int(end_time_hour)
        # end_time_minute = int(end_time_minute)