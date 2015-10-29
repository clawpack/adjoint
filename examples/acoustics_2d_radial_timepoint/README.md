This directory contains the code to generate the plots for the
two-dimensional acoustics example with mixed boundary conditions
for the paper "Adjoint Methods for Guiding Adaptive Mesh Refinement."

### Folder Organization
* **adjoint:**

Contains code to solve the adjoint problem.

The output times specified in this directory should agree with those for the
forward code. 

* **compare:**

Contains the code to compare the pressure-flagging and adjoint-flagging methods. This can be used to generate the figures found in the paper, as well as identifying differences in the files used to run each method.


### Running the Code

* Go to the folder **adjoint** and run in a terminal:

```
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.

* Go to the main folder **acoustics_2d_radial_timepoint** and run in the terminal:

```
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.

### Running Variations

* Running the example with adjoint flagging:

Run in the terminal:

```
python run_adjoint_flagging.py
```

* Running the example with pressure flagging:

Go to the folder **compare** and run in the terminal:

```
make new -f Makefile_pflag
make .plots -f Makefile_pflag
```

* To compare the two methods:

Go to the folder **compare** and run in the terminal:

```
python compare_methods.py
```

This will run both the pressure flagging and the adjoint flagging methods. The results from both methods will be compages in the resulting gauge plot. The plots generated are those appearing in the paper. See paper for an analysis of the results. 


