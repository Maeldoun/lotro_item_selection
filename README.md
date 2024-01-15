Purpose: 
The purpose of this program is to allow the user to find the best items available considering the item slot and essence values

Setup (main.exe):
* If you trust me, then you can just clone down the 150ItemInfo.ods and the main.exe.
* Run the main.exe and tell windows you're not scared to run it.

Setup (Python):
* Clone this repository
* Open a cmd prompt or powershell prompt
* cd to the cloned repository
* Install Python (3.11 is what I used)
* Optionally create a Virtual Environment using the requirments txt file.
  * python -m venv .venv
  * activate the environment
    * .venv\Scripts\activate.bat
* install the required packages
  * if necessary, change directory to the top of the cloned folder
  * pip install -r requirements.txt

Use:
* Update the 150ItemInfo.ods file's "Control" sheet with the desired class, stats, equipment slot, etc
* Run the python script from your virtual environment (assming you're still in an active environment)
  * python main.py
* You should get a screen that shows the item and a new file should be created in the current directory called top_items.csv.
* You can review that csv file for more details.

NOTE: the 150ItemInfo.ods was given to me, and I can't verify it's validity.

NOTE: the csv that is generated will create if it doesn't exist or append to a created existing file.

TODO: automate item lists

TODO: make a gui, so the spreadsheet doesn't control it
