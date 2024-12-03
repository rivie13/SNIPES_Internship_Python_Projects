'''
updateMerkai_SDWAN_details.py
created by: Riviera Sperduto
creation date: sometime in October 2024?
last edit date: 11/21/2024
'''

#this variableData file import sometimes doesn't work
#you will need to pull the file from a different directory occasionally
#for unknown reasons...

###sometimes the __init__.py file causes a problem... I have deleted it to prevent the issue? Seems to have fixed it....
from variableData import APIKey, csvFilePath

import csv
import meraki



##This program is based off of the test file pythonTest.py and
##the original automation program created by someone else
##called getMeraki-details.py

#### TODO ####
#
# NONE FOR NOW...
#
# 

##functions for program and testing.....

def APIKeyGen():
    key = APIKey
    return key

def getAPIDashboard(key):
    ##instantiate meraki Dashboard API session
    dashboard = meraki.DashboardAPI(api_key=key)
    return dashboard

def OrgIDCapture(dashboard):
    organizations = dashboard.organizations.getOrganizations()
    for org in organizations:
        orgID = org['id']
    return orgID


def getMXAppliances(dashboard, orgID):
    ##put all models in list to use the list as a parameter in the API call
    models = ['MX250', 'MX450', 'MX65', 'MX68', 'MX68CW-NA']
    MXDevices = dashboard.organizations.getOrganizationDevices(orgID, total_pages = 'all', models=models)
    return MXDevices

def getMXDeviceStoreNumber(mxDevice):

    #set the storeName to ''

    storeNumber = ''

    ##get the name from the mxdevice
    mxDeviceName = mxDevice["name"]

    ##split up the name into parts
    splitName = mxDeviceName.split()

    ##debug code
    #print(mxDeviceName)

    ##TEST STORE FIX BELOW
    if mxDeviceName == "EMPLOY-TEST-STORE":
        storeNumber = mxDeviceName
        return storeNumber

    ##go through the parts of the name and find store number
    for part in splitName:
        if part.isdigit():
            storeNumber = part
        

    return storeNumber


#takes a store number from an MX device and goes through CSV sheet to find a matching
#store number.... returns the csvFile store name that matches with the MX device store number
def findCSVStoreNumberMatch(mxdeviceStoreNumber):

    ##raw string to get the correct file path when opening the file...
    ##path is held in the variableData.py file so you only have to change it in one place
    csvFile = csvFilePath
   
    
    ###need to set CSVStoreName to '' this is so if no match is found in list then at
    #least the program can see the '' does not match any store name and will move on to
    #next device

    csvStoreName = ''


    ###need to deal with the test store here....
    ###if test store is being used return
    ##test store as csvStoreNumber
    if mxdeviceStoreNumber == "EMPLOY-TEST-STORE":
        csvStoreName = mxdeviceStoreNumber
        return csvStoreName

    rows = []

    with open(csvFile, 'r') as openCSVFile:
        csvReader = csv.reader(openCSVFile)
        for row in csvReader:
            rows.append(row)


        for row in rows:
            columnCounter = 1
            for col in row:
                if columnCounter == 1:
                    if mxdeviceStoreNumber in col:
                        csvStoreName = col

    return csvStoreName

def doStoreNumbersMatch(csvStoreName, mxdeviceStoreNumber):
    
    numbersMatch = False

    if mxdeviceStoreNumber in csvStoreName:
        numbersMatch = True
    
    return numbersMatch

##function to go through CSV file with a specific csvStoreName to find row associated with the csvStoreName
def findRowDataFromCSV(csvStoreName):
    csvFile = csvFilePath   

    #need to deal with the test store here.....
    ###or deliberately choose to not deal with test store 
    ###need to still get the row data from here so it can
    ##be added to the test store....
    ###if I still need to get row data then that means I need to put in a store that
    ##is not the test store

    #!!!!!!!!!!!!!!!!! to deal with test store issue put in a row in the CSV for the test store....
    #!!!!!!!!!!!!!!!!! use a different csv file I guess when not testing anymore???
    #!!!!!!!!!!!!!!!!! will deal with test store loop issue (don't want to keep writing test store data back into test store page... need to make sure getting different store info in page for test)


    rows = []

    rowData = []

    with open(csvFile, 'r') as openCSVFile:
        csvReader = csv.reader(openCSVFile)
        for row in csvReader:
            rows.append(row)

        for row in rows:
            for col in row:
                if csvStoreName in col:
                    rowData = row
    
    return rowData

