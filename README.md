# iSALE-tracer-analysis

## mk_tracer_files.sh

A bash script to run in parallel iSALEPlot on a simulation creating the large set of tracer-#.txt files that are needed to create a decent resolution plot using tracer_interperter.py or quiver_mag_angle.py. Usage is as follows:

```bash
~/$ chmod a+x mk_tracer_files.sh
~/$ ./mk_tracer_files.sh [PATHTOPLOT.inp] [PATHTODATA.dat] [LOGFILEPATH]
```

The .inp file format can be found in the iSALEPlot documentation, and the .dat file should be the simulations data file output. The last argument is simply where you want the log file to be placed for this run, the log file is simply a text file that records the latest tracer to be anaylized. This script runs iSALEPlot in batches of 20 parallel processes from tracer = 0 to tracer = 10000, which is usually a decent level of resolution for a simulation. If more files are required simply edit the bounds of the first for loop in the script.

## tracer_interpreter.py

tracer_interpreter.py is the main analysis program. This library contains the functions that create the tracer-out.txt file that compiles all of the tracer-#.txt files from the iSALEPlot program, as well as the functions that read and plot the tracer-out files data. 

### creating the tracer-out.txt file

once you've made the tracer-#.txt files using the iSALEPlot program provided with iSALE you can proceed to create the tracer-out.txt. This is done by passing all of the tracer-#.txt files into the tracer_interpreter.py program with the -m flag as follows:

```bash
python tracer_interpreter.py -m tracer-*.txt
```

This will result in the creation of a TracerResults directory in the WD and the output of a tracer-parsed.txt and a tracer-out.txt in the TracerResults directory. By default running this appends data to any pre-exsisting tracer-out.txt file in the TracerResults directory if you would rather overwrite any pre-exsisting tracer-out.txt file use the -n flag in addition to the -m flag. From here you can proceed to analysis.

### analysis of tracer data

There are many options to control the plots output by the tracer_interpreter.py program if at anytime you need to check the function of these different flags simply use the -h flag to display the help message with full documentation. Here is a list of all options:

    SYNTAX:
        python tracer_interperter.py -[FLAG] [INPUT]

    FLAGS:
        -h -> print this help message
        -m -> make the parsed tracer files used to plot must be followed by input tracer files path
        -n -> overwrite any prexsiting tracer-out file
        -v -> specify variables to plot in a tuple format (i.e. (Xmark,Ymark), requres 2 in order to plot, can plot up to 3)
        -i -> specify input file path for plotting (optional)
        -T -> give plot a title (optional)
        -t -> specify time of simulation to plot currently only initial or final (optional)
        -s -> change size of markers (size in pixels, default = 30)
        -c -> change the colormap used in the plot (look at matplotlib colormaps)
        -S -> save plot image (optional)
        -r -> range of depths to plot must be a list of integer rows, or a range start, end, and step size (i.e. [1,2,3,4] or 12,42,3)
        -M -> print max and min values to consul (optional)
        -R -> preform and plot a polynomial regression default degree is 1 (optional)
        -d -> set degree of the polynomial regression (optional)

## quiver_mag_angle.py

A plotting program that does a quiver plot on angle data for a tracer-out.txt file, as well as colormaps for another variable. Usage similar to tracer_interperter, and due to dependencies in tracer_interperter they must be placed in the same directory to both work.

    SYNTAX:
        python quiver_mag_angle.py [-FLAGS] [SYNTAX]

    FLAGS:
        -h -> print this help message
        -i -> set input filepath (optional; default=TracerResults/tracer-out.txt)
        -a -> choose angle variable to display (optional; options Ang,Dip; default=Ang)
        -v -> choose colormap variable (optional;default=initial depth)
        -r -> range of depths to plot must be a list of integer rows, or a range start, end, and step size (i.e. [1,2,3,4] or 12,42,3) (optional; default=All)
        -t1 -> title of the initial plot (optional)
        -t2 -> title of the final plot (optional)
        -S -> save plot image (optional)
        -c -> choose colormap (optional; default=gist_rainbow)

## cleanup_tracer_data.py

A basic python script developed to allow easy trimming of the tracer-out.txt data. Basic usage of this script can be seen bellow:

    SYNTAX:
        python cleanup_tracer_data.py [tracer-out.txt] -[FLAG] [INPUT]

    FLAGS:
        -h -> print this help message
        -i -> cut data by initial value instead of final values as is default
        -ch -> cut data by x value from the right, input must be a number (float or int) that represents in km the maximum x value allowed, cutting all data with a larger x value than the input. (optional)
        -cvu -> cut data by y value from above so that input is the largest allowed y value in km (optional)
        -cvd -> cut data by y value from bellow so that input is the smallest allowed y value in km (optional)
