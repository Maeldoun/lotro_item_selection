# %%
from pathlib import Path

import duckdb as ddb
import pandas as pd

ILVL_FILTER = 500
post_xml_items = Path("./data/PostXMLItems.csv")
scaling_stats = Path("./data/ScalingStatValues.csv")
item_db_output = Path("./data/ItemDatabase.csv")
# %%
df_item_data = pd.read_csv(
    post_xml_items,
    usecols=[
        "itemId",
        "iLvl",
        "Vitality Scaling",
        "Will Scaling",
        "Agility Scaling",
        "Might Scaling",
        "Fate Scaling",
        "Maximum Morale Scaling",
        "Maximum Power Scaling",
        "Finesse Scaling",
        "Critical Rating Scaling",
        "Outgoing Healing Rating Scaling",
        "Incoming Healing Rating Scaling",
        "Tactical Mastery Scaling",
        "Physical Mastery Scaling",
        "Tactical Mitigation Scaling",
        "Physical Mitigation Scaling",
        "Block Rating Scaling",
        "Parry Rating Scaling",
        "Evade Rating Scaling",
        "Critical Defense Scaling",
        "Resistance Rating Scaling",
        "Armour Scaling",
        "Out of Combat Power Regen Scaling",
        "In Combat Power Regen Scaling",
        "In Combat Morale Regen Scaling",
        "Out of Combat Morale Regen Scaling",
    ],
)

# %%
df_unpivot_item = ddb.sql(
    """
    SELECT * 
    FROM (
        UNPIVOT df_item_data
        ON COLUMNS (* EXCLUDE (itemId, iLvl))
        INTO
            NAME stat_name
            VALUE stat_scaling_id
        )
    WHERE stat_scaling_id > 0 
    """
)


# %%

df_scaling_stat_values = pd.read_csv(scaling_stats)
df_scaling_stat_values = df_scaling_stat_values.loc[
    df_scaling_stat_values["iLvl"].between(ILVL_FILTER, ILVL_FILTER + 50)
]
# %%
df_unpivot_stat = ddb.sql(
    """
    SELECT * 
    FROM (
        UNPIVOT df_scaling_stat_values
        ON COLUMNS (* EXCLUDE (iLvl))
        INTO
            NAME stat_scaling_id
            VALUE stat_value
        )
    WHERE stat_value NOT NULL
        and stat_value > 0
    """
)

# %%
df_unpivot_item_stat = ddb.sql(
    """
    SELECT ui.itemID
        ,ui.stat_name
        ,us.stat_value
    FROM df_unpivot_item ui
    JOIN df_unpivot_stat us on ui.stat_scaling_id = us.stat_scaling_id
        and ui.iLvl = us.iLvl
    """
)
# %%
df_item_stat = ddb.sql(
    """
    PIVOT df_unpivot_item_stat ON stat_name USING SUM(stat_value)
    """
)
# %%
df_item_data = pd.read_csv(
    post_xml_items,
    usecols=[
        "itemId",
        "itemName",
        "slot",
        "quality",
        "armourType",
        "dps",
        "minDamage",
        "maxDamage",
        "weaponType",
        "essenceSlots",
        "iLvl",
    ],
)
# %%
# TODO: add ist."Maximum Moral Scaling" as Maximum_Morale if items get it as a stat in the future
df_item_database = ddb.sql(
    """
    SELECT id.itemId as ItemID
        ,id.itemName as Name
        ,id.iLvl as Itemlvl
        ,CASE 
            WHEN id.weaponType NOT NULL
                THEN id.weaponType
            WHEN id.armourType IS NULL
                THEN id.slot
            ELSE concat(id.armourType, '_', id.slot)
            END  as EquipSlot
        ,id.quality as Quality
        ,LEN(essenceSlots) - LEN(REPLACE(essenceSlots, 'P', '')) as PrimaryEssence
        ,LEN(essenceSlots) - LEN(REPLACE(essenceSlots, 'V', '')) as VitalEssence
        ,LEN(essenceSlots) - LEN(REPLACE(essenceSlots, 'S', '')) as BasicEssence
        ,ist."Armour Scaling" as Armour
        ,ist."Might Scaling" as Might
        ,ist."Agility Scaling" as Agility
        ,ist."Will Scaling" as Will
        ,ist."Vitality Scaling" as Vitality
        ,ist."Fate Scaling" as Fate
        ,ist."Physical Mastery Scaling" as Physical_Mastery_Rating
        ,ist."Tactical Mastery Scaling" as Tactical_Mastery_Rating
        ,ist."Physical Mitigation Scaling" as Physical_Mitigation
        ,ist."Tactical Mitigation Scaling" as Tactical_Mitigation
        ,ist."Critical Rating Scaling" as Critical_Rating
        ,ist."Critical Defense Scaling" as Critical_Defense
        ,ist."Finesse Scaling" as Finesse_Rating
        ,ist."Resistance Rating Scaling" as Resistance_Rating
        ,ist."Block Rating Scaling" as Block_Rating
        ,ist."Parry Rating Scaling" as Parry_Rating
        ,ist."Evade Rating Scaling" as Evade_Rating
        ,ist."Outgoing Healing Rating Scaling" as Outgoing_Healing_Rating
        ,ist."Incoming Healing Rating Scaling" as Incoming_Healing_Rating
        ,id.dps as DPS
        ,id.minDamage as minDamage
        ,id.maxDamage as maxDamage        
        ,ist."Maximum Power Scaling" as Maximum_Power
    FROM df_item_data id
    JOIN df_item_stat ist on id.itemId = ist.itemId
    """
)
# %%
df_final = df_item_database.to_df()
df_final.to_csv(item_db_output)
