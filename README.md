# HISPECEchelleSim
### Requirements / Setup
The primary requirement for running the echelle sim is the _pyechelle_ package. Install it directly from the [gitlab repo](https://gitlab.com/Stuermer/pyechelle). Installing the pip version may include some bugs that have been otherwise fixed. Note that pyechelle requires python 3.8 or newer for some of its dependencies.

After installing pyechelle, locate its root directory and copy the contents of the HISPECEchelleSim/hdf folder into the pyechelle/models folder, replacing the available_models.txt file. This is just making the HISPEC .hdf models available for use with pyechelle.  

### Current Notebooks
The Constant Trace Creation notebook is used to simulate a constant flux across all HISPEC fibers. This can be used for trace fitting and demonstrates the basic scripting of pyechelle.

The Standard Star Tutorial is WIP to simulate an observation of a standard star with realistic LFC, science, and sky background fibers, as well as the addition of detector noise. It is not currently valid, but does demonstrate the use of custom spectra with pyechelle.
