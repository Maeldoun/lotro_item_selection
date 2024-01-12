# %% importng packages
import duckdb as ddb
import pandas as pd

# %% set controling variables
df_control = pd.read_excel(
    r".\150ItemInfo.ods",
    sheet_name="Control",
)
l_class = df_control.iloc[0]["L_CLASS"]
equipment_slot = df_control.iloc[0]["EquipSlot"]
essence_tier = df_control.iloc[0]["EssenceTier"]
count_items_to_show = df_control.iloc[0]["count_items_to_show"]
stats = df_control["Stat"].loc[df_control["Evaluate"] == 1].values.tolist()
query_stats = " ".join([str(elem) + " + " for elem in stats])[:-2]

# %% build data dfs
maw = [3, 4, 5]  # ["Might", "Agility", "Will"]
not_maw = [i for i in range(32) if i not in maw]
df_idb_maw = pd.read_excel(
    r".\150ItemInfo.ods",
    sheet_name="IDB",
    usecols=["ItemID", "Might", "Agility", "Will", "EquipSlot"],
).fillna(0)
df_idb_not_maw = pd.read_excel(
    r".\150ItemInfo.ods",
    sheet_name="IDB",
    usecols=not_maw,
).fillna(0)
df_et = pd.read_excel(
    r".\150ItemInfo.ods",
    sheet_name="EssenceTiers",
    usecols=["Stat", essence_tier],
).rename(columns={essence_tier: "Value"})
df_msd = pd.read_excel(
    r".\150ItemInfo.ods",
    sheet_name="MainStatDerivations",
)
# %% Filter initals DFs according to the controlling variables
df_msd = df_msd.loc[df_msd["L_CLASS"] == l_class]
df_idb_maw = df_idb_maw.loc[df_idb_maw["EquipSlot"] == equipment_slot]
df_idb_not_maw = df_idb_not_maw.loc[df_idb_not_maw["EquipSlot"] == equipment_slot]

# %% preparing item list to explode the mainstat into derrivative stats
df_idb_unpivot = pd.melt(
    df_idb_maw,
    id_vars="ItemID",
    value_vars=[
        "Might",
        "Agility",
        "Will",
    ],
    var_name="Mainstat",
)

# %% exploding the mainstat into derrivative stats
df_derived_stats = ddb.sql(
    """
    SELECT i.ItemID
        ,i.value * msd.Block as Block
        ,i.value * msd.Critical_Rating as Critical_Rating
        ,i.value * msd.Evade as Evade
        ,i.value * msd.Finesse as Finesse
        ,i.value * msd.Outgoing_Healing as Outgoing_Healing
        ,i.value * msd.Parry as Parry
        ,i.value * msd.Physical_Mastery as Physical_Mastery
        ,i.value * msd.Physical_Mitigation as Physical_Mitigation
        ,i.value * msd.Resistance as Resistance
        ,i.value * msd.Tactical_Mastery as Tactical_Mastery
        ,i.value * msd.Tactical_Mitigation as Tactical_Mitigation
    FROM df_idb_unpivot as i 
    JOIN df_msd as msd on i.Mainstat = msd.Mainstat
    """
)

# %% unifying main stat derrivatives and item stats
df_stats_sum = ddb.sql(
    """
    SELECT i.ItemID
        ,i.Name
        ,ifnull(i.Armour, 0) as Armour
        ,ifnull(i.Fate, 0) as Fate
        ,ifnull(i.Vitality, 0) as Vitality
        ,sum(ifnull(i.Physical_Mastery_Rating, 0) + ds.Physical_Mastery) as Physical_Mastery_Rating
        ,sum(ifnull(i.Tactical_Mastery_Rating, 0) + ds.Tactical_Mastery) as Tactical_Mastery_Rating
        ,sum(ifnull(i.Physical_Mitigation, 0) + ds.Physical_Mitigation) as Physical_Mitigation
        ,sum(ifnull(i.Tactical_Mitigation, 0) + ds.Tactical_Mitigation) as Tactical_Mitigation
        ,sum(ifnull(i.Critical_Rating, 0) + ds.Critical_Rating) as Critical_Rating
        ,ifnull(i.Critical_Defence, 0) as Critical_Defense
        ,ifnull(i.Finesse_Rating, 0) as Finesse_Rating
        ,sum(ifnull(i.Block_Rating, 0) + ds.Block) as Block_Rating
        ,sum(ifnull(i.Parry_Rating, 0) + ds.Parry) as Parry_Rating
        ,sum(ifnull(i.Evade_Rating, 0) + ds.Evade) as Evade_Rating
        ,sum(ifnull(i.Outgoing_Healing_Rating, 0) + ds.Outgoing_Healing) as Outgoing_Healing_Rating
        ,ifnull(i.Incoming_Healing_Rating, 0) as Incoming_Healing_Rating
        ,sum(ifnull(i.Resistance_Rating, 0) + ds.Resistance) as Resistance_Rating
        ,ifnull(i.Maximum_Morale, 0) as Maximum_Moral
        ,ifnull(i.Maximum_Power, 0) as Maximum_Power
        ,ifnull(i.PrimaryEssence, 0) as Primary_Essence
        ,ifnull(i.VitalEssence, 0) as Vital_Essence
        ,ifnull(i.BasicEssence, 0) as Basic_Essence
        ,ifnull(i.DPS, 0) as DPS
        ,ifnull(i.minDamage, 0) as minDamage
        ,ifnull(i.maxDamage, 0) as maxDamage
        ,ifnull(i.Itemlvl, 0) as Itemlvl
        ,i.Quality
        ,i.EquipSlot
    FROM df_derived_stats ds
    JOIN df_idb_not_maw i on i.ItemID = ds.ItemID
    GROUP BY i.ItemID
        ,i.Name
        ,i.Armour
        ,i.Fate
        ,i.Vitality
        ,i.Critical_Defence
        ,i.Finesse_Rating
        ,i.Critical_Defence
        ,i.Finesse_Rating
        ,i.Critical_Defence
        ,i.Finesse_Rating
        ,i.Incoming_Healing_Rating
        ,i.Maximum_Morale
        ,i.Maximum_Power
        ,i.PrimaryEssence
        ,i.VitalEssence
        ,i.BasicEssence
        ,i.DPS
        ,i.minDamage
        ,i.maxDamage
        ,i.Itemlvl
        ,i.Quality
        ,i.EquipSlot
    """
)

