% shift qtrue to proper position to plot, taking into account periodic BCs:
ntrue = length(qtrue);
qt2 = [qtrue;qtrue];
i1 = ntrue - floor((t-floor(t))*ntrue);

hold on
plot(xtrue,qt2(i1+1:i1+ntrue))
axis([0 1 -1 1.5])
hold off

if Frame==0
    q0 = q;
    end

if Frame>0
    err1 = sum(abs(q-q0))*dx;
    errinf = max(abs(q-q0));
    disp('      dx      errinf     err1')
    disp([dx errinf err1])
    end