c
c
c =========================================================
       subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)
c =========================================================
c
c     # Set initial conditions for q.
c     # Pulse in h, zero velocity
c
c
      implicit double precision (a-h,o-z)
      dimension q(meqn,1-mbc:mx+mbc)
      dimension aux(maux,1-mbc:mx+mbc)
      common /comeps/ eps
      common /comrp/ grav
      
      pi = 4.d0*datan(1.d0)
c
c
c
       do 150 i=1,mx
         xcell = xlower + (i-0.5d0)*dx
         q(1,i) = 0.d0 - aux(1,i)
         q(2,i) = 0.d0
         c = dsqrt(grav*q(1,i))
         x1 = -200.e3
         x2 = -150.e3
         x3 = -100.e3
         xmid = 0.5d0*(x1+x3)

         if (xcell.gt.x2 .and. xcell.lt.x3) then
            deta =  eps*dsin((xcell-xmid)*pi/(x3-xmid))
            q(1,i) = q(1,i) + deta
            q(2,i) = 0.d0
         endif
         

  150    continue
c
      return
      end

