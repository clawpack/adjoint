The code in this repository supplements a paper that is currently in production.


## Computational Experiments for the paper Analysis and Performance Evaluation of Adjoint-Guided Adaptive Mesh Refinement Using Clawpack

The code in this repository supplements the paper (currently in production): "Analysis and Performance Evaluation of Adjoint-Guided Adaptive Mesh Refinement Using Clawpack."

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

### Examples Included and Folder Organization

* **acoustics_1d_ex1:** contains the code to run the first one-dimensional variable coefficients 
linear acoustics equations example. 
The internal folder: **adjoint**, contains the code for the adjoint problem. 

* **acoustics_1d_ex2:** contains the code to run the second one-dimensional variable coefficients 
linear acoustics equations example. 
The internal folder: **adjoint**, contains the code for the adjoint problem. 

* **acoustics_2d_ex1:** contains the code to run the first two-dimensional variable coefficients 
linear acoustics equations example. 
The internal folder: **adjoint**, contains the code for the adjoint problem. 

* **acoustics_2d_ex2:** contains the code to run the second two-dimensional variable coefficients 
linear acoustics equations example. 
The internal folder: **adjoint**, contains the code for the adjoint problem. 

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
