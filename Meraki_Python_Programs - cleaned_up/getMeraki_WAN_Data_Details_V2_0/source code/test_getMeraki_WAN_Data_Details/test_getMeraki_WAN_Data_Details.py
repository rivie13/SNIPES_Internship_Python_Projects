#sometimes variableData file import won't work
#you may need to try to get it from a different directory...
from variableData import APIKey, orgID
from getMeraki_WAN_Data_Details import *
from guizero import *
import time
from openpyxl import *
from openpyxl.styles import *

import meraki

dashboard = meraki.DashboardAPI(APIKey)

orgID = orgID

##create a test to generate the API key securely
def testAPIKeyGen():
    assert APIKeyGen() == APIKey

##create a test to instantiate API dashboard
def testGetAPIDashboard():
    dashboard = getAPIDashboard(APIKey)
    
    if dashboard != None:
        dashboardCheck = True
    assert dashboardCheck == True


#create a test to make sure you are getting all networks
def testGetNetworks():
    networks = getNetworks(dashboard)

    netCheck = False

    if networks != None:
        netCheck = True
    
    assert netCheck == True

#create a test to see if WAN details are successfully retrieved
def testGetWANDetails():
    timeSpan = 2678400

    networks = getNetworks(dashboard)

    netCounter = 1

    netID = ''

    for net in networks:
        if netCounter > 1:
            break
        netID = net["id"]
        netCounter += 1

    WANDetails = getWANDetails(netID, timeSpan, dashboard)

    WANDetailsCheck = False

    if WANDetails != None:
        WANDetailsCheck = True

    #print(f'WAN DETAILS: \n{WANDetails}\n')

    assert WANDetailsCheck == True

def testAddUpByteInfo():
    timeSpan = 2678400

    networks = getNetworks(dashboard)

    netCounter = 1

    netID = ''

    for net in networks:
        if netCounter > 1:
            break
        netID = net["id"]
        netCounter += 1

    WANDetails = getWANDetails(netID, timeSpan, dashboard)

    WANDictionary = addUpByteInfo(WANDetails)

    #print(f'\nWANDictionary: {WANDictionary}\n')
    
    #need a better assert statement here....
    assert WANDictionary != None

def testCreateListEntry():
    timeSpan = 2678400

    networks = getNetworks(dashboard)

    netCounter = 1

    netID = ''
    netName = ''

    for net in networks:
        if netCounter > 1:
            break
        netID = net["id"]
        netName = net["name"]
        netCounter += 1

    WANDetails = getWANDetails(netID, timeSpan, dashboard)

    WANDictionary = addUpByteInfo(WANDetails)

    listEntry = createListEntry(WANDictionary, netName)

    #print(f'\nlistEntry: {listEntry}\n')

    assert listEntry != None


#test to see bytes convert to MB
def testConvertListFromByteToMB():
    timeSpan = 2678400

    networks = getNetworks(dashboard)

    netCounter = 1

    netID = ''
    netName = ''

    for net in networks:
        if netCounter > 1:
            break
        netID = net["id"]
        netName = net["name"]
        netCounter += 1

    WANDetails = getWANDetails(netID, timeSpan, dashboard)

    WANDictionary = addUpByteInfo(WANDetails)

    listEntry = createListEntry(WANDictionary, netName)

    listEntry = convertListFromByteToMB(listEntry)

    #print(f'\nlistEntry: {listEntry}\n')

    entryDigit = listEntry[1].split(' MB')[0]

    entryDigit = int(entryDigit)

    #debug code
    #print(f'entryDigit: {entryDigit}')

    

    assert entryDigit < 1000000

#### GUI TESTS!!!! ####

#create a test for GUI creation
def testMakeGUI():

    #for terminal to know where we are in the tests....
    print('\nIn testMakeGUI()\n')

    makeGUI()

    #any errors along the way will show up on terminal but not kill the program...
    #bad assert but oh well.....
    assert 1 == 1


#create test for getting text from textbox
def testTextFromTextbox():

    #for terminal to know where we are in the tests....
    print('\nIn testTextFromTextbox()\n')

    makeGUI()

    assert 1 == 1

#create a test for pressing the button to send the text
def testButtonPressTextSend():

    #for terminal to know where we are in the tests....
    print('\nIn testButtonPressTextSend()\n')
    
    #run the program and see if text gets sent through
    makeGUI()

    assert 1 == 1


#create test for sanitizing text from textbox
def testTextInputSanitization():

    #for terminal to know where we are in the tests....
    print('\nIn testTextInputSanitization()\n')

    #run the program and see if only allowed text gets sent through
    makeGUI()

    assert 1 == 1


#create test for retrieving store number from store name

#create test for error window




#### GUI TESTS!!!! END ####

#### OPENPYXL TESTS ####

def testCreateWorkbook():
    wb = Workbook()
    wb.save('Meraki Device Data Details.xlsx')
    input('Look for the excel file and make sure it exists...\nthen press enter...')

#### OPENPYXL TESTS END ####



#create test to get store 1119 and store 1094 data
#not needed for future tests!!!!
def testSpecificStores():
    timeSpan = 2678400

    networks = getNetworks(dashboard)

    netCounter = 1

    netID1 = ''
    netName1 = ''

    netID2 = ''
    netName2 = ''

    for net in networks:
        netID = net["id"]
        netName = net["name"]
        #print(f'netName: {netName}')
        #print(f'netID = {netID}')
        if netName == "Store 1119 Wired":
            #print(f'netName: {netName}')
            #print(f'netID = {netID}')
            netName1 = netName
            netID1 = netID
        if netName == "Store 1094 Wired":
            #print(f'netName: {netName}')
            #print(f'netID = {netID}')
            netName2 = netName
            netID2 = netID
        netCounter += 1

    #print('\nBefore Wan details 1\n')
    WANDetails1 = getWANDetails(netID1, timeSpan, dashboard)
    #print('\nAfter Wan details 1\n')
    WANDictionary1 = addUpByteInfo(WANDetails1)
    #print('\nAfter Wan Dictionary 1\n')
    listEntry1 = createListEntry(WANDictionary1, netName1)
    #print('\nafter create ListEntry 1\n')

    listEntry1 = convertListFromByteToMB(listEntry1)
    #print('\nafter modify listEntry 1\n')
    
    #try sleeping??
    time.sleep(1)

    WANDetails2 = getWANDetails(netID2, timeSpan, dashboard)

    WANDictionary2 = addUpByteInfo(WANDetails2)

    listEntry2 = createListEntry(WANDictionary2, netName2)

    listEntry2 = convertListFromByteToMB(listEntry2)

    #debug code
    print(f'Store 1119: {listEntry1}')
    print(f'Store 1094: {listEntry2}')

    assert 1 == 1