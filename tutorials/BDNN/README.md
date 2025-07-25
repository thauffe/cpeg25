# Birth-Death Neural Network analysis

## Inferring speciation and extinction rates through time

The birth-death neural-network model modulates speciation and extinction rates per lineage and through time as a function of 

1. **time**
2. one or multiple **categorical and/or continuous traits** (e.g. diet, body mass, geographic range)
3. one or more **time-dependent variables** (e.g. paleotemperature)
4. **phylogenetic relatedness** (e.g. classification into higher taxa or phylogenetic eigenvectors)

As the function is based on a fully connected feed-forward neural network, it is not based on *a priori* assumptions about its shape. For instance, it can account for non-linear and non-monotonic responses of the rates to variation in the predictors.
It can also account for any interactions among the predictors. 

The parameters of the BDNN model are estimated jointly with the origination and extinction times of all taxa and the preservation rates. 
The output can be used to estimate rate variation through time, across species, and to identify the most important predictors of such variation and their individual or combined effects. 


### Navigate to your cpeg25 repository and activate the virtual environment

Just as the standard PyRate diversification analysis, our BDNN inference will be performed in your command window or terminal and makes use of your virtual environment. Move into your cpeg25 repository and activate the venv.

* Windows
 
    ```
    cd c:\...\cpeg25
    .\venv\Scripts\activate
    ```

* Mac and Linux

    ```
    cd /.../cpeg25
    source venv/bin/activate
    ```


### Running a BDNN inference

We are employing the same PyRate input file as for the standard diversification analysis and the time-variable preservation model with heterogeneity among species is also the same.

There are a number of additional arguments needed to run the BDNN model:

1. **Specify the BDNN model itself.** This is done by adding the flag `-BDNNmodel 1`.
2. **Adding species traits.** While the BDNN could be used with just time as predictor, we want to include species-specific traits with the `-trait_file` argument. This provides the path to a tab-separated text file called _Traits.txt_ located in your _bdnn_analysis_ folder. 

    We will use species-specific traits, including a categorical measure of body size, geographic distribution across main continents and islands, and taxonomic family membership. The body mass categories are centered in 0 by subtracting the median while geography and family are binary variables.

    | Species | Body size | Africa | Americas | Eurasia	| Island | Elephantidae | Gomphotheriidae |
    |:-------------:| -----------:| -----------:| -----------:| -----------:| -----------:| -----------:|
    | Konobelodon\_britti | 1 | 0 | 1 | 0 | 0 | 0 | 1 |
    | Mammuthus\_creticus | -4 | 0 | 0 | 1 | 1 | 1 | 0 |
    | Stegotetrabelodon\_syrticus | 2 | 1 | 0 | 1 | 0 | 1 | 0 |

3. **Adding time-dependent variables.** For these workshop, these are are a global temperature curve and the binary factor _Humans_ where we naively assume that humans are globally present since 100,000 years ago. There is no strong evidence that humans influence the speciation rate, so we provide separate text files with time-dependent variables to the `-BDNNtimevar` option, whereas typically a single file is sufficient. The file for speciation has the _Humans_ predictor set to zero, while the file for extinction includes the binary coding. Continuous predictors like the paleotemperature should be z-scaled (i.e. subtract the mean and divide by the standard deviation) to aid MCMC convergence.

    | Age | Paleotemperature | Humans |
    |:-:|:-:|:-:|
    | 0 | -1.49 | 1 |
    | 0.05 | -3.05 | 1 |
    | 0.1 | 2.53 | 1 |
    | 0.2 | -1.95 | 0 |
    | . | . | . |
    | . | . | . |
    | . | . | . |
    | 39.80 | 2.43 | 0 |
    | 39.90 | 2.48 | 0 |


By default, the mean or modal values of the time-dependent variables are computed in 1-million-year time bins (or the value of `-BDNNtimeres`). This would conceal the Plio-Pleistocene climate fluctuations, whereas earlier, more constant conditions do not require such high temporal resolution. Thus, we use stages as time windows and subject them to the `-fixShift` argument.

* Windows

    ```
    python .\programs\PyRate\PyRate.py ^
    .\bdnn_analysis\Proboscidea.py ^
    -qShift .\bdnn_analysis\Stages.txt ^
    -mG ^
    -BDNNmodel 1 ^
    -trait_file .\bdnn_analysis\Traits.txt ^
    -BDNNtimevar .\bdnn_analysis\Timevar_speciation.txt .\bdnn_analysis\Timevar_extinction.txt ^
    -fixShift .\bdnn_analysis\Time_windows.txt ^
    -n 1000000 -s 10000 -p 100000
    ```

