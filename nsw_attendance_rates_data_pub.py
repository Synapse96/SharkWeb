from models import HighSchool
import csv


def parse_names_locations():
    with open('static/datahub_nongov_locations-2017.csv') as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        for row in rows:
            if "Secondary" in row[6]:
                school = HighSchool.objects(id=row[0]) ## school's id isn't available in this data set
                if school is not None:
                    school.name = str(row[2])
                    school.street = str(row[3])
                    school.suburb = str(row[4])
                    school.postcode = int(row[5])

    with open('static/NSW-Public-Schools-Master-Dataset-07032017.csv') as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        for row in rows:
            if "Secondary" in row[10]:
                school = HighSchool.objects(id=row[0])
                if school is not None:
                    school.name = str(row[2])
                    school.street = str(row[3])
                    school.suburb = str(row[4])
                    school.postcode = int(row[5])


# Parses the attendance rates from the Data-set and places into the Schema
def parse_attendance_rates():
    # TODO: connect to mLab here
    with open('static/2011-2017-attendance-rates-by-nsw-government-schools.csv') as csvfile:
        rates = csv.reader(csvfile, delimiter=",")
        for row in rates:
            if "High School" in row[1]:
                school = HighSchool.objects(id=row[0])
                if school is not None:
                    for i in range(0, 6):
                        school.attendance_rate[str(2011 + i)] = row[i + 2]


# Get the attendance rates (within [from_year,to_year] OPTIONAL)
# for the given NSW HighSchool if it exists
def get_attendance_rate(id, from_year=2011, to_year=2017):
    # TODO: connect to mLab here
    school = HighSchool.objects(id=id)
    rates = []
    if school is not None and from_year >= 2011 and to_year <= 2017:
        rates = school.attendance_rate.values()
        if from_year > 2011 or to_year < 2017:
            rates = rates[from_year - 2012:to_year - 2012]
    return rates


