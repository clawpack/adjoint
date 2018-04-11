from numpy import *
from matplotlib.pyplot import *
from pylab import *

# Setting up local variables
tols1 = ['1e-1','5e-2','1e-2','5e-3','1e-3','5e-4','1e-4','5e-5','1e-5','5e-6','1e-6','5e-7','1e-7','5e-8','1e-8']
tols2 = ['1e-1','1e-1','1e-2','5e-3','1e-3','5e-4','1e-4','5e-5','1e-5','5e-6','1e-6','5e-7','1e-7','5e-8','1e-8']
nvals1 = len(tols1)
nvals2 = len(tols2)

xpts = linspace(7,8,51840)
aframes = 272
fframes = 68

# Timing and cells from adjoint-error flagging (wo_dttf)
aerr_regrid_times = [  0.34546667,   0.54173333,   7.04166667,   7.9764    ,
                     11.0902    ,  13.10933333,  18.81613333,  19.3402    ,
                     19.81413333,  19.57746667,  19.3888    ,  20.00666667,
                     20.31586667,  20.5228    ,  21.74833333]
aerr_times =        [   1.59453333,    1.41066667,   49.7838    ,   57.41646667,
                     94.03206667,  102.0296    ,  180.90886667,  181.3828    ,
                     196.79806667,  193.936     ,  197.32653333,  216.01133333,
                     232.9678    ,  237.95313333,  254.9188    ]

# Timing and cells from error-flagging
err_regrid_times = [  3.39333333e-02,3.39333333e-02, 3.39333333e-02,   3.90666667e-02,   2.74933333e-01,
                    1.20060000e+00,   8.95800000e+00,   8.82813333e+00,
                    1.57788000e+01,   1.69757333e+01,   2.45866000e+01,
                    2.50084667e+01,   3.27431333e+01,   3.40129333e+01,
                    4.51994000e+01]
err_times =        [ 1.01066667e-01,1.01066667e-01, 1.01066667e-01,   1.09066667e-01,   6.43800000e-01,
                    2.73693333e+00,   6.57001333e+01,   6.35487333e+01,
                    9.40468667e+01,   1.16356933e+02,   2.04287867e+02,
                    2.39294533e+02,   3.57770533e+02,   3.57764067e+02,
                    5.00936933e+02]

# Timing and cells from adjoint-magnitude flagging
amag_regrid_times = [  7.86353333,  11.27773333,  12.91313333,  13.5374    ,
                     14.431     ,  15.13446667,  15.79033333,  16.0214    ,
                     16.7012    ,  17.39093333,  17.408     ,  17.69086667,
                     18.63646667,  19.1488    ,  19.6326    ]
amag_times =        [  99.433     ,  137.71966667,  164.38586667,  176.40306667,
                     196.5406    ,  215.56973333,  223.08      ,  224.06506667,
                     230.02913333,  233.08226667,  237.43206667,  238.77506667,
                     245.03646667,  247.90946667,  254.83593333]

# Timing and cells from difference-flagging
mag_regrid_times = [  5.83813333,   6.4396    ,   8.19706667,  10.8272    ,
                    17.16193333,  19.45466667,  23.54473333,  24.0328    ,
                    26.91746667,  27.77793333,  30.71753333,  31.33973333,
                    34.1494    ,  35.04853333,  37.60506667]
mag_times =        [  62.35513333,   70.39846667,   91.7976    ,  157.0992    ,
                    319.25366667,  376.70653333,  478.69006667,  487.7926    ,
                    547.37546667,  575.29913333,  649.66366667,  667.6186    ,
                    728.5252    ,  748.44173333,  803.78753333]


# -------------------------------
# Calculated Errors:
# -------------------------------

mag_errors_fine = [  1.23259096e-02,   4.98163462e-04,   1.10411928e-04,
                   6.96127184e-05,   1.13041147e-05,   5.45272817e-06,
                   1.00414550e-08,   6.51570064e-08,   1.43455811e-07,
                   5.70596959e-08,   1.03181748e-07,   6.89130173e-08,
                   6.51632550e-08,   4.82854012e-08,   3.83880987e-08]
amag_errors_fine = [  3.18967109e-02,   5.78957001e-02,   3.77220092e-05,
                    4.04839511e-05,   2.24628789e-06,   9.53335480e-07,
                    3.58287988e-07,   1.85421648e-07,   5.31639205e-08,
                    6.94218693e-08,   1.28840429e-08,   2.03169810e-08,
                    3.41971342e-08,   4.28829973e-08,   4.45304836e-08]