* Mac and Linux

    ```
    python ./programs/PyRate/PyRate.py \
    ./bdnn_analysis/Proboscidea.py \
    -qShift ./bdnn_analysis/Stages.txt \
    -mG \
    -BDNNmodel 1 \
    -trait_file ./bdnn_analysis/Traits.txt \
    -BDNNtimevar ./bdnn_analysis/Timevar_speciation.txt ./bdnn_analysis/Timevar_extinction.txt \
    -fixShift ./bdnn_analysis/Time_windows.txt \
    -n 1000000 -s 10000 -p 100000
    ```

This analysis will take ca. 5-10 min.


### Plot speciation and extinction rates through time

The BDNN run creates a new folder called _pyrate_mcmc_logs_ in your _bdnn_analysis_ directory. As with the standard Pyrate diversification analysis, we can plot speciation and extinction rates through time. 

* Windows

    ```
    python .\programs\PyRate\PyRate.py ^
    -plotBDNN .\bdnn_analysis\pyrate_mcmc_logs\Proboscidea_1_G_BDS_BDNN_16_8TVc_mcmc.log ^
    -b 0.25
    ```

* Mac and Linux

    ```
    python ./programs/PyRate/PyRate.py \
    -plotBDNN ./bdnn_analysis/pyrate_mcmc_logs/Proboscidea_1_G_BDS_BDNN_16_8TVc_mcmc.log \
    -b 0.25
    ```

<img src="https://github.com/thauffe/cpeg25/blob/main/pictures/bdnn_rtt.png" alt="trace plot" width="1000">

Marginal speciation and extinction rates through time. Marginal rates are the average species-specific rates across each species being extant at a moment in time.

### Display the influence of traits and paleotemperature on rates

We can create partial dependence plots (PDP) to visualize the influence of single predictors and all two-way interactions on speciation and extinction rates with the `-plotBDNN_effects` command.

The flag `-BDNN_groups` is used to group 0/1 encoded predictors that are different states of the same predictor, e.g. for the the taxonomic trait _Family_. This will ensure that their effects are displayed together in a single plot. Note that the declaration of the `-BDNN_groups` includes *escaped quotes (i.e. \"). If you are using a Linux or Mac system, the expression can be simplified with single quotes (') for the outer quotes and double quotes (") for the trait and its states.

We have centered the body mass category in 0 and z-scaled the paleotemperature. To display their effects on their original scale, we backtransform them with the `-plotBDNN_transf_features` argument. This specifies the path to a small text file including the mean and standard deviation used to scale the predictors.

We also set the `-resample` argument to 50 for not creating the effect plots based on all MCMC iterations. There could be thousands if we run the MCMC for longer.

* Windows

    ```
    python .\programs\PyRate\PyRate.py ^
    -plotBDNN_effects .\bdnn_analysis\pyrate_mcmc_logs\Proboscidea_1_G_BDS_BDNN_16_8TVc_mcmc.log ^
    -BDNN_groups "{\"Geography\": [\"Africa\", \"Americas\", \"Eurasia\", \"Island\"], \"Family\": [\"Deinotheriidae\", \"Elephantidae\", \"Gomphotheriidae\", \"Mammutidae\", \"Stegodontidae\", \"OtherFamilies\"]}" ^
    -plotBDNN_transf_features ./bdnn_analysis/Backscale.txt ^
    -b 0.25 ^
    -resample 50
    ```

* Mac and Linux

    ```
    python ./programs/PyRate/PyRate.py \
    -plotBDNN_effects ./bdnn_analysis/pyrate_mcmc_logs/Proboscidea_1_G_BDS_BDNN_16_8TVc_mcmc.log \
    -BDNN_groups '{"Geography": ["Africa", "Americas", "Eurasia", "Island"], "Family": ["Deinotheriidae", "Elephantidae", "Gomphotheriidae", "Mammutidae", "Stegodontidae", "OtherFamilies"]}' \
    -plotBDNN_transf_features ./bdnn_analysis/Backscale.txt \
    -b 0.25 \
    -resample 50
    ```

<img src="https://github.com/thauffe/cpeg25/blob/main/pictures/bdnn_pdp_geography.png" alt="trace plot" width="700">

Partial dependent (PD) speciation rate for the predictor geography. PD plots convey the effect of one or two predictors by marginalizing over the remaining one (i.e. ignoring their effect by averaging over them).

### Obtain predictor importance

