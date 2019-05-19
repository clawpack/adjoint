from numpy import *
from matplotlib.pyplot import *
from pylab import *

# Setting up local variables
tols = ['1e-0','6e-1','3e-1',
        '1e-1','6e-2','3e-2',
        '1e-2','6e-3','3e-3',
        '1e-3','6e-4','3e-4',
        '1e-4','6e-5','3e-5',
        '1e-5']

## ---------------------------------
## Setting up vectors of amount of work done:
## ---------------------------------

# Timing and cells from adjoint-magnitude flagging
amag_regrid = [ 168.3828    ,  160.60822222,  150.9964    ,  138.6031    ,
               82.6206    ,   47.2141    ,   35.9217    ,   14.6139    ,
               2.756     ,    0.796     ,    0.3159    ,    0.2619    ,
               0.2592    ,    0.2268    ,    0.2229    ,    0.2215    ]
amag_times = [  1.58622970e+03,   1.49281189e+03,   1.34246280e+03,
              1.16435800e+03,   6.55311900e+02,   3.61060100e+02,
              2.66386500e+02,   1.03079700e+02,   1.77373000e+01,
              5.11060000e+00,   1.97270000e+00,   1.55870000e+00,
              1.49700000e+00,   1.25520000e+00,   1.24660000e+00,
              1.23730000e+00]
amag_regrid = amag_regrid[::-1]
amag_times = amag_times[::-1]

# Timing and cells from adjoint-error flagging
aerr_regrid = [ 222.4333,  221.5709,  219.9372,  219.7524,  215.9752,  213.4921,
               213.1097,  202.8152,  104.2194,    0.3299,    0.3157,    0.2973,
               0.322 ,    0.3236,    0.3348,    0.3322]
aerr_times = [  1.65396950e+03,   1.64503170e+03,   1.63447290e+03,
              1.63348660e+03,   1.58072580e+03,   1.55252160e+03,
              1.54025240e+03,   1.39645700e+03,   6.43393800e+02,
              1.42510000e+00,   1.40220000e+00,   1.29830000e+00,
              1.38490000e+00,   1.37970000e+00,   1.42630000e+00,
              1.41970000e+00]
aerr_regrid = aerr_regrid[::-1]
aerr_times = aerr_times[::-1]

# Timing and cells from difference-flagging
diff_regrid = [ 101.3334,  100.4365,   99.8504,  101.3604,   99.7821,   96.9741,
               94.8886,   88.6307,   80.675 ,   76.9986,   49.4936,   29.1913,
               14.6271,    1.3023,    0.2764,    0.1175]
diff_times = [  1.71767820e+03,   1.71282980e+03,   1.70584980e+03,
              1.70690280e+03,   1.71527140e+03,   1.67923300e+03,
              1.63604370e+03,   1.54464870e+03,   1.39813830e+03,
              1.29744650e+03,   7.76082100e+02,   4.37399700e+02,
              2.10789500e+02,   1.55218000e+01,   3.33560000e+00,
              1.47840000e+00]
diff_regrid = diff_regrid[::-1]
diff_times = diff_times[::-1]

# Timing and cells from error-flagging
err_regrid = [ 207.3158,  194.2371,  182.5131,  164.8369,  103.2788,   59.2029,
              22.7793,    2.6414,    0.7793,    0.446 ,    0.2799,    0.2688,
              0.2807,    0.2664,    0.2709,    0.2642]
err_times = [  1.70307200e+03,   1.48634670e+03,   1.28684730e+03,
             1.04123930e+03,   5.06128100e+02,   2.31970000e+02,
             7.67219000e+01,   8.73310000e+00,   2.72430000e+00,
             1.68660000e+00,   1.16740000e+00,   1.12400000e+00,
             1.18160000e+00,   1.16350000e+00,   1.19180000e+00,
             1.16100000e+00]
err_regrid = err_regrid[::-1]
err_times = err_times[::-1]

## ---------------------------------
## Setting up vectors with error in solutions:
## ---------------------------------
diff_errors_fine = [  1.88803323e-02,   1.80756249e-02,   1.31571836e-02,
                    2.44708545e-03,   6.67765406e-04,   1.13649307e-04,
                    4.30387844e-05,   2.34284826e-06,   8.14584907e-06,
                    5.12725708e-07,   5.49981515e-06,   3.11343017e-07,
                    3.09194313e-07,   3.08818669e-07,   3.08488960e-07,
                    3.08261548e-07]

