import json

def fetch_json(path:str):
  BASE_PATH = 'data/json'
  selected_path = BASE_PATH + path +'.json'
  with open(selected_path) as read_file:
    data = json.load(read_file)
  return data

def fetch_polls():
  return  fetch_json('/polls_bundestag')

def fetch_politician():
  return fetch_json('/votes_bundestag_politician')

def fetch_votes():
  return fetch_json('/votes_bundestag')
