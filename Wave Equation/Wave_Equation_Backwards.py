# this is a numerical simulation of the 1d wave equation u_tt - u_xx = 0

import numpy as np
from scipy import exp
from matplotlib.pylab import *



# This is the plotting function
def save_graph(x,filename,f,limits,n):
    figure()
    axis(limits)
    
    line, = plot(x,x)

    for i in range(0,n):
	print i
        line.set_ydata(f[i])
        draw()
        savefig("graphs/" + '%s%04d' % (filename, i) + ".png")



# domain = [0,1]
# let h = |[0,1]|/m = 1/m, where m is the number of divisions of the spatial axis
a = 0.
b = 1.
m = 500
dr = (b-a)/m

# we will discritize the interval [a,b] into m equally sized intervals and this will be the spatial lattice we will do the numerics on
pts = np.arange(a,b + dr/2.,dr)

# time steps
dt = 0.001

# maximum number of iterations
maxiter = 2500

# we set the initial data here. We just use a simple Gaussian for convenience.
u0=1/(2.*3.14159*0.01)*exp(-(pts-0.5)**2/(2.*0.01))
n = len(pts)
u1=u0*1.
u2= zeros(n)

u = []
u.append(u0*1.)
u.append(u1*1.)

# we set a counting variable i, a common quantity that shows up (dt/dr)^2, n the number of points in the lattice, and some dummy lists that we will need to use to solve a tridiagonal problem
i = 1
cfl = (dt/dr)**2
b = zeros(n)
d = zeros(n)
c = zeros(n)

# forward method (i.e. for the next time step, a position only depends on the values of the 2 previous time steps and not on any of its neighbours

while (i <= maxiter):
	for j in range(0,n):
		b[j] = 2.*u1[j] - u0[j]

	c[0] = -cfl/(1.+cfl)
	d[0] = b[0]/(1.+cfl)
	for k in range(1,n-1):
		c[k] = -cfl/(1. + 2.*cfl + c[k-1]*cfl)
		d[k] = (b[k] + d[k-1]*cfl)/( 1. + 2.*cfl + c[k-1]*cfl )

	u2[n-1] = (b[n-1] + d[n-2]*cfl)/(1. + cfl + c[n-2]*cfl)
	for l in reversed(range(n-1)):
		u2[l] = - c[l]*u2[l+1] + d[l]

	# update
	u.append(u2*1.)
	u0 = u1*1.
	u1 = u2*1.
	i = i + 1

save_graph(pts,"test",u,limits=[0,1,-50,50],n=maxiter,)

