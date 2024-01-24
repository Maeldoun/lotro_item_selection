# Make sure there is an items.xml and progressions.xml
# in the data subdirectory. Then this will create the
# ItemDatabase.csv which main.py uses to generat item lists
import item_parsing

item_parsing.main()
import stat_curve_parsing

stat_curve_parsing.main()
import database_creation
