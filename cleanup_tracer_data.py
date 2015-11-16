import sys

def __main__(filename,max_x=1e9,max_y_d=1e9,max_y_u=1e9,cut_from_final=True,remove_sym_axis=False,dist_cut= 1e9):
    """
    DESCRIPTION:
        A data cutting script that takes in a tracer-out.txt file and outputs a tracer-out file called tracer-out.trimmed. By defult the program cuts any tracers that fly to "infinity" as well as any data points that have 0 temp or pressure as they have likely become gasses. In addition the usage of a number of flags can allow for cutting data via spacial constraints.

    SYNTAX:
        python cleanup_tracer_data.py [tracer-out.txt] -[FLAG] [INPUT]

    FLAGS:
        -h -> print this help message
        -i -> cut data by initial value instead of final values as is default
        -ch -> cut data by x value from the right, input must be a number (float or int) that represents in km the maximum x value allowed, cutting all data with a larger x value than the input. (optional)
        -cvu -> cut data by y value from above so that input is the largest allowed y value in km (optional)
        -cvd -> cut data by y value from bellow so that input is the smallest allowed y value in km (optional)
        -rs -> boolean to remove symetry axis (default=True)
        -d -> distance cut off if final pos are too far apart cut (int value in meters)
    """
    in_file = open(filename,'r')
    out_str = ""
    i = 0
    line = in_file.readline()
    header = in_file.readline()
    init_vals = in_file.readline().split()
    final_vals = in_file.readline().split()
    while line:
        next_line = in_file.readline()
        next_header = in_file.readline()
        next_init_vals = in_file.readline().split()
        next_final_vals = in_file.readline().split()
        try:
            if cut_from_final:
                if (int(float(final_vals[1])) >= max_x or -int(float(final_vals[2])) >= max_y_d or int(float(final_vals[2])) >= max_y_u or int(float(final_vals[1])) <= 0 or (int(float(final_vals[1])) >= 47427 and int(float(final_vals[2])) >= 47427) or int(float(final_vals[6])) == 0 or int(float(final_vals[7])) == 0 or int(float(final_vals[3])) >= dist_cut) or (int(float(next_final_vals[1])) <= 0 or (int(float(next_final_vals[1])) >= 47427 and int(float(next_final_vals[2])) >= 47427) or int(float(next_final_vals[6])) == 0 or int(float(next_final_vals[7])) == 0):
                    print("skipping line: " + str(i))
                    line = next_line
                    header = next_header
                    init_vals = next_init_vals
                    final_vals = next_final_vals
                    i += 1
                    continue
            else:
                if (int(float(init_vals[1])) >= max_x or -int(float(init_vals[2])) >= max_y_d or int(float(init_vals[2])) >= max_y_u or int(float(init_vals[1])) <= 0 or int(float(final_vals[1])) >= 47427 and int(float(final_vals[2])) >= 47427 or int(float(final_vals[6])) == 0 or int(float(final_vals[7])) == 0 or int(float(final_vals[3])) >= dist_cut) or (int(float(next_final_vals[1])) <= 0 or int(float(next_final_vals[1])) >= 47427 and int(float(next_final_vals[2])) >= 47427 or int(float(next_final_vals[6])) == 0 or int(float(next_final_vals[7])) == 0):
                    print("skipping line: " + str(i))
                    line = next_line
                    header = next_header
                    init_vals = next_init_vals
                    final_vals = next_final_vals
                    i += 1
                    continue
        except IndexError: 
            line = next_line
            header = next_header
            init_vals = next_init_vals
            final_vals = next_final_vals
            continue
        out_str += line + header
        if init_vals:
            for val in init_vals[:-1]:
                out_str += val + "\t"
            out_str += init_vals[-1] + "\n"
        if final_vals:
            for val in final_vals[:-1]:
                out_str += val + "\t"
            out_str += final_vals[-1] + "\n"
        line = next_line
        header = next_header
        init_vals = next_init_vals
        final_vals = next_final_vals
        i += 1
    file_list = filename.split('.')[:-1]
    if len(file_list) == 1: file_ext = file_list[0]
    else:
        file_ext = reduce(lambda x,y: x + '.' + y, file_list)
    out_file = open(file_ext+'.trimmed','w')
    out_file.write(out_str)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        kwargs = {}
        if '-ch' in sys.argv:
            ch_index = sys.argv.index('-ch')
            kwargs['max_x'] = float(sys.argv[ch_index+1])*1000
        if '-cvd' in sys.argv:
            cvd_index = sys.argv.index('-cvd')
            kwargs['max_y_d'] = float(sys.argv[cvd_index+1])*1000
        if '-cvu' in sys.argv:
            cvu_index = sys.argv.index('-cvu')
            kwargs['max_y_u'] = float(sys.argv[cvu_index+1])*1000
        if '-i' in sys.argv:
            kwargs['cut_from_final'] = False
        if '-rs' in sys.argv:
            kwargs['remove_sym_axis'] = True
        if '-d' in sys.argv:
            d_index = sys.argv.index('-d')
            kwargs['dist_cut'] = int(sys.argv[d_index+1])
        __main__(sys.argv[1],**kwargs)
