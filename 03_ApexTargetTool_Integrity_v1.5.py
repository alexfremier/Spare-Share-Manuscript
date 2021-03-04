# ---------------------------------------------------------------------------
# ApexTargetTool_Integrity_v1.3.py
# Created on: 2020-08-04
#   (Spyder 3.6)
# Description: Calculates integrity for agricultural lands
#              Count of cells above a treshold of mean natural adjacent
# ArcVersion:   ArcGIS Pro, Python27
# --------------------------------------------------------------------------
#
# Import arcpy module
import arcpy
from arcpy import env
from arcpy.sa import *
import numpy

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Check out the ArcGIS Image Analyst extension license
arcpy.CheckOutExtension("ImageAnalyst")

# Overwrites existing data
arcpy.env.overwriteOutput = True

# Turn off log processing operations (increase speed)
arcpy.SetLogHistory(False)

# Setting up the folders and files
projectFolder = "C:\GIS_Projects\ApexTargets"
projectGDB = projectFolder + "\\" + "ApexTargets_Working.gdb"
focalFolder = projectFolder + "\\BaseRasters\\Focal"
scratchFolder = projectFolder + "\\Scratch"

# Input Files
inBounds = projectGDB + "\\Apex_Intactness_CER"  # Intactness file to add to
#inLandcover = projectGDB + "\\ESACCI_LC_L4_LCCS_Map_300m_1992_mol" 
inLandcover = projectGDB + "\\ESACCI_LC_L4_LCCS_Map_300m_2015_mol" #land cover for snap

# Set Global Environmental Settings
arcpy.env.workspace = projectFolder
arcpy.env.scratchWorkspace = scratchFolder
arcpy.env.extent = inBounds
arcpy.env.mask = inBounds
arcpy.env.cellsize = inLandcover
arcpy.env.snapraster = inLandcover

# Output variables and such
cellResult = arcpy.GetRasterProperties_management(inLandcover, "CELLSIZEX")
#Get the elevation standard deviation value from geoprocessing result object
cellsize = cellResult.getOutput(0)
halfcellsize = float(cellsize) / 2
#print ("cell size is: " + cellsize)

polyBounds = projectGDB + "\\bounds_temp"
##### CHECK THIS TO MAKE SURE WORKING WITH EG OR C.ER
Name_PolyBin = "CtryEco" #country ecoregions
#Name_PolyBin = "ECO_NAME" #ecoregions
#Name_PolyBin = "Iso3_Code" #countries

# raster where partial ag is delineated as ag (class 30 and 40)
rastHumNat = "C:\GIS_Projects\ApexTargets\BaseRasters\LandCover\\humnat40"

# raster of only ag land (including 30 and 40)
#rastAgMask = "C:\GIS_Projects\ApexTargets\BaseRasters\LandCover\\ag40"

# raster of only ag land (including 30 and 40)
#rastHumMask = "C:\GIS_Projects\ApexTargets\BaseRasters\LandCover\\hum40"

# raster of ag lands as 0, 30 as 0.25 and 40 as 0.75. Natural as 1
rastNatGrity = "C:\GIS_Projects\ApexTargets\BaseRasters\LandCover\\NatGrity"

print()
print ("starting the code...")

#Create a new boundary file but delete old one first
if arcpy.Exists(polyBounds):
    arcpy.Delete_management(polyBounds)

arcpy.Copy_management(inBounds, polyBounds)


####################################
###### Create Landcover map  #######
####################################
# Run one at global scale - 300m take a while
# Code here works and is only if the base landcover map need updating

# print()
# print ("reclassing the landcover map...")

# ### reclass ag to 0 for mask
# remap = RemapRange([[10, 41, 0]])
# outAgMask = Reclassify(inLandcover, "VALUE", remap, "NODATA")
# outAgMask.save(rastAgMask)

# ## reclass hum to 0 for mask
# remap = RemapRange([[10, 41, 0], [190, 190, 0]])
# outAgMask = Reclassify(inLandcover, "VALUE", remap, "NODATA")
# outAgMask.save(rastHumMask)

