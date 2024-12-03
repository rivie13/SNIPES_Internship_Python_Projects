11/14/2024
getMeraki_WAN_Data_Details
README.txt


Hello and thank you for using the getMeraki_WAN_Data_Details application!

NOTE: SOMETIMES WHEN RUNNING A SECURITY CHECK WILL COME UP... MAKE SURE TO PRESS 'ALLOW ONCE' EVERY TIME IT POPS UP TO ALLOW THE PROGRAM TO RUN..... BLOCKING THE PROGRAM OR WAITING TO LONG WILL CAUSE IT TO NOT WORK...


BEFORE USING THE PROGRAM!!!!
    - Make sure that you have the latest version of python installed on your machine!!!!!!
    - Make sure that you install the required libraries/packages that are needed to run the program!!!!!!
    - Make sure to update API key in variableData.py file!!!! if not you will get an error!!!!


To use:
1. double click the executable file (the floppy disk looking icon)

2. wait about 1 to 2 minutes for the program to actually start...

3. when the GUI pops up, put in as many stores as you want to look up, putting in an entry that is
not a 4 digit number will cause an error screen to pop up.... put in one store at a time, make sure to hit
insert store button after each store to make it show up on the list....

4. after putting in all stores you want to look up hit the 'exit app' button
wait another 1 to 2 minutes for meraki to go look up the data you want
as long as you put in at least 1 valid store to look up a report will be generated and
will tell you how many stores are inside the report...
if you did not put in an accurate store number, the program will tell you that no report was generated
for 0 stores....

5. after program closes, back in the folder there should be an excel file called 'Meraki Device Data Details.xlsx'.... open that file, your data will be inside in an organized manner....
note: all data in excel file is shown in MB will add units to data to make it more clear....
******************************************************************************************************************

Make sure to update the API key that is in the variableData file, if you don't then there could be errors

Sometimes for unkown reasons a 400 level error will occur when running the test usually along the lines of
'invalid API key' or 'unavailable resource' (not exactly like this but something along those lines...)
If these errors occcur and you are sure you have a correct API key in the file, then you need to retry the program
which may let it work or wait a bit and try again. I believe these errors may occur from making too many requests
in a short amount of time but I am not fully sure.


******************************************************************************************************************
if you run into errors:
first, wait for the program to close out but before that make sure to look at the command prompt
screen and see what the error is, then try to run the program again and see if you get the same error....
the command prompt screen closes quickly so make sure to look and see before then...


depending on the error and how many times said error shows up, you will not be able to use the executable anymore....
if the Meraki API changes how the specific call executes, then that would probably
change the way that the program works which means it would need to be maintained to make
it work again. Luckily, the terminal should show you what that error is and you should be able to
use vscode to fix the code, test it again, then create another executable once the problem is fixed....

******************************************************************************************************************
to create executable:
open program that executable is based off of in vscode (getMeraki_WAN_Data_Details.py)
open the terminal...
change directory to source code with command: cd 'source code' (include the single quotes!!)
RUN THE PROGRAM TO MAKE SURE IT WORKS PROPERLY.
if the program runs properly then type the following command in the terminal:
     pyinstaller --onefile --paths='C:\Users\Riviera.Sperduto\OneDrive - JAKO ENTERPRISES LTD\Desktop\Meraki_Python_Programs\getMeraki_WAN_Data_Details_V2_0\source code\variableData.py' getMeraki_WAN_Data_Details.py

    --onefile : makes a single executable file for the program
    --paths= "" : makes sure to look in the directory/file for the specific imports or other dependencies you need.....
            this path is to the import file that had trouble connecting to the executable.....
    
    your --paths="" : YOUR PATH WILL BE DIFFERENT MAKE SURE TO GET YOUR PROPER PATH...
        ^^^ paths="" : the path where variable data file lives.... should be in same directory as the getMeraki_WAN_Data_Details.py file..... if you right click on variableData.py and hit copy as path you will get the information you need!!!


If done correctly you should be able to look inside the getMeraki_WAN_Data_Details directory with file explorer
you should see that there are new files and folders.... go to the newly created dist directory, inside you should see your executable file....

move the executable to wherever you want to.... I put mine into another folder on my desktop....
    meraki logs and excel spreadsheet will be generated in same file that the executable lives in....


I have included the source code and the tests for the program in this folder....
you can edit/add things to both if needed or wanted.
******************************************************************************************************************
TO RUN THE TESTS:

1. open vscode and open the folder getMeraki_WAN_Data_Details_V1_0 (might be different version now!)
2. open a terminal and type in the command: cd 'source code'      (include the single quotes!)
3. type in the command: python -m pytest test_getMeraki_WAN_Data_Details -s
4. Wait for the tests to complete
5. If successful run, congrats program is good, if not fix the errors.

Remember new tests can be added if you decide to add more functionality later!!
******************************************************************************************************************TTO RUN THE PROGRAM MANUALLY:

1. open vscode click File menu tab and open the folder getMeraki_WAN_Data_Details_V1_0 (might be different version now!)
2. open a terminal and type in the command: cd 'source code'      (include the single quotes!)
3. type in the command: python updateMeraki_SDWAN_details.py
4. wait for program to run successfully or not.
