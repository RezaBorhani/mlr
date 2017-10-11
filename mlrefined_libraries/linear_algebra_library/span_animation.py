import numpy as np
from matplotlib import gridspec
from IPython.display import display, HTML
import copy
import math

# import custom JS animator
from mlrefined_libraries.JSAnimation_slider_only import IPython_display_slider_only

# import standard plotting and animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import clear_output
import time
from matplotlib import gridspec
import copy

# func,
def visualize(vec1,vec2,**kwargs):
    # size up vecs
    vec1 = np.asarray(vec1)
    vec2 = np.asarray(vec2)
    vec1copy = copy.deepcopy(vec1)
    vec1copy.shape = (len(vec1copy),1)
    vec2copy = copy.deepcopy(vec2)
    vec2copy.shape = (len(vec2copy),1)
    
    # renderer    
    fig = plt.figure(figsize = (14,7))
    artist = fig
   
    # create subplot with 3 panels, plot input function in center plot
    gs = gridspec.GridSpec(1, 3, width_ratios=[1,3, 1]) 
    ax1 = plt.subplot(gs[0]); ax1.axis('off');
    ax3 = plt.subplot(gs[2]); ax3.axis('off');

    # plot input function
    ax2 = plt.subplot(gs[1])
    
    ### create grid of points ###
    s = np.linspace(-5,5,10)
    xx,yy = np.meshgrid(s,s)
    xx.shape = (xx.size,1)
    yy.shape = (yy.size,1)
    pts = np.concatenate((xx,yy),axis=1)
    pts = np.flipud(pts)
    
    # decide on num_frames
    num_frames = 10
    if 'num_frames' in kwargs:
        num_frames = kwargs['num_frames']
        num_frames = min(num_frames,len(xx))
    
    # animate
    print ('starting animation rendering...')
    
    def animate(k):
        # clear the panel
        ax2.cla()
        
        # print rednering update
        if np.mod(k+1,25) == 0:
            print ('rendering animation frame ' + str(k+1) + ' of ' + str(num_frames))
        if k == num_frames - 1:
            print ('animation rendering complete!')
            time.sleep(1.5)
            clear_output()  
        
        ### take pt of grid and estimate with inputs ###        
        # scatter every point up to k
        for i in range(k+1):
            pt = pts[i,:]
            ax2.scatter(pt[0],pt[1],s = 70, c = 'k',edgecolor = 'w',linewidth = 1)
            
        # get current point and solve for weights
        vec3 = pts[k,:]   
        vec3.shape = (len(vec3),1)
        A = np.concatenate((vec1copy,vec2copy),axis=1)
        b = vec3
        alpha = np.linalg.solve(A,b)

        # plot original vectors
        vector_draw(vec1copy.flatten(),ax2)
        vector_draw(vec2copy.flatten(),ax2)

        # send axis to vector adder for plotting
        vec1 = np.asarray([alpha[0]*vec1copy[0],alpha[0]*vec1copy[1]]).flatten()
        vec2 = np.asarray([alpha[1]*vec2copy[0],alpha[1]*vec2copy[1]]).flatten()
        vector_add_plot(vec1,vec2,ax2)
           
        # plot x and y axes, and clean up
        ax2.grid(True, which='both')
        ax2.axhline(y=0, color='k', linewidth=1.5,zorder = 1)
        ax2.axvline(x=0, color='k', linewidth=1,zorder = 1)

        # set viewing limits
        ax2.set_xlim([-6,6])
        ax2.set_ylim([-6,6])

        # turn off grid
        ax2.grid('off')
        
        # return artist
        return artist,
    
    anim = animation.FuncAnimation(fig, animate,frames=num_frames, interval=num_frames, blit=True)
        
    return(anim)    

# draw a vector
def vector_draw(vec,ax):
    head_length = 0.5
    head_width = 0.5
    veclen = math.sqrt(vec[0]**2 + vec[1]**2)
    vec_orig = copy.deepcopy(vec)
    vec = (veclen - head_length)/veclen*vec
    ax.arrow(0, 0, vec[0],vec[1], head_width=head_width, head_length=head_length, fc='k', ec='k',linewidth=2,zorder = 3)
     
# simple plot of 2d vector addition / paralellagram law
def vector_add_plot(vec1,vec2,ax):     
    # plot each vector
    head_length = 0.5
    head_width = 0.5
    veclen = math.sqrt(vec1[0]**2 + vec1[1]**2)
    vec1_orig = copy.deepcopy(vec1)
    vec1 = (veclen - head_length)/veclen*vec1
    veclen = math.sqrt(vec2[0]**2 + vec2[1]**2)
    vec2_orig = copy.deepcopy(vec2)
    vec2 = (veclen - head_length)/veclen*vec2
    ax.arrow(0, 0, vec1[0],vec1[1], head_width=head_width, head_length=head_length, fc='b', ec='b',linewidth=2,zorder = 2)
    ax.arrow(0, 0, vec2[0],vec2[1], head_width=head_width, head_length=head_length, fc='b', ec='b',linewidth=2,zorder = 2)
    
    # plot the sum of the two vectors
    vec3 = vec1_orig + vec2_orig
    vec3_orig = copy.deepcopy(vec3)
    veclen = math.sqrt(vec3[0]**2 + vec3[1]**2)
    vec3 = (veclen - math.sqrt(head_length))/veclen*vec3
    ax.arrow(0, 0, vec3[0],vec3[1], head_width=head_width, head_length=head_length, fc='r', ec='r',linewidth=3,zorder=2)
    
    # connect them
    ax.plot([vec1_orig[0],vec3_orig[0]],[vec1_orig[1],vec3_orig[1]],linestyle= '--',c='b',zorder=2,linewidth = 1)
    ax.plot([vec2_orig[0],vec3_orig[0]],[vec2_orig[1],vec3_orig[1]],linestyle= '--',c='b',zorder=2,linewidth = 1)

    