In the last step, we (a) assess if the variation in species-time-specific rates exceeds the expectation under a constant diversification process, and (b) rank the predictors according to their influence on speciation and extinction rates. 

To safe some time, we use some optional arguments that:

* Relax the fair permutation of predictors across our time bins of unequal length by setting the shortest bin with `-BDNN_pred_importance_window_size` to 0.1 Ma instead of the true duration of 11,700 years 
* Obtain the expected variation in rates under a constant diversification process for only 10 simulations (instead of the default 100) by setting `-BDNN_nsim_expected_cv` to 10, and
* Perform only 25 instead of 100 permutations by specifying `-BDNN_pred_importance_nperm 25`

You can then get the predictor importance with:

* Windows

    ```
    python .\programs\PyRate\PyRate.py ^
    -BDNN_pred_importance .\bdnn_analysis\pyrate_mcmc_logs\Proboscidea_1_G_BDS_BDNN_16_8TVc_mcmc.log ^
    -BDNN_groups "{\"Geography\": [\"Africa\", \"Americas\", \"Eurasia\", \"Island\"], \"Family\": [\"Deinotheriidae\", \"Elephantidae\", \"Gomphotheriidae\", \"Mammutidae\", \"Stegodontidae\", \"OtherFamilies\"]}" ^
    -plotBDNN_transf_features ./bdnn_analysis/Backscale.txt ^
    -b 0.25 ^
    -resample 50 ^
    -BDNN_pred_importance_window_size 0.1 ^
    -BDNN_nsim_expected_cv 10 ^
    -BDNN_pred_importance_nperm 25
    ```

* Mac and Linux

    ```
    python ./programs/PyRate/PyRate.py \
    -BDNN_pred_importance ./bdnn_analysis/pyrate_mcmc_logs/Proboscidea_1_G_BDS_BDNN_16_8TVc_mcmc.log \
    -BDNN_groups '{"Geography": ["Africa", "Americas", "Eurasia", "Island"], "Family": ["Deinotheriidae", "Elephantidae", "Gomphotheriidae", "Mammutidae", "Stegodontidae", "OtherFamilies"]}' \
    -plotBDNN_transf_features ./bdnn_analysis/Backscale.txt \
    -b 0.25 \
    -resample 50 \
    -BDNN_pred_importance_window_size 0.1 \
    -BDNN_nsim_expected_cv 10 \
    -BDNN_pred_importance_nperm 25
    ```

#### Assessment of significant rate variation

The `-BDNN_pred_importance` command creates several files in the _pyrate_mcmc_log_ folder. The `_coefficient_of_rate_variation.csv` file summarizes the variation in the inferred speciation and extinction rates among taxa and compares them with the upper 95% quantile of rate variation under a constant diversification process with the same root age and a similar number of taxa ± 25% as the analysed dataset. An output with higher empirical rate variation than expected permits to dig into which predictors are mainly causing this variation.

| rate | cv_empirical | cv_expected |
|:---- |:------------:|:-----------:|
speciation | 0.61 | 0.17
extinction | 1.06 | 0.23

#### Ranking the predictors

The files `_sp_predictor_influence.csv` and `_ex_predictor_influence.csv` provide the ranked importance for the predictor variables (i.e. the features of the neural network) according to the consensus across three explainable artificial intelligence metrics. The main parts of the table are exemplified here for the three most important predictors of extinction:

| feature1 | feature1_state | posterior_probability | shap | delta_lik | rank |
|:-------- |:-------------- | ---------------------:| ----:| ---------:| ----:|
Family | Deinotheriidae_Gomphotheriidae| 0.94 | 0.45 | -105.4 | 2
Paleotemperature | none | 1.00 | 0.64 | -176.9 | 1
Humans | 0_1 | 1.00 | 0.58 | -40.6 | 2
time | none | 0.86 | 0.09 | -24.1 | 4

The column `feature1` lists the predictors, `feature1_state` shows the pairwise comparison for categorical predictors, `posterior_probability` quantifies the consistency of the direction of the predictors' effect (e.g. the proportion of the 50 sub-sampled MCMC generations for which the family Deinotheriidae had a lower extinction rate than Gomphotheriidae), `shap` measures the effect size of the predictor (e.g. their extinction rate differs by 0.45 units), `delta_lik` is the decrease in model likelihood when permuting the predictor, and finally the `rank` column provides the consensus among the individual importance ranking of these three metrics. Due to the shortcuts taken to make this step faster, there could be ties in the ranks (e.g. between the predictor _Paleotemperature_ and _Humans_)
