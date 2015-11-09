This code produces the shallow water equations tsunami example presented in the paper "Adjoint Methods for Guiding Adaptive Mesh Refinement." 

### Folder Organization
* **adjoint:**

Contains code to solve the adjoint problem.

The output times specified in this directory should agree with those for the forward code.

* **compare:**

Contains the code to compare the surface-flagging and adjoint-flagging methods.
This can be used to generate the figures found in the paper, as well as identifying differences 
in the files used to run each method.

### Running the Code

* Go to the folder **adjoint** and run in a terminal:

```
python maketopo.py
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.

* Go to the main folder **tsunami_Alaska** and run in the terminal:

```
python maketopo.py
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps. Note that this simulation takes a long time to complete.

### Running Variations

* Running the example with adjoint flagging:

Run in the terminal:

```
python run_adjoint_flagging.py
```

* Running the example with surface flagging:

Go to the folder **compare** and run in the terminal:

```
python maketopo.py
make new -f Makefile_sflag_lowtol
make .plots -f Makefile_sflag_lowtol
```

or:

```
python maketopo.py
make new -f Makefile_sflag_hightol
make .plots -f Makefile_sflag_hightol
```

The first of these will run the example with a tolerance of 0.14, and the second will run 
the example with a tolerance of 0.09. This tolerance is set in setrun_sflag_lowtol.py and 
setrun_sflag_hightol.py. Note that both of these simulations take a long time to complete.

* To compare the two methods:

Go to the folder ** compare** and run in the terminal:

```
python compare_methods.py
```

This will run two version of the surface-flagging method (one with a low tolerance and one
 with a high tolerance), and the adjoint-flagging method. The output at the two gauges will 
be compared in the gauge plot. See the paper for analysis on the results.

Note that this runs three GeoClaw simulations, and therefore takes a long time to complete.
