from math import *
from matplotlib import pyplot as plt
from matplotlib import colors as col
import numpy as np
import sys,os

def cart_comp(x,y):
    """
    A basic comparison function to insure that layers are selected in terms of larger positive to larger negative
    """
    return int(y-x)

def parse_tracer_file(files,overwrite_old_data=False):
    """
    takes iSALE tracer file and appends the information at time 0 and final time and smashes it into a text file with tracer numbers and in a readable format this is then used to generate the final results file which can be used to plot by calling mk_final_results
    @param: file_name -> name of the tracer file 
    @writes: TracerResults/tracer-out.txt -> parsed output file
    """
    out_dict = {}
    for filename in files:

        out_str = ""

        tracer_file_name = filename.split('/')
        tracer_num = tracer_file_name[-1].strip('tracer-').strip('.txt')
        tracer_file = open(filename)

        header = tracer_file.readline().split()
        header = [item for item in header if item != '(m)']
        header_out = tracer_num + '\n'
        for item in header[0:-1]:
            header_out += item + '\t'
        try: header_out += header[3][0:3] + '\t' + header[3][3:6]
        except IndexError: header_out += header[-1]
        out_str += header_out + '\n'

        initial_values = tracer_file.readline().split()
        initial_values_out = 'initial values\t'
        for value in initial_values:
            initial_values_out += value + '\t'
        out_str += initial_values_out + '\n'

        if len(initial_values) > 3:
            max_v1 = float(initial_values[3])
            max_v2 = float(initial_values[4])
            for i,line in enumerate(tracer_file):
                values = line.split()
                try: 
                    if values[3].isalpha(): print("extra header in file: " + filename + " on line: " + str(i)); continue
                except IndexError: continue
                if float(values[3]) > max_v1:
                    max_v1 = float(values[3])
                if float(values[4]) > max_v2:
                    max_v2 = float(values[4])
        else:
            max_v1 = ""
            max_v2 = ""
            for line in tracer_file:
                values = line.split()

        final_values_out = 'final/max values\t'
        for value in values[:3]:
            final_values_out += value + '\t'
        final_values_out += str(max_v1) + '\t' + str(max_v2)
        out_str += final_values_out + '\n'

        if float(initial_values[2]) not in out_dict.keys(): out_dict[float(initial_values[2])] = out_str
        else: out_dict[float(initial_values[2])] += out_str

    keys = out_dict.keys()
    keys.sort(cmp=cart_comp)

    if not os.path.exists("TracerResults/"):
        os.makedirs("TracerResults")
    if overwrite_old_data: output_file = open("TracerResults/tracer-parsed.txt", 'w+')
    else: output_file = open("TracerResults/tracer-parsed.txt", 'a+') #+ tracer_num + "-out.txt", 'a+')

    for key in keys:
        output_file.write(out_dict[key] + "new layer\n")

    tracer_file.close()
    output_file.close()

