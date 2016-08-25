#-*- coding:utf-8 -*-
import re
import csv

def pre_deal():
    csv_file = csv.reader(file("/home/www/git/airbnb_kick_crawler/kickstarter_stat/project_new.csv", 'rb'))

    dataset = []
    for line in csv_file:
        #data = line.split()
        project_id = line[0]
        launch_date = line[2]
        creator_id = line[5]
        name = line[12]

        dataset.append((creator_id, name, launch_date, project_id))

    project_url_list = []

    for l in dataset[25876:]:
        project_url = '/'.join(l)
        project_name = re.sub(r'[?|!|"|/]', ' ', l[1])
        project_name = project_name.replace('&', 'and').replace('(Canceled)', '')\
            .replace('(Suspended)', '').replace('\'', '').replace('.', '')\
            .replace('(', '').replace(')', '').replace(';', '').replace(':', '')
        project_name = re.sub(r'\s{1,}', '-', project_name.strip())
        project_name = re.sub(r'-{2,}', '-', project_name)

        project_url = '/'.join(['projects', l[0], project_name])

        project_url_list.append((project_url, l[2], l[3]))

    return project_url_list

if __name__ == '__main__':
    pre_deal()
