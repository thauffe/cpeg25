Inferring the evolutionary history of the Proboscidea
================
Rebecca Cooper

# Introduction

`DeepDiveR` is an R package for estimating biodiversity through time
from fossil occurrence data (Cooper et al 2024). It produces formatted
input data and a configuration file that can then be executed in Python
through the command line, enabling a clear and reproducible workflow. In
this tutorial we will use DeepDiveR to analyse the past diversity of
Proboscidea, the order containing elephants and their extinct relatives,
using the data of Cantalapiedra et al. (2021).

# Installation

To install the `DeepDiveR` library, it needs to be downloaded from the
GitHub repository using either the package `remotes` or a manual
download.

``` r
# Option 1: install the package from GitHub
remotes::install_github("DeepDive-project/DeepDiveR")
# Option 2: load it from a directory after downloading it from
# https://github.com/DeepDive-project/DeepDiveR
# deepdiver_path <- "path_to_DeepDiveR"
# setwd(deepdiver_path)
# library(devtools)
# load_all(".")
```

We can then load the `DeepDiveR` package.

``` r
library(DeepDiveR)
```

# Preparing the input data

First we will load our proboscidean occurrence data. This is located in
the repository for the workshop, and can be downloaded from the GitHub.

``` r
# Load proboscidean data
path_dat <- "~/cpeg25/deepdive_analysis"
proboscidea <- read.csv(paste0(path_dat, "/Proboscidea_occurrences_DD.csv"))
```

Next, we will view the first few rows of the `data.frame` to get a sense
of its contents.

``` r
head(proboscidea)
```

    ##                         Taxon Region MinAge MaxAge
    ## 1       Eritherium azzouzorum Africa   56.0   59.2
    ## 2        Daouitherium rebouli Africa   53.0   56.0
    ## 3   Phosphatherium escuilliei Africa   53.0   56.0
    ## 4        Khamsaconus bulbosus Africa   52.5   53.0
    ## 5     Numidotherium koholense Africa   51.0   52.0
    ## 6 Moeritherium chehbeurameuri Africa   38.0   39.0
    ##                                              Locality
    ## 1                             Sidi Chennane_siteSet_1
    ## 2 Grand Daoui Quarries - Ouled Abdoun Basin_siteSet_1
    ## 3 Grand Daoui Quarries - Ouled Abdoun Basin_siteSet_1
    ## 4                   N'Tagourt 2, Ouazarzate_siteSet_1
    ## 5                                  El Kohol_siteSet_1
    ## 6                               Bir El Ater_siteSet_1

We can see our ‘data.frame’ has 2104 occurrences with 5 columns
describing the data. These columns describing the taxon name, the
geographic region where it occurs, the minimum and maximum age range,
and a locality identifier. Each row in the `data.frame` corresponds to a
single occurrence. This is the standard format of data needed by
`DeepDiveR`. The dataset we are using today has already been thoroughly
checked through by the authors that compiled it (Cantalapiedra et
al. 2021).

We now need to specify the time bins into which our occurrences will be
placed. They do not need to be equally spaced, geological intervals can
be used if desired. Here we will use divisions based on the stages of
the Cenozoic, split to average to approximately one million year
duration each. We will do this by describing a vector which provides the
bin boundaries, in millions of years.

``` r
# Describe vector of bin boundaries
bins <- c(66, 65, 64, 63, 61.6, 60, 59.2, 58.13333, 57.06667, 56, 54.975, 53.95, 52.925, 51.9, 50.875, 
          49.85, 48.825, 47.8, 46.85714, 45.91429, 44.97143, 44.02857, 43.08571, 42.14286, 41.2, 
          40.03667, 38.87333, 37.71, 36.7575, 35.805, 34.8525, 33.9, 32.88667, 31.87333, 30.86, 29.84667, 
          28.83333, 27.82, 26.862, 25.904, 24.946, 23.988, 23.03, 22.16667, 21.30333, 20.44, 19.3225, 
          18.205, 17.0875, 15.97, 14.895, 13.82, 12.725, 11.63, 10.534, 9.438, 8.342, 7.246, 6.2895, 
          5.333, 4.4665, 3.6, 2.58, 0.774, 0)
```

