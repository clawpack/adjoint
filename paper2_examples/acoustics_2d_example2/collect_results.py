
from pylab import *
import clawpack.pyclaw.gauges as gauges
from scipy.interpolate import interp1d

fs = 15 # fontsize

gaugeno=0
t1 = 20.5
t2 = 21.5

truns = ['1600x1200','0025','005','01','02','lte0025','lte005','lte01','lte02']
outdirs = ['_output_%s' % trun for trun in truns]

tunif = linspace(t1,t2,10000)

punif = {}
perr = {}
cpu = {}

for k in range(len(truns)):
    outdir = outdirs[k]
    trun = truns[k]
    
    timings = open('%s/timing.txt' % outdir).readlines()
    for line in timings:
        if 'Total time:' in line:
            tokens = line.split()
            cpu[k] = float(tokens[-1])
            print('%s: CPU = %s' % (trun,tokens[-1]))
    gauge = gauges.GaugeSolution(gaugeno, outdir)
    t = gauge.t
    q = gauge.q
    p = q[0,:]
    j = where(logical_and(t>t1-0.1,t<t2+0.1))[0]
    tt = t[j]
    pp = p[j]
    
    pfcn = interp1d(tt,pp)
    punif[trun] = pfcn(tunif)
    if k>0:
        pfine = punif[truns[0]]
        perr[trun] = abs(punif[trun] - pfine).max()
        print('%s: diff = %.4f' % (trun,perr[trun]))
    
tol = [.0025,.005,.01,.02]
cpu_lte = [1329,581,225,63]
cpu_a = [407,125,17,2]
err_a = [0.0027,.0083,.0354,.0837]
err_lte = [.0031,.0067,.0122,.0347]
cpu_fine = 2823.5

figure(21)
clf()
loglog(tol,err_lte,'bo-',label='forward error flagging') 
loglog(tol,err_a,'rs-',label='adjoint error flagging')    
axis('scaled'); grid(True)
axis([1e-3,1e-1,1e-3,1e-1])
loglog([1e-3,0.1],[1e-3,0.1],'k--')
tick_params(axis='both', which='major', labelsize=fs)
xlabel('tolerance specified',fontsize=fs)
ylabel('max diff in p over [t1,t2]',fontsize=fs)
legend(loc='lower right',framealpha=1,fontsize=10)
if 1:
    fname = 'error_plot.png'
    savefig(fname, bbox_inches='tight')
    print('Created ',fname)

figure(22, figsize=(8,5))
clf()
semilogx(tol,cpu_fine*ones(len(tol)),'g--',lw=3,label='uniform fine grid')
semilogx(tol,cpu_lte,'bo-',label='forward error flagging')
semilogx(tol,cpu_a,'rs-',label='adjoint error flagging')

axis([1e-3,0.1,0,3000])
tick_params(axis='both', which='major', labelsize=fs)
#text(tol[0],cpu_fine+20, 'uniform fine grid',fontsize=fs)
grid(True)
xlabel('tolerance specified',fontsize=fs)
ylabel('CPU time (seconds)',fontsize=fs)
legend(loc='lower right',framealpha=1)
if 1:
    fname = 'cpu_plot.png'
    savefig(fname, bbox_inches='tight')
    print('Created ',fname)