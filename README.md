##### Spare half, share the rest: A revised planetary boundary for biodiversity intactness and integrity #####
> Manuscript data and code
> https://github.com/alexfremier/Spare-Share-Manuscript.git
> Curator: Alexander Fremier (alex.fremier@wsu.edu)
> Co-authors:  Fabrice DeClerck (fabrice@eatforum.org), Sarah Jones (s.jones@cgiar.org), Natalia Estrada Carmona (n.e.carmona@cgiar.org)
> Project start year: 2020
> Project location:  Montpellier France

##### Brief Project Description #####
The Spare-Share manuscript outlines a revision to the planetary boundary for biodiversity. The manuscript presents the concepts and calculates
Biodiversity Intactness and Ecosystem Integrity for ecoregions, countries, and country-ecoregions across the globe.  This GitHub repository 
contains the source code for the spatial analysis in Python using ArcGIS Pro plug-ins and summary analysis using R. The repository includes 
multiple summary tables and data from the project.  We do not supply the base data from other projects (e.g. HFP, LIA, gHM, CSIRO, and 
ESACCI-LC).   

#### Installing / Getting started #####
Three separate python scripts call ArcGIS Pro modules to: (1) prepare base data for calculations, (2) calculate Intactness, and (3) calculate
Integrity and write output two outfiles - a shapefile and an XLSX file with tabular data.  The R code summarizes the Python code output data
(XLSX file). 

01_ApexTargetTool_DataPrep_v1.5.py
02_ApexTargetTool_Intactness_v1.5.py
03_ApexTargetTool_Integrity_v1.5.py
04_Apex2021_DataSummary_v1.5.r

##### Built With #####
Python (v3.6)
ArcGIS Pro (v2.5.1 ESRI 2020) Spatial Analyst extension required
R (v R-4.0.2)

##### Base Data #####
Human Footprint map (Ventor et al. 2016) [HP4] https://datadryad.org/stash/dataset/doi:10.5061/dryad.052q5 
Low Impact Areas [LIA] (Jacobson et al. 2019) https://datadryad.org/stash/dataset/doi:10.5061/dryad.z612jm67g
Global Human Modification Index (Kennedy et al. 2019) https://figshare.com/articles/Global_Human_Modification/7283087 
CSIRO Habitat Condition (Hoskins et al. 2020)  Data upon request from this paper.
European Space Agency Climate Change Initiative-Land Cover Project (ESACCI-LC) (Defourney et al. 2017) 
     http://www.esa-landcover-cci.org/?q=node/164
Ecoregions	 (Dinerstein, et al. 2017)
GAUL    FAO Global Administrative Unit Layer (FAO, 2014). http://www.fao.org/geonetwork/srv/en/metadata.show?id=12691 

Venter, O. et al. Global terrestrial Human Footprint maps for 1993 and 2009. Scientific data 3, 1-10 (2016).
Jacobson, A. P., Riggio, J., Tait, A. M. & Baillie, J. E. Global areas of low human impact (‘Low Impact Areas’) and 
     fragmentation of the natural world. Scientific reports 9, 1-13 (2019).
Kennedy, C. M., Oakleaf, J. R., Theobald, D. M., Baruch‐Mordo, S. & Kiesecker, J. Managing the middle: A shift in 
      conservation priorities based on the global human modification gradient. Global Change Biology 25, 811-826 (2019).	
Hoskins, A. J. et al. BILBI: supporting global biodiversity assessment through high-resolution macroecological modelling. 
      Environmental Modelling & Software 132, 104806 (2020).
Defourny, P. et al. CCI-LC PUGv2 Phase II. Land Cover Climate Change Initiative-Product User Guide v2 (2017).
Dinerstein, E. et al. An ecoregion-based approach to protecting half the terrestrial realm. BioScience 67, 534-545 (2017).
GAUL FAO Global Administrative Unit Layer (2014)

##### Provided Data #####
Below is a description of dataset produced for this manuscript.

Apex2021_Biome_Intactness.csv - Table of Biodiversity Intactness (Et3) summarized by biome
Apex2021_FullTable_CER.csv - Table of Biodiversity Intactness (all) and Ecosystem Integrity (10%,20%,30%) by Country-Ecoregions
Apex2021_FullTable_ER.csv - Table of Biodiversity Intactness (all) and Ecosystem Integrity (10%,20%,30%) by Ecoregions
Apex2021_FullTable_GAUL.csv - Table of Biodiversity Intactness (all) and Ecosystem Integrity (10%,20%,30%) by Country
Apex2021_Stats_ER_Integ10.txt - Summary statistics for Biodiversity Intactness and Ecosystem Integrity (10%) by Ecoregion
Apex2021_Stats_ER_Integ20.txt - Summary statistics for Biodiversity Intactness and Ecosystem Integrity (20%) by Ecoregion
Apex2021_Stats_ER_Integ30.txt - Summary statistics for Biodiversity Intactness and Ecosystem Integrity (30%) by Ecoregion