# # reclass ag to 0, urban to 0, mosaic30 to 0.25 and mosaic to 0.75, nat to 1
# remap = RemapRange([[10, 21, 0], [30, 30, 25], [40, 40, 75], [190, 190, 0], [50, 180, 100], [200, 202, 100]])
# outNatGrity = Reclassify(inLandcover, "VALUE", remap, "NODATA")
# outNatGrityFl = Divide(outNatGrity, 100.00)
# outNatGrityFl.save(rastNatGrity)


# #####################################
# ####### Calculating Integrity #######
# #####################################
arcpy.env.workspace = focalFolder

print()
print ("calculating the focal statistics...")

# masking for when playing with the code
#arcpy.env.extent = projectGDB + "\\bnds_test"
#arcpy.env.mask = projectGDB + "\\bnds_test"


# perform focal stats (set up for multipl radii but not implemented)
def focal ( radius ):
    
    # Integrity raster for each radii
    rastFocal = focalFolder + "\\FocI" + str(radius)
    
    # Converting radius to cell units
    cellradius = radius/ float(cellsize)
    
    # Focal Statistics - Mean and Annulus applied here
    outFocalMean = FocalStatistics(rastNatGrity, NbrAnnulus(0.5, cellradius, "CELl"), "MEAN", "DATA")

    # Making an integer for analysis (fraction to percent)
    outFocalTim = Times(outFocalMean, 100)
    outFocalInt = Int(outFocalTim)
    outFocalInt.save(rastFocal)
    
    return


# function: zonal statistics - no masking
def fstats ( radius, thresh ):

    num = str(round(thresh, 1))
    
    # Integrity raster for each radii
    rastFocal = focalFolder + "\\FocI" + str(radius)
    
    # Conditioning out all cell below the threshold
    outCon = Con(Raster(rastFocal) > thresh, 1, 0)

    # Calculating zonal stats and joining back to spatial data
    outTable = projectGDB + "\\" + "integrity_zonalstatstable"

    outZSaT = ZonalStatisticsAsTable(polyBounds, Name_PolyBin, outCon, outTable, "DATA", "MEAN", "CURRENT_SLICE")
    tabJoin = arcpy.JoinField_management(polyBounds, Name_PolyBin, outTable, Name_PolyBin, ["MEAN"])

    # Calculating threshold means
    IRT_Field = "Grit_" + str(radius) + "_" + num[0]
    arcpy.arcpy.AddField_management(polyBounds, IRT_Field, "DOUBLE")
    arcpy.arcpy.CalculateFields_management(polyBounds, "PYTHON3", [[IRT_Field, '!MEAN!']])
    arcpy.DeleteField_management(polyBounds, ["MEAN"])

    return



# function: zonal statistics masking out integrity lands of 1
def fstats_mask ( radius, thresh ):
    
    num = str(round(thresh, 1))
    
    # Integrity raster for each radii
    rastFocal = focalFolder + "\\FocI" + str(radius)

    # keeping on the values in the integrity map above the thresh
    outCon = Con(Raster(rastFocal) > thresh, 1, 0)
    
    # masking out the lands with base integrity of 1
    outMult = Times(outCon, maskHum)

    # Calculating zonal stats and joining back to spatial data
    outTable = projectGDB + "\\" + "integrity_zonalstatstable"
    outZSaT = ZonalStatisticsAsTable(polyBounds, Name_PolyBin, outMult, outTable, "DATA", "MEAN", "CURRENT_SLICE")
    tabJoin = arcpy.JoinField_management(polyBounds, Name_PolyBin, outTable, Name_PolyBin, ["MEAN"])

    # Calculating threshold means
    IRT_Field = "GritM_" + str(radius) + "_" + num[0]
    arcpy.arcpy.AddField_management(polyBounds, IRT_Field, "DOUBLE")
    arcpy.arcpy.CalculateFields_management(polyBounds, "PYTHON3", [[IRT_Field, '!MEAN!']])
    arcpy.DeleteField_management(polyBounds, ["MEAN"])

    return



