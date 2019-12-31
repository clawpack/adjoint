      subroutine setprob
      implicit double precision (a-h,o-z)
      character*25 fname

      real(kind=8) :: p1,c1,p2,c2
      common /comaux/ p1,c1,p2,c2

c
c     # Set the material parameters for the acoustic equations
c
c
      iunit = 7
      fname = 'setprob.data'
c     # open the unit with new routine from Clawpack 4.4 to skip over
c     # comment lines starting with #:
      call opendatafile(iunit, fname)
                
c
      read(7,*) p1
      read(7,*) c1
      read(7,*) p2
      read(7,*) c2

      return
      end
