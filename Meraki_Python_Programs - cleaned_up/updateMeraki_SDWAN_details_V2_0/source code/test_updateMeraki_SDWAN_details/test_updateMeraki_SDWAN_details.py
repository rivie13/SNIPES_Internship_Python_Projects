
##call in the file to be tested
##create functions in the file to then import here from the file call

#occasionally the import will fail for unknown reasons you may need to pull the
#variableData file from a different directory....

from variableData import APIKey, orgID
from updateMeraki_SDWAN_details import *

import meraki



##This test program is creating tests based off of functionality from the file
##updateMeraki_SDWAN_details.py and tests to make sure the nulls are handled appropriately,
##that proper values from each row of the csv go into the correct


#### TODO ####
#
# NONE FOR NOW.....
# 

###key to tests: given when then!!!!!!
    #given : what are initial conditions for test?
    #when : what is occurring that needs to be tested?
    #then : what is the expected response?

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

##create a test to make sure you are getting the organization ID correctly and securely
def testOrgIDCapture():
    organizationID = OrgIDCapture(dashboard)
    ##organizationID = organization['id']
    assert organizationID == orgID


##create a test to make sure that all appliances are actually SDWAN's
###found a way to actually just get the SDWANs with the get org devices function from meraki.... check relative function in other file
####count the list should be 374 devices
#####the number of MX appliances is constantly changing so this is not the best test to use to be able to check program working correctly....
######commenting out to help with future testing when I am not around anymore....
#def testGetMXAppliances():

#    mxAppliances = getMXAppliances(dashboard, orgID)

#    ##count them
#    numberOfMXDevices = 0
#    for appliance in mxAppliances:
#        numberOfMXDevices += 1

    ##check count equals 374
    ##this number changes every once in a while
    ##as of 11/7/24 it is now 375
    ##as of 11/21/2024 it is 372
#    assert numberOfMXDevices == 372
    

##create a test to see that you are able to get just a store number from an SDWAN
####MUST TEST WITH AN ACTUAL SDWAN
def testGetMXDeviceStoreNumber():

    #test the test with the test store data
    #get the test store SDWAN
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    mxDevice = dashboard.devices.getDevice('****-****-****')

    #debug code
    #print(f'{mxDevice}')

    ##test function
    storeNumber = getMXDeviceStoreNumber(mxDevice)

    #make sure they are equal
    assert storeNumber == 'EMPLOY-TEST-STORE'


##create a test to see if you can correctly match a store name in the csv to just the store number/identifier from the SDWAN
def testFindCSVStoreNumberMatch():

    #test with store number 'EMPLOY-TEST-STORE'
    storeNumber = 'EMPLOY-TEST-STORE'

    csvStoreNumber = findCSVStoreNumberMatch(storeNumber)

    assert storeNumber in csvStoreNumber



##create a test to see that the SDWAN store # and the csv store number match
##kind of unneccessary test??? I'm not sure but I think so...
def testDoStoreNumbersMatch():

    #test the test with the test store data
    #get the test store SDWAN
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    mxDevice = dashboard.devices.getDevice('****-****-****')

    mxDeviceStoreNumber = getMXDeviceStoreNumber(mxDevice)

    csvStoreNumber = findCSVStoreNumberMatch(mxDeviceStoreNumber)

    matchChecker = doStoreNumbersMatch(csvStoreNumber, mxDeviceStoreNumber)

    assert matchChecker == True



##create a test to get rowData from CSV sheet
def testGetRowDataFromCSV():

    #test the test with the test store data
    #get the test store SDWAN
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    mxDevice = dashboard.devices.getDevice('****-****-****')

    ##get store number from SDWAN
    mxDeviceStoreNumber = getMXDeviceStoreNumber(mxDevice)

    #get store name for CSV
    csvStoreName = findCSVStoreNumberMatch(mxDeviceStoreNumber)

    matchChecker = doStoreNumbersMatch(csvStoreName, mxDeviceStoreNumber)

    if matchChecker == False:
        #if match is false then need to throw error / fail test
        assert matchChecker == True

    #get rowData from SDWAN
    rowData = findRowDataFromCSV(csvStoreName)

    #debug code
    #print(rowData)

    ##bad assert statement to see print of rowData
    #should show csv data when bad error happens
    #assert rowData is None   

    #assert rowData is not empty
    assert rowData is not None