## running the focal stats for multiple radii
listRadii = [1000]
#listRadii = [1000, 5000, 10000]

#for radius in listRadii:
#    print ("   Radius = " + str(radius))
#    focal (radius)



# Calling the radius function for the different boundaries
thresholds = [10, 20, 30, 50]


# Unmasked Integrity calculation for each polygon
print()
print ("calculating the ecoregion mean statistics... LX Method")

for radius in listRadii:        
    print (" Un-masked zonal stats ")
    print ("    Radius = " + str(radius))
    for thresh in thresholds:
        print ("     threshold: " + str(thresh))
        fstats (radius, thresh )



# Masked Integrity calculation for each polygon
print()
print ("calculating the ecoregion mean statistics... Sk8 Method")


for radius in listRadii:
    print (" Masked zonal stats (Integrity <= 0.75)")
    print ("    Radius = " + str(radius))
    
    #create mask to only summary integrity in human lands
    maskHum = SetNull(Raster(rastHumNat) > 0.75, 1)
    
    for thresh in thresholds:
        print ("     threshold: " + str(thresh))
        fstats_mask (radius, thresh )
        



################################################################
####### Reclassing Intact, Integrity and Export to Excel #######
################################################################
print()
print ("binning the Intact and Integrity data ...")

arcpy.AddField_management(polyBounds, 'II_Class', "DOUBLE")

# > Variable Intactness and 80% Integrity
with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 1.0 AND Grit_1000_1 <= 1.0") as cursor:
    for row in cursor:
        row[0] = 1
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 0.8 AND Grit_1000_1 <= 1.0") as cursor:
    for row in cursor:
        row[0] = 2
        cursor.updateRow(row)
        
with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 0.5 AND Grit_1000_1 <= 1.0") as cursor:
    for row in cursor:
        row[0] = 3
        cursor.updateRow(row)

      
        
# Intactness variable, 80-100% Integrity
with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 1.0 AND Grit_1000_1 <= 0.8") as cursor:
    for row in cursor:
        row[0] = 4
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 0.8 AND Grit_1000_1 <= 0.8") as cursor:
    for row in cursor:
        row[0] = 5
        cursor.updateRow(row)
        
with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 0.5 AND Grit_1000_1 <= 0.8") as cursor:
    for row in cursor:
        row[0] = 6
        cursor.updateRow(row)
        cursor.updateRow(row)


# 100% Integrity
with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 1.0 AND Grit_1000_1 <= 0.5") as cursor:
    for row in cursor:
        row[0] = 7
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 0.8 AND Grit_1000_1 <= 0.5") as cursor:
    for row in cursor:
        row[0] = 8
        cursor.updateRow(row)
        
with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 0.5 AND Grit_1000_1 <= 0.5") as cursor:
    for row in cursor:
        row[0] = 9
        cursor.updateRow(row)
        
with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 <= 0.1 AND Grit_1000_1 <= 0.1") as cursor:
    for row in cursor:
        row[0] = 12
        cursor.updateRow(row)


# Correcting NULL values
with arcpy.da.UpdateCursor(polyBounds, "II_Class", "ensb_thr3 is NULL") as cursor:
    for row in cursor:
        row[0] = 13
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_Class", "Grit_1000_1 is NULL") as cursor:
    for row in cursor:
        row[0] = 14
        cursor.updateRow(row)



################################################################
####### Reclassing Intact, Integrity and Export to Excel #######
################################################################
print()
print ("binning the MASKED Intact and Integrity data ...")

arcpy.AddField_management(polyBounds, 'II_M_Class', "DOUBLE")

# > Variable Intactness and 80% Integrity
with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 1.0 AND GritM_1000_1 <= 1.0") as cursor:
    for row in cursor:
        row[0] = 1
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 0.8 AND GritM_1000_1 <= 1.0") as cursor:
    for row in cursor:
        row[0] = 2
        cursor.updateRow(row)
        
with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 0.5 AND GritM_1000_1 <= 1.0") as cursor:
    for row in cursor:
        row[0] = 3
        cursor.updateRow(row)

      
        
