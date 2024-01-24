Purpose: 
The purpose of this program is to allow the user to find the best items available considering the item slot and essence values

If using MacOS, you need to remove pywin32 from the requirements.txt.

Setup (main.exe):
* If you trust me, then you can just clone down the data folder and the main.exe.
* Run the main.exe and tell windows you're not scared to run it.

Setup (Python):
* Clone this repository
* Open a cmd prompt or powershell prompt
* cd to the cloned repository
* Install Python (3.11 is what I used, but more recent won't work until packages are upadeted for 3.12)
* Optionally create a Virtual Environment using the requirments txt file.
  * python -m venv .venv
  * activate the environment
    * .venv\Scripts\activate.bat
* install the required packages
  * if necessary, change directory to the top of the cloned folder
  * pip install -r requirements.txt

Use:
* Update the Control.csv with the desired class, stats, equipment slot, etc
* Run the python script from your virtual environment (assming you're still in an active environment)
  * python main.py
* You should get a screen that shows the item and a new file should be created in the current directory called top_items.csv.
* You can review that csv file for more details.

Database Creation:
* If you need to refresh the "database", you can:
  * Download the items.xml and progression.xml files from lotro-companion
  * Make sure the files are saved into the "data" folder
  * Run main_db.py
  * NOTE: if the parsing of the xml files fails, I didn't write the scripts, I got the from Kruelle, and I won't be able to assit in troublshooting immediately

Big thank you to Kruelle for the scripts to parse the .xml files. It saved me a bunch of work to largely rely on his scripts.

NOTE: the csv that is generated will create if it doesn't exist or append to a created existing file.

TODO: make a gui, so the Control.csv doesn't control it