Now we can prepare the input file for `DeepDive`, using the function
`prep_dd_input`. Here we need to specify the `data.frame` containing the
occurrence data and vector of time bins. We also want to provide the
number of replicates, i.e. how many times we want the occurrences to be
placed into the time bins. Here we will specify 10 replicates, to
illustrate the process, but a higher number of replicates is needed to
capture temporal uncertainty in final analyses e.g. 100 (for a dataset
of this size 100 replicates takes approximately 7 minutes to run; for a 
real analysis you should increase this number to e.g. 50,000 training 
simulations and 1000 test simulations).
Finally, we also need to give the name of the file that we want to be
created. The file takes the form `.csv`, indicating that the values are
comma-separated. This will be the file we need to input into `DeepDive`.

``` r
# Create input file for DeepDive
prep_dd_input(
  # Specify occurrence data.frame
  dat = proboscidea,
  # Specify vector containing time bin boundaries
  bins = bins,
  # Specify number of replicates
  r = 10, 
  # Specify name of created file
  output_file = "proboscidea_deepdive_input.csv" 
)
```

# Preparing the configuration file

Now we need to create a configuration file for `DeepDive`, using the
function `create_config`. Here we will describe all of the internal
settings for the analysis. Some of the settings must be described by the
user. These include…

``` r
# Create configuration file for DeepDive
config <- create_config(
  # Specify the name for the simulations
  name = "proboscidea",
  # Specify the name of the data file
  data_file = "proboscidea_deepdive_input.csv",
  # Specify vector containing time bin boundaries
  bins = bins,
  # Specify the number of geographic regions to simulate
  n_regions = length(unique(proboscidea$Region))
)
```

Other settings are autofilled by `create_config()`. In order to alter
these, we can use the function `edit_config()`. First, we know that
there are 3 extant species of elephants (the African savanna elephant
*Loxodonta africana*, the African forest elephant *Loxodonta cyclotis*
and the Asian elephant *Elephas maximus*), so let’s condition our
simulations on this number of living species.

``` r
# Modify the number of extant species ("present_diversity") in simulations
edit_config(config = config,
            module = "general",
            parameter = "present_diversity", 
            value = 3)


edit_config(config = config,
            module = "simulations",
            parameter = "extant_sp", 
            value = c(3, 300))
```

It is possible to allow the geographic regions available in the
simulations to change through time. In order to do this, we will create
an `regions_matrix` object which will be incorporated in the
configuration file. Here, we will assume that dispersal of proboscideans
to Europe and Asia began between 33.9 and 27 Ma, to North America
between 20 and 16 Ma, and to South America between 5.3 and 0.8 Ma.
Regions disappearing instead of connecting can be made by setting the
label argument to: presence = “FALSE”. By default presence = “TRUE” and
regions will be connected and remain available until the present day.

``` r
# Create data.frame describing the time for which each region is available
region_ages <- rbind(c("Africa", max(bins), max(bins)), # first proboscideans appear in Africa
                    c("Asia", 33.9, 27),  # Cantalapiedra et al. + Eocene/Oligocene boundary, they can enter Eurasia
                    c("Europe", 33.9, 27),  
                    c("North America", 20, 16),  # Cantalapiedra et al, they can enter North America
                    c("South America", 5.3, 0.8))  # Carrillo et al. and Cantalapiedra et al's data, they can enter South America
region_ages <- as.data.frame(region_ages)

# Label columns
colnames(region_ages) <- c("Region", "MaxAge", "MinAge")

# Connect region data to configuration file
regions_matrix(config = config, region_ages = region_ages)
```

