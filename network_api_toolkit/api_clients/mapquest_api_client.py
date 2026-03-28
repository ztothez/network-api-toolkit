#1.3.4.1: Option 1 - Modify the MapQuest API App 
import urllib.parse
import os
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    print("(1) Metric\n" + "(2) Imperial\n")
    options = int(input("Give option: (1-2)"))
    key = os.getenv("MAPQUEST_API_KEY")
    if not key:
        raise ValueError("MAPQUEST_API_KEY not set in environment variables")
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    noapi = main_api + urllib.parse.urlencode({"from": orig, "to":dest})
    print("URL: " + (noapi))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    if options == 1:
        if json_status == 0:
            print("API Status: " + str(json_status) + " = A successful route call.\n" + "Directions from " + (orig) + " to " + (dest) +
                  "\nTrip Duration:   " + str(json_data["route"]["formattedTime"]) + "\nKilometers:      " +
                  str("{:.2f}".format((json_data["route"]["distance"])*1.61) + "\nFuel Used (Ltr): " +
                                      str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)+"\n=============================================")))
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                print((each["narrative"]) + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
            print("=============================================\n")
        elif json_status == 402:
            print("\n****************************************************************"+ ("\nStatus Code: " + str(json_status) + " Invalid user inputs for one or both locations."
            +"\n****************************************************************\n"))
        else:
            print("\n************************************************************************\n" + ("Status Code: " + str(json_status) + " Refer to:\n"
                    + "https://developer.mapquest.com/documentation/directions-api/status-codes\n" + "************************************************************************"))
    elif options == 2:
            if json_status == 0:
                print("API Status: " + str(json_status) + " = A successful route call.\n" + "Directions from " + (orig) + " to " + (dest) +
                  "\nTrip Duration:   " + str(json_data["route"]["formattedTime"]) + "\nMiles:      " +
                  str("{:.2f}".format(json_data["route"]["distance"]) + "\nFuel Used (Gal): " + str("{:.2f}".format(json_data["route"]["fuelUsed"])
                         +"\n=============================================")))
                for each in json_data["route"]["legs"][0]["maneuvers"]:
                    print(str(each["narrative"] + str("{:.2f}".format(each["distance"]) + " miles")))
                print("=============================================")
            elif json_status == 402:
                    print("\n****************************************************************"+ ("\nStatus Code: " + str(json_status) + " Invalid user inputs for one or both locations."
                +"\n****************************************************************\n"))
            else:
                print("\n************************************************************************\n" + ("Status Code: " + str(json_status) + " Refer to:\n"
                        + "https://developer.mapquest.com/documentation/directions-api/status-codes\n" + "************************************************************************"))
    else:
       print("Choice of option was not made.")
