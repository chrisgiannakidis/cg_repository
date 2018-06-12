import numpy as np
from mpl_toolkits . mplot3d import Axes3D
import matplotlib . pyplot as plt
from matplotlib import cm
from cg558 import Greeks
import sys
import time

start_time = time.time()

#########################################
''' We input the file by using a command line argument.'''
#########################################

ff= sys.argv[1:2]

str1 = ''.join(ff)
f=open(str1,"r") # if you want to open the file externally, use this

#f=open("greeks.txt","r") # if you want to open the file internally, use this

file = f.readlines()
inputs = list(map(float, file))

# Option parameters
sigma = inputs[0] # Flat volatility
strike = inputs[1] # Fixed strike
epsilon = inputs[2] # The % on the left / right of Strike .
# Asset prices are centered around Spot (" ATM Spot ")
shortexpiry = inputs[3] # Shortest expiry in days
longexpiry = inputs[4] # Longest expiry in days
riskfree = inputs[5] # Continuous risk free rate
divrate = inputs[6] # Continuous div rate
#Grid definition
dx = int(inputs[7])
dy = int(inputs[8]) # Steps throughout asset price and expiries axis

# xx: Asset price axis , yy: expiry axis , zz: greek axis

greeks_sensitivities = ['Value Calls', 'Value Puts', 'Delta Calls',
                        'Delta Puts', 'Vega', 'Theta Calls', 'Theta Puts', 
                        'Rho Calls', 'Rho Puts', 'Gamma', 'Vanna', 
                        'Charm Calls', 'Charm Puts', 'Vomma', 'Veta', 'Speed',
                        'Zomma', 'Color', 'Ultima', 'Dual_Delta Calls', 
                        'Dual_Delta Puts', 'Dual_Gamma', 'Phi']

diverging_colormaps = ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                        'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
                        'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 
                        'RdYlBu', 'RdYlGn', 'Spectral', 'bwr', 'seismic']

xx , yy = np. meshgrid (np. linspace ( strike *(1 - epsilon ), (1+ epsilon )* \
                                      strike , dx), 
                        np. linspace ( shortexpiry , longexpiry , dy ))

greeks_attributes = greeks_sensitivities
greeks_attributes = [item.replace(' Puts','') for item in greeks_attributes]
greeks_attributes = [item.replace(' Calls','') for item in greeks_attributes]

for i in range (0,23):
    print (" Calculating ",greeks_sensitivities[i], "(", i+1, "/23) ... ")
    
    if 'Puts' in greeks_sensitivities[i]: 
       Type = 2
    else:
       Type = 1
       
       
    
    zz = np. array ([ getattr (Greeks ([Type, x, strike , riskfree , divrate ,y, 
                               sigma ]), greeks_attributes[i]) for
                 x,y in zip(np. ravel (xx), np. ravel (yy ))])
    zz = zz. reshape (xx. shape )    

    fig = plt . figure ()
    fig . suptitle (greeks_sensitivities[i],fontsize =40)
    ax = fig .gca( projection ="3d")
    surf = ax. plot_surface (xx , yy , zz , rstride =1, cstride =1, alpha =0.75 , \
                             cmap = getattr(cm,diverging_colormaps[i]))
                             
    ax. set_xlabel ("Asset price ", fontsize = 20)
    ax. set_ylabel ("Expiry ", fontsize = 20)
    ax. set_zlabel (greeks_sensitivities[i], fontsize = 20)
    # Plot 3D contour
    zzlevels = np. linspace (zz.min (), zz. max (), num =8, endpoint = True )
    xxlevels = np. linspace (xx.min (), xx. max (), num =8, endpoint = True )
    yylevels = np. linspace (yy.min (), yy. max (), num =8, endpoint = True )
    cset = ax. contourf (xx , yy , zz , zzlevels , zdir ="z",offset =zz. min (),
    cmap = getattr(cm,diverging_colormaps[i]) , linestyles ="dashed ")
    cset = ax. contourf (xx , yy , zz , xxlevels , zdir ="x",offset =xx. min (),
    cmap = getattr(cm,diverging_colormaps[i]) , linestyles ="dashed ")
    cset = ax. contourf (xx , yy , zz , yylevels , zdir ="y",offset =yy. max (),
    cmap = getattr(cm,diverging_colormaps[i]) , linestyles ="dashed ")
    
    for c in cset . collections :
        c. set_dashes ([(0 , (2.0 , 2.0))]) # Dash contours
    plt . clabel (cset , fontsize =20 , inline =1)
    ax. set_xlim (xx. min (), xx. max ())
    ax. set_ylim (yy. min (), yy. max ())
    ax. set_zlim (zz. min (), zz. max ())
    #ax. relim ()
    #ax. autoscale_view (True ,True , True )
    # Colorbar
    colbar = plt . colorbar (surf , shrink =1.0 , extend ="both", aspect = 10)
    l,b,w,h = plt . gca (). get_position (). bounds
    ll ,bb ,ww ,hh = colbar .ax. get_position (). bounds
    colbar .ax. set_position ([ll , b +0.1*h, ww , h *0.8])
    # Show chart

    if (i==0):
        total_time = 23 * (time.time() - start_time)

    print(" Elasped time is ",time.time() - start_time, " seconds")
    
    print(" Remaining time is approximately ",
          total_time - time.time() + start_time, " seconds")
    
print(" Remaining time is a few seconds... ")

print ("All Greeks - risk sensitivities are done")
    
plt . show ()

print(" ")