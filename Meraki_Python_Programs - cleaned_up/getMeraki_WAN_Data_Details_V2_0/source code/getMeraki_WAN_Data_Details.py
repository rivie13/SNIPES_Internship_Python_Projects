#getMeraki_WAN_Data_Details
#Created by: Riviera Sperduto
#Created for: SNIPES USA
#Creation date: 10/22/2024
#Last edit: 11/21/2024

#sometimes the first import won't work and the variableData file needs to 
#be pulled in from a different directory
from variableData import APIKey, orgID
import meraki
from openpyxl import *
from openpyxl.styles import *
import csv
from datetime import *
import os
import math
from guizero import *

#TODO:
# 1. Find out what functions to create
# 2. test those functions
# 3. create main based off of tests
#
# 4. Almost at the place where an MVP is created
# need to just create a function that will be used in a new button
# 5. new function is to close GUI and find traffic for requested stores
# and to then put it in an excel sheet
# 5a. While finishing up the new functions, CREATE TESTS FOR EVERYTHING!!!
# 6. once the above works the MVP will be created
# 7. AFTER MVP CREATION: clean up the code, make excel sheet nicer,
# make gui nicer, make code more efficient if possible....
#

#FIGURE OUT HOW TO CREATE EXCEL SHEET
#excel sheet: store number,  wan 1 upload,  wan 1 download,  wan 2 upload, wan 2 download
#               'number'        'num'            'num'          'num'        'num'


###START FUNCTIONS NEEDED FOR PROGRAM###

def APIKeyGen():
    key = APIKey
    return key

def getAPIDashboard(key):
    ##instantiate meraki Dashboard API session
    dashboard = meraki.DashboardAPI(api_key=key)
    return dashboard

def getNetworks(dashboard):
    networks = dashboard.organizations.getOrganizationNetworks(orgID)
    return networks

def getWANDetails(netID, timeSpan, dashboard):

    strNetID = str(netID)

    #adding resolution = 86400 fixed the issue????
    WANDetails = dashboard.appliance.getNetworkApplianceUplinksUsageHistory(strNetID, timespan = timeSpan, resolution = 86400)
    
    return WANDetails

def addUpByteInfo(WANDetails):
    WANDictionary = {
        "CellularSent": 0,
        "CellularReceived": 0,
        "WAN 1 Sent": 0,
        "WAN 1 Received": 0,
        "WAN 2 Sent": 0,
        "WAN 2 Received": 0
    }

    for details in WANDetails:
        #get all devices associated with network WAN 
        devices = details["byInterface"]

        #add up byte information depending on which device it is....
        for device in devices:
            interface = device["interface"]
            if interface == 'cellular':
                #debug code
                #print(f'\ninterface: {interface}\nsent: {device["sent"]}\nreceived: {device["received"]}\n')
                if device["sent"] is None:
                    WANDictionary["CellularSent"] += 0
                if device["received"] is None:
                    WANDictionary["CellularReceived"] += 0
                else:
                    WANDictionary["CellularSent"] += device["sent"]
                    WANDictionary["CellularReceived"] += device["received"]
                
            if interface == 'wan1':
                if device["sent"] is None:
                    WANDictionary["WAN 1 Sent"] += 0
                if device["received"] is None:
                    WANDictionary["WAN 1 Received"] += 0
                else:
                    WANDictionary["WAN 1 Sent"] += device["sent"]
                    WANDictionary["WAN 1 Received"] += device["received"]
            if interface == 'wan2':

                if device["sent"] is None:
                    WANDictionary["WAN 2 Sent"] += 0
                if device["received"] is None:
                    WANDictionary["WAN 2 Received"] += 0                    
                else:
                    WANDictionary["WAN 2 Sent"] += device["sent"]
                    WANDictionary["WAN 2 Received"] += device["received"]

    #print(f'WANDictionary: {WANDictionary}')

    return WANDictionary

def createListEntry(WANDictionary, netName):
    #take the dictionary and put it into a list.....
    
    listEntry = [netName, WANDictionary["WAN 1 Sent"], WANDictionary["WAN 1 Received"], WANDictionary["WAN 2 Sent"], WANDictionary["WAN 2 Received"], WANDictionary["CellularSent"], WANDictionary["CellularReceived"]]

    #it's actually a list but I'm too lazy to change now
    return listEntry

def convertListFromByteToMB(listEntry):
    
    #take all of the fields in the list with bytes and change to MB
    listEntry[1] = listEntry[1]/1048576
    listEntry[2] = listEntry[2]/1048576
    listEntry[3] = listEntry[3]/1048576
    listEntry[4] = listEntry[4]/1048576
    listEntry[5] = listEntry[5]/1048576
    listEntry[6] = listEntry[6]/1048576

    #This creates a list with the original list but rounds up all the number elements
    modifiedList = [listEntry[0]] + [math.ceil(x) for x in listEntry[1:]]

    for i in range(1, len(modifiedList)):
        modifiedList[i] = str(modifiedList[i]) + ' MB'




    #debug code
    #print(f'The modified list with units added: {modifiedList}')

    return modifiedList



###END FUNCTIONS NEEDED FOR PROGRAM###