def mk_final_results(directory="TracerResults", filename='tracer-parsed.txt', overwrite_old_data=False):
    """
    takes parsed tracer file from iSALE and outputs a file containing info such as dip and distance between tracers as well as any saved iSALE plot variables and positions for the first tracer.
    @param: directory -> directory to look for input file
    @param: filename -> name of parsed iSALE tracer file
    @writes: TracerResults/tracer-out.txt containing info meantioned above
    """
    if not directory.endswith('/'):
        directory += '/'
    tracer_out_file = open(directory + filename, 'r')
    if overwrite_old_data: final_results_file = open(directory + 'tracer-out.txt', 'w+')
    else: final_results_file = open(directory + 'tracer-out.txt', 'a+')
    current_tracer = tracer_out_file.readline().strip('\n')
    header = tracer_out_file.readline().split()
    CT_inital_values = map(float,tracer_out_file.readline().split()[2:])
    CT_final_values = map(float,tracer_out_file.readline().split()[2:])
    newlayer = False
    while current_tracer:
        current_tracer_str = ''
        next_tracer = tracer_out_file.readline().strip('\n')
        if next_tracer == 'new layer': next_tracer = tracer_out_file.readline().strip('\n'); newlayer=True
        NT_header = tracer_out_file.readline().split()
        NT_initial_values = map(float,tracer_out_file.readline().split()[2:])
        NT_final_values = map(float,tracer_out_file.readline().split()[2:])
        if len(CT_inital_values) < 3 or len(CT_final_values) < 3 or len(NT_initial_values) < 3 or len(NT_final_values) < 3:
            break
        current_tracer_str += current_tracer + "-" + next_tracer + '\n'
        try: current_tracer_str += 'Time\tXmark\tYmark\tDis\tDip\tAng\t' + header[3] + '\t' + header[4] + '\n'
        except IndexError: current_tracer_str += 'Time\tXmark\tYmark\tDis\tDip\tAng\t' + '\n'
        for CT_values, NT_values in zip((CT_inital_values,CT_final_values), (NT_initial_values,NT_final_values)):
            if CT_values[0] != NT_values[0]:
                break
            CT_x = float(CT_values[1])
            CT_y = float(CT_values[2])
            NT_x = float(NT_values[1])
            NT_y = float(NT_values[2])
            a = (NT_x - CT_x)
            b = (NT_y - CT_y)
            a_d,b_d = abs(a),abs(b)
            c = sqrt(a**2 + b**2)
            if a == 0: theta,theta_d = pi/2,pi/2
            else:
                theta = acos((c**2 + a**2 - b**2)/(2*a*c))*(180/pi)
                theta_d = acos((c**2 + a_d**2 - b_d**2)/(2*a_d*c))*(180/pi)
            if b < 0: theta = -theta
            theta = theta
            if newlayer: c,theta,d_theta = 'None','None','None'; newlayer = False
            try: current_tracer_str += str(CT_values[0]) + '\t' + str(CT_values[1]) + '\t' + str(CT_values[2]) + '\t' + str(c) + '\t' + str(theta_d) + '\t' + str(theta) + '\t' + str(CT_values[3]) + '\t' + str(CT_values[4]) + '\n'
            except IndexError: current_tracer_str += str(CT_values[0]) + '\t' + str(CT_values[1]) + '\t' + str(CT_values[2]) + '\t' + str(c) + '\t' + str(theta_d) + '\t' + str(theta) + '\n'
        final_results_file.write(current_tracer_str)
        current_tracer = next_tracer
        CT_inital_values = NT_initial_values
        CT_final_values = NT_final_values
    tracer_out_file.close()
    final_results_file.close()

def read_tracer_out_file(filepath):
    """
    A utility function that reads in tracer out formated files into a dictionary of layers determined by initial y position each of which contains it's own dictionary of either final or initial values.
    @param: filepath -> the path to the tracer-out file to read in
    """
    tracer_out_file = open(filepath, 'r')
    layers = {}
    line,l = 'mary had a little lamb',0
    while line:
        l += 1
        values = line.split()
        if values[0] == 'Time':
            initial = tracer_out_file.readline().split()
            final = tracer_out_file.readline().split()
            if initial[2] not in layers.keys():
                layers[initial[2]] = {'initial':{}, 'final':{}}
            if ('Xmark_short' not in layers[initial[2]]['initial']):
                layers[initial[2]]['initial']['Xmark_short'] = []
            if ('Ymark_short' not in layers[initial[2]]['initial']):
                layers[initial[2]]['initial']['Ymark_short'] = []
            if ('Xmark_short' not in layers[initial[2]]['final']):
                layers[initial[2]]['final']['Xmark_short'] = []
            if ('Ymark_short' not in layers[initial[2]]['final']):
                layers[initial[2]]['final']['Ymark_short'] = []
            for i in range(len(values)):
                if values[i] not in layers[initial[2]]['initial'].keys():
                    layers[initial[2]]['initial'][values[i]] = []
                if values[i] not in layers[initial[2]]['final'].keys():
                    layers[initial[2]]['final'][values[i]] = []
                if initial[i] == 'None' or final[i] == 'None': continue
                layers[initial[2]]['initial'][values[i]].append(initial[i])
                layers[initial[2]]['final'][values[i]].append(final[i])
                if values[i] == 'Xmark' and 'None' not in initial and 'None' not in final:
                    layers[initial[2]]['initial']['Xmark_short'].append(initial[i])
                    layers[initial[2]]['final']['Xmark_short'].append(final[i])
                elif values[i] == 'Ymark' and 'None' not in initial and 'None' not in final:
                    layers[initial[2]]['initial']['Ymark_short'].append(initial[i])
                    layers[initial[2]]['final']['Ymark_short'].append(final[i])
        line = tracer_out_file.readline()
    return layers

