

import pandas as pd
import geopandas as gpd

if __name__ == '__main__':
    #load the full database
    path = r"C:\Users\deniser\OneDrive - Høgskulen på Vestlandet\artikler\2024 - hans\GIS\Pro\nasjonal skreddatabase\Skred_Skredhendelse"
    
    # add the file name to the path
    db_file = path + "\Skred_Skredhendelse.shp" 
    
    # read the file as a dataframe
    point_data = gpd.read_file(db_file) 

    #define time period
    date1 = pd.to_datetime('2023-08-06')
    date2 = pd.to_datetime('2023-08-12')

    # point_data = the dataframe before it is cut for the dates, point_data_hans is the dataframe after
    point_data_hans = point_data.loc[(point_data['Tidspunkt'] >= date1) & (point_data['Tidspunkt'] <= date2)]

    # find points in column skredType with tag either 140 (Løsmassedskred, uspesifisert), 142 (Flomskred), 143 (Leirskred), 144 (Jordskred) or 145 (Jordskred, uspesifisert)
    losmasseskred_hans = point_data_hans[{'skredType'== 140}, {'skredType'== 142}, {'skredType'== 143}, {'skredType'== 144}, {'skredType'== 145}] 

    # Find unique ID values for the skredID that can be searched in the two other data files
    unique_rows = losmasseskred_hans['skredID'].nunique() 
    
    # make a list of the skredIDs so we can search the other database for these events
    rows = losmasseskred_hans["skredID"] 

    #load polygon and release point data
    polygon_data = gpd.read_file(path + "\Skred_Skredhendelse_UtlopUtlosningOmr.shp")
    subset_poly = polygon_data[polygon_data['skredID'].isin(rows)]

    release_point_data = gpd.read_file(path + "\Skred_Skredhendelse_UtlopUtlosningPkt.shp")
    subset_releasepoint = release_point_data[release_point_data['skredID'].isin(rows)]


    # these lines are used to save data files consisting of only losmasseskred and a given time periode (Hans) for loading in GIS
    subset_releasepoint.to_file(path + '\losmasse_hans_startpunkt.shp', driver='ESRI Shapefile')
    subset_poly.to_file(path + '\losmasse_hans_polygon.shp', driver='ESRI Shapefile')
    losmasseskred_hans.to_file(path + '\losmasseskred_hans.shp', driver='ESRI Shapefile')
