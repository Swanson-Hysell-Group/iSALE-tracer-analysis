from math import *
from matplotlib import pyplot as plt
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
            for i in range(len(values)):
                if values[i] not in layers[initial[2]]['initial'].keys():
                    layers[initial[2]]['initial'][values[i]] = []
                if values[i] not in layers[initial[2]]['final'].keys():
                    layers[initial[2]]['final'][values[i]] = []
                try:
                    if 'Xmark_short' or 'Ymark_short' not in layers[initial[2]]['initial']:
                        layers[initial[2]]['initial']['Xmark_short'] = []
                        layers[initial[2]]['final']['Xmark_short'] = []
                        layers[initial[2]]['initial']['Ymark_short'] = []
                        layers[initial[2]]['final']['Ymark_short'] = []
                        last_ix = 1
                        last_fx = 1
                        last_iy = 1
                        last_fy = 1
                    if ('None' in initial or 'None' in final) and ('Xmark' and 'Ymark' in layers[initial[2]]['initial'].keys()):
                        layers[initial[2]]['initial']['Xmark_short'] += layers[initial[2]]['initial']['Xmark'][last_ix:-1]
                        layers[initial[2]]['final']['Xmark_short'] += layers[initial[2]]['final']['Xmark'][last_fx:-1]
                        layers[initial[2]]['initial']['Ymark_short'] += layers[initial[2]]['initial']['Ymark'][last_iy:-1]
                        layers[initial[2]]['final']['Ymark_short'] += layers[initial[2]]['final']['Ymark'][last_fy:-1]
                        last_ix = len(layers[initial[2]]['initial']['Xmark']) + 1
                        last_fx = len(layers[initial[2]]['final']['Xmark']) + 1
                        last_iy = len(layers[initial[2]]['initial']['Ymark']) + 1
                        last_fy = len(layers[initial[2]]['final']['Ymark']) + 1
                        continue
                    layers[initial[2]]['initial'][values[i]].append(initial[i])
                    layers[initial[2]]['final'][values[i]].append(final[i])
                except IndexError: pass #print("IndexError in readfile"); print(l,i)
        line = tracer_out_file.readline()
    return layers

def plot_tracer_data(v1,v2,layers_to_plot="All",filepath="TracerResults/tracer-out.txt",title='My_Plot',initial_or_final="ff",linestyle='None',markerstyle='o',save_plot=False, plot_legend=True, preform_regression=False, degree_regression=1,display_max_min=False):
    layers = read_tracer_out_file(filepath)
    try:
        legend = []
        keys = map(float, layers.keys())
        keys.sort(cmp=cart_comp)
        keys = map(str, keys)
        x_max,x_min,y_max,y_min = 0.,1e9,0.,1e9
        if preform_regression: all_x,all_y = [],[]
        if layers_to_plot=="All": layers_to_plot=range(len(keys))
        for n in layers_to_plot:
            if n > len(keys) or n < -len(keys)-1:
                print("n out of range no corrisponding layer, skipping for n = " + str(n))
                continue
            key = keys[n]
            if initial_or_final == 'ff': x_time,y_time = 'final','final'
            elif initial_or_final == 'if': x_time,y_time = 'initial','final'
            elif initial_or_final == 'fi': x_time,y_time = 'final','initial'
            elif initial_or_final == 'ii': x_time,y_time = 'initial','initial'
            else:
                print(initial_or_final + " is not a valid time input options are [ff,if,fi,ii]")
                return
            x_values = layers[key][x_time]
            y_values = layers[key][y_time]
            if (v1 == 'Xmark' or v1 == 'Ymark' or v2 == 'Xmark' or v2 == 'Ymark'):
                if (v1 == 'Dip' or v1 == 'Ang' or v1 == 'Dis'): v2 += '_short'
                elif (v2 == 'Dip' or v2 == 'Ang' or v2 == 'Dis'): v1 += '_short'
            x = x_values[v1]
            y = y_values[v2]
            x = map(float,x)
            y = map(float,y)
            if not x or not y: continue
            if max(x) > x_max: x_max = max(x)
            if min(x) < x_min: x_min = min(x)
            if max(y) > y_max: y_max = max(y)
            if min(y) < y_min: y_min = min(y)
            if len(x) > len(y):
                x = x[:len(y)]
            elif len(x) < len(y):
                y = y[:len(x)]
            if preform_regression: all_x += x; all_y += y
            c = float(n)/max(layers_to_plot)
            plot_color = (1-c,0,c)
            plot_handle = plt.plot(x,y,linestyle=linestyle,marker=markerstyle,color=plot_color)
            legend.append(str(int(float(key))))
        plt.xlabel(v1)
        plt.ylabel(v2)
        plt.title(title)
        plt.axis([x_min,x_max,y_min,y_max])
        if preform_regression:
            polycoefs = np.polyfit(all_x,all_y,degree_regression)
            x_range = range(int(min(all_x)),int(max(all_x)))
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
            print("Fit Equation = " + regression_entry)
        if plot_legend:
            plt.legend(legend,prop={'size':10},loc=1)
        if save_plot:
            directory = reduce(lambda x,y: x + '/' + y, filepath.split('/')[:-1]) + '/'
            plt.savefig(directory + title + '_' + v1 + '_' + v2 + '_' + initial_or_final +'.png')
        if display_max_min:
            print("lowest layer: " + keys[layers_to_plot[-1]] + ", highest_layer: " + keys[layers_to_plot[0]])
            print(v1 + ": " + "(max = " + str(x_max) + ", min = " + str(x_min) + ")")
            print(v2 + ": " + "(max = " + str(y_max) + ", min = " + str(y_min) + ")")
        plt.show()

    except KeyError:
        print("one of the input variables [" + v1 + "," + v2 + "] does not exist options include: " + reduce(lambda x,y: x + ', ' + y, layers[key][x_time   ].keys()))
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
        args.append(sys.argv[v_index+1])
        args.append(sys.argv[v_index+2])
        kwargs = {}
        if '-i' in sys.argv:
            i_index = sys.argv.index('-i')
            kwargs['filepath'] = sys.argv[i_index+1]
        if '-T' in sys.argv:
            T_index = sys.argv.index('-T')
            kwargs['title'] = sys.argv[T_index+1]
        if '-k' in sys.argv:
            k_index = sys.argv.index('-k')
            kwargs['markerstyle'] = sys.argv[k_index+1]
        if '-l' in sys.argv:
            l_index = sys.argv.index('-l')
            kwargs['linestyle'] = sys.argv[l_index+1]
        if '-H' in sys.argv:
            kwargs['plot_legend'] = False
        if '-t' in sys.argv:
            t_index = sys.argv.index('-t')
            kwargs['initial_or_final'] = sys.argv[t_index+1]
        if '-s' in sys.argv:
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