def plot_tracer_data(v,layers_to_plot="All",filepath="TracerResults/tracer-out.txt",title='My_Plot',initial_or_final="fff",size=30,colormap='gist_rainbow',save_plot=False, preform_regression=False, degree_regression=1,display_max_min=False):
    layers = read_tracer_out_file(filepath)
    try:
        legend = []
        x_tot,y_tot,z_tot = [],[],[]
        keys = map(float, layers.keys())
        keys.sort(cmp=cart_comp)
        keys = map(str, keys)
        x_max,x_min,y_max,y_min,z_max,z_min = 0.,1e9,0.,1e9,0.,1e9
        if preform_regression: all_x,all_y = [],[]
        if layers_to_plot=="All": layers_to_plot=range(len(keys))
        if ('Xmark' or 'Ymark' in v):
            if ('Dip' or 'Ang' or 'Dis' in v):
                f = lambda p: p + '_short' if (p == 'Xmark' or p == 'Ymark') else p
                v = map(f,v)
        try: v1,v2,v3 = v
        except ValueError: v1,v2 = v
        x_time,y_time,z_time = None,None,None
        if initial_or_final[0] == 'f': x_time = 'final'
        elif initial_or_final[0] == 'i': x_time = 'initial'
        if initial_or_final[1] == 'f': y_time = 'final'
        elif initial_or_final[1] == 'i': y_time = 'initial'
        if len(initial_or_final) > 2 and len(v) > 2 and initial_or_final[2] == 'f': z_time = 'final'
        elif len(initial_or_final) > 2 and len(v) > 2 and initial_or_final[2] == 'i': z_time = 'initial'
        if not x_time and (not y_time or not z_time):
            print(initial_or_final + " is not a valid time input options are [ff,if,fi,ii,iii,ifi,iff,fii,ffi,fif,fff]")
            return
        for n in layers_to_plot:
            if n > len(keys) or n < -len(keys)-1:
                print("n out of range no corrisponding layer, skipping for n = " + str(n))
                continue
            key = keys[n]
            x_values = layers[key][x_time]
            y_values = layers[key][y_time]
            if z_time: z_values = layers[key][z_time]
            else: z_values = None
            x = map(float,x_values[v1])
            y = map(float,y_values[v2])
            if not x or not y: continue
            if z_values != None:
                z = map(float,z_values[v3])
                if not z: continue
                if max(z) > z_max: z_max = max(z)
                if min(z) < z_min: z_min = min(z)
            if max(x) > x_max: x_max = max(x)
            if min(x) < x_min: x_min = min(x)
            if max(y) > y_max: y_max = max(y)
            if min(y) < y_min: y_min = min(y)
            x_tot += x
            y_tot += y
            if z_values:
                z_tot += z
            else:
                z_tot += [int(float(key)) for i in range(len(x))]
        plot_handle = plt.scatter(x_tot,y_tot,c=z_tot,s=size,cmap=colormap)
        cbar = plt.colorbar()
        if len(v) > 2: cbar.set_label(v3)
        else: cbar.set_label('initial depth')
        plt.xlabel(v1)
        plt.ylabel(v2)
        plt.title(title)
        x_space = max(map(abs,x_tot))
        y_space = max(map(abs,y_tot))
        plt.axis([x_min-.05*x_space,x_max+.05*x_space,y_min-.05*y_space,y_max+.05*y_space])
        if preform_regression:
            polycoefs = np.polyfit(x_tot,y_tot,degree_regression)
            x_range = range(int(min(x_tot)),int(max(x_tot)))
            polyvals = np.polyval(polycoefs,x_range)
            reg = plt.plot(x_range,polyvals)
            plt.setp(reg, color='k', linewidth=3.0)
            regression_entry = ""
            for coef in polycoefs[:-1]:
                regression_entry += str(round(coef,3)) + "*x^" + str(degree_regression) + " + "
                degree_regression -= 1
            regression_entry += str(round(polycoefs[-1],3))
            #regression_entry += str(R_2)
            legend.append(regression_entry)
            plt.legend(reg,legend)
            print("Fit Equation = " + regression_entry)
        if save_plot:
            figure = plt.gcf()
            figure.set_size_inches(16, 9)
            directory = reduce(lambda x,y: x + '/' + y, filepath.split('/')[:-1]) + '/'
            var_out_str = reduce(lambda x,y: x + '_' + y, v)
            if not os.path.exists(directory+'Plots/'): os.mkdir(directory+'Plots/')
            plt.savefig(directory + 'Plots/' + title.replace(' ','_') + '_' + var_out_str + '_' + initial_or_final +'.png',dpi=1296)
        if display_max_min:
            print("lowest layer: " + keys[layers_to_plot[-1]] + ", highest_layer: " + keys[layers_to_plot[0]])
            print(v1 + ": " + "(max = " + str(x_max) + ", min = " + str(x_min) + ")")
            print(v2 + ": " + "(max = " + str(y_max) + ", min = " + str(y_min) + ")")
            if len(v) > 2: print(v3 + ": " + "(max = " + str(z_max) + ", min = " + str(z_min) + ")")
        plt.show()

    except KeyError:
        print("one of the input variables " + str(v) + " does not exist options include: " + reduce(lambda x,y: x + ', ' + y, layers[key][x_time   ].keys()))
    except IndexError:
        print("layer number out of range must be between: [" + str(0) + "," + str(len(layers.keys())-1) + "]")

