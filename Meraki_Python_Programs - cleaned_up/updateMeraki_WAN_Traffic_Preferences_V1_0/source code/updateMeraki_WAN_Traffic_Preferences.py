'''
updateMeraki_SDWAN_details.py
Created by: Riviera Sperduto
Creation date: 11/21/2024
Last edit date: 11/21/2024
'''

from time import sleep
from variableData import APIKey, orgID

import meraki

### TODO ###
#
# 1. get the networks
# 2. skip HQ and DC networks
# 3. set all the stuff.....
# 4. display how many store networks were updated....
# 5. done....
#

### FUNCTIONS FOR PROGRAM ### **********************************************

def APIKeyGen():
    key = APIKey
    return key

def getAPIDashboard(key):
    
    #instantiate meraki Dashboard API session
    dashboard = meraki.DashboardAPI(api_key=key)
    return dashboard

def orgIDCapture():
    organizationID = orgID
    return organizationID

def getMXAppliances(dashboard, orgID):
    ##put all models in list to use the list as a parameter in the API call
    models = ['MX65', 'MX68', 'MX68CW-NA']
    MXDevices = dashboard.organizations.getOrganizationDevices(orgID, total_pages = 'all', models=models)
    return MXDevices

def getMXDeviceName(mxDevice):

    mxDeviceName = mxDevice["name"]

    return mxDeviceName

def getMXDeviceTags(mxDevice):
    mxDeviceTags = mxDevice["tags"]
    return mxDeviceTags


def getNetworkID(mxDevice):
    networkID = mxDevice["networkId"]

    return networkID

def getDeviceTrafficSettingSelections(dashboard, networkID):

    deviceTrafficSettings = {}

    deviceTrafficSettings = dashboard.appliance.getNetworkApplianceTrafficShapingUplinkSelection(networkID)

    return deviceTrafficSettings

def checkIfSettingsNeedUpdate(deviceTrafficSettings):
    #assume settings need change at first
    settingsNeedUpdated = { 
        "Load Balancing" : True,
        "Active-Active" : True,
        "Protocol" : True,
        "Source" : True,
        "Source Port" : True,
        "Destination" : True,
        "Destination Port" : True,
        "Preferred Uplinks" : True
    }

    ### ADD CHECKS / CODE HERE!!!!!!!!

    #get these values from the dictionary/list??? I think it is a list inside a dictionary...
    #hard to tell.... I used chatGPT to help figure out how to get the specific values I was looking for
    #gave chatGPT the json data deviceTrafficSettings and asked how to get certain parts
    #it gave me pieces of the code below which helped me get the data I needed...
    WANPreferences = deviceTrafficSettings["wanTrafficUplinkPreferences"]
    if WANPreferences and WANPreferences[0].get("preferredUplink", None) is not None:
        preferredUplink = WANPreferences[0].get("preferredUplink", [])


    ###lots and lots of debug code.....
    #print(f'loadBalancing {deviceTrafficSettings["loadBalancingEnabled"]}')
    #print(f'Active Active {deviceTrafficSettings["activeActiveAutoVpnEnabled"]}')
    #print(f'\n\nnested settings?: {deviceTrafficSettings["wanTrafficUplinkPreferences"]}\n\n')
    #print(f'\n\nWANPreferences = {WANPreferences}\n\n')
    #print(f'preferredUplink: {preferredUplink}')

    if deviceTrafficSettings["loadBalancingEnabled"] == False:
        #debug code
        #print("updated settingsNeedUpdated Load Balancing setting!!")
        settingsNeedUpdated["Load Balancing"] = False


    #check if activeActive is there first....

    if "activeActiveAutoVpnEnabled" in deviceTrafficSettings:

        if deviceTrafficSettings["activeActiveAutoVpnEnabled"] == False:
            #debug code
            #print("updated settingsNeedUpdated Active-Active setting!!")
            settingsNeedUpdated["Active-Active"] = False

    if WANPreferences and WANPreferences[0].get("preferredUplink", None) is not None and preferredUplink == 'wan1':
        #debug code
        #print("updated settingsNeedUpdated preferredUplink setting!!")
        settingsNeedUpdated["Preferred Uplinks"] = False
    

    if WANPreferences:
        #print('FOUND WAN PREFERENCES!!!')

        #grab the list's first element
        WANTrafficFilters = WANPreferences[0].get("trafficFilters", [])

        #grab the second element of list
        WANPreferredUplink = WANPreferences[0].get("preferredUplink", [])
        #print(f'preferredUplink = {WANPreferredUplink}')

        #technically debug code?
        #if WANTrafficFilters:
            #print(f'WAN Traffic Filters: {WANTrafficFilters}\n\n')

        #put the elements of the list in the var...
        #only works if the above if and print statement are uncommented.... not sure why it would
        #be needed.....
        #WANTrafficFilters = WANTrafficFilters.get("trafficFilters", None)

        trafficFilters = WANTrafficFilters[0]

        #access the dictionary for later use...
        valueDictionary = trafficFilters.get("value", None)

        source_port = valueDictionary.get("source", {}).get("port", None)
        source_cidr = valueDictionary.get("source", {}).get("cidr", None)
        destination_port = valueDictionary.get("destination", {}).get("port", None)
        destination_cidr = valueDictionary.get("destination", {}).get("cidr", None)

        #debug code....
        #print(f"Source Port: {source_port}")
        #print(f"Source CIDR: {source_cidr}")
        #print(f"Destination Port: {destination_port}")
        #print(f"Destination CIDR: {destination_cidr}")
        
        # Accessing nested settings:
        if WANTrafficFilters and len(WANTrafficFilters) > 0:
            first_filter = WANTrafficFilters[0]
            #debug code....
            #print(f'nested settings 2?? trafficFilters.value: {first_filter.get("value", None)}')
            #print(f'nested settings 3?? trafficFilters.value.protocol: {first_filter.get("value", {}).get("protocol", None)}')

            protocolValue = first_filter.get("value", {}).get("protocol", None)
            
            if protocolValue == 'any':
                settingsNeedUpdated["Protocol"] = False
        

        if source_port == "any":
            settingsNeedUpdated["Source Port"] = False

        if source_cidr == "any":
            settingsNeedUpdated["Source"] = False

        if destination_port == "any":
            settingsNeedUpdated["Destination Port"] = False

        if destination_cidr == "any":
            settingsNeedUpdated["Destination"] = False


    #debug code....
    #else:
        #print('FOUND NO WAN PREFERENCES!!!')
    

    #need to return a dictionary of what settings need to be updated....
    return settingsNeedUpdated

