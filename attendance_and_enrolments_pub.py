from models import HighSchool
from mongoengine import connect


# Get the attendance rates (within [from_year,to_year] OPTIONAL)
# for the given NSW HighSchool if it exists
def get_attendance_rate(id, from_year=2011, to_year=2017):
    connect('high_school')
    school = HighSchool.objects(id=id)
    rates = []
    if school is not None and from_year >= 2011 and to_year <= 2017:
        rates = school.attendance_rate.values()
        if from_year > 2011 or to_year < 2017:
            rates = rates[from_year - 2012:to_year - 2012]
    return rates


# get enrolment numbers within [2014,2018]
# for the NSW HighSchool if it exists
def get_enrolments(id, from_year=2014, to_year=2018):
    connect('high_school')
    school = HighSchool.objects(id=id)
    enrolments = []
    if school is not None and from_year >= 2014 and to_year <= 2018:
        rates = school.enrolments.values()
        if from_year > 2014 or to_year < 2018:
            rates = rates[from_year - 2015:to_year - 2015]
    return enrolments
