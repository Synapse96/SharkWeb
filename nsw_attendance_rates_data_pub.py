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


