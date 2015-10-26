      subroutine setprob

      implicit none

      common /cqinit/ x1,x2

      common /comaux/ Zl, cl, Zr, cr
      double precision rhol, Zl, cl, rhor, Zr, cr
      double precision x1,x2
c
c     # Set the material parameters for the acoustic equations
c
      character*25 fname

      fname = 'setprob.data'
      call opendatafile(7, fname)

c     # x1,x2 for initial conditions:
      read(7,*) x1
      read(7,*) x2
c
c     # Piecewise constant medium with single interface at x=0
c     # Density and sound speed to left and right:
      read(7,*) rhol
      read(7,*) cl
      Zl = rhol*cl

      read(7,*) rhor
      read(7,*) cr
      Zr = rhor*cr

      return
      end
