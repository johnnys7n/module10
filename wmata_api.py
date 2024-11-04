import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "7b76ef34687d474e98fd7740058f3c8e"
INCIDENTS_URL = "https://jhu-intropython-mod10.replit.app/" # WMATA Incidents API did not work
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type: str):
  # first making sure that the unit_type provided is either elevators or escalators
  if unit_type.lower() not in ["elevators", "escalators"]:
    return "Error: Invalid unit type. Please use 'elevators' or 'escalators'"
  
  # since the UnitType is all caps in the WMATA response and pluralized, we need to adjust the input
  unit_type = unit_type.upper()[:-1]

  # create an empty list called 'incidents'
  incidents = []

  # use 'requests' to do a GET request to the WMATA Incidents API
  response = requests.get(INCIDENTS_URL, headers=headers)
  response.raise_for_status()
  
  try: # check if the response status code is 200
  # retrieve the JSON from the response
    elevator_incident = response.json()
    # check if the 'ElevatorIncidents' key in the JSON response is empty
    if len(elevator_incident.get("ElevatorIncidents")) == 0:
      return "No incidents found"

    # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
    #   -StationCode, StationName, UnitType, UnitName
    # add each incident dictionary object to the 'incidents' list
    for incident in elevator_incident.get("ElevatorIncidents"):
      if incident.get("UnitType") == unit_type:
        incidents.append({
          "StationCode": incident["StationCode"],
          "StationName": incident["StationName"],
          "UnitType": incident["UnitType"],
          "UnitName": incident["UnitName"]
        })
    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)

  except requests.exceptions.HTTPError as err:
    # if the response status code is not 200, return an error message
    return f"Houston, we have a problem - HTTP request Error: {err}"

  except Exception as e:
    # if any other error occurs, return an error message
    return f"An error has occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
