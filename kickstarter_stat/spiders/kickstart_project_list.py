#-*- coding:utf-8 -*-

from datetime import datetime, timedelta
import time
import json

from bs4 import BeautifulSoup
import scrapy

import requests

from kickstarter_stat.csv_predeal import pre_deal

class KickstarterListProjectsSpirder(scrapy.Spider):
    name = 'kick_listing'

    start_urls = ['https://www.kickstarter.com/discover/advanced?state=live&category_id=12&woe_id=0&sort=popularity&seed=2446887&page=1']

    allowed_domains = ['bitly.com', 'kickstarter.com']

    def parse(self, response):
        #project_list_lis = response.xpath("//ul[@id='projects_list']//li[@class='project col col-3 mb4']//a[@class='project-thumbnail-wrap']")

        bitly_home = requests.get('https://bitly.com')

        project_name_list = pre_deal()

        bitly_cookie = bitly_home.cookies
        for project in project_name_list:
            #project_link = str(project.xpath("./@href").extract()[0])

            pure_url = project[0].split('?')[0]

            project_url = "https://www.kickstarter.com/" + pure_url + "/widget.js"
            try:
                project_widget_dom = requests.get(url=project_url,
                    headers={'X-Requested-With': 'XMLHttpRequest'})
            except:
                project_widget_dom = None
                print 'url error', project_url

            if project_widget_dom and project_widget_dom.status_code == 200:
                widget_dom = BeautifulSoup(project_widget_dom.content)
                short_link = widget_dom.find(id='shortlink_embed')

                if short_link:
                    short_link_code = short_link.text.split('/')[-1]

                    #call for stat data
                    bitly_url = 'https://bitly.com/proxy/v3/link/clicks'

                    headers = {'x-xsrftoken': bitly_cookie['_xsrf']}

                    launch_date = datetime.fromtimestamp(float(project[1]))
                    start_date = launch_date + timedelta(days=120)

                    post_data = {'link': 'http://bitly.com/' + short_link_code,
                        'timezone': 0, 'unit': 'day', 'units': '130',
                        'unit_reference_ts': str(time.mktime(start_date.timetuple())).split('.')[0], 'rollup': 'false'}

                    res = requests.post(bitly_url, data=post_data,
                        cookies=bitly_cookie, headers=headers)

                    if res.status_code == 200:
                        stat_obj = json.loads(res.content)
                        with open('kickstarter_stat/data/' + short_link_code + '.dat', 'wb') as data_file:
                            stat_data = stat_obj['data']['link_clicks']

                            data_file.write('id         +project            + date +   click\n')

                            for data in stat_data:
                                data_file.write(str(project[2]) + '  http://kck.st/' +
                                    short_link_code + ' ' + str(datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d')) +
                                    ' ' + str(data['clicks']) + '\n')
                    else:
                        print 'error: bitly post error code:', res.status_code
            else:
                with open('kickstarter_stat/errro.dat', 'a') as error_file:
                    error_file.write(str() + ' ' + project_url + '\n')
                print 'error: widget js error!'
