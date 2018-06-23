import urllib.request
import xml.etree.ElementTree as ET
import random
from bs4 import BeautifulSoup
from openpyxl import Workbook
import argparse


def get_courses_list(number_to_select=20):
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    tree = ET.fromstring(urllib.request.urlopen(url).read())
    schema = './/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'
    courses = tree.findall(schema)
    return random.sample([course.text for course in courses], number_to_select)


def get_course_info(course_slug):
    tree = urllib.request.urlopen(course_slug).read()
    soup = BeautifulSoup(tree, 'lxml')
    try:
        course_lang = soup.find('div', attrs={'class':
                                              'rc-Language'}).get_text()
    except AttributeError:
        course_lang = 'No data'
    try:
        start_date = soup.find('div', attrs={'id':
                                             'start-date-string'}).get_text()
    except AttributeError:
        start_date = 'No data'
    try:
        cnt_weeks = len(soup.find_all('div', attrs={'class':
                                                    'week'}))
    except AttributeError:
        cnt_weeks = 'No data'
    try:
        rating = soup.find('div', class_='ratings-text').text
    except AttributeError:
        rating = 'No data'
    try:
        course_name = soup.title.string.split('|')[0]
    except AttributeError:
        course_name = 'No data'

    return {
            'Course name': course_name,
            'Course Language': course_lang,
            'Start Date': start_date,
            'Weeks lenght': cnt_weeks,
            'Rating': rating
            }


def output_courses_info_to_xlsx(courses, filepath):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Coursera data'
    ws.append(['Course name',
               'Course Language',
               'Start Date',
               'Weeks lenght',
               'Rating'])
    for course in courses:
        ws.append([course['Course name'],
                   course['Course Language'],
                   course['Start Date'],
                   course['Weeks lenght'],
                   course['Rating']])
    wb.save(filename=filepath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Script will collect data from Cursera'
            )
    parser.add_argument('filepath', help='Please enter file in xlsx format')
    args = parser.parse_args()
    courses_list = get_courses_list()
    course_info = [get_course_info(course) for course in courses_list]
    output_courses_info_to_xlsx(course_info, args.filepath)