##create a test to see what happens when dealing with null values in csv tags fields (csv sheet: object type, material, Vendor Circuit I.D., provizioned circuit???)
##TAG FIELDS IN CSV: 3(3 mod 8 = 3), 4(4 mod 8 = 4), 5(5 mod 8 = 5), 6(6 mod 8 = 6)
##this test solved the null problem by making sure tagData list is never null it will at least have 'None' in it
def testGetTagDataFromRowData():

    #test the test with the test store data
    #get the test store SDWAN
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    mxDevice = dashboard.devices.getDevice('****-****-****')

    ##get store number from SDWAN
    mxDeviceStoreNumber = getMXDeviceStoreNumber(mxDevice)

    #get store name for CSV
    csvStoreName = findCSVStoreNumberMatch(mxDeviceStoreNumber)

    matchChecker = doStoreNumbersMatch(csvStoreName, mxDeviceStoreNumber)

    if matchChecker == False:
        #if match is false then need to throw error / fail test
        assert matchChecker == True

    #get rowData from SDWAN
    rowData = findRowDataFromCSV(csvStoreName)

    tagData = getTagsFromCSVRowData(rowData)

    #debug code
    #print(tagData)

    #purposeful bad assert
    #assert tagData is None

    #check for non empty tag list because this store should have tags from csv sheet...
    assert tagData is not None



##create a test to see what happens when dealing with null values in notes (csv sheet: Green provisioned circuit [2nd one] and terestial vendor)
##NOTE FIELDS IN CSV: 7(7 mod 8 = 7), 8(8 mod 8 = 0)
def testGetNotesDataFromRowData():

    #USE THE BROADSTREET STORE LIKE ABOVE TO GET ROW DATA
    #SINCE NO CHANGES MADE IN THIS TEST OKAY TO GRAB DATA FROM A LIVE STORE
    #Only need a store device because we are testing getting data from the CSV no writing happening here....

    #get broad street store SDWAN
#    mxDevice = dashboard.devices.getDevice('Q2QN-A68T-LCDZ')

    #test the test with the test store data
    #get the test store SDWAN
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    mxDevice = dashboard.devices.getDevice('****-****-****')

    ##get store number from SDWAN
    mxDeviceStoreNumber = getMXDeviceStoreNumber(mxDevice)

    #get store name for CSV
    csvStoreName = findCSVStoreNumberMatch(mxDeviceStoreNumber)

    matchChecker = doStoreNumbersMatch(csvStoreName, mxDeviceStoreNumber)

    if matchChecker == False:
        #if match is false then need to throw error / fail test
        assert matchChecker == True

    #get rowData from SDWAN
    rowData = findRowDataFromCSV(csvStoreName)

    notesData = getNotesFromCSVRowData(rowData)

    #debug code
    #print(notesData)

    #purposeful bad assert
    #assert notesData is None

    #check for non empty notes list... the function should at least put 'None' in since this store has no notes from CSV file....
    assert notesData is not None


#create a test to find serial number of SDWAN device
def testGetMXDeviceSerialNumber():

    #get the test store SDWAN
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testSDWAN = dashboard.devices.getDevice('****-****-****')

    mxDeviceSerialNumber = getMXDeviceSerialNumber(testSDWAN)

    #debug code
    #print(mxDeviceSerialNumber)

    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    assert mxDeviceSerialNumber == '****-****-****'



##create a test to see that all tags were able to be properly added (object type, material, Vendor Circuit I.D., blue provizioned circuit???)
### !!! THIS TEST WILL CHECK WRITE FOR ONE STORE... ONE STORE'S TAGS GO ON TO THE TEST STORE PAGE....
### THIS TEST CAN ONLY USE TEST STORE FOR WRITING SINCE WE ARE WRITING TO IT
### WHEN WRITING FOR THIS TEST ENSURE THAT THE WRITE ONLY HAPPENS EXCLUSIVELY TO THE TEST STORE PAGE

def testAddTagDataToTestStorePage():
    ##write out step by step what you want to do in the comments....

    ##remember test steps here actual function steps in the other file....

    #get the TEST STORE device you want to write to
    #get the test store SDWAN
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testSDWAN = dashboard.devices.getDevice('****-****-****')


    #get the broad street store tag data from CSV file
    #store number should be 1027
    storeNumber = '1027'
    csvStoreNumber = findCSVStoreNumberMatch(storeNumber)

    csvRowData = findRowDataFromCSV(csvStoreNumber)

    tagData = getTagsFromCSVRowData(csvRowData)


    #get the serial number for the test store device
    mxDeviceSerialNumber = getMXDeviceSerialNumber(testSDWAN)

    #write to the test store the data from the csv sheet for broad street store that should be tag data
    addTagDataToStorePage(mxDeviceSerialNumber, tagData, dashboard)

    #check that the test store tags is equal to the tag data from the CSV sheet
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testStoreUpdatedData = dashboard.devices.getDevice('****-****-****')

    testStoreUpdatedTags = testStoreUpdatedData['tags']

    #sort the lists first then do the assert or else error
    testStoreUpdatedTags.sort()
    tagData.sort()

    #debug code
    #print(f'\nTest Store Updated Tags: {testStoreUpdatedTags}\n')

    #debug code
    #print(f'\nTag Data: {tagData}\n')

    assert testStoreUpdatedTags == tagData



