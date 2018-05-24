from models import HighSchool
from mongoengine import connect
import csv


connect(host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb')


def parse_government_schools():
    with open('static/NSW-Public-Schools-Master-Dataset-07032017.csv') as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        connect('high_school')
        for row in rows:
            if "Secondary" in row[10] or "Central" in row[10]:
                if not HighSchool.objects(id=row[0]):
                    if row[6] == '':
                        row[6] = 0
                    school = HighSchool(id=row[0],
                                        name=row[2],
                                        street=row[3],
                                        suburb=row[4],
                                        postcode=row[5],
                                        students=int(float(row[6])),
                                        selective=row[11],
                                        gender=row[19])
                    school.save()


def parse_attendance_rates():
    with open('static/2011-2017-attendance-rates-by-nsw-government-schools.csv') as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        connect('high_school')
        for row in rows:
            if row[0] != "school_code" and row[0] != '':
                for school in HighSchool.objects(id=int(row[0])):
                    attendance_rates = {}
                    for i in range(0, 7):
                        attendance_rates[str(2011 + i)] = row[i + 2]
                    school.update(attendance_rates=attendance_rates)


def parse_selective_entry_scores():
    with open('static/2015-2018-selective-high-schools-minimum-entry-scores.csv') as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        connect('high_school')
        for row in rows:
            name = row[0].replace(" (Virtual)", "")
            name = name.replace(" (Day)", "")
            name = name.replace("(", "")
            name = name.replace(")", "")
            for school in HighSchool.objects(name=name):
                entry_scores = {}
                for i in range(0, 4):
                    entry_scores[str(2015 + i)] = row[i + 1]
                school.update(selective_entry_scores=entry_scores)


def parse_enrolments():
    with open('static/secondary-enrolments-by-school-2014-2018.csv') as csvfile:
        connect('high_school')
        rows = csv.reader(csvfile, delimiter=",")
        enrollments = {}
        for row in rows:
            if row[0] != '' and row[0] != "School Code" and "Student Enrolments" not in row[0] \
                    and "Opened" not in row[0]:
                school = HighSchool.objects(id=row[0])
                if school is not None:
                    for i in range(0, 4):
                        enrollments[str(2014 + i)] = row[i + 3]
                    school.update(enrollments=enrollments)
