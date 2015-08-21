import sys,os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import tracer_interpreter as ti

def mag_angle_plot(v='initial_depth',a='Ang',layers_to_plot="All",filepath="TracerResults/tracer-out.txt",t1='My_Plot_Initial',t2='My_Plot_Final',colormap='gist_rainbow',save_plot=False):

    layers = ti.read_tracer_out_file(filepath)

    keys = map(float, layers.keys())
    keys.sort(cmp=lambda x,y: int(y-x))
    keys = map(str,keys)
    if layers_to_plot=="All": layers_to_plot=range(len(keys))

    XI,YI,XF,YF,AI,AF = [],[],[],[],[],[]
    c1,c2 = [],[]

    for n in layers_to_plot:
        key = keys[n]
        XI += map(float,layers[key]['initial']['Xmark_short'])
        YI += map(float,layers[key]['initial']['Ymark_short'])
        XF += map(float,layers[key]['final']['Xmark_short'])
        YF += map(float,layers[key]['final']['Ymark_short'])
        if a == 'Ang' or a == 'Dip':
            AI += map(float,layers[key]['initial'][a])
            AF += map(float,layers[key]['final'][a])
        else: print('the input angle variable must be either Ang or Dip'); return
        if v != 'initial_depth':
            try:
                c1 += map(float,layers[key]['initial'][v])
                c2 += map(float,layers[key]['final'][v])
            except KeyError: print(v + " not available. Options are: " + str(layers[key]['final'].keys())); return
        else:
            c1 += [int(float(key)) for i in range(len(layers[key]['initial']['Xmark_short']))]
            c2 += [int(float(key)) for i in range(len(layers[key]['initial']['Xmark_short']))]

    XMI = map(lambda x: np.cos(x*(np.pi/180)),AI)
    YMI = map(lambda x: np.sin(x*(np.pi/180)),AI)
    XMF = map(lambda x: np.cos(x*(np.pi/180)),AF)
    YMF = map(lambda x: np.sin(x*(np.pi/180)),AF)

    plt.subplot(2,1,1)
    plt.quiver(XI,YI,XMI,YMI,c1,cmap=colormap,pivot='tail')
    cbar = plt.colorbar()
    cbar.set_label(v)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(t1)
    plt.subplot(2,1,2)
    plt.quiver(XF,YF,XMF,YMF,c2,cmap=colormap,pivot='tail')
    cbar = plt.colorbar()
    cbar.set_label(v)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(t2)

    if save_plot:
        figure = plt.gcf()
        figure.set_size_inches(16, 9)
        directory = reduce(lambda x,y: x + '/' + y, filepath.split('/')[:-1]) + '/'
        if not os.path.exists(directory+'Plots/'): os.mkdir(directory+'Plots/')
        plt.savefig(directory + 'Plots/' + t1.replace(' ','_') + '_' + t2.replace(' ','_') + '_' + a + '_' + v,dpi=1296)

    plt.show()

def __main__():
    """
    DESCRIPTION:
        Plotting Script that uses tracer-out.txt files created by tracer_interperter.py to plot the angle based quantites in a quiver plot. 

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
    """
    kwargs = {}
    if '-h' in sys.argv:
        help(__main__)
    if '-i' in sys.argv:
        i_index = sys.argv.index('-i')
        kwargs['filepath'] = sys.argv[i_index+1]
    if '-a' in sys.argv:
        a_index = sys.argv.index('-a')
        kwargs['a'] = sys.argv[a_index+1]
    if '-v' in sys.argv:
        v_index = sys.argv.index('-v')
        kwargs['v'] = sys.argv[v_index+1]
    if '-r' in sys.argv:
        r_index = sys.argv.index('-r')
        r_val = sys.argv[r_index+1]
        try: kwargs['layers_to_plot'] = range(*map(int,r_val.split(',')))
        except ValueError: kwargs['layers_to_plot'] = map(int,list(r_val.strip('[ ]').split(',')))
    if '-t1' in sys.argv:
        t1_index = sys.argv.index('-t1')
        kwargs['t1'] = sys.argv[t1_index+1]
    if '-t2' in sys.argv:
        t2_index = sys.argv.index('-t2')
        kwargs['t2'] = sys.argv[t2_index+1]
    if '-S' in sys.argv:
        kwargs['save_plot'] = True
    if '-c' in sys.argv:
        c_index = sys.argv.index('-c')
        kwargs['colormap'] = sys.argv[c_index+1]
    mag_angle_plot(**kwargs)

if __name__=='__main__':
    __main__()
