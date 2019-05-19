## clawpack/adjoint

The code in this repository supports flagging cells for refinement (in either AMRClaw or GeoClaw) based on the solution of an adjoint equation.

This work in progress is part of the PhD thesis research of Brisa Davis (@BrisaDavis).  Some details on this approach and sample results can be found in the papers:
 
    - B. N. Davis, and R. J. LeVeque, Adjoint Methods for Guiding Adaptive Mesh Refinement
    in Tsunami Modeling, in Global Tsunami Science: Past and Future, Volume I, 2017, pp.
    4055-4074.

The general approach is to first solve the adjoint equation (which is itself a hyperbolic PDE) backwards in time from the desired final time T of the "forward problem" to its initial time t_0.  The data for the adjoint equation is some function phi designed so that the inner product of phi with the solution q at the final T (and perhaps at earlier times) is the quantity of interest (QoI). Solving the adjoint equation extends this to a function phi(x,t) defined for all t (in one space dimension). An appropriate inner product of phi(x,t) with the computed solution q(x,t) can then be used to flag the grid cells where the solution at time t will have an effect on the QoI at time T. If the problem is autonomous in time then the inner product of q(x,t) with phi(x,t+tau) will indicate the cells where the forward solution at time t will affect the QoI at time T-tau.  

It is assumed that the forward problem is linear (perhaps with spatially varying coefficients) so that the adjoint equation is independent of the forward solution.  Some examples are included for acoustics (in 1 and 2 dimensions) and tsunami modeling with GeoClaw (where we wish to track waves on the ocean scale that will reach a particular target community, in which case the adjoint can be based on the shallow water equations linearized about the ocean at rest).

The general strategy is:

 1. Solve the adjoint equation backward in time on a uniform and relatively coarse grid, saving the solution at particular times T, T-dT, T-2*dT, ..., t_0
 
 2. Solve the forward equation from time t_0.  At each regridding time interpolate in space and time as needed to compute inner products with the saved adjoint solution.
 

  
Several improvements are under development, including:

 - Performing better error estimation based on the adjoint solution, rather than simply flagging cells where the inner product of forward and adjoint solutions is above some threshold,
 - Allowing AMR to be used in step 1, for the solution of the adjoint equation.


This code was recently updated to work with the Clawpack 5.4.0 software. For more information visit 
[the Clawpack webpage](http://www.clawpack.org/ ). 
The Clawpack software is open source, and the code is openly available at 
[Clawpack on GitHub](https://github.com/clawpack/clawpack). Some of the main algorithms used in this 
project can be found in the book 
[Finite Volume Methods for Hyperbolic Problems](http://depts.washington.edu/clawpack/book.html), although 
the use of the adjoint method for guiding adaptive mesh refinement in Clawpack is new to this work. 

### Software Dependencies

The examples were recently updated to Clawpack 5.4.0 form (only changes to the Makefiles were required and version 5.3.0 Makefiles are also inculded in some examples).

The [Clawpack prerequisites] include Fortran and Python.  Then see then [Clawpack installation instructions](http://www.clawpack.org/installing.html), and finally clone this repository as a subdirectory of `$CLAW` in order for the Makefiles to work properly (see [Setting environment variables](http://www.clawpack.org/setenv.html))


### Examples Included

* 1-dimensional heterogeneous acoustics 
    * An example with wall boundary conditions, and demonstrates both a time point and time range of interest.
* 2-dimensional radially symmetric acoustics 
    * An example with wall boundary conditions, and a time point of interest.
    * An example with wall boundary conditions, and a time range of interest.
    * An example with both wall and outflow boundary conditions, and a time range of interest.
* 2-dimensional shallow water equations 
    * A tsunami propagation example.

### Folder Organization

### *paper1_examples*

The examples in this folder are published in 

B. N. Davis, and R. J. LeVeque, Adjoint Methods for Guiding Adaptive Mesh Refinement
in Tsunami Modeling, in Global Tsunami Science: Past and Future, Volume I, 2017, pp.
4055-4074.

This paper can be found at: 
https://link.springer.com/article/10.1007/s00024-016-1412-y

This code has been modified since the publication of this paper. 
To download a copy of the code at the time of publication please see 

https://github.com/BrisaDavis/adjoint/releases/tag/paper1_aspublished

### *examples*

This folder contains suplimentary examples using the adjoint method. 
Analysis of these examples can be found in the pre-print

    Adjoint Methods for Guiding Adaptive Mesh Refinement in Wave Propagation Problems

This pre=print can be found at: 
https://arxiv.org/abs/1511.03645

The majority of the content of this pre-print was re-worked and appeared in 
"Adjoint Methods for Guiding Adaptive Mesh Refinement in Tsunami Modeling".

* **acoustics_1d_heterogeneous:** contains the code to run the 1-dimensional heterogeneous acoustics example. 
The internal folders: 
    * **forward:** contains the code for the forward problem
    * **adjoint:** contains the code for the adjoint problem

* **acoustics_2d:** contains the code to run the 2-dimensional acoustics examples. The internal folders: 
    * **radial_timepoint:** contains the code for the example with wall boundary conditions and 
a time point of interest. The internal folder: **adjoint**, contains the code for the adjoint problem.
    * **radial_walls:** contains the code for the example with wall boundary conditions and 
a time range of interest. The internal folder: **adjoint**, contains the code for the adjoint problem.
    * **radial_mixed:**  contains the code for the example with mixed boundary conditions and 
a time range of interest. The internal folder: **adjoint**, contains the code for the adjoint problem.
    * **src:** contains all of the code that is common between the three 2-dimensional acoustics examples.

### Running the Code

After installing Clawpack and other prerequisites, clone this repository and then go any of the folders and follow the instructions in the README.md in that folder.