# Intactness variable, 80-100% Integrity
with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 1.0 AND GritM_1000_1 <= 0.8") as cursor:
    for row in cursor:
        row[0] = 4
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 0.8 AND GritM_1000_1 <= 0.8") as cursor:
    for row in cursor:
        row[0] = 5
        cursor.updateRow(row)
        
with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 0.5 AND GritM_1000_1 <= 0.8") as cursor:
    for row in cursor:
        row[0] = 6
        cursor.updateRow(row)
        cursor.updateRow(row)


# 100% Integrity
with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 1.0 AND GritM_1000_1 <= 0.5") as cursor:
    for row in cursor:
        row[0] = 7
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 0.8 AND GritM_1000_1 <= 0.5") as cursor:
    for row in cursor:
        row[0] = 8
        cursor.updateRow(row)
        
with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 0.5 AND GritM_1000_1 <= 0.5") as cursor:
    for row in cursor:
        row[0] = 9
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 <= 0.1 AND GritM_1000_1 <= 0.1") as cursor:
    for row in cursor:
        row[0] = 9
        cursor.updateRow(row)
        

# Correcting NULL values
with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "ensb_thr3 is NULL") as cursor:
    for row in cursor:
        row[0] = 13
        cursor.updateRow(row)

with arcpy.da.UpdateCursor(polyBounds, "II_M_Class", "GritM_1000_1 is NULL") as cursor:
    for row in cursor:
        row[0] = 14
        cursor.updateRow(row)



################################################################
####### Calculating Deficits in Intact, Integrity ###### #######
################################################################
print()
print ("calculting Deficits in Intact and Integrity ...")

#unmasked deficit calculation
arcpy.AddField_management(polyBounds, 'Intact_Def', "DOUBLE")
fields = ['ensb_thr3', 'Intact_Def']
          
with arcpy.da.UpdateCursor(polyBounds, fields) as cursor:
    # Update field to calculate deficit
    for row in cursor:
        if (row[0] is None):
            row[1] = None
        else:
            row[1] = row[0] - 0.5
        
        cursor.updateRow(row) 


#masked deficit calculation
arcpy.AddField_management(polyBounds, 'Integrity_Def', "DOUBLE")
fields = ['Grit_1000_1', 'Integrity_Def']

with arcpy.da.UpdateCursor(polyBounds, fields) as cursor:
    # Update field to calculate deficit
    for row in cursor:
        if (row[0] is None):
            row[1] = None
        else:
            row[1] = row[0] - 0.9
            
        cursor.updateRow(row) 
        
#masked deficit calculation
arcpy.AddField_management(polyBounds, 'IntegrityM_Def', "DOUBLE")
fields = ['GritM_1000_1', 'IntegrityM_Def']

with arcpy.da.UpdateCursor(polyBounds, fields) as cursor:
    # Update field to calculate deficit
    for row in cursor:
        if (row[0] is None):
            row[1] = None
        else:
            row[1] = row[0] - 0.9
        
        cursor.updateRow(row) 



####################################
###### Creating Output Files #######
####################################
print()
print ("copying output files ...")

# Rename the working field into the final file
polyFinal = projectGDB + "\\Apex2021_II_CER"

# Adding the Area column in Hectares to the file
arcpy.AddGeometryAttributes_management(polyBounds, 'AREA_GEODESIC', '', 'HECTARES')
 
arcpy.Copy_management(polyBounds, polyFinal)

# Export to Excel
arcpy.TableToExcel_conversion(polyBounds, projectFolder + "\\OutputFiles\\Apex2021_II_CER.xlsx")



##################################
###### Clean the workspace #######
##################################
print()
print ("cleaning up ...")

#arcpy.Delete_management(outTable)

arcpy.env.workspace = scratchFolder

listTiffs = arcpy.ListRasters("*", "TIF")
for tif in listTiffs:
    arcpy.Delete_management(tif)
    print (tif)

listCRFs = arcpy.ListWorkspaces("*.crf")
for crf in listCRFs:
    arcpy.Delete_management(crf)
    print (crf)
