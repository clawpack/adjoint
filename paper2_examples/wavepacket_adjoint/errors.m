
% Errors computed with different methods at time t=1 and t=2
%
%             dx          max-norm      1-norm

errmct1 = [ ...
            1.0000e-02   6.8816e-01   6.1604e-02 ; ...
	    5.0000e-03   2.6733e-01   1.7351e-02 ; ...
	    2.5000e-03   8.7570e-02   4.8530e-03 ; ...
	    1.2500e-03   2.8395e-02   1.4789e-03 ; ...
	    6.2500e-04   1.1194e-02   4.0201e-04 ; ...
	    3.1250e-04   4.7687e-03   1.0281e-04 ...
	  ];


errmct2 = [ ...
            1.0000e-02   8.2678e-01   7.4587e-02 ; ...
	    5.0000e-03   4.0509e-01   3.0794e-02 ; ...
	    2.5000e-03   1.2578e-01   7.1907e-03 ; ...
	    1.2500e-03   4.1194e-02   2.5240e-03 ; ...
	    6.2500e-04   1.6829e-02   7.3586e-04 ; ...
	    3.1250e-04   7.4854e-03   1.9510e-04 ...
	  ];


errlwt1 = [ ...
            1.0000e-02   1.0141e+00   9.9809e-02 ; ...
	    5.0000e-03   6.6104e-01   6.3131e-02 ; ...
	    2.5000e-03   2.1398e-01   1.8959e-02 ; ...
	    1.2500e-03   5.5757e-02   4.8552e-03 ; ...
	    6.2500e-04   1.4036e-02   1.2173e-03 ; ...
	    3.1250e-04   3.5135e-03   3.0448e-04  ...
	  ];


errlwt2 = [ ...
            1.0000e-02   9.9843e-01   9.7020e-02 ; ...
	    5.0000e-03   9.7158e-01   9.9624e-02 ; ...
	    2.5000e-03   4.0659e-01   3.6796e-02 ; ...
	    1.2500e-03   1.1085e-01   9.6707e-03 ; ...
	    6.2500e-04   2.8044e-02   2.4335e-03 ; ...
	    3.1250e-04   7.0257e-03   6.0893e-04  ...
	  ];

clf
%Haxes = axes('position',[.1 .1 .8 .8]);
set(gca,'fontsize',15)
loglog(errlwt1(:,1),errlwt1(:,2),'-','LineWidth',2.0)
hold on
loglog(errmct1(:,1),errmct1(:,2),'--','LineWidth',2.0)
%loglog(errsbt1(:,1),errsbt1(:,2),'-.')
title('max-norm errors at t = 1')
%legend('Lax-Wendroff','MC-limiter','Superbee')
legend('Lax-Wendroff','MC-limiter')
loglog(errlwt1(:,1),errlwt1(:,2),'.','MarkerSize',25)
loglog(errmct1(:,1),errmct1(:,2),'.','MarkerSize',25)

loglog([2e-4 2e-3],[2e-2 2e0])
text(2.3e-4,1e-1,'slope 2','fontsize',15)

hold off
figure

clf
%Haxes = axes('position',[.1 .1 .8 .8]);
set(gca,'fontsize',15)
loglog(errlwt2(:,1),errlwt2(:,2),'-','LineWidth',2.0)
hold on
loglog(errmct2(:,1),errmct2(:,2),'--','LineWidth',2.0)
%loglog(errsbt2(:,1),errsbt2(:,2),'-.')
title('max-norm errors at t = 2')
%legend('Lax-Wendroff','MC-limiter','Superbee')
legend('Lax-Wendroff','MC-limiter')
loglog(errlwt2(:,1),errlwt2(:,2),'.','MarkerSize',25)
loglog(errmct2(:,1),errmct2(:,2),'.','MarkerSize',25)

loglog([2e-4 2e-3],[2e-2 2e0])
text(2.3e-4,1e-1,'slope 2','fontsize',15)

hold off
figure

disp(['Errors at t = 2'])
ne = size(errmct2,1);
A = [1  log(errmct2(ne-1,1));  1 log(errmct2(ne,1))];
b = [log(errmct2(ne-1,2));  log(errmct2(ne,2))];
y = A\b;
C = exp(y(1));
order = y(2);
disp(['max-norm error for MC = ' num2str(C) ' * h^(' num2str(order) ')'])

ne = size(errlwt2,1);
A = [1  log(errlwt2(ne-1,1));  1 log(errlwt2(ne,1))];
b = [log(errlwt2(ne-1,2));  log(errlwt2(ne,2))];
y = A\b;
C = exp(y(1));
order = y(2);
disp(['max-norm error for LW = ' num2str(C) ' * h^(' num2str(order) ')'])

clf
%Haxes = axes('position',[.1 .1 .8 .8]);
set(gca,'fontsize',15)
loglog(errlwt1(:,1),errlwt1(:,3),'-','LineWidth',2.0)
hold on
loglog(errmct1(:,1),errmct1(:,3),'--','LineWidth',2.0)
%loglog(errsbt1(:,1),errsbt1(:,3),'-.')
title('1-norm errors at t = 1')
%legend('Lax-Wendroff','MC-limiter','Superbee')
legend('Lax-Wendroff','MC-limiter')
loglog(errlwt1(:,1),errlwt1(:,3),'.','MarkerSize',25)
loglog(errmct1(:,1),errmct1(:,3),'.','MarkerSize',25)

loglog([2e-4 2e-3],[2e-2 2e0])
text(2.3e-4,1e-1,'slope 2','fontsize',15)

hold off
figure

clf
%Haxes = axes('position',[.1 .1 .8 .8]);
set(gca,'fontsize',15)
loglog(errlwt2(:,1),errlwt2(:,3),'-','LineWidth',2.0)
hold on
loglog(errmct2(:,1),errmct2(:,3),'--','LineWidth',2.0)
%loglog(errsbt2(:,1),errsbt2(:,3),'-.')
title('1-norm errors at t = 2')
%legend('Lax-Wendroff','MC-limiter','Superbee')
legend('Lax-Wendroff','MC-limiter')
loglog(errlwt2(:,1),errlwt2(:,3),'.','MarkerSize',25)
loglog(errmct2(:,1),errmct2(:,3),'.','MarkerSize',25)

loglog([2e-4 2e-3],[2e-2 2e0])
text(2.3e-4,1e-1,'slope 2','fontsize',15)

hold off

ne = size(errmct2,1);
A = [1  log(errmct2(ne-1,1));  1 log(errmct2(ne,1))];
b = [log(errmct2(ne-1,3));  log(errmct2(ne,3))];
y = A\b;
C = exp(y(1));
order = y(2);
disp(['1-norm error for MC = ' num2str(C) ' * h^(' num2str(order) ')'])

ne = size(errlwt2,1);
A = [1  log(errlwt2(ne-1,1));  1 log(errlwt2(ne,1))];
b = [log(errlwt2(ne-1,3));  log(errlwt2(ne,3))];
y = A\b;
C = exp(y(1));
order = y(2);
disp(['1-norm error for LW = ' num2str(C) ' * h^(' num2str(order) ')'])
