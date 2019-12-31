This code was for the original Example 1, the first one-dimensional variable
coefficient acoustics example, presented in the preprint version of
''Analysis and Performance Evaluation of Adjoint-Guided Adaptive Mesh Refinement Using Clawpack''.

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

* Go to the main folder **acoustics_1d_ex1** and run in the terminal:

```
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.

### Extra Python Scripts

If you run the script generate_tolplots.py in the terminal you will generate 
the tolerance, error, and CPU timing plots that appear in the paper. 


