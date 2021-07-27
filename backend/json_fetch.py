from backend.types import Poll, Vote
import json

def fetch_json(path:str):
  BASE_PATH = 'data/json'
  selected_path = BASE_PATH + path +'.json'
  with open(selected_path) as read_file:
    data = json.load(read_file)
  return data

def fetch_polls():
  return  fetch_json("/polls_bundestag")

def fetch_politician():
  return fetch_json("/votes_bundestag_politician")

def fetch_party_votes():
  return fetch_json("/votes_bundestag")

def polls(id: int)->Poll:
  polls = fetch_polls()
  selected = list(filter(lambda poll:poll["id"] == id, polls))[0]
  return selected

def politician_poll(id: int, name: str)->Poll:
  politician_polls = fetch_politician()
  selected_by_id = list(filter(lambda poll:poll["poll"]["id"] == id, politician_polls))
  selected_by_name = list(filter(lambda poll:name in poll["mandate"]["label"], selected_by_id))[0]
  #Remove no_show
  if (selected_by_name["vote"] == "no_show"):
    return
  return selected_by_name
 
def party_votes(id: str)->Vote:
  party_votes = fetch_party_votes()
  selected = party_votes[id]
  return selected