# %% calculating essence values from unified items stats
df_ev = ddb.sql(
    """
    SELECT ss.*
        ,ss.Physical_Mastery_Rating / (SELECT Value FROM df_et where Stat = 'Physical_Mastery_Rating') as Physical_Mastery_Rating_Essence_Value
        ,ss.Tactical_Mastery_Rating / (SELECT Value FROM df_et where Stat = 'Tactical_Mastery_Rating') as Tactical_Mastery_Rating_Essence_Value
        ,ss.Physical_Mitigation / (SELECT Value FROM df_et where Stat = 'Physical_Mitigation') as Physical_Mitigation_Essence_Value
        ,ss.Tactical_Mitigation / (SELECT Value FROM df_et where Stat = 'Tactical_Mitigation') as Tactical_Mitigation_Essence_Value
        ,ss.Critical_Rating / (SELECT Value FROM df_et where Stat = 'Critical_Rating') as Critical_Rating_Essence_Value
        ,ss.Critical_Defense / (SELECT Value FROM df_et where Stat = 'Critical_Defense') as Critical_Defense_Essence_Value
        ,ss.Finesse_Rating / (SELECT Value FROM df_et where Stat = 'Finesse_Rating') as Finesse_Rating_Essence_Value
        ,ss.Block_Rating / (SELECT Value FROM df_et where Stat = 'Block_Rating') as Block_Rating_Essence_Value
        ,ss.Parry_Rating / (SELECT Value FROM df_et where Stat = 'Parry_Rating') as Parry_Rating_Essence_Value
        ,ss.Evade_Rating / (SELECT Value FROM df_et where Stat = 'Evade_Rating') as Evade_Rating_Essence_Value
        ,ss.Outgoing_Healing_Rating / (SELECT Value FROM df_et where Stat = 'Outgoing_Healing_Rating') as Outgoing_Healing_Rating_Essence_Value
        ,ss.Incoming_Healing_Rating / (SELECT Value FROM df_et where Stat = 'Incoming_Healing_Rating') as Incoming_Healing_Rating_Essence_Value
        ,ss.Resistance_Rating / (SELECT Value FROM df_et where Stat = 'Resistance_Rating') as Resistance_Rating_Essence_Value
    FROM df_stats_sum ss
    """
)

# %% acquiring total essence values
df_final = ddb.sql(
    f"""
    SELECT *
        ,Primary_Essence + Vital_Essence + Basic_Essence + Physical_Mastery_Rating_Essence_Value + Tactical_Mastery_Rating_Essence_Value + Physical_Mitigation_Essence_Value + Tactical_Mitigation_Essence_Value + Critical_Rating_Essence_Value + Critical_Defense_Essence_Value + Finesse_Rating_Essence_Value + Block_Rating_Essence_Value + Parry_Rating_Essence_Value + Evade_Rating_Essence_Value + Outgoing_Healing_Rating_Essence_Value + Incoming_Healing_Rating_Essence_Value + Resistance_Rating_Essence_Value as Total_Essence_Value
        ,Primary_Essence + Vital_Essence + Basic_Essence + {query_stats} as Total_Selected_Essence_Value
    FROM df_ev 
    ORDER BY Total_Selected_Essence_Value desc
    LIMIT {count_items_to_show}
    """
)
# df_final.show(max_width=1000)
# %% send to file
print(df_final)
df_final.to_csv(r".\top_items.csv")

# %%