def __main__():
    """
    DESCRIPTION:
      Creates parsed tracer-out and tracer-parsed files which collect data from a collection of iSALE tracer files and remove extranious information keeping only start and end times as well as compiling all the data in one place and for plot variables it keeps the max value for all time, this then can be used with this script to plot and save plots of this data.

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
        -c -> change the colormap used in the plot (look at matplotlib colormaps) (optional)
        -S -> save plot image (optional)
        -r -> range of depths to plot must be a list of integer rows, or a range start, end, and step size (i.e. [1,2,3,4] or 12,42,3)
        -M -> print max and min values to consul (optional)
        -R -> preform and plot a polynomial regression default degree is 1 (optional)
        -d -> set degree of the polynomial regression (optional)
    """

    if '-h' in sys.argv:
        help(__main__)
    elif '-m' in sys.argv:
        m_index = sys.argv.index('-m')
        overwrite_old_data = False
        if len(sys.argv) < m_index+1:
            print("at least one tracer file path must be specified after the -m flag")
            return
        if '-n' in sys.argv:
            sys.argv.remove('-n')
            overwrite_old_data = True
        parse_tracer_file(sys.argv[m_index+1:],overwrite_old_data)
        mk_final_results(overwrite_old_data=overwrite_old_data)
    elif '-v' in sys.argv:
        args = []
        v_index = sys.argv.index('-v')
        args.append(sys.argv[v_index+1].strip('( )').split(','))
        kwargs = {}
        if '-i' in sys.argv:
            i_index = sys.argv.index('-i')
            kwargs['filepath'] = sys.argv[i_index+1]
        if '-T' in sys.argv:
            T_index = sys.argv.index('-T')
            kwargs['title'] = sys.argv[T_index+1]
        if '-s' in sys.argv:
            k_index = sys.argv.index('-s')
            kwargs['size'] = int(sys.argv[k_index+1])
        if '-c' in sys.argv:
            l_index = sys.argv.index('-c')
            kwargs['colormap'] = sys.argv[l_index+1]
        if '-t' in sys.argv:
            t_index = sys.argv.index('-t')
            kwargs['initial_or_final'] = sys.argv[t_index+1]
        if '-S' in sys.argv:
            kwargs['save_plot'] = True
        if '-r' in sys.argv:
            r_index = sys.argv.index('-r')
            r_val = sys.argv[r_index+1]
            try: kwargs['layers_to_plot'] = range(*map(int,r_val.split(',')))
            except ValueError: kwargs['layers_to_plot'] = map(int,list(r_val.strip('[ ]').split(',')))
        if '-R' in sys.argv:
            kwargs['preform_regression'] = True
        if '-d' in sys.argv:
            d_index = sys.argv.index('-d')
            kwargs['degree_regression'] = int(sys.argv[d_index+1])
        if '-M' in sys.argv:
            kwargs['display_max_min'] = True
        plot_tracer_data(*args,**kwargs)
    else:
        print('no orders detected or bad syntax used try -h')


if __name__=="__main__":
    __main__()