def updateTrafficSettings(dashboard, networkID, settingsNeedUpdated):

    #debug code below....
    activeActive = settingsNeedUpdated["Active-Active"]
    loadBal = settingsNeedUpdated["Load Balancing"]
    protocol = settingsNeedUpdated["Protocol"]
    sourcePort = settingsNeedUpdated["Source Port"]
    sourceCIDR = settingsNeedUpdated["Source"]
    destinationPort = settingsNeedUpdated["Destination Port"]
    destinationCIDR = settingsNeedUpdated["Destination"]
    preferredUplink = settingsNeedUpdated["Preferred Uplinks"]
    #print(f'activeActive: {activeActive}')
    #print(f'loadBal: {loadBal}')
    #print(f'protocol: {protocol}')
    #print(f'sourcePort: {sourcePort}')
    #print(f'sourceCIDR: {sourceCIDR}')
    #print(f'destinationPort: {destinationPort}')
    #print(f'destinationCIDR: {destinationCIDR}')
    #print(f'preferredUplink: {preferredUplink}')

    #update variables if needed to throw into API call below.....
    if activeActive == True:
        activeActive = False
    
    if loadBal == True:
        loadBal = False
    
    if protocol != "any" or protocol != "Any":
        protocol = "Any"
    
    if sourcePort != "any" or sourcePort != "Any":
        sourcePort = "Any"
    
    if sourceCIDR != "any" or sourceCIDR != "Any":
        sourceCIDR = "Any"
    
    if destinationPort != "any" or destinationPort != "Any":
        destinationPort = "Any"
    
    if destinationCIDR != "any" or destinationCIDR != "Any":
        destinationCIDR = "Any"
    
    if preferredUplink != "wan1" or preferredUplink != "WAN1" or preferredUplink != "Wan1":
        preferredUplink = "wan1"
    


    ###Add code here!

    updatedTrafficSettings = dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkSelection(
        networkID,
        activeActiveAutoVpnEnabled = activeActive,
        loadBalancingEnabled = loadBal,
        wanTrafficUplinkPreferences = [{'trafficFilters': [{'type': 'custom', 'value': {'protocol': protocol, 'source': {'port': sourcePort, 'cidr': sourceCIDR}, 'destination': {'port': destinationPort, 'cidr': destinationCIDR}}}], 'preferredUplink': preferredUplink}]
    )

    return updatedTrafficSettings





### END FUNCTIONS FOR PROGRAM ### ******************************************

### START PROGRAM ### ******************************************************

def main():
    #print('Hello World!')

    key = APIKeyGen()

    dashboard = getAPIDashboard(key)

    orgID = orgIDCapture()

    mxDevices = getMXAppliances(dashboard, orgID)

    updateCounter = 0

    for mxDevice in mxDevices:
        name = getMXDeviceName(mxDevice)
        
        #check for tags here and if tag contains DC in it then we continue to next device....
        #not allowed to mess with DC networks....
        tags = getMXDeviceTags(mxDevice)

        #make sure the tags don't contain DC.... if they do we found a DC network....
        if any('DC' in string for string in tags):
            #found a DC network....
            #debug code??
            print(f'found a DC network: {name}\ntags: {tags}\ncontinuing on to next device/network....')
            sleep(3)
            continue

        netID = getNetworkID(mxDevice)
        deviceTrafficSettings = getDeviceTrafficSettingSelections(dashboard, netID)
        #debug code....
        #print(f'\n\ndeviceTrafficSettings for network {name}:\n{deviceTrafficSettings}\n\n')
        settingsNeedUpdated = checkIfSettingsNeedUpdate(deviceTrafficSettings)
        #debug code....
        #print(f'\n\nDo Settings need updated T/F for network {name}: {settingsNeedUpdated}\n\n')
        #check if all settings need update or not.... for use in main....
        result = all(x == False for x in settingsNeedUpdated.values())
        #print(f'are all values false? {result}')
        if result == True:
            #if true no update needs to happen so skip this one go to next mxDevice....
            print(f'device: {name} does not need updated.... \nmoving to next device....')
            sleep(3)
            continue
        
        #THIS IS WHERE THE UPDATE ACTUALLY HAPPENS..... ONLY SHOULD HAPPEN IN ACTUAL FILE!!!!!!!
        updatedSettings = updateTrafficSettings(dashboard, netID, settingsNeedUpdated)
        #debug code
        #print(f'updatedSettings: {updatedSettings}')

        print(f'device: {name} was updated....\nmoving on to next device....')
        updateCounter += 1
        sleep(3)

    print(f'{updateCounter} device(s) was/were updated in Meraki....')

#run the main function.... executes the program....
if __name__ == '__main__':
    main()

### END PROGRAM ### ********************************************************