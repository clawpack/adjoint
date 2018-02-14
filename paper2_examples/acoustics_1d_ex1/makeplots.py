
from pylab import *
import adjoint_tools as A
import matplotlib.patches as mpatches

xpts = linspace(-12,12,400)
X,T,qxt,vxt,levs = A.read_data(xpts,'_output_25000')
Xa,Ta,qa,va,levsa = A.read_data(xpts,'adjoint/_output',adjoint=True)

if any(abs(T-Ta)>1e-12) or any(abs(X-Xa)>1e-12):
    raise Exception("*** X and Xa or T and Ta do not match")

tmax = T.max()

size = 12
# Generating norms image
figure(1,(10,8))
clf()
axes([0.08,0.09,0.42,0.83])
etanorm = abs(qxt[:,:])
contourf(X,T,etanorm,[.01,1.0],colors=['r'])
plot([0,0],[0,tmax],'k--')
title("Forward Solution Contours", fontsize=size)
xticks([-5,-2.5,0, 2.5, 5],['-5','-2.5','0','2.5','5'],\
       fontsize=size)
xlabel("Distance from density interface",fontsize=size)
ylabel("Seconds",fontsize=size)

axes([0.53,0.09,0.42,0.83])
etaanorm = abs(qa[:,:])
contourf(Xa,Ta,etaanorm,[0.01,4.0],colors=['b'],alpha=0.3)
plot([0,0],[0,tmax],'k--')
title("Adjoint Solution Contours", fontsize=size)
tick_params(axis='y', labelleft='off')
xticks([-5,-2.5,0, 2.5, 5],['-5','-2.5','0','2.5','5'],\
    fontsize=size)
xlabel("Distance from density interface",fontsize=size)
#savefig('swe1d_norms.png')

# Generating overlayed image
figure(1,(10,8))
clf()
axes([0.08,0.09,0.42,0.83])
etanorm = abs(qxt[:,:])
contourf(X,T,etanorm,[.01,1.0],colors=['r'])

contourf(Xa,Ta,etaanorm,[0.01,4.0],colors=['b'],alpha=0.3)
plot([0,0],[0,tmax],'k--')
title("Overlayed Solution Contours", fontsize=size)
xticks([-5,-2.5,0, 2.5, 5],['-5','-2.5','0','2.5','5'],\
       fontsize=size)
xlabel("Distance from density interface",fontsize=size)
ylabel("Seconds",fontsize=size)
fdata = mpatches.Patch(color='red', label='Forward Solution')
adata = mpatches.Patch(color='blue',alpha=0.3, label='Adjoint Solution')
legend(handles=[fdata,adata],loc=2)

axes([0.53,0.09,0.42,0.83])
q_innerprod = qxt[:,:] * qa[:,:] + vxt[:,:]*va[:,:]
contourf(X,T,abs(q_innerprod),[.01,0.1,1],colors=['g','g'])
plot([0,0],[0,tmax],'k--')
title("Inner Product Contours", fontsize=size)
xticks([-5,-2.5,0, 2.5, 5],['-5','-2.5','0','2.5','5'],\
       fontsize=size)
xlabel("Distance from density interface",fontsize=size)
tick_params(axis='y', labelleft='off')
savefig('acoustics1d_ip_ex1.png')

X1,T1,qxt1,vxt1,levs1 = A.read_data(xpts,'_output_1e1')
X2,T2,qxt2,vxt2,levs2 = A.read_data(xpts,'_output_1e-4')

# Generating levels image
figure(1,(10,8))
clf()
axes([0.08,0.09,0.42,0.83])
contourf(X1, T1, levs1,[0,1,2,3,4,5],colors=[[1,1,1],[0.8,0.8,0.8],[0.8,1,0.8],\
        [1,.7,.7],[0.6,0.6,1]])
contour(X1, T1, levs1,[1,2,3,4,5],colors=['k','g','r','b'])
plot([0,0],[0,tmax],'k--')
title("Levels for tol = 1e2", fontsize=size)
xlabel("Distance from density interface",fontsize=size)
ylabel("Seconds",fontsize=size)
l2 = mpatches.Patch(color=[0.8,0.8,0.8], label='Level 2')
l3 = mpatches.Patch(color=[0.8,1,0.8], label='Level 3')
l4 = mpatches.Patch(color=[1,.7,.7], label='Level 4')
l5 = mpatches.Patch(color=[0.6,0.6,1], label='Level 5')
legend(handles=[l2,l3,l4,l5],loc=2)

axes([0.53,0.09,0.42,0.83])
contourf(X2, T2, levs2,[0,1,2,3,4,5],colors=[[1,1,1],[0.8,0.8,0.8],[0.8,1,0.8],\
        [1,.7,.7],[0.6,0.6,1]])
contour(X2, T2, levs2,[1,2,3,4,5],colors=['k','g','r','b'])
plot([0,0],[0,tmax],'k--')
title("Levels for tol = 1e-4", fontsize=size)
xlabel("Distance from density interface",fontsize=size)

savefig('acoustics_levels_ex1.png')