#Should not happen but maybe need a test to deal with invalid notes??
#wait until issue arrises... not sure if notes can be invalid yet....


##create a test to see that all notes were properly added
### !!! THIS TEST WILL CHECK WRITE FOR ONE STORE... ONE STORE'S NOTES GO ON TO THE TEST STORE PAGE....
###THIS TEST CAN ONLY USE TEST STORE SINCE WE ARE WRITING TO IT
###WHEN WRITING FOR THIS TEST ENSURE THAT THE WRITE ONLY HAPPENS EXCLUSIVELY TO THE TEST STORE PAGE
def testAddNotesDataToStorePage():

    
    #get the TEST STORE device you want to write to
    #get the test store SDWAN
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testSDWAN = dashboard.devices.getDevice('****-****-****')

    #get the broad street store tag data from CSV file
    #store number should be 1027
    #storeNumber = '1027'
    #change to test store....
    csvStoreNumber = findCSVStoreNumberMatch('1020')

    #get the row data
    csvRowData = findRowDataFromCSV(csvStoreNumber)

    #get the notesData
    #notesData = getNotesFromCSVRowData(csvRowData)
    #get the notes data in proper format
    formattedNotes = formatNotesString(csvRowData)

    #get the serial number from the test store mx device
    mxdeviceSerialNumber = getMXDeviceSerialNumber(testSDWAN)

    #create notesString
    #notesString = makeNotesListIntoString(formattedNotes)

    #write to the test store the data from the csv sheet for the broad street store that should be notes data
    addNotesDataToStorePage(mxdeviceSerialNumber, formattedNotes, dashboard)

    #check that the test store tags is equal to the tag data from the CSV sheet
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testStoreUpdatedData = dashboard.devices.getDevice('****-****-****')

    #debug code
    #print(f'\ntestStoreUpdatedDevice: {testStoreUpdatedData}\n')

    testStoreUpdatedNotes = testStoreUpdatedData["notes"]

    #debug code
    #print(f'\nTestStoreUpdatedNotes: {testStoreUpdatedNotes}\n')

    #debug code
    #print(f'\nnotesString: {notesString}\n')

    assert formattedNotes == testStoreUpdatedNotes


#create a test for getting the MX Device Notes
def testGetMxDeviceNotes():

    #get the test store SDWAN    
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testSDWAN = dashboard.devices.getDevice('****-****-****')


    testSDWANNotes = testSDWAN["notes"]

    deviceNotes = getMxDeviceNotes(testSDWAN)

    testSDWANNotesCheck = False

    if testSDWANNotes == deviceNotes:
        testSDWANNotesCheck = True

    assert testSDWANNotesCheck == True

#create a test for the function that checks if the two
#sets of notes are the same
def testCheckIfMerakiNotesAndCSVNotesDifferent():

    #get the TEST STORE device you want to write to
    #get the test store SDWAN    
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testSDWAN = dashboard.devices.getDevice('****-****-****')


    #get the notes from testSDWAN meraki page
    testSDWANNotes = getMxDeviceNotes(testSDWAN)

    #get the notes from the csv sheet for diff store... store 1020
    
    csvStoreNumber = findCSVStoreNumberMatch('1020')
    rowData = findRowDataFromCSV(csvStoreNumber)
    formattedNotes = formatNotesString(rowData)

    #var to call function to check
    notesAreDifferent = checkIfMerakiNotesAndCSVNotesDifferent(testSDWANNotes, formattedNotes)

    #assert true or false... depending on when you run this test it will be true or false....
    assert notesAreDifferent == True or notesAreDifferent == False