##to not have to deal with null tags just make sure that the tagData returns 'None' if no tags found in csv sheet
def getTagsFromCSVRowData(rowData):

    #start at 1 go up to 8.... there are more than 8 fields but will reduce in csv
    fieldCounter = 1

    #hold the tag data in here after fetching
    tagData = []

    for data in rowData:
        #print(f'\ndata: {data}\nfieldCounter: {fieldCounter}\n')
        #should never reach this point but if it does then put it back
        if fieldCounter == 6:
            fieldCounter = 1
            #at last item so move to new row of data
            continue
        if fieldCounter % 6 == 2 or fieldCounter % 6 == 3 or fieldCounter % 6 == 4:
            #print(f'INSIDE IF:\ndata: {data}\nfieldCounter: {fieldCounter}\n')
            if data == '':
                fieldCounter += 1
                continue
            #skip over the invalid tags here... don't have to remove invalid tags later
            
            if data == 'NEW HORIZON':
                fieldCounter += 1
                continue
            if data == 'Cell - Primary':
                fieldCounter += 1
                continue
            

            ##add the tag data to the tagData list
            tagData.append(data)

        fieldCounter += 1

    #if empty put 'None' in there
    if tagData is None:
        tagData.append('None')

    return tagData

def getNotesFromCSVRowData(rowData):

    #start at 1 go up to 8
    fieldCounter = 1

    #notesData holder... put data in here
    notesData = []

    for data in rowData:
        if fieldCounter % 8 == 7 or fieldCounter % 8 == 0:
            if data == '':
                continue
        #add note data to noteData list
            notesData.append(data)
        fieldCounter += 1
        #should never get here but just in case....
        if fieldCounter == 9:
            fieldCounter = 1
    
    #if empty put 'None' in there
    if notesData is None:
        notesData.append('None')

    return notesData


def addTagDataToStorePage(mxDeviceSerialNumber, tagData, dashboard):
    #what should be brought into this function???
    #tagData, mxDeviceSerialNumber, dashboard

    #what is it doing???

    #BEFORE GOING ON WITH THIS I NEED TO GET MX DEVICE SERIAL #

    #perform the update with the data given
    dashboard.devices.updateDevice(mxDeviceSerialNumber, tags = tagData)

    return

def addNotesDataToStorePage(mxDeviceSerialNumber, notesString, dashboard):

    #perform update with data given like above
    dashboard.devices.updateDevice(mxDeviceSerialNumber, notes = notesString)

    return


def getMXDeviceSerialNumber(mxDevice):

    ##get the name from the mxdevice
    mxDeviceSerialNumber = mxDevice["serial"]
    return mxDeviceSerialNumber


#need to get the device notes so that I can
#compare them to the csv sheet
#if the meraki notes have something but csv 
#does not don't delete the meraki notes
#for blank csv notes.....
def getMxDeviceNotes(mxDevice):
    
    #similar to how things were done before when 
    #checking note data

    #get the notes from Meraki
    mxDeviceNotes = mxDevice["notes"]

    if mxDeviceNotes is None:

        #set notes to ''
        mxDeviceNotes = ''


    return mxDeviceNotes


#create a function to see if meraki and csv notes
#are different
def checkIfMerakiNotesAndCSVNotesDifferent(mxDeviceNotes, cleanCSVNotesString):
    #assume notes are different to start
    notesAreDifferent = True

    if mxDeviceNotes == cleanCSVNotesString:
        notesAreDifferent = False
    
    return notesAreDifferent

#create a function to get mxDevice tags....
def getMxDeviceTags(mxDevice):
    mxDeviceTags = mxDevice["tags"]

    if mxDeviceTags is None:
        mxDeviceTags = ''
    
    return mxDeviceTags

#create a function to see if meraki and csv tags are different....
def checkIfMerakiTagsAndCSVTagsDifferent(mxDeviceTags, csvTags):

    tagsAreDifferent = True

    if sorted(mxDeviceTags) == sorted(csvTags):
        tagsAreDifferent = False
    
    return tagsAreDifferent


#create a function to format the notes in the right way
#need to bring in the row data and take out the appropriate parts
#and put them into the appropriate slot in the string
def formatNotesString(csvRowData):
    #start off with blank full notes string
    formattedNotesString = ''

    #get the managing partner
    managingPartner = ''
    #get the provider
    provider = ''
    #get the speed
    speed = ''

    #get the nonSpeed data
    otherData = ''

    #create the counter to get the right data
    fieldCounter = 1

    for data in csvRowData:
        if fieldCounter == 3:
            managingPartner = data
        if fieldCounter == 5:
            provider = data
        if fieldCounter == 6:
            if 'MB' in data or 'CUST PROVIDED' in data or 'GB' in data:
                #debug code
                #print(f'found speed: {data}')
                speed = data
            else:
                #debug code
                #print(f'found other data: {data}')
                otherData = data
        fieldCounter += 1

    #when all data is retrieved
    if speed != '':

        formattedNotesString = f'Managing Partner: {managingPartner}\nProvider: {provider}\nSpeed: {speed}'
    if otherData != '':
        formattedNotesString = f'Managing Partner: {managingPartner}\nProvider: {provider}\n{otherData}'
    return formattedNotesString

