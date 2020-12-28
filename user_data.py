import requests
import json
from os import getenv as getenv
import re

class UserData:
  def __init__(self, config_filename):
    self.config_filename = config_filename
    # might need to do an init/rebuild routine here before allowing the rest of the methods to function
    # just to make sure we always have a good data file
    
  def save_station(self, station):
    try:
      with open(self.config_filename, "r+") as user_data:
        data = json.load(user_data)
        if station['id'] and station['name']:
          data['stations'].append(station)
          user_data.seek(0)
          user_data.write(json.dumps(data, indent=4))
          user_data.truncate()
          user_data.close()
    except Exception as e:
      print(e)

  def remove_station(self, station_id):
    try:
      with open(self.config_filename, "r+") as user_data:
        data = json.load(user_data)
        station_ids = []
        if len(data['stations']) > 0:
          for station in data['stations']:
            station_ids.append(station['id'])
          data['stations'].pop(station_ids.index(int(station_id)))
          user_data.seek(0)
          user_data.write(json.dumps(data, indent=4))
          user_data.truncate()
        user_data.close()
    except Exception as e:
      print(e)

  def get_saved_station_ids(self):
    try:
      with open(self.config_filename, "r") as user_data:
        data = json.load(user_data)
        station_ids = []
        if len(data['stations']) > 0:
         for station in data['stations']:
           station_ids.append(station['id'])
        else:
          return station_ids
        user_data.close()
        return station_ids
    except Exception as e:
      print(e)

  def get_saved_station_titles(self):
    try:
      with open(self.config_filename, "r") as user_data:
        data = json.load(user_data)
        station_titles = []
        if len(data['stations']) > 0:
          for station in data['stations']:
            station_titles.append(station['title'])
        else:
          return station_titles
        user_data.close()
        return station_titles
    except Exception as e:
      print(e)

  def saved_station_check(self, station_id):
    return 0

  def get_station_list_position(self, station_id):
    return 0

  def get_stations(self):
    try:
      with open(self.config_filename, "r") as user_data:
        data = json.load(user_data)
        station_titles = []
        if len(data['stations']) > 0:
          return data['stations']
        user_data.close()
        return station_titles
    except Exception as e:
      print(e)
      return [{}]

  def save_search(self, search_term):
    return 0

  def clear_search_history(self):
    return 0

  def get_search_history(self):
    return {}

  def save_favorite_genre(self, genre):
    return 0

  def remove_favorite_genre(self, genre):
    return 0

  def check_repair(self):
    #check to see if the json in the config file is valid and deserializes,
    #attempt to fix or reinitialize if there's an issue
    return 0

  def create_file(self):
    #initialize user setting file
    return 0

  
#x = UserData("data.json")
#
#stations = x.get_stations()
#
#for station in stations:
#  print(station)
  
  