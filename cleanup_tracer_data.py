import sys

def __main__(filename,max_x=1e9,max_y_d=1e9,max_y_u=1e9,cut_from_final=True):
    """
    DESCRIPTION:
        Script designed to cut data from a tracer-out.txt file to remove any bad or extreame data. By default removes any tracers that have flown to inf otherwise only cuts according input flags.

    SYNTAX:
        python cleanup_tracer_data.py [tracer-out.txt] -[FLAG] [INPUT]

    FLAGS:
        -h -> print this help message
        -i -> cut data by initial value instead of final values as is default
        -ch -> cut data by x value from the right, input must be a number (float or int) that represents in km the maximum x value allowed, cutting all data with a larger x value than the input. (optional)
        -cvu -> cut data by y value from above so that input is the largest allowed y value in km (optional)
        -cvd -> cut data by y value from bellow so that input is the smallest allowed y value in km (optional)
    """
    in_file = open(filename,'r')
    line = "mary had a little lamb"
    out_str = ""
    i = 0
    while line:
        line = in_file.readline()
        header = in_file.readline()
        init_vals = in_file.readline().split()
        final_vals = in_file.readline().split()
        try:
            if cut_from_final:
                if int(float(final_vals[1])) >= max_x or -int(float(final_vals[2])) >= max_y_d or int(float(final_vals[2])) >= max_y_u or int(float(final_vals[1])) <= 0 or int(float(final_vals[1])) >= 47427 and int(float(final_vals[2])) >= 47427 or int(float(final_vals[6])) == 0 or int(float(final_vals[7])) == 0:
                    print("skipping line: " + str(i))
                    i += 1
                    continue
            else:
                if int(float(init_vals[1])) >= max_x or -int(float(init_vals[2])) >= max_y_d or int(float(init_vals[2])) >= max_y_u or int(float(init_vals[1])) <= 0 or int(float(final_vals[1])) >= 47427 and int(float(final_vals[2])) >= 47427:
                    print("skipping line: " + str(i))
                    i += 1
                    continue
        except IndexError: continue
        out_str += line + header
        if init_vals:
            for val in init_vals[:-1]:
                out_str += val + "\t"
            out_str += init_vals[-1] + "\n"
        if final_vals:
            for val in final_vals[:-1]:
                out_str += val + "\t"
            out_str += final_vals[-1] + "\n"
        i += 1
    out_file = open(filename.split('.')[:-1][0]+'.trimmed','w')
    out_file.write(out_str)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        kwargs = {}
        if '-ch' in sys.argv:
            ch_index = sys.argv.index('-ch')
            kwargs['max_x'] = int(sys.argv[ch_index+1])*1000
        if '-cvd' in sys.argv:
            cvd_index = sys.argv.index('-cvd')
            kwargs['max_y_d'] = int(sys.argv[cvd_index+1])*1000
        if '-cvu' in sys.argv:
            cvu_index = sys.argv.index('-cvu')
            kwargs['max_y_u'] = int(sys.argv[cvu_index+1])*1000
        if '-i' in sys.argv:
            kwargs['cut_from_final'] = False
        __main__(sys.argv[1],**kwargs)
