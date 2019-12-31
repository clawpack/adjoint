
# Computational Experiments to accompany the paper

###  "Analysis and Performance Evaluation of Adjoint-Guided Adaptive Mesh Refinement Using Clawpack" 

by Brisa N. Davis and Randall J. LeVeque

This version goes with version 2 of the paper, currently submitted for publication.

Check out the `paper2v1` branch for the version of the code that accompanies the original preprint https://arxiv.org/abs/1810.00927. 

This version is updated in the following ways:
 - It uses Clawpack v5.6.1, which has the adjoint flagging now built in.
 - Example 1 from the original paper has been dropped from v2 of the paper, so the subdirectories have been renamed.
 
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
* clawpack 5.6.1 : [Clawpack](http://www.clawpack.org/ )
* git: to clone this repository

Note: Later versions of Clawpack should work, other versions of gfortran and python might work as well.

**Operating system.**

* Linux
* Mac OS X

### Examples Included and Folder Organization

* **acoustics_1d_ex1_old:** contains the code to run the first one-dimensional variable coefficients 
linear acoustics example from v1 of the paper, not used in v2 of the paper.
The internal folder: **adjoint**, contains the code for the adjoint problem. 

* **acoustics_1d_example1:** contains the code to run the one-dimensional variable coefficients 
linear acoustics example that is Example 1 in v2 of the paper. 
The internal folder: **adjoint**, contains the code for the adjoint problem. 

* **acoustics_2d_example2:** contains the code to run the first two-dimensional variable coefficients 
linear acoustics problem that is Example 2 in v2 of the paper.
The internal folder: **adjoint**, contains the code for the adjoint problem. 

* **acoustics_2d_example3:** contains the code to run the second two-dimensional variable coefficients 
linear acoustics problem that is Example 3 in v2 of the paper.
The internal folder: **adjoint**, contains the code for the adjoint problem. 

### Running the Code
* **Install Clawpack 5.6.1:**
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
    git clone https://github.com/clawpack/adjoint.git
    cd adjoint
    git checkout paper2v2
```

* **Run the code**

* Go any of the folders in `paper2_examples` and follow the instructions in the README.md in that folder.
