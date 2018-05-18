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


def parse_attendance_rates():
    with open('static/2011-2017-attendance-rates-by-nsw-government-schools.csv') as csvfile:
        rates = csv.reader(csvfile, delimiter=",")
        for row in rates:
            if "High School" in row[1]:
                school = HighSchool.objects(id=row[0])
                if school is not None:
                    for i in range(0, 5):
                        school.attendance_rate[str(2012 + i)] = row[i + 2]


if __name__ == '__main__':
    parse_attendance_rates()
