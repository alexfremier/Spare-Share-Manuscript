# ---------------------------------------------------------------------------
# ApexTargetTool_DataPrep_v1.1.py
# Created on: 2020-08-04
#   (Spyder 3.6)
# Description: Compares input data and preps data for analysis for I and I
# ArcVersion:   ArcGIS Pro, Python27
# --------------------------------------------------------------------------
#
# Import arcpy module
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Overwrites existing data
arcpy.env.overwriteOutput = True

# Setting up the folders
projectFolder = "C:\GIS_Projects\ApexTargets"
projectGDB = projectFolder + "\\" + "ApexTargets_Working.gdb"
rasterFolder = "C:\GIS_Projects\ApexTargets\BaseRasters\Ready"
errorsFolder = "C:\GIS_Projects\ApexTargets\BaseRasters\Errors"
scratchFolder = projectFolder + "\\Scratch"

# Input Files
#inBounds = projectGDB + "\\GAWD_ER"  #country by ecoregions cleaned up GAWD
inBounds = projectGDB + "\\GAUL_ER_2017"  #country by ecoregions cleaned up GAUL

#inLandcover = projectGDB + "\\ESACCI_LC_L4_LCCS_Map_300m_2015_mol" #land cover for snap
inLandcover = projectGDB + "\\ESACCI_LC_L4_LCCS_Map_300m_1992_mol" #land cover for snap


# Set Global Environmental Settings
arcpy.env.scratchWorkspace = scratchFolder
arcpy.env.extent = inBounds
arcpy.env.mask = inBounds
arcpy.env.cellSize = inLandcover
arcpy.env.snapraster = inLandcover

# Output folders and variables
polyBounds = projectGDB + "\\bounds_temp"   #country by ecoregions cleaned

# raster where partial ag is delineated as 0 not 1 (class 30 and 40)
rastHumNat = "C:\GIS_Projects\ApexTargets\BaseRasters\LandCover\\humnat40"

print()
print ("starting the code...")


####################################
###### Create Landcover map  #######
#################################### 
# Run one at global scale - 300m take a while
# Code here works and is only if the base landcover map need updating

print()
print ("reclassing the landcover map...")

# reclass ag to 0, urban to 0, nat to 1  (bare grounds & snow/ice)
remap = RemapRange([[10, 41, 0], [190, 190, 0], [50, 180, 1], [200, 202, 1]])
outHumNat = Reclassify(inLandcover, "VALUE", remap, "NODATA") 
outHumNat.save(rastHumNat)


###################################
####### Create Ensemble Map  ######
###################################
env.workspace = rasterFolder
#
# Delete old ones first
rastEnsembR = "ensb_raw"
rastEnsembA = "ensb_avg"
rastEnsembT2 = "ensb_thr2"
rastEnsembT3 = "ensb_thr3"
if arcpy.Exists(rastEnsembR):
    arcpy.Delete_management(rastEnsembR)
    arcpy.Delete_management(rastEnsembA)
    arcpy.Delete_management(rastEnsembT2)
    arcpy.Delete_management(rastEnsembT3)

# Getting the INTACT rasters
listIntact = arcpy.ListRasters("*", "GRID")
print()
print("working with these rasters... " + str(listIntact))

# First addition, add the rest
print ("working on ensemble surfaces...")
outEnsemb = Plus(listIntact[0], listIntact[1])

for raster in listIntact[2:]:
    outEnsemb = Plus(outEnsemb, raster) 

# Raw ensemble raster (VISUALIZE AGREEMENT AMONG RASTERS)
outEnsemb.save(rastEnsembR)     

# Average ensemble raster (ADD CODE TO FLOOR THIS DATASET)
ensembResult = arcpy.GetRasterProperties_management(outEnsemb, "MAXIMUM")
ensembMax = ensembResult.getOutput(0)
outNorm = Raster(outEnsemb) / float(ensembMax)
outNorm.save(rastEnsembA)

# Theshold ensemble raster  (SET THRESHOLD HERE)
outThresh = Con(outEnsemb, "1", "0", "Value >= 2")
outThresh.save(rastEnsembT2)

# Theshold ensemble raster  (SET THRESHOLD HERE)
outThresh = Con(outEnsemb, "1", "0", "Value >= 3")
outThresh.save(rastEnsembT3)

# Add to listIntact
listBaseRasters = arcpy.ListRasters("*", "GRID")
print (listBaseRasters)



###############################################
###### Correspondence maps  #######
############################################### 
# Comparing natlands to each Intact raster
env.workspace = rasterFolder
listIntact = arcpy.ListRasters("*", "GRID")
listIntact.remove("ensb_avg")
listIntact.remove("ensb_raw")

#maskTemp = projectGDB + "\\bnds_test"
#arcpy.env.extent = maskTemp
#arcpy.env.extent = inBounds
#arcpy.env.mask = inBounds

for intact in listIntact:
    
    # measuring correspondence
    print ("combining LULC with: " + intact)
    outCombine = Combine([rastHumNat, intact])
    combRast = errorsFolder + "\\cb_" + intact
    outCombine.save(combRast)

    # showing the where the errors are 
    print ("selecting error cells: " + intact)
    expression = "(HUMNAT40 = 0) AND (%s = 1)"%intact
    outCon = Con(combRast, inLandcover, "", expression)
    errorRast = errorsFolder + "\\er_" + intact
    outCon.save(errorRast)
    del outCombine


######################################################
####### Create text file for Consistency Check #######
######################################################
file = open(errorsFolder + "\\Consistency_Check.csv","w") 
file.write("Intact Raster, Combine Value, Count (cells), HumNat40 (code), IRaster (code) \n") 
print ()

# search and write all cell values
env.workspace = errorsFolder
listCB = arcpy.ListRasters("cb_*", "GRID")

for cb in listCB:
    print ("writing agreement for each raster:  " + cb)
    
    with arcpy.da.SearchCursor(cb, ['VALUE', 'COUNT', 'HumNat40', cb[3:]]) as cursor:
        for row in cursor:
            print(cb + "," + str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]))
            file.write(cb + "," + str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "\n")
    print ( )  
              

file.close()   
   
#######################################################
####### Create text file for Consistency Errors #######
#######################################################
file = open(errorsFolder + "\\Consistency_Errors.csv","w") 
file.write("Land Cover Class, Count (cells) \n") 
print ()

# search and write all cell values
env.workspace = errorsFolder
listER = arcpy.ListRasters("er_*", "GRID")

for er in listER:
    print ("writing error sheet for each raster:  " + er)
    
    with arcpy.da.SearchCursor(er, ['VALUE', 'COUNT']) as cursor:
        for row in cursor:
            print(er + "," + str(row[0]) + "," + str(row[1]))
            file.write(er + "," + str(row[0]) + "," + str(row[1]) + "\n")
    print ( )  
              

file.close()   
     


##################################
###### Clean the workspace #######
##################################
print()
print ("cleaning up ...")

env.workspace = projectFolder

listTiffs = arcpy.ListRasters("*", "TIF")
for tif in listTiffs:
    arcpy.Delete_management(tif)
    print (tif)