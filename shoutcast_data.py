import requests
import json
from os import getenv as getenv
import re
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class ShoutCast:
  def __init__(self, api_key, return_format):
    self.api_key = api_key
    self.return_format = return_format

  @staticmethod
  def error_body(error):
    # Strip api key from returned error, maybe this can be passed in as a header?
    error_message = re.sub(r"(.*)(\?)(.*)", r"\1", str(error))
    error_body = {
      'error': True,
      'error_messages': [error_message]
    }
    return json.dumps(error_body)

  def generes(self):
    return self.handle_get(f"http://api.shoutcast.com/genre/secondary?parentid=0&k={self.api_key}&f={self.return_format}")

  def stations_by_genre_id(self, genre_id):
    return self.handle_get(f"http://api.shoutcast.com/station/advancedsearch?genre_id={genre_id}&f={self.return_format}&k={self.api_key}")

  def search(self, search_term):
    search_value = re.sub(r"\s","+", search_term)
    return self.handle_get(f"http://api.shoutcast.com/station/advancedsearch?search={search_value}&k={self.api_key}&f={self.return_format}")

  def station_info(self, station_id):
    return self.handle_get(f"http://yp.shoutcast.com/sbin/tunein-station.xspf?id={station_id}")

  def handle_get(self, url):
    # The only HTTP method used will be get since all the rest endpoints take parameters in the URL
    try:
      genre_body = requests.get(url)
      genre_body.raise_for_status()
    except requests.exceptions.HTTPError as e:
      return self.error_body(e)
    except requests.exceptions.ConnectionError as e:
      return self.error_body(e)
    except requests.exceptions.Timeout as e:
      return self.error_body(e)
    except requests.exceptions.RequestException as e:
      return self.error_body(e)
    try:
      if(genre_body.status_code == 200):
        if "<?xml" in genre_body.text:
          # The only xml should be returned by the station_info method
          # Parsing the xml manually to avoid using ET or xmltodict
          # I'm not sure at this point if a full array needs to be returned for retry logic or the first will just be assumed to work
          locations = re.findall(r"\<location\>.*?\<\/location\>", str(genre_body.content))
          titles = re.findall(r"\<title\>.*?\<\/title\>", str(genre_body.content))
          location_urls = list(map(lambda location: re.sub(r"\<.*?\>", "", location), locations))
          titles_filtered = list(map(lambda title: re.sub(r"\<.*?\>", "", title), titles))
          station_infos = {
            "locations": location_urls,
            "titles": titles_filtered
          }
          return station_infos
        else:
          #should be json
          genre_dict = genre_body.json()
          genre_dict['error'] = False
          return genre_dict
    except Exception as e:
      return self.error_body(e)

#x = ShoutCast(getenv('SHOUTCAST_API_KEY', 'json')
#print(json.dumps(x.search("industrial")))
#print(json.dumps(x.generes()))
#print(json.dumps(x.stations_by_genre_id('91')))
#print(json.dumps(x.station_info("23036")))
#print(json.dumps(x.station_info("1015786")))

