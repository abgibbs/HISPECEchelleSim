# HISPECEchelleSim
### Requirements / Setup
The primary requirement for running the echelle sim is the _pyechelle_ package. There is a fork of the original package, which makes using custom efficiency data work. Install it directly from the [gitlab repo](https://gitlab.com/abgibbs/pyechelle.git) using pip. Note that pyechelle requires python 3.8 or newer for some of its dependencies.

After installing pyechelle, locate its root directory and copy the contents of the HISPECEchelleSim/hdf folder into the pyechelle/models folder, replacing the available_models.txt file. This is just making the HISPEC .hdf models available for use with pyechelle.  

#### PSI-SIM
We use the PSI-SIM package for collecting planetary and stellar spectra, and to calculate instrument throughput and thermal backgrounds. Install it from [github](https://github.com/planetarysystemsimager/psisim.git). You do not need to have the optional EXOSIMS or PICASO packages working.

#### HxRG Noise Generator
To simulate realistic detector noise, we use the nghxrg package. Once again, it can be installed from [github](https://github.com/BJRauscher/nghxrg.git).

### Current Notebooks
The Constant Trace Creation notebook is used to simulate a constant flux across all HISPEC fibers. This can be used for trace fitting and demonstrates the basic scripting of pyechelle.

The Standard Star Tutorial is WIP to simulate an observation of a standard star with realistic LFC, science, and sky background fibers, as well as the addition of detector noise. It should be noted that it is a best guess at what the LFC, science, and sky fiber outputs will look like and is not a finished product, but it does demonstrate the use of custom spectra with pyechelle.

### Newest Models ###
The latest HISPEC Zemax models for PyEchelle are 20231006A for yJ and 20231006B for HK. New hdf files for these specific models were made. This also incorporated an update to PyEchelle these more uniformly sampled the PSF, buts an issue arises now where the Zemax file sometimes craps out when providing the Huygens PSF for some reason that I haven't been able to replicate in the command line. 

These new hdf files contain the information of all three fibers in one file - the SimulateTelluric_HK.py and SimulateTelluric_YJ.py scripts show how they can be read in within the Pyechelle framework. To acquire these hdf files which are close to 1 GB large each, go to the HISPEC SharePoint under HISPEC - Sybsystems [L3]/ Data Reduction Pipeline [DRP]/Simulated Data/Pyechelle Inputs/. Download the files (HISPEC_20231006A_YJ.hdf and HISPEC_20231006A_HK.hdf) and place them into the pyechelle/models folder for PyEchelle.
