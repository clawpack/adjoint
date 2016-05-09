## Computational Experiments for Use of the Adjoint Method in Adaptive Mesh Refinement

This code implements a method for identifying and refining the computational grid only in 
regions that will influence a given target area in a specified time range. 

The goal is to continue adding other examples using the adjoint method to guide adaptive mesh refinement to 
this repository. 

The code in the repository **method-sw-paper** supplements the paper: "Adjoint Methods for Guiding Adaptive Mesh Refinement in Tsumani Modeling."

The code is designed to work with the Clawpack 5 software. For more information visit 
[the Clawpack webpage](http://www.clawpack.org/ ). 
The Clawpack software is open source, and the code is openly available at 
[Clawpack on GitHub](https://github.com/clawpack/clawpack). Some of the main algorithms used in this 
project can be found in the book 
[Finite Volume Methods for Hyperbolic Problems](http://depts.washington.edu/clawpack/book.html), although 
the use of the adjoint method for guiding adaptive mesh refinement in Clawpack is new to this work. 

### Software Dependencies
**All the required software is open source.**

* gfortran 5.0.0
* python 2.7.10
* clawpack 5.3.0 : [Clawpack](http://www.clawpack.org/ )
* git: to clone this repository

Note: Clawpack 5.0 or higher is required, other versions of gfortran and python might work as well.

**Operating system.**

* Linux
* Mac OS X

### Examples Included

* 1-dimensional heterogeneous acoustics 
    * An example with wall boundary conditions, and demonstrates both a time point and time range of interest.
* 2-dimensional radially symmetric acoustics 
    * An example with wall boundary conditions, and a time point of interest.
    * An example with wall boundary conditions, and a time range of interest.
    * An example with both wall and outflow boundary conditions, and a time range of interest.
* 2-dimensional shallow water equations 
    * A tsunami propagation example.
* 1-dimensional shallow water equations
    * A tsunami propagation example in one dimension with wall boundary conditions.

### Folder Organization
* **acoustics_1d_heterogeneous:** contains the code to run the 1-dimensional heterogeneous acoustics example. 
The internal folders: 
    * **forward:** contains the code for the forward problem
    * **adjoint:** contains the code for the adjoint problem

* **acoustics_2d:** there are various 2d acoustics examples. They can be found in the following folders: 
    * **radial_timepoint:** contains the code for the example with wall boundary conditions and 
a time point of interest. The internal folder: **adjoint**, contains the code for the adjoint problem.
    * **radial_walls:** contains the code for the example with wall boundary conditions and 
a time range of interest. The internal folder: **adjoint**, contains the code for the adjoint problem.
    * **radial_mixed:**  contains the code for the example with mixed boundary conditions and 
a time range of interest. The internal folder: **adjoint**, contains the code for the adjoint problem.

* **method-sw-paper/tsunami_Alaska:** contains the code to run the 2-dimensional shallow water equations example. 
The internal folder: **adjoint**, contains the code for the adjoint problem. 

* **method-sw-paper/shelf1d:** contains a one dimensional test problem consisting of a flat ocean floor, a
flat continental shelf, and solid wall reflecting boundaries.

### Running the Code
* **Install Clawpack 5.3.0:**
    - Go to: http://www.clawpack.org/installing.html#installation-instructions
    - Follow the download and installation intructions in the section: Install all Clawpack packages 
    - Follow the setup instructions in the section: Set environment variables.
    - Follow the testing instruction in the section: Testing your installation.
        * If your installation works, you already have python and gfortran installed.
        * If your installation does not work, follow the instruction in the section: Installation Prerequisites

* **Clone this repository to your local machine:**
    - In a terminal, go the to main Clawpack directory
    - Create a copy of the adjoint repository by running the code:

```
git://github.com/BrisaDavis/adjoint.git
```

* **Run the code**

    * Go any of the folders and follow the instructions in the README.md in that folder.
