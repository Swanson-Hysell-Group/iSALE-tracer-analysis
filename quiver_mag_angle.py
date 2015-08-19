from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import tracer_interperter as ti

layers = ti.read_tracer_out_file("TracerResults/tracer-out.txt")

keys = map(float,layers.keys())
keys.sort(cmp=lambda x,y: int(y-x))
keys = map(str,keys)

X,Y,AI,AF = [],[],[],[]

for key in keys[:-1]:
    X += map(float,layers[key]['initial']['Xmark_short'])
    Y += map(float,layers[key]['initial']['Ymark_short'])
    AI += map(float,layers[key]['initial']['Ang'])
    AF += map(float,layers[key]['final']['Ang'])

XMI = map(np.cos,AI)
YMI = map(np.sin,AI)
XMF = map(np.cos,AF)
YMF = map(np.sin,AF)

plt.subplot(2,1,1)
plt.quiver(X,Y,XMI,YMI)
plt.subplot(2,1,2)
plt.quiver(X,Y,XMF,YMF)

plt.show()

X += map(float,layers['-3450.0']['initial']['Xmark_short'])
Y += map(float,layers['-3450.0']['initial']['Ymark_short'])
AI += map(float,layers['-3450.0']['initial']['Ang'])
AF += map(float,layers['-3450.0']['final']['Ang'])