def makeGUI():

    #test to see if we can get a list of the stores....
    #it worked....
    listOfStores = []

    app = App(title = "SNIPES WAN/CELLULAR DEVICES DETAILS CHECKER", layout = "grid")

    textBoxInstructionsBox = Box(app, border= True, grid = [0,0])

    textBoxInstructionsText = Text(textBoxInstructionsBox, text = "Please enter a single store number: ", size = 11, color = "black", font="Arial")

    storeNumInputBox = TextBox(textBoxInstructionsBox, width = "10")


    #print(f'storeNumInputBox.value: {storeNumInputBox.value}')

    #create the list box where store numbers will sit
    storeListBox = ListBox(app, grid=[4,1])

    #button press happens after listbox creation
    #To be able to reliably get all the data after GUI is closed
    #put it into a list and add data to list when it gets added to ListBox object
    #then you can access the data later....
    searchButton = PushButton(app, command=lambda:buttonPressTextSend(storeNumInputBox.value, storeListBox, app, listOfStores), grid= [3, 1], text= "Insert Store")


    #button press to close out the app after all stores have been found...
    exitButton = PushButton(app, command=lambda:buttonPressExitApp(app, listOfStores), grid=[3,3], text = "Exit App")


    #this should always be last....
    #do not fool yourself this should be last.....
    app.display()

    #test to see if we got the lists
    #print(f'storeListBox: {printList}')

    #return the list of stores after GUI is done
    return listOfStores

def buttonPressExitApp(app, listOfStores):
    app.destroy()
    return listOfStores

def buttonPressTextSend(text, listbox, app, listOfStores):

    #function to clean the text here
    text = checkInputText(text, app)
    
    listbox.append(text)

    listOfStores.append(text)


def checkInputText(text, app):

    if text.isdigit() and len(text) == 4:
        return text

    else:
        #need to put function here
        errorString = "Input Error"
        errorOutput(errorString, app)
        return None
    

#### ERROR HANDLING FUNCTIONS #######################

def errorOutput(errorType, app):

    if errorType == "Input Error":
        errorString = "You did not enter a store number"
        errorWindowCreation(errorString, app)

    return


def errorWindowCreation(errorText, app):

    errorWindow = Window(app, title = "ERROR", height = 75, width = 400)

    errorTextOutput = Text(errorWindow, text = errorText)

    return

#### END ERROR HANDLING FUNCTIONS #######################

###START CODE###

###START MAIN###
def main():

    #get the API key
    APIKey = APIKeyGen()

    #Instantiate a dashboard object for the API
    dashboard = getAPIDashboard(APIKey)

    #don't need today's date maybe???
    #don't need today's date if using timespan param...
    #max timespan is 31 days .... 2678400 is the param to be used
    timeSpan = 2678400

    #create the workbook
    wb = Workbook()


    #get the ws
    ws = wb.active

    #change title of sheet
    ws.title = "Meraki Device Data Details"

    #this is where all of the added up data for all networks wil go into
    #separated by each network....
    #this is a list of lists.... take the dictionary and make it into a list....
    workbookData = []

    #makeGUI()
    #get the list of stores from user...
    listOfStores = makeGUI()

    foundStore = 0

    #with the list of stores go through them all for each
    #network find a match between a store number and a
    #network name...
    #when match is found between a store and a network 
    #use the network id to do a try/catch block for getting the
    #network traffic by device
    #if good then add data to excel sheet
    #if doesn't work then there should be an error displayed
    #and after error is shown should continue until end of program...



    networks = getNetworks(dashboard)

    netName = ''
    netID = ''

    #since getting weird issues only when trying it this way I need a new strat
    #I can get the data from meraki so just get all of it 
    #put each entry into the list of dictionaries
    #once you have the list of stores
    #for every store check against all netNames within list of dictionaries
    #see if you have a match
    #when match found

    listOfNetworkLists = []

    #going through all networks
    for net in networks:
        #go through all the stores
        for store in listOfStores:
    
            netID = net["id"]
            netName = net["name"]

            #if netID contains an N break this loop and go to next network...
            if 'N' in netID:
                #print('skipping this network....')
                break

            #print(f'store: {store}')
            #print(f'netID: {netID}')
            #print(f'netName: {netName}')

            #if store in netName proceed with matching
            if store in netName:
                #do the stuff
                #debug code...
                #print('store in net name....')

                WANDetails = getWANDetails(netID, timeSpan, dashboard)

                WANDictionary = addUpByteInfo(WANDetails)

                listEntry = createListEntry(WANDictionary, netName)

                listEntry = convertListFromByteToMB(listEntry)

                workbookData.append(listEntry)
                    
            else:
                pass
                #print(f'store number {store} does not exist in the Meraki organization...')

    #debug code
    #print(f'workbookData: {workbookData}')

    ft = Font(bold=True)

    headers = ["Store Name", "WAN 1 Sent", "WAN 1 Received", "WAN 2 Sent", "WAN 2 Received", "Cellular Sent", "Cellular Received"]

    workbookData.insert(0, headers)

    #debug code
    #print(f'workbookData: {workbookData}')

    ft = Font(bold=False)

    numberOfStores = len(workbookData) - 1

    if numberOfStores >= 1:
        for row in workbookData:
            ws.append(row)
        #change workbook name
        #the save should be last so everything gets saved before program close!!!
        wb.save('Meraki Device Data Details.xlsx')
    


    #final print statement

    if numberOfStores < 1:
        print(f'Generated no report for 0 stores...')
    else:
        print(f'Successfully generated report(s) for {numberOfStores} store(s)...')


    
###END MAIN###





#This is how you run the file..... need to run main function
if __name__ == '__main__':
    main()


###END CODE ###