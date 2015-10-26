This code produces the shallow water equations tsunami example presented in the paper "Adjoint Methods for Guiding Adaptive Mesh Refinement." 


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
visualization apps.

### Running Variations

* Running the example with adjoint flagging:

Run in the terminal:

```
python run_adjoint_flagging.py
```

* Running the example with surface flagging:

Run in the terminal:

```
python maketopo.py
make new -f Makefile_sflag
make .plots -f Makefile_sflag
```

* To compare the two methods:

Run in the terminal:

```
python compare_methods.py
```

This will run two version of the surface-flagging method (one with a low tolerance and one with a high tolerance), and the adjoint-flagging method. The output at the two gauges will be compared in the gauge plot. See the paper for analysis on the results.