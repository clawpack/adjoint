c     
c     
c=========================================================
      subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)
c=========================================================
c     
c     # Set initial conditions for q.
c     # Pulse in pressure, zero velocity
c     
c     
      implicit none

      integer, intent(in) :: meqn, mbc, mx, maux
      double precision, intent(in) :: xlower, dx, aux
      double precision, intent(out) :: q
      dimension q(meqn, 1-mbc:mx+mbc)
      dimension aux(maux, 1-mbc:mx+mbc)

      common /cqinit/ beta
      double precision beta

      integer i
      double precision xcell, pi, a
      pi = 4.d0*datan(1.d0)
      a = dsqrt(beta/pi)
c     
c     
      do 150 i=1,mx
         xcell = xlower + (i-0.5d0)*dx

         if (xcell.gt.5d0 .and. xcell.lt.9d0) then
             q(1,i) = a*dexp(-beta*(xcell-7.5d0)**2)
         else
             q(1,i) = 0.d0
         endif

         q(2,i) = 0.d0
 150  continue
c
      return
      end
