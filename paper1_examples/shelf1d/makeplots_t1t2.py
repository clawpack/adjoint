
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
t1 = 3800.0
t2 = 4200.0

# Read region where adjoint functional is nonzero
# Used to plot box below.
adjoint_setprobdata = ClawData()
adjoint_setprobdata.read('adjoint/setprob.data', force=True)
x1 = adjoint_setprobdata.x1
x2 = adjoint_setprobdata.x2

figure(1,(10,8))
clf()
axes([0.08,0.09,0.42,0.83])
etanorm = abs(qxt[:,0,:])
contourf(X,T,etanorm,[.01,1.0],colors=['r'])

q_innerprod = qxt[:,0,:] * qa[:,0,:] + qxt[:,1,:]*qa[:,1,:]

t = T[:,0]
num_t = len(t)
# Shift adjoint solution in time downwards between t1 and t2 and
# accumulate the inner product of shifted adjoint with forward solution:
etaanorm = zeros(qa[:,0,:].shape)
q_innerprod2 = zeros(qa[:,0,:].shape)
qa2 = qa.copy()
for nt in range(len(t)-1,-1,-1):
    if (t[nt]>=t1) and (t[nt]<=t2):
        etaanorm += abs(qa2[:,0,:])
        q_innerprod2 += abs(qxt[:,0,:] * qa2[:,0,:] + qxt[:,1,:]*qa2[:,1,:])
    # shift qa2 downward in time:
    qa2 = zeros(qa.shape)
    qa2[:nt,:,:] = qa[(num_t-nt):,:,:]
    #print '+++ shifted row %s and above to first %s' % (num_t-nt,nt)
    #print '+++ t[nt] = %g' % t[nt]
    if t[nt] <= t1: break

size = 12
textsize = 12
contourf(Xa,Ta,etaanorm,[.01,1e10],colors=['b'],alpha=0.3)
plot([-50000,-50000],[0,tmax],'k--')
title("Overlayed Solution Contours", fontsize=textsize)
# plot box around area of interest:
plot([x1,x2,x2,x1,x1],[t1,t1,t2,t2,t1],'b-')
yticks([3600, 1800],['1','.5','0'],\
       fontsize=size)
xticks([-350000,-250000,-150000, -50000],['350','250','150','50','0'],\
       fontsize=size)
xlabel("Kilometers offshore",fontsize=textsize)
ylabel("Hours",fontsize=textsize)

axes([0.53,0.09,0.42,0.83])
contourf(X,T,q_innerprod2,[.01,1e10],colors=['g'])
plot([-50000,-50000],[0,tmax],'k--')
title("Inner Product Contours", fontsize=textsize)
# plot box around area of interest:
plot([x1,x2,x2,x1,x1],[t1,t1,t2,t2,t1],'b-')
tick_params(axis='y', labelleft='off')
xticks([-350000,-250000,-150000, -50000],['350','250','150','50','0'],\
       fontsize=size)
yticks([3600, 1800],['1','.5','0'],\
       fontsize=size)
xlabel("Kilometers offshore",fontsize=textsize)

savefig('swe1d_timewindow.png')
