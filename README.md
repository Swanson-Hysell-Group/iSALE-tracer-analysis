# iSALE-tracer-analysis

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
        -v -> specify variables to plot (requres 2 in order to plot)
        -i -> specify input file path for plotting (optional)
        -T -> give plot a title (optional)
        -t -> specify time of simulation to plot currently only initial or final (optional)
        -l -> change line style of plot (for options look at matplotlib linestyle)
        -k -> change marker style of plot (for options look at matplotlib marker)
        -s -> save plot image (optional)
        -r -> range of depths to plot must be a list of integer rows, or integer end range (i.e. [1,2,3,4] or 10=range(10))
        -H -> hide legend (optional)
        -M -> print max and min values to consul (optional)
        -R -> preform and plot a polynomial regression default degree is 1 (optional)
        -d -> set degree of the polynomial regression (optional)

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

## quiver_mag_angle.py

A plotting program that does a quiver plot on angle data for a tracer-out.txt file. Yet to be completed in a usable manner under development.
