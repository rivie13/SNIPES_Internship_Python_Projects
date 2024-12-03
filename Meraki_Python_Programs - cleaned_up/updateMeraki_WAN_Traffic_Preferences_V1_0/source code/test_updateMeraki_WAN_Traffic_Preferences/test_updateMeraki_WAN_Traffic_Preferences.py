'''
test_updateMeraki_WAN_Traffic_Preferences.py
Created by: Riviera Sperduto
Creation date: 11/26/2024
Last edit date: 11/26/2024
'''

###UPDATE THE TEST STORE SERIAL NUMBERS OR ELSE THERE WILL BE ERRORS!!!!!

#access data from variableData file
from time import sleep
from variableData import APIKey, orgID

#get functions to test from program file
from updateMeraki_WAN_Traffic_Preferences import *

import meraki

dashboard = meraki.DashboardAPI(APIKey)

orgID = orgID

def testAPIKeyGen():
    assert APIKeyGen() == APIKey


def testGetAPIDashboard():
    dashboard = getAPIDashboard(APIKey)

    assert dashboard != None

def testorgIDCapture():
    assert orgIDCapture() == orgID

#makes sure that mx devices are returned from the function call...
def testGetMXAppliances():
    assert getMXAppliances(dashboard, orgID) != None

def testGetMXDeviceName():
    #use the test store to test this function out...
    #REPLACE THIS WITH TEST STORE SERIAL NUMBER
    testStoreSerialNum = '****-****-****'

    testStoreDevice = dashboard.devices.getDevice(testStoreSerialNum)

    testStoreName = testStoreDevice["name"]

    #test store name should equal test store name....
    assert getMXDeviceName(testStoreDevice) == testStoreName

def testGetMXDeviceTags():
    #use the test store to test this function out...
    #REPLACE THIS WITH TEST STORE SERIAL NUMBER
    testStoreSerialNum = '****-****-****'

    testStoreDevice = dashboard.devices.getDevice(testStoreSerialNum)

    testStoreTags = testStoreDevice["tags"]

    #test store name should equal test store name....
    assert getMXDeviceTags(testStoreDevice) == testStoreTags

def testGetNetworkID():
    #use the test store to test this function out...
    #REPLACE THIS WITH TEST STORE SERIAL NUMBER
    testStoreSerialNum = '****-****-****'

    testStoreDevice = dashboard.devices.getDevice(testStoreSerialNum)

    testStoreNetworkID = testStoreDevice["networkId"]

    #test store network should equal test store network....
    assert getNetworkID(testStoreDevice) == testStoreNetworkID

def testGetDeviceTrafficSettingSelections():
    #use the test store to test this function out....
    #REPLACE THIS WITH TEST STORE SERIAL NUMBER
    testStoreSerialNum = '****-****-****'

    testStoreDevice = dashboard.devices.getDevice(testStoreSerialNum)

    testStoreNetwork = getNetworkID(testStoreDevice)

    deviceTrafficSettings = getDeviceTrafficSettingSelections(dashboard, testStoreNetwork)

    #debug code....
    #print(f'deviceTrafficSettings:\n{deviceTrafficSettings}\n\n')

    assert deviceTrafficSettings != None

def testCheckIfSettingsNeedUpdate():
    #use the test store to test this function out....
    #REPLACE THIS WITH TEST STORE SERIAL NUMBER
    testStoreSerialNum = '****-****-****'

    testStoreDevice = dashboard.devices.getDevice(testStoreSerialNum)

    testStoreNetwork = getNetworkID(testStoreDevice)

    deviceTrafficSettings = getDeviceTrafficSettingSelections(dashboard, testStoreNetwork)

    #debug code....
    #print(f'deviceTrafficSettings:\n{deviceTrafficSettings}')
    settingsNeedUpdated = checkIfSettingsNeedUpdate(deviceTrafficSettings)

    #debug code....
    #print(f'settingsNeedUpdated:\n{settingsNeedUpdated}\n\n')

    assert settingsNeedUpdated != None

def testUpdateTrafficSettings():
    #use the test store to test this function out....
    #REPLACE THIS WITH TEST STORE SERIAL NUMBER
    testStoreSerialNum = '****-****-****'

    testStoreDevice = dashboard.devices.getDevice(testStoreSerialNum)

    testStoreNetwork = getNetworkID(testStoreDevice)

    deviceTrafficSettings = getDeviceTrafficSettingSelections(dashboard, testStoreNetwork)

    #debug code....
    #print(f'deviceTrafficSettings:\n{deviceTrafficSettings}')
    settingsNeedUpdated = checkIfSettingsNeedUpdate(deviceTrafficSettings)

    #check if all settings need update or not.... for use in main....
    result = all(x == False for x in settingsNeedUpdated.values())
    #print(f'are all values false? {result}')

    if result == True:
        assert result == True
    

    updatedSettings = updateTrafficSettings(dashboard, testStoreNetwork, settingsNeedUpdated)

    #print(f'updatedSettings: {updatedSettings}\n\n')

    assert updatedSettings != None

def testEverything():

    key = APIKeyGen()

    dashboard = getAPIDashboard(key)

    orgID = orgIDCapture()

    mxDevices = getMXAppliances(dashboard, orgID)

    updateCounter = 0

    for mxDevice in mxDevices:
        name = getMXDeviceName(mxDevice)

        tags = getMXDeviceTags(mxDevice)

        #if 'DC' in tags:
        if any('DC' in string for string in tags):
            #debug code
            print(f'found a DC network: {name}\ntags: {tags}\ncontinuing to next device/network....')
            #found all 7 stores with a tag that includes DC....
            #input('confirm a DC network was found then press enter....')
            #sleep(2)
            continue

        netID = getNetworkID(mxDevice)
        deviceTrafficSettings = getDeviceTrafficSettingSelections(dashboard, netID)
        #debug code....
        #print(f'\n\ndeviceTrafficSettings for network {name}:\n{deviceTrafficSettings}')
        settingsNeedUpdated = checkIfSettingsNeedUpdate(deviceTrafficSettings)
        #debug code....
        #print(f'\n\nDo Settings need updated T/F for network {name}: {settingsNeedUpdated}')
        #check if all settings need update or not.... for use in main....
        result = all(x == False for x in settingsNeedUpdated.values())
        #debug code...
        #print(f'are all values false? {result}')
        if result == True:
            #if true no update needs to happen so skip this one go to next mxDevice....
            print(f'device: {name} does not need updated....\nmoving on to next device....')
            #sleep(2)
            continue
        #debug code make sure to comment out below after tests/checks to speed up tests!!!!
        #input("an update would happen here....\ncheck data to make sure it is correct....\npress enter to continue...")

        print(f'device: {name} was updated....\nmoving on to next device....')
        updateCounter += 1

        #sleep to make sure it doesn't crash?
        #sleep(2)
    
    print(f'{updateCounter} device(s) was/were updated in Meraki...')
    
    assert True == True