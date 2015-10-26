
from pylab import *
import adjoint_tools as A

X,T,qxt = A.read_data('forward/_output')
Xa,Ta,qa = A.read_data('adjoint/_output',adjoint=True)

print "Read qxt and qa"

if any(abs(T-Ta)>1e-12) or any(abs(X-Xa)>1e-12):
    raise Exception("*** X and Xa or T and Ta do not match")

tmax = T.max()

size = 26
# Generating norms image
figure(1,(10,8))
clf()
axes([0.05,0.05,0.42,0.9])
qnorm = abs(qxt[:,0,:]) + abs(qxt[:,1,:])
contourf(X,T,qnorm,[.01,10],colors=['r'])
plot([0,0],[0,tmax],'k--')
title("Forward Solution", fontsize=size)
yticks(fontsize=size)
xticks([-4,-2,0,2], fontsize=size)

axes([0.53,0.05,0.42,0.9])
qanorm = abs(qa[:,0,:]) + abs(qa[:,1,:])
contourf(Xa,Ta,qanorm,[.01,10],colors=['b'],alpha=0.3)
plot([0,0],[0,tmax],'k--')
title("Adjoint Solution", fontsize=size)
tick_params(axis='y', labelleft='off')
xticks([-4,-2,0,2], fontsize=size)
savefig('acoustics1d_norms.png')

# Generating overlayed image
figure(1,(10,8))
clf()
axes([0.05,0.05,0.42,0.9])
qnorm = abs(qxt[:,0,:]) + abs(qxt[:,1,:])
contourf(X,T,qnorm,[.01,10],colors=['r'])

qanorm = abs(qa[:,0,:]) + abs(qa[:,1,:])
contourf(Xa,Ta,qanorm,[.01,10],colors=['b'],alpha=0.3)
plot([0,0],[0,tmax],'k--')
title("Overlayed Solutions", fontsize=size)
yticks(fontsize=size)
xticks([-4,-2,0,2], fontsize=size)

axes([0.53,0.05,0.42,0.9])
q_innerprod = qxt[:,0,:] * qa[:,0,:] + qxt[:,1,:]*qa[:,1,:]
contourf(X,T,abs(q_innerprod),[.01,0.1,10],colors=['g','g'])
plot([0,0],[0,tmax],'k--')
title("Inner Product", fontsize=size)
xticks([-4,-2,0,2], fontsize=size)
tick_params(axis='y', labelleft='off')
savefig('acoustics1d_innerprod.png')
