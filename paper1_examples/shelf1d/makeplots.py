
from pylab import *
import adjoint_tools as A

X,T,qxt = A.read_data('forward/_output')
Xa,Ta,qa = A.read_data('adjoint/_output',adjoint=True)

if any(abs(T-Ta)>1e-12) or any(abs(X-Xa)>1e-12):
    raise Exception("*** X and Xa or T and Ta do not match")

tmax = T.max()

size = 12
# Generating norms image
figure(1,(10,8))
clf()
axes([0.08,0.09,0.42,0.83])
etanorm = abs(qxt[:,0,:])
contourf(X,T,etanorm,[.01,1.0],colors=['r'])
plot([-50000,-50000],[0,tmax],'k--')
title("Forward Solution Contours", fontsize=size)
yticks([3600, 1800],['1','.5','0'],\
       fontsize=size)
xticks([-350000,-250000,-150000, -50000],['350','250','150','50','0'],\
       fontsize=size)
xlabel("Kilometers offshore",fontsize=size)
ylabel("Hours",fontsize=size)

axes([0.53,0.09,0.42,0.83])
etaanorm = abs(qa[:,0,:])
contourf(Xa,Ta,etaanorm,[0.01,1.0],colors=['b'],alpha=0.3)
plot([-50000,-50000],[0,tmax],'k--')
title("Adjoint Solution Contours", fontsize=size)
tick_params(axis='y', labelleft='off')
xticks([-350000,-250000,-150000, -50000],['350','250','150','50','0'],\
       fontsize=size)
yticks([3600, 1800],['1','.5','0'],\
       fontsize=size)
xlabel("Kilometers offshore",fontsize=size)
savefig('swe1d_norms.png')

# Generating overlayed image
figure(1,(10,8))
clf()
axes([0.08,0.09,0.42,0.83])
contourf(X,T,etanorm,[.01,1.0],colors=['r'])

contourf(Xa,Ta,etaanorm,[0.01,1.0],colors=['b'],alpha=0.3)
plot([-50000,-50000],[0,tmax],'k--')
title("Overlayed Solution Contours", fontsize=size)
xticks([-350000,-250000,-150000, -50000],['350','250','150','50','0'],\
       fontsize=size)
yticks([3600, 1800],['1','.5','0'],\
       fontsize=size)
xlabel("Kilometers offshore",fontsize=size)
ylabel("Hours",fontsize=size)

axes([0.53,0.09,0.42,0.83])
q_innerprod = qxt[:,0,:] * qa[:,0,:] + qxt[:,1,:]*qa[:,1,:]
contourf(X,T,abs(q_innerprod),[.01,0.1,1],colors=['g','g'])
plot([-50000,-50000],[0,tmax],'k--')
title("Inner Product Contours", fontsize=size)
xticks([-350000,-250000,-150000, -50000],['350','250','150','50','0'],\
       fontsize=size)
yticks([3600, 1800],['1','.5','0'],\
       fontsize=size)
xlabel("Kilometers offshore",fontsize=size)
tick_params(axis='y', labelleft='off')
savefig('swe1d_innerprod.png')