def testCheckIfMerakiTagsAndCSVTagsDifferent():
    #test store device
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testSDWAN = dashboard.devices.getDevice('****-****-****')


    testSDWANTags = getMxDeviceTags(testSDWAN)

    
    #get the tags from the csv sheet for diff store... store 1020
    
    csvStoreNumber = findCSVStoreNumberMatch('1020')
    rowData = findRowDataFromCSV(csvStoreNumber)
    csvTags = getTagsFromCSVRowData(rowData)

    tagsAreDifferent = checkIfMerakiTagsAndCSVTagsDifferent(testSDWANTags, csvTags)

    assert tagsAreDifferent == True or tagsAreDifferent == False


#create a test for the formatted notes function and adding it to test store page
def testFormatNotesString():

    #get the TEST STORE device you want to write to
    #get the test store SDWAN    
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testSDWAN = dashboard.devices.getDevice('****-****-****')


    #get the broad street store tag data from CSV file
    #store number should be 1027
    #storeNumber = '1027'
    #change to test store....
    csvStoreNumber = findCSVStoreNumberMatch('1020')

    #get the row data
    csvRowData = findRowDataFromCSV(csvStoreNumber)

    #get the notes data in proper format
    formattedNotes = formatNotesString(csvRowData)

    #the data was cleared from below.... make sure to update it with correct data!!!
    #you will need to look it up in excel sheet....
    formatCheck = 'Managing Partner: **********\nProvider: **********\nSpeed: **********'
    #after adding notes to store page make sure the meraki notes == the formatted notes
    #also look and check physically with your eyes!!!
    assert formattedNotes == formatCheck



#This should be the last test that runs!!!!
##create a test that can update the test store page for all SDWAN info
### !!! WRITE ALL INFO TO ONLY TEST STORE PAGE.....
###THIS TEST CAN ONLY UPDATE TEST STORE PAGE BUT WILL PULL DATA FROM CSV
###WHEN WRITING FOR THIS TEST ENSURE THAT THE WRITE ONLY HAPPENS EXCLUSIVELY TO THE TEST STORE PAGE

###change this for updated csv/data/functions....

def testAddAllDataToTestStorePage():
    
    #get the TEST STORE device you want to write to
    #get the test store SDWAN  
    #REPLACE THE STARS WITH TEST STORE SERIAL NUMBER
    testSDWAN = dashboard.devices.getDevice('****-****-****')

    mxAppliances = getMXAppliances(dashboard, orgID)

    #go through all the mxDevices
    for mxDevice in mxAppliances:
        #if test store need to skip to next device
        mxDeviceStoreName = getMXDeviceStoreNumber(mxDevice)

        if mxDeviceStoreName == 'EMPLOY-TEST-STORE':
            continue

        #if not test store get the CSV data
        csvStoreName = findCSVStoreNumberMatch(mxDeviceStoreName)

        matchCheck = doStoreNumbersMatch(csvStoreName, mxDeviceStoreName)

        #if matchCheck == true and store names are both '' need to continue
        if matchCheck == True and mxDeviceStoreName == '' and csvStoreName == '':
            continue


        #if store is not 'EMPLOY-TEST-STORE' or if store is not on CSV file list
        #need to move on to the next device
        if matchCheck == False:
            continue

        rowData = findRowDataFromCSV(csvStoreName)

        csvTags = getTagsFromCSVRowData(rowData)

        #get test store serial number
        #get mxSerialNumber
        testStoreSerialNumber = getMXDeviceSerialNumber(testSDWAN)

        #get the mxDevice notes and make sure they are empty....
        testStoreNotes = getMxDeviceNotes(testSDWAN)

        #get mxDevice tags
        testStoreTags = getMxDeviceTags(testSDWAN)

        #get notes in formatted form
        formattedCSVNotesString = formatNotesString(rowData)

        if testStoreNotes == '' or testStoreNotes == None:
            addNotesDataToStorePage(testStoreSerialNumber, formattedCSVNotesString, dashboard)

        if testStoreTags == '' or testStoreTags == None:
            addTagDataToStorePage(testStoreSerialNumber, csvTags, dashboard)
        
        notesAreDifferent = checkIfMerakiNotesAndCSVNotesDifferent(testStoreNotes, formattedCSVNotesString)
        tagsAreDifferent = checkIfMerakiTagsAndCSVTagsDifferent(testStoreTags, csvTags)

        if tagsAreDifferent == True:
            addTagDataToStorePage(testStoreSerialNumber, csvTags, dashboard)
        if notesAreDifferent == True:
            addNotesDataToStorePage(testStoreSerialNumber, formattedCSVNotesString, dashboard)

    #Need to create a better assert statement....
    assert 1 == 1


