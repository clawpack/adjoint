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
      common /cparam/ grav,x1,x2

      write(*,*) "Values: ", x1,x2,eps,grav

      pi = 4.d0*datan(1.d0)
c
c
       do 150 i=1,mx
         xcell = xlower + (i-0.5d0)*dx
         q(1,i) = 0.d0 - aux(1,i)
         q(2,i) = 0.d0

         if (xcell.gt.x2 .and. xcell.lt.x1) then
            q(1,i) = q(1,i) + 0.4
            q(2,i) = 0.d0
         endif
         

  150    continue
c
      return
      end