##END FUNTIONS FOR PROGRAM AND TESTING



######START CODE###########
def main():

    #debug code
    #print('\nInside Program\n')
    #print(f'got the API key')

    ##get the api key
    key = APIKey

    ##Instantiate a dashboard object for the API
    dashboard = getAPIDashboard(key)

    ##get the organization ID
    organizationID = OrgIDCapture(dashboard)

    ##get all the SDWANs
    MXAppliances = getMXAppliances(dashboard, organizationID)

    #count the number of updates that happen:
    storeCounter = 0

    notesUpdateCounter = 0
    tagsUpdateCounter = 0

    ##loop to go through all the MX devices (SDWANs)
    for mxDevice in MXAppliances:
        mxDeviceStoreNumber = getMXDeviceStoreNumber(mxDevice)

        #if test store continue....
        if mxDeviceStoreNumber == 'EMPLOY-TEST-STORE':
            continue

        csvStoreName = findCSVStoreNumberMatch(mxDeviceStoreNumber)
        matchChecker = doStoreNumbersMatch(csvStoreName, mxDeviceStoreNumber)
        
        ##if match not found here then must quit so we don't update a store with the wrong information
        ##ACTUALLLLYYYYYY if match not found here then that means we have an SDWAN that is not on the CSV list!!!
        ###This means that we have to move on to the next device in the list....
        if matchChecker == False or csvStoreName == 'EMPLOY-TEST-STORE' or mxDeviceStoreNumber == 'EMPLOY-TEST-STORE':
            
            continue
        

        ##if store nums match and they equal '' or 'EMPLOY-TEST-STORE'
        if matchChecker == True and ((mxDeviceStoreNumber == '' and csvStoreName == '') or (mxDeviceStoreNumber == 'EMPLOY-TEST-STORE' and csvStoreName == 'EMPLOY-TEST-STORE')):
            continue

        #if at this point then that means stores match and are legit values in the csv file and meraki

        #call function to go through the csv and find the row data associated with the specific csvStoreName
        csvRowData = findRowDataFromCSV(csvStoreName)

        csvTags = getTagsFromCSVRowData(csvRowData)

        #get the serial number for this mxDevice!!
        mxDeviceSerialNumber = getMXDeviceSerialNumber(mxDevice)

        #get the mxDevice notes and make sure they are empty
        merakiMxDeviceNotes = getMxDeviceNotes(mxDevice)

        #get the mxDevice tags for comparrison later...
        merakiMxDeviceTags = getMxDeviceTags(mxDevice)

        
        #new function here to format notes string.
        formattedCSVNotesString = formatNotesString(csvRowData)

        #if there are no notes on Meraki already then update them!
        if merakiMxDeviceNotes == '' or merakiMxDeviceNotes == None:
            addNotesDataToStorePage(mxDeviceSerialNumber, formattedCSVNotesString, dashboard)
            notesUpdateCounter += 1
        
        #need a new function here to check if notes from meraki
        #are different from notes on csv
        notesAreDifferent = checkIfMerakiNotesAndCSVNotesDifferent(merakiMxDeviceNotes, formattedCSVNotesString)


        #if notes are same skip
        #if notes are different then add csv notes to
        #meraki notes (overwrite old notes)
        if notesAreDifferent == True:

            #need a new function to add meraki and csv notes together

            #if different then just add what is on the sheet to meraki since sheet is truth source
            addNotesDataToStorePage(mxDeviceSerialNumber, formattedCSVNotesString, dashboard)
            notesUpdateCounter += 1
        

        #put in check to see if tags are same... if same then skip
        #if tags are diff then add csvTags to meraki notes (overwrite the old or empty tag(s))....
        if merakiMxDeviceTags == '' or merakiMxDeviceTags == None:
            addTagDataToStorePage(mxDeviceSerialNumber, csvTags, dashboard)
            tagsUpdateCounter += 1
        
        tagsAreDifferent = checkIfMerakiTagsAndCSVTagsDifferent(merakiMxDeviceTags, csvTags)

        if tagsAreDifferent == True:
            #add the tag data
            addTagDataToStorePage(mxDeviceSerialNumber, csvTags, dashboard)
            tagsUpdateCounter += 1
        
        #increment the update counter
        storeCounter += 1

        
    #print({MXAppliances})
    

    print(f'\nStore update(s) successful.\nStore count: {storeCounter}\nNumber of store\'s that got notes section updated: {notesUpdateCounter}\nNumber of store\'s that got tags section updated: {tagsUpdateCounter}\n')



#This is how you run the file..... need to run main function
if __name__ == '__main__':
    main()

    

######END CODE#############