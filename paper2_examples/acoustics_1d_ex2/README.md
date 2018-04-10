This code produces Example 2, the second one-dimensional variable coefficient acoustics example, presented in ''Analysis and Performance Evaluation of Adjoint-Guided Adaptive Mesh Refinement Using Clawpack''.

### Folder Organization
* **adjoint:**

Contains code to solve the adjoint problem.

The start and end times specified in this directory should agree with those for the forward code.

### Running the Code

* Go to the folder **adjoint** and run in a terminal:

```
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.

* Go to the main folder **acoustics_1d_ex2** and run in the terminal:

```
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.


