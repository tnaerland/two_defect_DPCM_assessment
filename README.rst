===========================================================
Two Defect DPCM Assessment 
===========================================================
 
:Author: Tine Uberg Naerland <tine.uberg@gmail.com>
:License: BSD license 2.0

If you are searching for specific examples of a work session, please refer to
the reference in the tail of this document. The code is under the BSD 2.0 license. As an additional clause, you are also required to cite the original release paper when using it in a scientific publication: ` Is it possible to unambiguously assess the presence of two defects by temperature and injection dependent lifetime spectroscopy?` (see the tail of this document for details)
 
 
Prerequisites
-------------
 
* The source depends on Python-XY version 2.7.10.0, a scientific python package distribution available from http://python-xy.github.io/downloads.html. 
 
* In addition the following libraries need to be installed using the python package manager: `progressbar <https://pypi.python.org/pypi/progressbar2>`_
 
Data
--------------------
 
In the data folder there are three sub-folders. All of them are containing four types of files:

* A file containing the lifetime data as basis for the DPCM plot analysis. This file is a txt file ending with “curves”
* A file showing the lifetime curves. This file is a png file ending with a letter (or nothing in case of the pure defects)
* A file with the DPCM plot. This file is a png file ending with “curves”
* A file containing the metrics of the DPCM analysis. Max_Et, Min_Et, Max_k and Min_k gives the lower and higher Et and k values corresponding to an additional 2.5% on the min_ARV. (This information is not used in the paper referenced below). “min_residual_value_used_in_plot” is giving the minimum ARV value for the plot overall. “min_residual_value_used_in_plot_Et” and “min_residual_value_used_in_plot_k” are giving the Et and k values of the “min_residual_value_used_in_plot”. This file is a txt file ending with “metrics”
 
 
Combinations of defects
''''''''''''''''''''''''
In the sub-folder ‘Combinations of defects’ there is one sub-folder per defect considered. In each of these sub-folder there is one separate sub-folder for each of the other respective defects that are combined with the defect. As an example, in the following folder “Data/Combinations of defects/Au/CuI” the CuI defect in combination with Au can be found.
In the folder with the raw files there are four sets of files as described above. The sets of files are identified with letters ‘a’ – ‘d’. In the “Combinations of defects” folder these letters refer to the fractions 50%, 62.5%, 75%, and 87.5% of the defect in the upper sub-folder. I.e. in “Data/Combinations of defects/Au/CuI” the files have a dominance of Au concentration wise. The reason for only probing half of the fractions in each folder is to omit generating equal data when CuI is combined with Au. The code itself could have been developed to omit the same combinations as have already been ran, but for now, this is how it is written.
All the metrics are gathered and ordered in the file metrics on the root of ‘Combinations of Defects’
 
Pure defects
''''''''''''''''''''''''
 
In the sub-folder ‘Pure defects” there is one sub-folder per defect considered.
In here there are four sets of files as described above, each corresponding to the 100% pure defect.
The metrics from the DPCM analysis are gathered and ordered in the file metrics on the root of ‘Pure defects’.
 
Combined and pure defects analyzed for different injection ranges
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
In this folder there are 2 sub-folders: one for the combined defects and one for the pure defects. In both cases there are three sub-folders corresponding to analysis made at low injection (1e13-1e14 cm-3), mid injection (1e14-1e15 cm-3), and high injection (1e15-1e16).
In the case of the combined defects, these are all arranged as in the ‘Combined defects’, explained above. Notice that the data in these folders always corresponds to the 50/50% combination of the defects. For more information see the paper references in the tail of this document.
 
Simulation Code
--------------------
 
The simulation code folder contains two sub-folders; (i) Defect Combinations and (ii) Pure Defects. Both of these sub-folders contain the same four python files; 

* Step 1 Calculation of tau_p0
* Step 2 Simulating lifetime curves
* Step 3 DPCM plot – TIDLS
* Step 4 Gather metrics
 
 
Step 1 Calculation of tau_p0
'''''''''''''''''''''''''''''
This is the initial file where we define the defects, the fractions and some of the material properties. (The same values will be repeated in the other steps and needs to kept consistent.) Step 1 will calculate τ_p0 values in correspondence with the fractions chosen that will give us a lifetime curve at room temperature equaling approximately 50 µs at 5 ⨯ 1014 cm-3 (the mid-point of the injection range for the DPCM analysis). The reason why we want to keep the lifetime curves around 50 µs is to assure that the lifetime curves falls in a lifetime range covered by our DPCM analysis. (We could have extended the lifetime range of the DPCM analysis, but this would either lengthen the simulations or cause higher error.) 
When we run the ‘Step 1 Calculation of tau_p0’ it will produce a folder in the directory called tau_p0_data with folders for all the defects, and in sub-folders under each defect, the will be respective defects that the defect in the first sub folder is combined with. In the second defect sub-folder a file “tau_p0_rawdata” containing information of the defects to be combined, the fractions and the tau_p0 value corresponding to these fractions is saved. 
The process should maximum take a couple of minutes. The num=10000 in line 32: tau_p0_1 = np.logspace(-7, 1, num=10000) can be made smaller to shorten the time.

 
Step 2 Simulating lifetime curves
''''''''''''''''''''''''''''''''''' 
This step produces the lifetime curves in the respective sub-folders from the information given in the “tau_p0_rawdata” from Step 1. From this step one figure file displaying the lifetime data is produced in addition to a text-file with lifetime values for a specific set of injection values defined in the code of the Step 2. It is this text file that the Step 3 DPCM plots reads from.
The script as is should take approximately 10 min to run. 

Step 3 DPCM plot – TIDLS
'''''''''''''''''''''''''''''''''''
This step produces the DPCM plots and also a text file with some defined metrics as explained above under ‘Data’. Depending on the resolution defined by the following parameters

``Et = np.linspace(0.0, 1.125, num=150)``

``k = np.logspace(-3, 3, num=150)``

``tau_p0 = np.logspace(-13, -3, num=700)`` 

the simulations will take minutes to weeks. With the parameters listed above DPCM-plots as reported in the paper referenced below are produced, but each plot takes approximately two hours to produce. 
 
Step 4 Gather metrics
''''''''''''''''''''''''''''''''''' 
To easier access the metrics produced from Step 3 a script ‘Step 4 Gather metrics’ was made. This script will collect all the metrics from all the files in the sub-folders and list them in a csv-file ‘metrics.csv’ that will be located at the root together with the python files.
 
Details and Examples
--------------------
 
Please refer to the reference below
 
 
Bibtex entry
------------
 
When using *Two Defect DPCM Assessment* in a publication, please acknowledge the code by citing the following paper. 

.. code::
 
    @article{Naerland:2017a,
          author         = "Naerland, Tine and Bernardini, Simone and Bertoni, Mariana"
          title          = "{ Is it possible to unambiguously assess the presence of two defects by temperature and injection dependent lifetime spectroscopy?}",
          journal        = "JPV",
          volume         = "",
          pages          = "",
          doi            = "",
          year           = "2017",    }


