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

      common /cqinit/ betal, betar, freql, freqr
      double precision betal, betar, freql, freqr

      integer i
      double precision xcell
c     
c     
      do 150 i=1,mx
         xcell = xlower + (i-0.5d0)*dx

c     # wave packet with left-going and right-going wave packets:
         q(1,i) = dexp(-betar*(xcell-3.0d0)**2) * dsin(freqr*xcell)
     .            + dexp(-betal*(xcell+2.5d0)**2) * dsin(freql*xcell)
         q(2,i) = 0.d0
         go to 150

 150  continue
c     
      return
      end
