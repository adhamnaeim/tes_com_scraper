import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

present_date = datetime.now()
present_date = datetime(year=present_date.year,month=present_date.month,day=present_date.day)

def crawler():
    pagination_condition = True
    pagination = 1
    output_dict = {}
    while pagination_condition:
        link = f'https://www.tes.com/jobs/browse?currentpage={pagination}&keywords=&siteCountry=&sort=date'
        response = requests.get(link)
        response_soup = BeautifulSoup(response.text,'html.parser')
        json_parsed = response_soup.select_one('script:contains("title")').text.split('initialState__=')[1]
        json_parsed = json.loads(json_parsed[:-1])
        for job in json_parsed['jobsList']['jobs']:
            job_display_start_date = [int(x) for x in job['advert']['displayStartDateShort'].split('-')]
            job_display_start_date = datetime(day=job_display_start_date[-1],month=job_display_start_date[1],year=job_display_start_date[0])
            print(job['title'],job_display_start_date,present_date)
            if job_display_start_date == present_date:
                if job['jobId'] not in output_dict:
                    output_dict[job['jobId']] = job
            else:
                print('last day job entry, exiting.')
                output =  list(output_dict.values())
                return output
        pagination += 1



if __name__ == "__main__":
    crawler_output = crawler()
    with open("output.json", "w") as outfile:
        outfile.write(json.dumps(crawler_output))