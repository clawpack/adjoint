c     ==================================================================
      subroutine setaux(mbc,mx,my,xlower,ylower,
     &                  dx,dy,maux,aux)
c     ==================================================================
c
c     # set auxiliary arrays
c
c     # acoustics in a heterogeneous medium:
c     #  aux(i,j,1) = density p in (i,j) cell
c     #  aux(i,j,2) = sound speed c in (i,j) cell
c
c
      use amr_module, only : NEEDS_TO_BE_SET
      use adjoint_module, only: innerprod_index, adjoint_flagging

      implicit double precision (a-h,o-z)
      double precision aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)
      common /comaux/ p1,c1,p2,c2


      do j = 1-mbc,my+mbc
        do i = 1-mbc,mx+mbc
            xcell = xlower + (i-0.5d0)*dx

            if (adjoint_flagging .and. 
     &             (aux(1,i,j) .eq. NEEDS_TO_BE_SET)) then
                aux(innerprod_index,i,j) = 0.d0
            endif

            if (xcell .lt. 0.d0) then
                aux(1,i,j) = p1
                aux(2,i,j) = c1
            else
                aux(1,i,j) = p2
                aux(2,i,j) = c2
            endif
        enddo
      enddo

      return
      end

