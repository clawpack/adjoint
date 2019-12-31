
from pylab import *
import clawpack.pyclaw.gauges as gauges

gaugeno=0
t1 = 20.5
t2 = 21.5

labels = ['Fine grid','tol = 0.005','tol = 0.01','tol = 0.02','tol = 0.0025']
outdirs = ['_output_fine', '_output_005', '_output_01', 
           '_output_02', '_output_0025']
colors = ['r','k','m','b','m']
lws = [2.5,1.5,1.5,1.5,1.5]

figure(400, figsize=(11,8))
clf()
ax1 = subplot(211)
ax2 = subplot(212)

for k in range(4):
    outdir = outdirs[k]
    gauge = gauges.GaugeSolution(gaugeno, outdir)
    t = gauge.t
    q = gauge.q
    p = q[0,:]

    ax1.plot(t, p, color=colors[k], lw=lws[k], label=labels[k])
    ax2.plot(t, p, color=colors[k], lw=lws[k], label=labels[k])

    pphi = where(logical_and(t>t1,t<t2), p, 0)
    print('%s: max value of p in [t1,t2] is %.3f' % (labels[k],pphi.max()))

ax1.plot([t1,t1],[-1,1],'k--')
ax1.plot([t2,t2],[-1,1],'k--')
ax2.plot([t1,t1],[-1,1],'k--')
ax2.plot([t2,t2],[-1,1],'k--')

ax1.set_xlim(0,22)
ax1.set_ylim(-0.5,0.5)
ax1.grid(True)
ax1.legend(loc='lower left', framealpha = 1)

ax2.set_xlim(18,22)
ax2.set_ylim(-0.2,0.2)
ax2.grid(True)
ax2.legend(loc='lower left', framealpha = 1)

ax1.set_title('Gauge at x = 1.0, y = 5.5',fontsize=15)

if 1:
    fname = 'GaugePlots.png'
    savefig(fname, bbox_inches='tight')
    print('Created %s' % fname)

