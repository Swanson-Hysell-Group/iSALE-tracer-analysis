import sys,os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import tracer_interpreter as ti
import pdb


def truncate_colormap(place,size,res,colormap):
    num_bounded_entries = res*(1-place/size)
    num_unbounded_entries = int(round(res*(place/size)))

    bounded_cmap = plt.cm.get_cmap(colormap)
    bounded_clist = bounded_cmap(np.linspace(0.,1.,num_bounded_entries))
    unbounded_clist = [[0.,1.,0.,1.] for i in range(num_unbounded_entries+1)]

    clist = np.vstack((bounded_clist,unbounded_clist))
    cmap = colors.LinearSegmentedColormap.from_list('custom',clist)
    return cmap

def mag_angle_plot(v='initial_depth', a='Ang', layers_to_plot="All", filepath="TracerResults/tracer-out.txt", t1='My_Plot_Initial', t2='My_Plot_Final', colormap='hot', cmap_bound=None, cmap_interval1=None, cmap_interval2=None, save_plot=False, plot_difference=False, just_final=False, just_initial=False):

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
                if plot_difference:
                    l2 = map(float,layers[key]['initial'][v])
                    l1 = map(float,layers[key]['final'][v])
                    c1 += [b-c for b,c in zip(l1,l2)]
                else:
                    c1 += map(float,layers[key]['initial'][v])
                    c2 += map(float,layers[key]['final'][v])
            except KeyError: print(v + " not available. Options are: " + str(layers[key]['final'].keys())); return
        else:
            if plot_difference:
                l2 = map(float,layers[key]['initial']['Ymark_short'])
                l1 = map(float,layers[key]['final']['Xmark_short'])
                c1 += [b-c for b,c in zip(l1,l2)]
            else:
                c1 += [int(float(key)) for i in range(len(layers[key]['initial']['Xmark_short']))]
                c2 += [int(float(key)) for i in range(len(layers[key]['initial']['Xmark_short']))]

    XMI = map(lambda x: np.cos(x*(np.pi/180)),AI)
    YMI = map(lambda x: -np.sin(x*(np.pi/180)),AI)
    XMF = map(lambda x: np.cos(x*(np.pi/180)),AF)
    YMF = map(lambda x: -np.sin(x*(np.pi/180)),AF)

    if cmap_interval1 != None:
        cmap_interval1 = range(0,8*(cmap_bound+int(cmap_bound/10)),cmap_interval1)
    if cmap_interval2 != None:
        cmap_interval2 = range(0,8*(cmap_bound+int(cmap_bound/10)),cmap_interval2)

    cmap1,cmap2,bounds1,bounds2 = colormap,colormap,None,None
    if cmap_bound != None:
        if c1 != [] and max(c1) > cmap_bound and min(c1) < cmap_bound:
            size = float(max(c1)-min(c1))
            res = 2**12
            place = float(size-cmap_bound)+min(c1)
            cmap1 = truncate_colormap(place,size,res,colormap)
            bounds1 = np.linspace(min(c1),cmap_bound+int(cmap_bound/10),len(c1))
        if c2 != [] and max(c2) > cmap_bound and min(c2) < cmap_bound:
            size = float(max(c2)-min(c2))
            res = 2**12
            place = float(size-cmap_bound)+min(c2)
            cmap2 = truncate_colormap(place,size,res,colormap)
            bounds2 = np.linspace(min(c2),cmap_bound+int(cmap_bound/10),len(c2))

    if plot_difference:
        plt.quiver(XF,YF,XMF,YMF,c1,cmap=cmap1,pivot='tail')
        cbar = plt.colorbar(boundaries=bounds1, ticks=cmap_interval1, cmap=cmap1)
        print(max(c1),min(c1))
        cbar.set_label('delta_' + v)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(t1)
    elif just_final:
        plt.quiver(XF,YF,XMF,YMF,c2,cmap=cmap2,pivot='tail')
        cbar = plt.colorbar(boundaries=bounds2, ticks=cmap_interval2, cmap=cmap2)
        cbar.set_label(v)
        print(max(c2),min(c2))
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(t2)
    elif just_initial:
        plt.quiver(XI,YI,XMI,YMI,c1,cmap=cmap1,pivot='tail')
        cbar = plt.colorbar(boundaries=bounds1, ticks=cmap_interval1, cmap=cmap1)
        print(max(c1),min(c1))
        cbar.set_label(v)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(t1)
    else:
        plt.subplot(2,1,1)
        plt.quiver(XI,YI,XMI,YMI,c1,cmap=cmap1,pivot='tail')
        cbar = plt.colorbar(boundaries = bounds1, ticks = cmap_interval1, cmap=cmap1)
        print(max(c1),min(c1))
        cbar.set_label(v)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(t1)
        plt.subplot(2,1,2)
        plt.quiver(XF,YF,XMF,YMF,c2,cmap=cmap2,pivot='tail')
        cbar = plt.colorbar(boundaries = bounds2, ticks = cmap_interval2, cmap=cmap2)
        print(max(c2),min(c2))
        cbar.set_label(v)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(t2)

    if save_plot:
        figure = plt.gcf()
        figure.set_size_inches(16, 9)
        directory = reduce(lambda x,y: x + '/' + y, filepath.split('/')[:-1]) + '/'
        if not os.path.exists(directory+'Plots/'): os.mkdir(directory+'Plots/')
        plt.savefig(directory + 'Plots/' + t1.replace(' ','_') + '_' + t2.replace(' ','_') + '_' + a + '_' + v + '_' + str(cmap_bound),dpi=648)

    plt.show()

    pdb.set_trace()

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
        -d -> plot difference instead of a before and after map difference
        -cb -> upper bound for colormap after which it's just black.
        -ci -> the interval for tick marks on the colorbar
        -ji -> just the initial plot
        -jf -> just the final plot
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
    if '-d' in sys.argv:
        kwargs['plot_difference'] = True
    if '-cb' in sys.argv:
        cb_index = sys.argv.index('-cb')
        kwargs['cmap_bound'] = int(float(sys.argv[cb_index+1]))
    if '-ci1' in sys.argv:
        ci1_index = sys.argv.index('-ci1')
        kwargs['cmap_interval1'] = int(float(sys.argv[ci1_index+1]))
    if '-ci2' in sys.argv:
        ci2_index = sys.argv.index('-ci2')
        kwargs['cmap_interval2'] = int(float(sys.argv[ci2_index+1]))
    if '-jf' in sys.argv:
        kwargs['just_final'] = True
    if '-ji' in sys.argv:
        kwargs['just_initial'] = True
    mag_angle_plot(**kwargs)

if __name__=='__main__':
    __main__()