aerr_errors_fine = [  1.25061800e-01,   1.36520589e-01,   9.19010865e-03,
                    1.90631184e-03,   3.89264680e-04,   2.91456948e-04,
                    5.59760452e-05,   3.60995231e-05,   5.65041457e-06,
                    4.10270591e-06,   2.06375769e-06,   1.27561156e-06,
                    4.10117068e-07,   2.71979599e-07,   1.21088515e-07]
err_errors_fine = [ 1.10835397e-01,1.10835397e-01, 1.10835397e-01,   1.11893952e-01,   1.16530170e-01,
                   4.44174340e-02,   1.16975451e-02,   2.45145744e-04,
                   8.84064936e-04,   6.32950648e-04,   1.35934422e-04,
                   6.96918161e-05,   1.34188941e-06,   3.19636407e-06,
                   8.82449743e-08]



size = 20

fig = figure(1,(10,8))
axes([0.11,0.23,0.85,0.72])
loglog(tols2[::2],err_errors_fine[::2],'r',label='Error-Flagging',linewidth=2)
loglog(tols1[::2],mag_errors_fine[::2],'b',label='Difference-Flagging',linewidth=2)
loglog(tols1[::2],aerr_errors_fine[::2],'k',label='Adjoint-Error Flagging',linewidth=2)
loglog(tols1[::2],amag_errors_fine[::2],'g',label='Adjoint-Magnitude Flagging',linewidth=2)
legend(bbox_to_anchor=(0.95,0), loc="lower right",bbox_transform=fig.transFigure, ncol=2,fontsize=size)
title("Tolerance vs. Error in J",fontsize=size)
xlabel("Tolerance",fontsize=size)
ylabel("Error in J",fontsize=size)
tick_params(axis='y',labelsize=size)
tick_params(axis='x',labelsize=size)
plt.axis([10**(-8), 10**(-1), 10**(-8), 10**(0)])
savefig('tolvserror_ex1.png')
clf()

fig2 = figure(1,(10,8))
axes([0.11,0.23,0.85,0.72])
plt.semilogy(err_times[::2],err_errors_fine[::2],'r',label='Error-Flagging',linewidth=2)
plt.semilogy(mag_times[:-6:2],mag_errors_fine[:-6:2],'b',label='Difference-Flagging',linewidth=2)
plt.semilogy(aerr_times[::2],aerr_errors_fine[::2],'k',label='Adjoint-Error Flagging',linewidth=2)
plt.semilogy(amag_times[::2],amag_errors_fine[::2],'g',label='Adjoint-Magnitude Flagging',linewidth=2)
plt.title('Error vs. Total CPU Time', fontsize=size)
plt.legend(loc=3,fontsize=size)
xlabel("CPU Time",fontsize=size)
ylabel("Error",fontsize=size)
plt.axis([0, 500, 2*10**(-7), 10**(-2)])
tick_params(axis='y',labelsize=size)
tick_params(axis='x',labelsize=size)
legend(bbox_to_anchor=(0.95,0), loc="lower right",bbox_transform=fig2.transFigure, ncol=2,fontsize=size)
plt.savefig('errvstime_ex1.png')
clf()

fig3 = figure(1,(10,8))
axes([0.11,0.23,0.85,0.72])
plt.semilogy(err_regrid_times[::2],err_errors_fine[::2],'r',label='Error-Flagging',linewidth=2)
plt.semilogy(mag_regrid_times[:-6:2],mag_errors_fine[:-6:2],'b',label='Difference-Flagging',linewidth=2)
plt.semilogy(aerr_regrid_times[::2],aerr_errors_fine[::2],'k',label='Adjoint-Error Flagging',linewidth=2)
plt.semilogy(amag_regrid_times[::2],amag_errors_fine[::2],'g',label='Adjoint-Magnitude Flagging',linewidth=2)
plt.title('Error vs. Regridding CPU Time', fontsize=size)
plt.legend(loc=3,fontsize=size)
xlabel("CPU Time",fontsize=size)
ylabel("Error",fontsize=size)
plt.axis([0, 50, 2*10**(-7), 10**(-2)])
tick_params(axis='y',labelsize=size)
tick_params(axis='x',labelsize=size)
legend(bbox_to_anchor=(0.95,0), loc="lower right",bbox_transform=fig3.transFigure, ncol=2,fontsize=size)
plt.savefig('errvsregridtime_ex1.png')
clf()
