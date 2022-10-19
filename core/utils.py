from dashboard.models import Item
from config.settings import API_KEY
from urllib import parse
import json
import urllib3
import datetime
# Search engine


def search_engine(search_term, search_sections, limit=None,offset=0,filter=None):
    
    #search_sections = search_sections.split(',')

    results = {}
    if  search_sections == 'items':
        items = Item.objects.filter(title__icontains=search_term)

        items = items.order_by('-id')

        results['items_count'] = items.count()
        
        if filter is not None:
            if filter == 'latest':
                #projects = projects.filter(pub_date__gte=one_week_ago)
                items = items.order_by('-id')
            else:
                items = items.order_by('id')
        else:
            items = items.order_by('-id')
        
        if limit is not None:
            if offset !=0:
                items = items[offset:offset+limit]
            else:
                items = items[:limit]
        
        results['items'] = items

    return results

def get_duraction(video_id):
    #url_data = parse.urlparse(url)
    #query = parse.parse_qs(url_data.query)
    http = urllib3.PoolManager()
    #video_id = query["v"][0]
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+API_KEY+"&part=contentDetails"
    response = http.request('GET', searchUrl)
    data = json.loads(response.data)
    all_data=data['items']
    contentDetails=all_data[0]['contentDetails']
    duration=contentDetails['duration']
    
    return duration

def durationtosecond(given_string):
    new_string = given_string.split('T')[1]
    new_string = given_string.split('T')[1]
    if 'H' in new_string and 'M' in new_string and 'S' in new_string:
        dt = datetime.datetime.strptime(new_string, '%HH%MM%SS')
        time_sec = int(dt.hour) * 3600 + int(dt.minute) * 60 + int(dt.second)

    elif 'M' in new_string and 'H' not in new_string and 'S' in new_string:
        dt = datetime.datetime.strptime(new_string, '%MM%SS')
        time_sec = int(dt.minute) * 60 + int(dt.second)
        
    elif 'H' in new_string and 'M' not in new_string and 'S' in new_string:
        dt = datetime.datetime.strptime(new_string, '%HH%SS')
        time_sec = int(dt.hour) * 3600 + int(dt.second)

    elif 'H' in new_string and 'M' in new_string and 'S' not in new_string:
        dt = datetime.datetime.strptime(new_string, '%HH%MM')
        time_sec = int(dt.hour) * 3600 + int(dt.minute) * 60
        
    elif 'H' in new_string and 'M' not in new_string and 'S' not in new_string:
        dt = datetime.datetime.strptime(new_string, '%HH')
        time_sec = int(dt.hour) * 3600
        
    elif 'H' not in new_string and 'M' in new_string and 'S' not in new_string:
        dt = datetime.datetime.strptime(new_string, '%MM')
        time_sec = int(dt.minute) * 60

    else:
        dt = datetime.datetime.strptime(new_string, '%SS')
        time_sec = int(dt.second)

    
    return time_sec