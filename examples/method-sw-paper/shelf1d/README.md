
Modified from clawpack/_apps_tsunami_shelf1d:

Tsunami interacting with 1d continental shelf
=============================================

This one dimensional test problem consists of a flat ocean floor, a
flat continental shelf, and solid wall reflecting
boundaries.

It is designed to illustrate how a tsunami wave is modified as it moves from
the deep ocean onto the continental shelf, and the manner in which some of
the energy can be trapped on the shelf and bounce back and forth.

### Folder Organization
* **adjoint:**

Contains code to solve the adjoint problem.  Data is a square pulse between
limits x1 and x2 specified in setrun.py.  These should be set to specify
the region of interest in the final solution.

The output times specified in this directory should agree with those for the
forward code. Also, note that the time is reversed in the setplot file in the 
after axis function. If the final time is changed, this needs to be updated 
accordingly. 

* **forward:**

Contains code to solve the forward problem.  Initial data is a Gaussian. This 
code generates plots with the forward and the adjoint solutions showed next to each 
other, so it should be run after the adjoint code is run.

### Running the Code

* ** ** Go to the folder **adjoint** and run in a terminal:

```
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.


* ** ** Go to the folder **forward** and run in a terminal:

```
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.

* ** ** Go to the main folder **shelf1d**:

Run one of the following in the terminal:

```
python makeplots.py 
```

Plots forward and adjoint solution and the inner product of the two.

```
python makeplots_t1t2.py 
```

Generalized to the case where the region [x1,x2] is of interest over some
time interval [t1,t2], not just at the final time.  The adjoint solution
is shifted appropriately to compute inner product at each time.