Now we need to describe the technical aspects of the neural network
training and analysis process. For a reliable estimate, you will need at
least 10,000 training simulations. However, for the purpose of running a
quick test analysis, we will use a low number of both training and test
simulations. Again we will edit the relevant parameters in the
configuration file using the `edit_config` function:

``` r
# Set number of training simulations to 1000
edit_config(config = config,
            module = "simulations",
            parameter = "n_training_simulations", 
            value = 1000)

# Set number of test simulations to 100
edit_config(config = config,
            module = "simulations",
            parameter = "n_test_simulations", 
            value = 100)
```

It is possible to train multiple models with varying neural network
architectures. Primarily, the number of Long Short-Term Memory layers
and nodes can be varied along with the layers and nodes in the dense
layer of the network. These can be single numbers e.g. 32, in which case
32 nodes will be implemented in one fully connected layer. Alternatively
a vector can be used e.g. c(64, 32). In the latter example, two layers
of fully connected nodes would be implemented with 64 nodes and 32 nodes
respectively. These settings are added to the configuration file using
the function `add_model` which should be called once for each model
architecture:

``` r
# Set number of LSTM and dense nodes for an additional model architecture
add_model(config = config,
          lstm_nodes = c(128, 64),
          dense_nodes = c(128, 64, 32), 
          model_name = "2")
```

    ## [1] "Model has been added to the configuration."

Now we are ready to write the configuration file to use in the analysis:

``` r
# Write the configuration file
config$write("proboscidea_config.ini")
```

# Executing the analysis

Once the configuration and input files are created, the full DeepDive
analysis including simulation, model training and predictions can be
carried out through a single command line entered in a Terminal (MacOS
and Linux) or Command prompt (Windows) window executing the Python
script run_dd_config.py.

First we will add some flags to run just a test batch of 100 simulations
using -plot_features and -n_sims. These flags cut the run short after
simulating and will not produce a trained model. However, running a
small test batch of simulations can be a useful first step exercise to
check if your parameterization for the simulations is capturing the
variation in the distribution of fossil data in the way you would
expect.

Additional flags, -wd and -cpu are available that can allow you to
adjust the location of your folder and the number of cpus to run the
analysis in the command line. Any settings specified by using flags will
overwrite the configuration settings (remember to replace the `...` with 
the full path to your cpeg25 folder:

``` python
cd /.../cpeg25 
source venv/bin/activate
cd programs/deepdive
python run_dd_config.py /.../cpeg25/deepdive_analysis/proboscidea_config.ini -plot_features -n_sims 100 -cpu 2
```

You can now navigate to the folder “proboscidea_output_feature_plots” to
see plots of the empirical fossil record and of your initial
simulations. In an ideal world, the goal is for the empirical fossil
record (blue data) to fall within the range of the simulated fossil
record (orange). If it does not, you can adjust the parameters of the
configuration and repeat this initial simulation step until you are
satisfied. Checking that the simulations reflect the distribution of the
empirical fossil record helps us to avoid potential sources of
extrapolation error.

Now we are ready to run the analysis for real!

``` python
python run_dd_config.py /.../cpeg25/deepdive_analysis/proboscidea_config.ini -cpu 2
```

This script will create a “simulations” folder containing the training
and test sets of simulations and a “trained_models” folder containing
the models and plots of training history. This folder additionally
includes plots of features of the empirical and simulated records
(e.g. number of occurrences through time and per region, number of
localities, fraction of singletons and sampled diversity), CSV files
with the predicted diversity trajectories for the test set and for the
empirical dataset, and a plot of the estimated diversity trajectory.

# References

Cooper, R. B., Allen, B. J., & Silvestro, D. (2024). DeepDiveR–A
software for deep learning estimation of palaeodiversity from fossil
occurrences. bioRxiv, 2024-09.

Cantalapiedra, J. L. et al. (2021) The rise and fall of proboscidean
ecological diversity. Nat. Ecol. Evol. 5, 1266–1272.
