######################################
########### DATA SUMMARY #############
######################################
#libraries
library("readxl")
library(reshape2)
library(formattable)
library(htmltools)
library(webshot)
library(dplyr)


# load the data
setwd("C:\\GIS_Projects\\ApexTargets\\OutputFiles")
IIdata <- read_excel("Apex2021_II_ER.xlsx")
df <- data.frame(IIdata)
dim(df)
colnames(df)

# remove rock and ice OR Greenland and Antarctica
df <- subset(df, ECO_NAME != "Rock and Ice")
df <- subset(df, REALM != "Antarctica")
#df <- subset(df, ADM0_NAME != "Greenland")
#df <- subset(df, ADM0_NAME != "Antarctica")
df[df==""]<-NA


#create text file
#setwd("C:\\Users\\Alex Fremier\\OneDrive - Washington State University (email.wsu.edu)\\Manuscripts_ONE\\AND-thropocene\\FinalPush_Reprise")
setwd("C:\\Users\\Alex Fremier\\OneDrive - Washington State University (email.wsu.edu)\\Documents\\GitHub\\SpareShare")
fileName <- "Apex2021_Stats_ER_Integ10.txt"
cat("Intactness and Integrity Stats ER", file=fileName, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")

#replace blank with NA and subset
dfnonNA <- subset(df, !is.na(ensb_thr3))


##############
##INTACTNESS##
##############
cat("##################", file=fileName, append=TRUE, sep="\n")
cat("### Intactness ###", file=fileName, append=TRUE, sep="\n")
cat("##################", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")


cntPoly <- dim(df)[1]
cat(c("Number of polygons: ", cntPoly), file=fileName, append=TRUE, sep="\n")

#replace blank with NA and subset
dfnonNA <- subset(df, !is.na(ensb_thr3))

cntNNA <- dim(dfnonNA)[1]
cat(c("Number of polygons with data: ", cntNNA), file=fileName, append=TRUE, sep="\n")

cntNA = dim(df)[1] - dim(dfnonNA)[1]
cat(c("Number of NA polygons (#): ", cntNA), file=fileName, append=TRUE, sep="\n")

gtArea  <- sum(dfnonNA$AREA_GEO)
cat(c("Area (ha) of footprint for intactness mapping: ", round(gtArea,0)), file=fileName, append=TRUE, sep="\n")


cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Above half-Earth ##", file=fileName, append=TRUE, sep="\n")

dfOverHalfEarth <- subset(dfnonNA, ensb_thr3 > 0.5)
cntOverHalfEarth <- length(dfOverHalfEarth$ensb_thr3)
cat(c("Number of polygons over half Earth: ", cntOverHalfEarth), file=fileName, append=TRUE, sep="\n")

perCEROverHE <- cntOverHalfEarth / cntNNA
cat(c("Fraction of polygons over half Earth: ", round(perCEROverHE,3)), file=fileName, append=TRUE, sep="\n")

sumAreaIntact <- sum(dfnonNA$ensb_thr3 * dfnonNA$AREA_GEO)
cat(c("Area of intact land (ha): ", round(sumAreaIntact,0)), file=fileName, append=TRUE, sep="\n")

perIntact <- sumAreaIntact / gtArea
cat(c("Fraction land area intact: ", round(perIntact,3)), file=fileName, append=TRUE, sep="\n")


cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Above half-Earth (surplus) ##", file=fileName, append=TRUE, sep="\n")

areaHalfEarth <- (dfOverHalfEarth$ensb_thr3 - 0.5) * dfOverHalfEarth$AREA_GEO
sumHalfEarth <- sum(areaHalfEarth)
cat(c("Area (ha) of polygons over half Earth: ", round(sumHalfEarth,0)), file=fileName, append=TRUE, sep="\n")

perOverHalfEarth <- sumHalfEarth / gtArea
cat(c("Fraction land area of polygons over half Earth: ", round(perOverHalfEarth,3)), file=fileName, append=TRUE, sep="\n")


cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Below half-earth ##", file=fileName, append=TRUE, sep="\n")

dfRestDef <- subset(dfnonNA, ensb_thr3 < 0.5)
cntRestDef <- dim(dfRestDef)[1]
cat(c("Number of polygons below half-Earth ", cntRestDef), file=fileName, append=TRUE, sep="\n")

perRestDef <- cntRestDef / cntNNA
cat(c("Fraction of polygons below half-Earth: ", round(perRestDef,3)), file=fileName, append=TRUE, sep="\n")

sumAreaNIntact <- gtArea - sum(dfnonNA$ensb_thr3 * dfnonNA$AREA_GEO)
cat(c("Area of non-intact land (ha): ", round(sumAreaNIntact,0)), file=fileName, append=TRUE, sep="\n")

perNIntact <- sumAreaNIntact / gtArea
cat(c("Fraction land area non-intact: ", round(perNIntact,3)), file=fileName, append=TRUE, sep="\n")


cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Below half-Earth (deficit) ##", file=fileName, append=TRUE, sep="\n")

areaRestDef <- (0.5 - dfRestDef$ensb_thr3) * dfRestDef$AREA_GEO
sumAreaRestDef <- sum(areaRestDef)
cat(c("Area (ha) of polygons below half Earth: ", round(sumAreaRestDef,0)), file=fileName, append=TRUE, sep="\n")

perAreaRestDef <- sumAreaRestDef / gtArea
cat(c("Fraction land area of polygons below half Earth: ", round(perAreaRestDef,3)), file=fileName, append=TRUE, sep="\n")


cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Threatened (Intactness < 10%) ##", file=fileName, append=TRUE, sep="\n")

#dfThreat = subset(dfnonNA, ensb_thr3 <= 0.10 & ensb_thr3 > 0.01)
dfThreat = subset(dfnonNA, ensb_thr3 <= 0.10)
cntThreat = dim(dfThreat)[1]
cat(c("Number of threatened polygons by intactness (#): ", cntThreat), file=fileName, append=TRUE, sep="\n")

perThreat = cntThreat / cntNNA
cat(c("Percentage of threatened polygons by intactness (#): ", round(perThreat,3)), file=fileName, append=TRUE, sep="\n")

areaThreat = sum(dfThreat$AREA_GEO)
cat(c("Area of threatened polygons by intactness (#): ", round(areaThreat,0)), file=fileName, append=TRUE, sep="\n")

perAreaThreat = areaThreat/gtArea
cat(c("Fraction land area of theatened polygons by intactness: ", round(perAreaThreat,3)), file=fileName, append=TRUE, sep="\n")


cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Extinction (Intactness < 1%) ##", file=fileName, append=TRUE, sep="\n")

dfExtinct = subset(dfnonNA, ensb_thr3 <= 0.01)
cntExtinct = dim(dfExtinct)[1]
cat(c("Number of extinct polygons by intactness (#): ", cntExtinct), file=fileName, append=TRUE, sep="\n")

perExtinct = cntExtinct / cntNNA
cat(c("Percentage of extinct polygons by intactness (#): ", round(perExtinct,3)), file=fileName, append=TRUE, sep="\n")

areaExtinct = sum(dfExtinct$AREA_GEO)
cat(c("Area of extinct polygons by intactness (#): ", round(areaExtinct,0)), file=fileName, append=TRUE, sep="\n")

perAreaExtinct = areaExtinct /gtArea
cat(c("Fraction land area of extinct polygons by intactness: ", round(perAreaExtinct,3)), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")


####################################
## Table of biome intactness ######
###################################

#summarize by biome
meta_biome <- df %>%
  filter(!is.na(ensb_thr3)) %>%
  filter(BIOME_NAME != "N/A") %>%
  group_by(BIOME_NAME) %>%
  summarize(BIOME_COUNT = n(),
            BIOME_AREA = sum(AREA_GEO, na.rm = TRUE))

#summarize by intacness by biome
meta_intact <- df %>%
  filter(!is.na(ensb_thr3)) %>%
  filter(BIOME_NAME != "N/A")%>%
  filter(ensb_thr3 >= 0.5) %>%
  group_by(BIOME_NAME) %>%
  summarize(INTACT_COUNT = n(),
            INTACT_AREA = sum(AREA_GEO, na.rm = TRUE))

dfbiome <- full_join(meta_biome, meta_intact,by = "BIOME_NAME")

dfbiome$BIOME_AREA <- dfbiome$BIOME_AREA / 1000000
dfbiome$INTACT_AREA <- dfbiome$INTACT_AREA / 1000000

dfbiome$Intact_AreaPer <- dfbiome$INTACT_AREA / dfbiome$BIOME_AREA
dfbiome$Intact_ERPer <- dfbiome$INTACT_COUNT/ dfbiome$BIOME_COUNT

dftable <- arrange(dfbiome, desc(Intact_ERPer))

colnames(dftable) <- c("Biome_Name", "Ecoregion Count (#)", "Area (M ha)", "Ecoregion Intact (#)",
                       "Intact Area (M ha)", "Intact % (by area)", "Intact % (by ecoregion)")



# write table of biome intactness
FT <- formattable(dftable,
                  align = c("l", rep("r", NCOL(dftable) - 1)),
                  list(`Summary Statistics by Biome` =
                         formatter("span", style = ~ style(color = "grey", font.weight = "bold")),
                         'Biome Area (M ha)' = formatter("span",
                                                             x ~ round(x , digits = 0)),
                         'Intact % (by ecoregion)' = formatter("span",
                                                             x ~ percent(x , digits = 1)),
                         'Intact Area (M ha)' = formatter("span",
                                                             x ~ round(x , digits = 0)),
                         'Intact % (by area)' = formatter("span",
                                                  x ~ percent(x , digits = 1))

                  ))
FT

write.csv(dftable, "Apex2021_Biome.csv", row.names = FALSE)

# Exporting the table as a figure
export_formattable <- function(f, file, width = "100%", height = NULL, 
                               background = "white", delay = 0.2)
{
  w <- as.htmlwidget(f, width = width, height = height)
  path <- html_print(w, background = background, viewer = NULL)
  url <- paste0("file:///", gsub("\\\\", "/", normalizePath(path)))
  webshot(url,
          file = file,
          selector = ".formattable_widget",
          delay = delay)
}

export_formattable(FT,"Apex2021_Biome.png")



##############
##INTEGRITY##
##############

cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("##################", file=fileName, append=TRUE, sep="\n")
cat("### Integrity ####", file=fileName, append=TRUE, sep="\n")
cat("##################", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")


#subset data based on integrity
df.humnat <- subset(df, !is.na(humnat40))

#subset data based on integrity
dfnonNAG <- subset(df.humnat, !is.na(Grit_1000_1))


cat(c("Number of polygons: ", cntPoly), file=fileName, append=TRUE, sep="\n")

cntNNAG <- dim(dfnonNAG)[1]
cat(c("Number of polygons with data: ", cntNNAG), file=fileName, append=TRUE, sep="\n")

cntNAG = dim(df)[1] - cntNNAG
cat(c("Number of NA polygons (#): ", cntNAG), file=fileName, append=TRUE, sep="\n")

gtAreaG  <- sum(dfnonNAG$AREA_GEO) # exclude area w/ NAs
cat(c("Area (ha) of footprint for integrity mapping: ", round(gtAreaG,0)), file=fileName, append=TRUE, sep="\n")

humArea <- sum(dfnonNAG$humnat40 * dfnonNAG$AREA_GEO)
cat(c("Area of natural lands (ha): ", round(humArea,0)), file=fileName, append=TRUE, sep="\n")

perHumArea <-  humArea / gtAreaG
cat(c("Fraction of natural lands (ha): ", round(perHumArea,2)), file=fileName, append=TRUE, sep="\n")


cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Above integrity boundary ##", file=fileName, append=TRUE, sep="\n")

dfAboveG <- subset(dfnonNAG, Grit_1000_1 >= 1)
cntAboveG <- length(dfAboveG$Grit_1000_1)
cat(c("Number of polygons above integrity target: ", cntAboveG), file=fileName, append=TRUE, sep="\n")

perAboveG <- cntAboveG / cntNNAG
cat(c("Fraction of polygons above integrity target: ", round(perAboveG,3)), file=fileName, append=TRUE, sep="\n")


sumAreaIntegrity <- sum(dfnonNAG$Grit_1000_1 * dfnonNAG$AREA_GEO)
cat(c("Area of land above the integrity boundary (ha): ", round(sumAreaIntegrity,0)), file=fileName, append=TRUE, sep="\n")

perIntegrity <- sumAreaIntegrity / gtAreaG
cat(c("Fraction land area above the integrity boundary: ", round(perIntegrity,3)), file=fileName, append=TRUE, sep="\n")

perIntegrityNonIntact <- (sumAreaIntegrity- sumAreaIntact) / (gtAreaG - sumAreaIntact)
cat(c("Fraction land area with Integrity excluding Intact lands: ", round(perIntegrityNonIntact,3)), file=fileName, append=TRUE, sep="\n")

sumAreaNonIntegrity <- (gtAreaG - sumAreaIntegrity)
cat(c("Area of land without Integrity: ", round(sumAreaNonIntegrity,3)), file=fileName, append=TRUE, sep="\n")



cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Below integrity boundary ##", file=fileName, append=TRUE, sep="\n")

dfBelowG <- subset(dfnonNAG, Grit_1000_1 < 1)
cntBelowG <- length(dfBelowG$Grit_1000_1)
cat(c("Number of polygons below the integrity target: ", cntBelowG), file=fileName, append=TRUE, sep="\n")

perBelowG <- cntBelowG / cntNNAG
cat(c("Fraction of polygons below the integrity target: ", round(perBelowG,3)), file=fileName, append=TRUE, sep="\n")

sumAreaNGPoly <- sum(dfBelowG$AREA_GEO)
cat(c("Area of land below the integrity target (ha): ", round(sumAreaNGPoly,0)), file=fileName, append=TRUE, sep="\n")

perGPoly <- sumAreaNGPoly / gtAreaG
cat(c("Fraction land area below the integrity target: ", round(perGPoly,3)), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")

sumAreaNIntegrity <- sum((1 - dfnonNAG$Grit_1000_1) * dfnonNAG$AREA_GEO) 
cat(c("Area of land below the integrity boundary (ha): ", round(sumAreaNIntegrity,0)), file=fileName, append=TRUE, sep="\n")

perNIntegrity <- sumAreaNIntegrity / gtAreaG
cat(c("Fraction land area below integrity: ", round(perNIntegrity,3)), file=fileName, append=TRUE, sep="\n")

perNIntegrityNonIntact <- (sumAreaNIntegrity) / (gtAreaG - sumAreaIntact)
cat(c("Fraction land area without Integrity excluding Intact lands: ", round(perNIntegrityNonIntact,3)), file=fileName, append=TRUE, sep="\n")


# these calculations are the same as above when the integrity target is 100%
cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Below integrity boundary (deficit) ##", file=fileName, append=TRUE, sep="\n")

sumAreaServDef <- sum((1 - dfnonNAG$Grit_1000_1) * dfnonNAG$AREA_GEO)
cat(c("Area (ha) of land with integrity deficit: ", round(sumAreaServDef,0)), file=fileName, append=TRUE, sep="\n")

perAreaServDef <- sumAreaServDef / gtAreaG
cat(c("Fraction land area with integrity deficit: ", round(perAreaServDef,3)), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")



cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Threatened (Integrity < 10%) ##", file=fileName, append=TRUE, sep="\n")

dfThreatG = subset(dfnonNAG, Grit_1000_1 < 0.1)
cntThreatG = dim(dfThreatG)[1]
cat(c("Number of threatened polygons by integrity (#): ", cntThreatG), file=fileName, append=TRUE, sep="\n")

perThreatG = cntThreatG / cntNNAG
cat(c("Percentage of threatened polygons (#) by integrity: ", round(perThreatG,3)), file=fileName, append=TRUE, sep="\n")

areaThreatG = sum(dfThreatG$AREA_GEO)
cat(c("Area of threatened polygons (#): ", round(areaThreatG,0)), file=fileName, append=TRUE, sep="\n")

perAreaThreatG = areaThreatG/gtArea
cat(c("Fraction land area of threatened polygons by integrity: ", round(perAreaThreatG,3)), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")



cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("## Extinct (Integrity < 1%) ##", file=fileName, append=TRUE, sep="\n")

dfExtinctG = subset(dfnonNAG, Grit_1000_1 < 0.01)
cntExtinctG = dim(dfExtinctG)[1]
cat(c("Number of Extinct polygons by integrity (#): ", cntExtinctG), file=fileName, append=TRUE, sep="\n")

perExtinctG = cntExtinctG / cntNNAG
cat(c("Percentage of Extinct polygons (#) by integrity: ", round(perExtinctG,3)), file=fileName, append=TRUE, sep="\n")

areaExtrinctG = sum(dfExtinctG$AREA_GEO)
cat(c("Area of Extinct polygons (#): ", round(areaExtrinctG,0)), file=fileName, append=TRUE, sep="\n")

perAreaExtinctG = areaExtrinctG/gtArea
cat(c("Fraction land area of extinct polygons by integrity: ", round(perAreaExtinctG,3)), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")



######################################################
## Listing Extinct Polygons - Intactness and Integrity
######################################################

# #GAUL
# cat("", file=fileName, append=TRUE, sep="\n")
# #list of name of extinct polygons - intactness
# listExtinct <- as.list(dfExtinct$ADM0_NAME)
# prtList = unlist(lapply(listExtinct, paste, collapse=" "))
# cat(c("List of Extinct polygons (Intactness <= 10%): ", prtList), file=fileName, append=TRUE, sep="\n")
# cat("", file=fileName, append=TRUE, sep="\n")
# 
# cat("", file=fileName, append=TRUE, sep="\n")
# #list of name of extinct polygons - integrity
# listExtinctG <- as.list(dfExtinctG$ADM0_NAME)
# prtListG = unlist(lapply(listExtinctG, paste, collapse=" "))
# cat(c("List of Extinct polygons (Integrity <= 10%): ", prtListG), file=fileName, append=TRUE, sep="\n")
# cat("", file=fileName, append=TRUE, sep="\n")


# #CER
# cat("", file=fileName, append=TRUE, sep="\n")
# #list of name of extinct polygons - intactness
# listExtinct <- as.list(dfExtinct$CtryEco)
# prtList = unlist(lapply(listExtinct, paste, collapse=" "))
# cat(c("List of Extinct polygons (Intactness <= 10%): ", prtList), file=fileName, append=TRUE, sep="\n")
# cat("", file=fileName, append=TRUE, sep="\n")
# 
# cat("", file=fileName, append=TRUE, sep="\n")
# #list of name of extinct polygons - integrity
# listExtinctG <- as.list(dfExtinctG$CtryEco)
# prtListG = unlist(lapply(listExtinctG, paste, collapse=" "))
# cat(c("List of Extinct polygons (Integrity <= 10%): ", prtListG), file=fileName, append=TRUE, sep="\n")
# cat("", file=fileName, append=TRUE, sep="\n")


# #ER
#list of name of threatened polygons - intactness
listThreat <- as.list(dfThreat$ECO_NAME)
prtList = unlist(lapply(listThreat, paste, collapse=" "))
cat(c("List of Threatened polygons (Intactness <= 10%): ", prtList), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")

#list of name of extinct polygons - intactness
listExtinct <- as.list(dfExtinct$ECO_NAME)
prtList = unlist(lapply(listExtinct, paste, collapse=" "))
cat(c("List of Extinct polygons (Intactness <= 1%): ", prtList), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")

#list of name of threatened polygons - integrity
listThreatG <- as.list(dfThreatG$ECO_NAME)
prtListG = unlist(lapply(listThreatG, paste, collapse=" "))
cat(c("List of Extinct polygons (Integrity <= 10%): ", prtListG), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")

#list of name of extinct polygons - integrity
listExtinctG <- as.list(dfExtinctG$ECO_NAME)
prtList = unlist(lapply(listExtinctG, paste, collapse=" "))
cat(c("List of Extinct polygons (Integrity <= 1%): ", prtList), file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")
cat("", file=fileName, append=TRUE, sep="\n")



##############################################
####### Supp Tables with all the summary data
##############################################

# Ecoregion Table
df.eg = df[, c(3,18,23:25,22,26,29:31,42)]

colnames(df.eg) <- c("ECO_NAME", "CSIRO68", "GHM1", "HFP4", "LIA", "ensb_thr3",
                     "Natural", "Integ1km10", "Integ1km20", "Integ1km30", "Area (ha)")

dftable <- arrange(df.eg, ECO_NAME)

FT <- formattable(dftable, align = c("l", rep("r", NCOL(dftable) - 1)),
                   list(`Summary Statistics by Ecoregion (Dinerstein 1997)` =
                        formatter("span", style = ~ style(color = "grey", font.weight = "bold")),
                        'ensb_thr3' = color_tile("#DeF7E9", "#71CA97"),
                        #'Integ1km10' = color_tile("green"),
                        area(col = 2:10) ~ function(x) round(x, digits = 2),
                        area(col = 11) ~ function(y) round(y, digits = 0)
                   ))
FT

write.csv(dftable, "Apex2021_FullTable_ER.csv", row.names = FALSE)


# Exporting the table as a figure
export_formattable <- function(f, file, width = "100%", height = NULL, 
                               background = "white", delay = 0.2)
{
  w <- as.htmlwidget(f, width = width, height = height)
  path <- html_print(w, background = background, viewer = NULL)
  url <- paste0("file:///", gsub("\\\\", "/", normalizePath(path)))
  webshot(url,
          file = file,
          selector = ".formattable_widget",
          delay = delay)
}

export_formattable(FT,"Apex2021_FullTable_ER.png")


 
 
# Country Ecoregion Table
#' df.eg = df[, c(13, 3, 5, 17, 18:21, 22:25, 38)]
#' colnames(df.eg)
#' colnames(df.eg) <- c("ADM0_NAME", "ECO_NAME", "BIOME_NAME", "CSIRO68", "GHM1", "HFP4", "LIA", "ensb_thr3", "Natural", "Integ1km10", "Integ1Km20", "Integ1Km10", "Area (ha)")
#' 
#' dftable <- arrange(df.eg, ADM0_NAME, ECO_NAME)
#' 
#' FT <- formattable(dftable[], align = c("l", rep("r", NCOL(dftable))),
#'                   list(`Summary Statistics by Country (GAUL 2016) and Ecoregion (Dinerstein 1997)` =
#'                          formatter("span", style = ~ style(color = "grey", font.weight = "bold")),
#'                        area(col = 4:12) ~ function(x) round(x, digits = 2),
#'                        area(col = 13) ~ function(y) round(y, digits = 0)
#'                   ))
#' FT
#' 
#' write.csv(dftable, "Apex2021_dftable_CER.csv", row.names = FALSE)
#' 
#' 
#' #' #' # GAUL Table
#' df.eg = df[, c(4,7,12:14,11,15,18,31)]
#' 
#' colnames(df.eg) <- c("ADM0_NAME", "CSIRO68", "GHM1", "HFP4", "LIA", "ensb_thr3", "Natural", "Integ1km10", "Area (ha)")
#' 
#' dftable <- arrange(df.eg, ADM0_NAME)
#' 
#' FT <- formattable(dftable, align = c("l", rep("r", NCOL(dftable) - 1)),
#'                    list(`Summary Statistics by ecoregion` =
#'                           formatter("span", style = ~ style(color = "grey", font.weight = "bold")),
#'                         'ensb_thr3' = color_tile("#DeF7E9", "#71CA97"),
#'                         #'Integ1km10' = color_tile("green"),
#'                         area(col = 2:8) ~ function(x) round(x, digits = 2),
#'                         area(col = 9) ~ function(y) round(y, digits = 0)
#'                    ))
#' FT
#' 
#' write.csv(dftable, "Apex2021_dftable_GAUL.csv", row.names = FALSE)


##### Summary of Intactness and Integrity Groups ####
group1 <- df %>%
  filter(ensb_thr3 >= 0.5) %>%
  filter(Grit_1000_1 >= 0.8) %>%
  select (ECO_NAME, ensb_thr3, Grit_1000_1, AREA_GEO)

group2 <- df %>%
  filter(ensb_thr3 < 0.5) %>%
  filter(Grit_1000_1 >= 0.8) %>%
  select (ECO_NAME, ensb_thr3, Grit_1000_1, AREA_GEO)

group3 <- df %>%
  filter(ensb_thr3 < 0.5) %>%
  filter(Grit_1000_1 < 0.8) %>%
  select (ECO_NAME, ensb_thr3, Grit_1000_1, AREA_GEO)

groupall <- df %>%
  filter(!is.na(ensb_thr3) & !is.na(Grit_1000_1)) %>%
  select (ECO_NAME, ensb_thr3, Grit_1000_1)

perGrp1 <- dim(group1)[1] / dim(groupall)[1]
perGrp2 <- dim(group2)[1] / dim(groupall)[1]
perGrp3 <- dim(group3)[1] / dim(groupall)[1]

cat("Percent of each polygon by Intactness (>50%) and (Integrity >80%):", file=fileName, append=TRUE, sep="\n")
cat(c("Group 1: ", round(perGrp1,2)), file=fileName, append=TRUE, sep="\n")
cat(c("Group 2: ", round(perGrp2,2)), file=fileName, append=TRUE, sep="\n")
cat(c("Group 3: ", round(perGrp3,2)), file=fileName, append=TRUE, sep="\n")

# area of groups
group1area <- sum(group1$AREA_GEO) /1000000
group2area <- sum(group2$AREA_GEO) /1000000
group3area <- sum(group3$AREA_GEO) /1000000



##### integrity threshold figure ######

grit <- dfnonNAG %>%
  select (c(3,22:30))

sumGrit <- summary(grit)

mdata <- melt(grit, id=c("ECO_NAME"))

boxplot(value~variable,data=mdata, main="Integrity Measures",
        xlab="", ylab="Mean Integrity (%)", las=2)



######################################
######## integrity histogram #####
######################################

# df <- data.frame(IIdata)
# colnames(df)
# 
# names(df)[26]<- '10%'
# names(df)[27]<- '20%'
# names(df)[28]<- '30%'
# names(df)[29]<- '50%'
# 
# 
# # reformat the data as a table
# meltDF <- df %>%
#   select(ECO_NAME, "10%", "20%", "30%", "50%") %>%
#   melt(id.var="ECO_NAME")
# 
# cleanDF <- na.omit(meltDF)
# 
# # histogram of integrity
# histo <- ggplot(cleanDF, aes(x=value, color=variable)) +
#   geom_histogram(fill="white", position="dodge", alpha=0.5, bins = 10) +
#   scale_color_brewer(palette="Dark2") +
#   labs(x = "Integrity (%)", y = "Count of Ecoregions") +
#   guides(color=guide_legend("Boundaries")) +
#   theme(legend.position=c(0.2, 0.65))
# 
# histo
# 
