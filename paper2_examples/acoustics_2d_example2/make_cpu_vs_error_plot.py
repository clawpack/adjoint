
from pylab import *

fs = 15 # fontsize

# adjoint-error:
cpu_a = [395+5, 123+5,17+5,2+5] #means + adjoint time
err_a = [0.0027,.0083,.0354,.0837]

# forward-error:
cpu_fb = [702,357,193,82] # means
err_fb = [0.0034,0.0087,0.0124,0.0294]

# uniform:
cpu_unif = [1097,345,43] # means
err_unif = [0.0037,0.0126,0.0445]

figure(23, figsize=(8,5))
clf()
loglog(err_unif,cpu_unif,'g^-',label='uniform grids')
loglog(err_fb,cpu_fb,'bo-',label='forward error flagging')
loglog(err_a,cpu_a,'rs-',label='adjoint error flagging')
loglog([1e-3,1e-1],[0.1*(1e-3)**(-1.5), 0.1* (1e-1)**(-1.5)],'k--',
        label='reference line')

xlim(1e-3,0.1)
#ylim(0,3000)
tick_params(axis='both', which='major', labelsize=fs)
grid(True)
xlabel('error achieved',fontsize=fs)
ylabel('CPU time (seconds)',fontsize=fs)
legend(loc='upper right',framealpha=1,fontsize=12)

if 0:
    fname = 'cpu_vs_error.png'
    savefig(fname, bbox_inches='tight')
    print('Created ',fname)
