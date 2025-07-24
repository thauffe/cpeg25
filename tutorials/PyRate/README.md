# Standard PyRate diversification analysis

## Generating the PyRate input file
### Prepare fossil occurrence table
You can prepare a table with fossil occurrence data in a text editor or a spreadsheet editor. The table must include 4 columns including 1) Taxon name, 2) Status specifying whether the taxon is "extinct" or "extant", 3) Minimum age, and 4) Maximum age. The table should have a header (first row) and **one row for each fossil occurrence** (see example below). Min and max ages represent the age ranges of each fossil occurrence, typically based on stratigraphic boundaries.

If a fossil assemblage or site contains several occurrences we should consider these occurrences as coeval even as we randomize their age within their temporal range. This can be done by specifying a _Site_ column in the input data, with a number specifying the ID of the assemblage for each occurrence. For instance in the example below, the first three occurrences were found in the same site and their random age will be identical.

You can find this table called _Proboscidea.txt_ in the _pyrate_analysis_ folder of your cpeg25 repository.
 
| Taxon\_name   | Status  | MinAge | MaxAge | Site
| ------------- |:-------------:| -----:| -----:| -----:|
Anancus\_kenyensis | extinct | 5.3    | 7.1 | 39
Mammuthus\_subplanifrons | extinct | 5.3 | 7.1  | 39
Stegodon\_kaisensis | extinct | 5.3 | 7.1  | 39
Loxodonta\_africana | extant | 0.012 | 0.126  | 171
Deinotherium\_giganteum | extinct | 11.2 | 12.85  | 159

### Generate the input file using R
The fossil occurrence need to be converted to a PyRate specific format, which will be performed with the help of R.

1. Launch RStudio, the Rgui on Mac and Window, or just R in the terminal of Linux.
2. Set the working directory. This is the path to your cpeg25 repository. Remember to use backslashes on Windows and slashes in Mac/Linux.

    Windows:

    ```
    setwd("c:\...\cpeg25")
    ```

    Mac and Linux:

    ```
    setwd("/Users/.../cpeg25")
    ```

3. Load the *pyrate_utilities.r* file. It is located in your _programs/PyRate_ folder. R's `file.path()` function will take care about slashes or backslashes.

    ```
    path_pyrate_utilities <- file.path("programs", "PyRate", "pyrate_utilities.r")
    source(path_pyrate_utilities)
    ```

4. Generate the input file for PyRate. We need to provide the path to the occurrence table as an argument to the `extract.ages()` function. We specify `replicate = 10` to generate 10 replicates, in each of which the fossil ages are randomized within their minimum and maximum boundaries. `outname = ""` omits any additional suffix to the name of the input file.

    ```
    path_occurrence_table <- file.path("pyrate_analysis", "Proboscidea.txt")
    extract.ages(path_occurrence_table, replicates = 10, outname = "")
    ```

5. Move the inpute file to the directory of BDNN analysis. Because we use the generated file for the PyRate and the BDNN practical, we move it into the directory of the respective tutorial. You can do this with your file manager, but we now do this quickly in R.

    ```
    from_pyrate <- file.path("pyrate_analysis", "Proboscidea.py")
    to_bdnn <- file.path("bdnn_analysis", "Proboscidea.py")
    file.copy(from = from_pyrate, to = to_bdnn, overwrite = TRUE)
    ```

## PyRate: inferring speciation and extinction rates through time

### Navigate to your cpeg25 repository and activate the virtual environment
The PyRate inference will be performed in your command window or terminal and make use of your virtual environment. Move into your cpeg25 repository and activate the venv.

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

### Running PyRate MCMC
To run PyRate, we need to tell ```python``` to execute the ```PyRate.py``` program and provide the input file that we just generated in R.

You can write the respective command in a single line in your terminal. Please, do not execute it yet.

* Windows

    ```
    python .\programs\PyRate\PyRate.py .\data\Proboscidea.py
    ```

* Mac and Linux

    ```
    python ./programs/PyRate/PyRate.py ./data/Proboscidea.py
    ```

However, this command may get long when you want to add optional arguments for your analyses (e.g. a different preservation model). It is often easier and safer to write your command first in an text editor and then paste it into the terminal. You can add line breaks to separate the individual commands. Windows uses ^ in the command window while Mac/Linux requires a backslash.

We specify here a model of preservation assuming that preservation rates are constant within a predefined time frame, but can vary across time frames (e.g. geological epochs). This time-variable Poisson process (TPP) model is useful if we expect rate heterogeneity to occur through time. With the `-qShift` flage, you provide the path to a text file with stage boundaries in your _data_ folder.

This models can be coupled with a Gamma model of rate heterogeneity, which enables us to account for heterogeneity in the preservation rate across lineages. To set the Gamma model we add the flag `-mG`.

Lastly, we set the number of mcmc generation `-n`, the sampling frequency of the mcmc chain `-s`, and the print frequency `-p`.

* Windows

    ```
    python .\programs\PyRate\PyRate.py ^
    .\pyrate_analysis\Proboscidea.py ^
    -qShift .\data\Stages.txt ^
    -mG ^
    -n 500000 -s 5000 -p 100000
    ```

* Mac and Linux

    ```
    python ./programs/PyRate/PyRate.py \
    ./pyrate_analysis/Proboscidea.py \
    -qShift ./data/Stages.txt \
    -mG \
    -n 500000 -s 5000 -p 100000
    ```

<img src="https://github.com/thauffe/cpeg25/blob/main/pictures/pyrate_run.png" alt="terminal pyrate" width="700">

Terminal output of the initialized PyRate analysis, which will take ca. 3 minutes to complete 500,000 MCMC iterations.

### Inspecting the MCMC log file
The PyRate run creates a new folder called _pyrate_mcmc_logs_ in your _pyrate_analysis_ directory. Within this new folder, you will find the MCMC log file called _Proboscidea_1_Grj_mcmc.log_. You can use the program _Tracer _ to check the analysis for convergence and the approximate length of the burn-in period.

### Plotting speciation and extinction rates through time
The _sp_rates.log_ and _ex_rates.log_ files form the _pyrate_mcmc_logs_ folder can be used to generate rates-through-time plots using the function `-plotRJ`. The flag `-b` specifies the burn-in period, which we set to 25%. 

* Windows

    ```
    python .\programs\PyRate\PyRate.py \
    -plotRJ .\pyrate_analysis\pyrate_mcmc_logs \
    -b 0.25
    ```

* Mac and Linux

    ```
    python ./programs/PyRate/PyRate.py \
    -plotRJ ./pyrate_analysis/pyrate_mcmc_logs \
    -b 0.25
    ```

<img src="https://github.com/thauffe/cpeg25/blob/main/pictures/pyrate_rtt.png" alt="RTT" width="1000">

Proboscidea speciation rate through time and frequency of Bayes Factors indicating significant posterior probability of a ate shift. 

This will generate an R script and a PDF file in your _pyrate_mcmc_logs_ folder with plots visualizing rates through time. It will also show histograms with the inferred times of rate shifts and calculate Bayes Factors to help determining the time when a rate shift is supported by significant posterior probability. The histograms include two horizontal dashed lines showing the thresholds for positive evidence of a rate shift (bottom line: logBF = 2) and for strong evidence of a rate shift (top line: logBF = 6). Thus, any point in the histogram showing sampling frequencies for a rate shift exceeding the thresholds indicate a time of significant rate change.

