Purpose: 
The purpose of this program is to allow the user to find the best items available considering the item slot and essence values

Setup:
* Clone this repository
* Open a cmd prompt or powershell prompt
* cd to the cloned repository
* Install Python (3.11 is what I used)
* Optionally create a Virtual Environment using the requirments txt file.
  * python -m venv .venv
  * activate the environment
    * .venv\Scripts\activate.bat
* install the required packages
  * pip install -r requirements.txt

Use:
* Update the 150ItemInfo.ods file's "Control" sheet with the desired class, stats, equipment slot, etc
* Run the python script from your virtual environment (assming you're still in an active environment)
*   python main.py
* You should get a screen that shows the item and a new file should be created in the current directory called top_items.csv.
* You can review that csv file for more details.