amag_errors_fine = [  1.66309793e-02,   1.66309793e-02,   1.66309793e-02,
                    1.63869141e-02,   1.63830704e-02,   1.63455552e-02,
                    1.76997206e-02,   1.46060597e-02,   1.13565015e-03,
                    5.12797344e-04,   2.74694425e-04,   3.40168469e-04,
                    3.38413701e-05,   1.26387074e-07,   8.35988978e-06,
                    0.00000000e+00]

aerr_errors_fine = [  1.91503471e-02,   1.91503471e-02,   1.91503471e-02,
                    1.91503471e-02,   1.91503471e-02,   1.91503471e-02,
                    1.91180102e-02,   8.06758744e-04,   4.41458490e-05,
                    7.03947247e-06,   7.14602929e-06,   1.95601111e-06,
                    1.14262929e-06,   2.76824135e-06,   2.12155203e-06,
                    1.96862724e-06]

err_errors_fine = [  1.66309793e-02,   1.66309793e-02,   1.66309793e-02,
                   1.66309793e-02,   1.66309163e-02,   1.66234431e-02,
                   1.64147606e-02,   1.50676298e-02,   1.10137446e-02,
                   7.27707216e-03,   2.06864462e-03,   6.11217733e-04,
                   8.21253224e-05,   5.67292759e-05,   8.46845563e-06,
                   4.05137217e-06]

size = 20
fig = figure(1,(10,8))
axes([0.11,0.23,0.85,0.72])
loglog(tols,err_errors_fine,'r',label='Error-Flagging',linewidth=2)
loglog(tols,diff_errors_fine,'b',label='Difference-Flagging',linewidth=2)
loglog(tols,aerr_errors_fine,'k',label='Adjoint-Error Flagging',linewidth=2)
loglog(tols,amag_errors_fine,'g',label='Adjoint-Magnitude Flagging',linewidth=2)
legend(bbox_to_anchor=(0.95,0), loc="lower right",bbox_transform=fig.transFigure, ncol=2,fontsize=size)
title("Tolerance vs. Error in J",fontsize=size)
xlabel("Tolerance",fontsize=size)
ylabel("Error in J",fontsize=size)
tick_params(axis='y',labelsize=size)
tick_params(axis='x',labelsize=size)
plt.axis([10**(-4), 10**(0), 5*10**(-4), 2*10**(-2)])
savefig('tolvserror_2d_ex3.png')
clf()

fig2 = figure(1,(10,8))
axes([0.11,0.23,0.85,0.72])
plt.semilogy(err_times[:],err_errors_fine[:],'r',label='Error-Flagging',linewidth=2)
plt.semilogy(diff_times[:],diff_errors_fine[:],'b',label='Difference-Flagging',linewidth=2)
plt.semilogy(aerr_times[:],aerr_errors_fine[:],'k',label='Adjoint-Error Flagging',linewidth=2)
plt.semilogy(amag_times,amag_errors_fine,'g',label='Adjoint-Magnitude Flagging',linewidth=2)
plt.title('Error vs. Total CPU Time', fontsize=size)
plt.legend(loc=3,fontsize=size)
xlabel("CPU Time",fontsize=size)
ylabel("Error",fontsize=size)
plt.axis([0, 800, 5*10**(-4), 2*10**(-2)])
tick_params(axis='y',labelsize=size)
tick_params(axis='x',labelsize=size)
legend(bbox_to_anchor=(0.95,0), loc="lower right",bbox_transform=fig2.transFigure, ncol=2,fontsize=size)
plt.savefig('errvstime_2d_ex3.png')
clf()

fig3 = figure(1,(10,8))
axes([0.11,0.23,0.85,0.72])
plt.semilogy(err_regrid,err_errors_fine,'r',label='Error-Flagging',linewidth=2)
plt.semilogy(diff_regrid,diff_errors_fine,'b',label='Difference-Flagging',linewidth=2)
plt.semilogy(aerr_regrid,aerr_errors_fine,'k',label='Adjoint-Error Flagging',linewidth=2)
plt.semilogy(amag_regrid,amag_errors_fine,'g',label='Adjoint-Magnitude Flagging',linewidth=2)
plt.title('Error vs. Regridding CPU Time', fontsize=size)
plt.legend(loc=3,fontsize=size)
xlabel("CPU Time",fontsize=size)
ylabel("Error",fontsize=size)
plt.axis([0, 140, 5*10**(-4), 2*10**(-2)])
tick_params(axis='y',labelsize=size)
tick_params(axis='x',labelsize=size)
legend(bbox_to_anchor=(0.95,0), loc="lower right",bbox_transform=fig3.transFigure, ncol=2,fontsize=size)
plt.savefig('errvsregridtime_2d_ex3.png')
clf()

