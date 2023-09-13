
import geopandas as gpd



if __name__ == '__main__':
    #load the full database
    #
    path = r"C:\Users\cda055\OneDrive - UiT Office 365\Impetus\Slushflow_db\NVE_60751B14_1683888916789_12228\NVEData\Skred_Skredhendelse"
    db_file = path + "\Skred_Skredhendelse.shp" # add the file name to the path
    point_data = gpd.read_file(db_file) # read the file as a dataframe

    slushflows = point_data[point_data['skredType'] == 133] # find points in colum skredType with tag 133 which are the recoarded slushflow events
    unique_rows = slushflows['skredID'].nunique() # Find unique ID values for the skredID that can be searched in the two other data files
    rows = slushflows["skredID"] # make a list of the skredIDs so we can search the other database for these events

    #load polygone and release pt data
    polygon_data = gpd.read_file(path + "\Skred_Skredhendelse_UtlopUtlosningOmr.shp")
    subset_poly = polygon_data[polygon_data['skredID'].isin(rows)]

    release_data = gpd.read_file(path + "\Skred_Skredhendelse_UtlopUtlosningPkt.shp")
    subset_release = polygon_data[polygon_data['skredID'].isin(rows)]

    # these lines are used to save data files consisting of only slushflows for loading in QGIS
    subset_release.to_file(path + '\subset_release.shp', driver='ESRI Shapefile')
    subset_poly.to_file(path + '\subset_poly.shp', driver='ESRI Shapefile')
    slushflows.to_file(path + '\slushflows.shp', driver='ESRI Shapefile')


