This code produces Example 2, the two-dimensional variable coefficient acoustics example, presented in ''Analysis and Performance Evaluation of Adjoint-Guided Adaptive Mesh Refinement Using Clawpack''.

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

* Go to the main folder **acoustics_2d_ex3** and run in the terminal:

```
make new
make .plots
```

The code will produce two new folders: _output and _plots. 
The first one contains all the output files, while the latter one contains the plots and interactive 
visualization apps.

### Extra Python Scripts

To run all the tests reported in the paper:

    # first run the code in adjoint subdirectory if you haven't already

    make .output -f Makefile_fine  # create reference solution
    python run_tests.py  # runs all tests

The results will be summarized in timings_errors.txt, listing both CPU
times and error estimates over [t1, t2].

The script make_cpu_vs_error_plot.py creates the performance plot in the
paper.

To make the gauge plots, the script plotgauge.py can be used. This requires
running the fine grid code and also the adjoint-error code with at least 3
tolerances and saving the results into directories named as indicated in
the script.


    
