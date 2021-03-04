# ---------------------------------------------------------------------------
# ApexTargetTool_Intactness_v1.2.py
# Created on: 2020-08-04
#   (Spyder 3.6)
# Description: Calculates intactness for all rasters in the folder including
#              multiple ensemble surfaces. Outputs are the ecoregional 
#              intactness and the ensemble surfaces.
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

# Overwrites existing data
arcpy.env.overwriteOutput = True

# Setting up the folders and files
projectFolder = "C:\GIS_Projects\ApexTargets"
rasterFolder = "C:\GIS_Projects\ApexTargets\BaseRasters\Ready"
projectGDB = projectFolder + "\\ApexTargets_Working.gdb"
humnatFolder  = "C:\GIS_Projects\ApexTargets\BaseRasters\LandCover"
outputFolder = projectFolder + "\\OutputFiles"
scratchFolder = projectFolder + "\\Scratch"

### Input Files ###
# country by ecoregions cleaned up
#inBounds = projectGDB + "\\GAWD_ER"  #country by ecoregions cleaned up GAWD
#Name_PolyBin = "CtryEco"
#inBounds = projectGDB + "\\Ecoregions2017"
#Name_PolyBin = "ECO_NAME"
inBounds = projectGDB + "\\GAUL_ER_2017"  #country by ecoregions cleaned
Name_PolyBin = "CtryEco"
#inBounds = projectGDB + "\\GAUL_2015" #countries only
#Name_PolyBin = "Iso3_Code"


# land cover for snap 
#inLandcover = projectGDB + "\\ESACCI_LC_L4_LCCS_Map_300m_1992_mol" 
inLandcover = projectGDB + "\\ESACCI_LC_L4_LCCS_Map_300m_2015_mol" 
# raster where partial ag is delineated as 0 not 1 (class 30 and 40)
rastHumNat = "C:\GIS_Projects\ApexTargets\BaseRasters\LandCover\\humnat40"

# Set Global Environmental Settings
arcpy.env.scratchWorkspace = scratchFolder
arcpy.env.extent = inBounds
arcpy.env.mask = inBounds
arcpy.env.cellsize = inLandcover
arcpy.env.snapraster = inLandcover

# Output variables and such
polyBounds = projectGDB + "\\bounds_temp"   #country-ecoegions or ecoregions cleaned


print()
print ("starting the code...")


#######################################################
####### Calculating Intactness and Area Natural #######
#######################################################
#Local variables
outTable = projectGDB + "\\" + "zonalstatstable"

#Create a new boundary file but delete old one first
if arcpy.Exists(polyBounds):
    arcpy.Delete_management(polyBounds)
arcpy.Copy_management(inBounds, polyBounds)

# Getting %NATURAL area and join back to spatial data
def intact ( raster ):
    fieldArea = raster
        
    outZSaT = ZonalStatisticsAsTable(polyBounds, Name_PolyBin, raster, outTable,\
                                     "DATA", "MEAN", "CURRENT_SLICE")
    tabJoin= arcpy.JoinField_management(polyBounds, Name_PolyBin, outTable, \
                                        Name_PolyBin, ["MEAN"])
    arcpy.AddField_management(polyBounds, fieldArea, "DOUBLE")
    arcpy.CalculateField_management(polyBounds, fieldArea, "!MEAN!", "PYTHON3")
    arcpy.DeleteField_management(polyBounds, ["MEAN"])
      
    arcpy.Delete_management(outTable)

    return

# Running the INTACT function with all the rasters
arcpy.env.workspace = rasterFolder
listBaseRasters = arcpy.ListRasters("*", "GRID")
listBaseRasters = ["csiro68", "ensb_thr3", "ghm1", "hfp4", 'lia']
print (listBaseRasters)

print ()
for lraster in listBaseRasters:
    print ("working on intact file for:  " + lraster)
    intact ( lraster )

# Running INTACT for Natlands file
print ("working on intact file for:  " + rastHumNat[-8:] )
arcpy.env.workspace = humnatFolder

intact ( rastHumNat[-8:] )


########################################
# Exporting the spatial and tabular data
########################################
arcpy.env.workspace = rasterFolder

arcpy.Copy_management(polyBounds, projectGDB + "\\Apex_Intactness_CER")   
arcpy.TableToExcel_conversion(polyBounds, projectFolder + "\\Intactness_CER.xlsx") #cause ArcGIS error which is a bug



#######################################################
####### Calculating Intactness Area for each Layer ####
#######################################################
# Grabbing the rasters
arcpy.env.workspace = rasterFolder
listBaseRasters = arcpy.ListRasters("*", "GRID")
listBaseRasters.remove("ensb_avg")
listBaseRasters.remove("ensb_raw")

# Create text file for output data
file = open(outputFolder + "\\Intactness_CER.csv","w") 
file.write("Raster, Intact (cells), NonIntact (cells), Percent Intact \n") 

print ()

# Function to search and write all cell values
def writefile ( raster ):
   
    with arcpy.da.SearchCursor(raster, ['VALUE', 'COUNT']) as cursor:
        for row in cursor:
            if row[0] == 1:
                Intact = row[1]
            else:
                notIntact = row[1]
            print('Cell Value {} and Cell Count {}'.format(row[0], row[1]))
        
        perIntact = str(round(100 * Intact / (notIntact + Intact),2))
        print("Percent Intact: " + str(perIntact))
        print()
        
        # write the cell counts and %
        file.write(str(raster) + "," + str(Intact) + "," + str(notIntact) + "," + str(perIntact) + "\n")
        
    
    return


# Run function for all INTACT rasters         
for lraster in listBaseRasters:
    print ("writing Intact area for each raster:  " + lraster)
    writefile ( lraster )


# Run function for all HUMNAT raster 
arcpy.env.workspace = humnatFolder      

print ("writing Intact area for each raster:  " + rastHumNat[-8:])
writefile ( rastHumNat[-8:] )

arcpy.env.workspace = rasterFolder 

        
#Get the geoprocessing result object
meanResult = arcpy.GetRasterProperties_management("ensb_avg", "MEAN")
#Get the elevation standard deviation value from geoprocessing result object
ensembMean = meanResult.getOutput(0)
print ("writing Intact area for each raster:  ")
print ("ensb_avg")
ensembMeanStr = str(round(float(ensembMean) * 100, 2))
print ("Percent protected: " + ensembMeanStr)
file.write(str("ensemb_avg") + "," + "NA" + "," + "NA" + "," + ensembMeanStr)


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