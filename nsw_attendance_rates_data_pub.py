from models import HighSchool
import csv


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
