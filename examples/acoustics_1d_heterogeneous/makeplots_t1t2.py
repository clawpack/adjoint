
from pylab import *
import adjoint_tools as A
from clawpack.clawutil.data import ClawData


X,T,qxt = A.read_data('forward/_output')
Xa,Ta,qa = A.read_data('adjoint/_output',adjoint=True)
print "Read qxt and qa"

if any(abs(T-Ta)>1e-12) or any(abs(X-Xa)>1e-12):
    raise Exception("*** X and Xa or T and Ta do not match")

tmax = T.max()

# Time region where solution is of interest
# Set t1 = t2 = tmax if only the final time, 
#     t1 = 0, t2 = tmax if the [x1,x2] region is of interest for all time
t1 = 18.0
t2 = 20.0

# Read region where adjoint functional is nonzero
# Used to plot box below.
adjoint_setprobdata = ClawData()
adjoint_setprobdata.read('adjoint/setprob.data', force=True)
x1 = adjoint_setprobdata.x1
x2 = adjoint_setprobdata.x2

figure(1,(10,8))
clf()
axes([0.05,0.05,0.42,0.9])
qnorm = abs(qxt[:,0,:]) + abs(qxt[:,1,:])
contourf(X,T,qnorm,[.01,10],colors=['r'])

q_innerprod = qxt[:,0,:] * qa[:,0,:] + qxt[:,1,:]*qa[:,1,:]

t = T[:,0]
num_t = len(t)
# Shift adjoint solution in time downwards between t1 and t2 and
# accumulate the inner product of shifted adjoint with forward solution:
qanorm = zeros(qa[:,0,:].shape)
q_innerprod2 = zeros(qa[:,0,:].shape)
qa2 = qa.copy()
for nt in range(len(t)-1,-1,-1):
    if (t[nt]>=t1) and (t[nt]<=t2):
        qanorm += abs(qa2[:,0,:]) + abs(qa2[:,1,:])
        q_innerprod2 += abs(qxt[:,0,:] * qa2[:,0,:] + qxt[:,1,:]*qa2[:,1,:])
    # shift qa2 downward in time:
    qa2 = zeros(qa.shape)
    qa2[:nt,:,:] = qa[(num_t-nt):,:,:]
    #print '+++ shifted row %s and above to first %s' % (num_t-nt,nt)
    #print '+++ t[nt] = %g' % t[nt]
    if t[nt] <= t1: break

size = 26
contourf(Xa,Ta,qanorm,[.01,1e10],colors=['b'],alpha=0.3)
plot([0,0],[0,tmax],'k--')
title("Overlayed Solutions", fontsize=size)
# plot box around area of interest:
plot([x1,x2,x2,x1,x1],[t1,t1,t2,t2,t1],'b-')
yticks(fontsize=size)
xticks([-4,-2,0,2], fontsize=size)

axes([0.53,0.05,0.42,0.9])
contourf(X,T,q_innerprod2,[.01,1e10],colors=['g'])
plot([0,0],[0,tmax],'k--')
title("Inner Product", fontsize=size)
# plot box around area of interest:
plot([x1,x2,x2,x1,x1],[t1,t1,t2,t2,t1],'b-')
xticks([-4,-2,0,2], fontsize=size)
tick_params(axis='y', labelleft='off')

savefig('acoustics1d_timewindow.png')
