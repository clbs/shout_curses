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
      with open(self.config_filename, "w+") as user_data:
        data = json.loads(user_data)
        if station.id and station.title and station.url:
          # check to see if station id is already in station list, if not
          # append list with new station
          data.stations.append(station)
          new_data = json.dumps(data)
          user_data.write(new_data)
    except Exception as e:
      print(e)
      return 1

    return 0

  def get_saved_station_ids(self):
    return 0

  def saved_station_check(self, station_id):
    return 0

  def get_station_list_position(self, station_id):
    return 0

  def remove_station(self,station):
    return 0

  def get_stations(self):
    #get all stations, check to see if valid data is found for every object in array
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

  

  
  
