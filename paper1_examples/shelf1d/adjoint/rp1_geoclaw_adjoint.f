c======================================================================
       subroutine rp1(maxm,meqn,mwaves,maux,mbc,mx,
     &                 ql,qr,auxl,auxr,fwave,s,amdq,apdq)
c======================================================================
c
c Solves normal Riemann problems for the 2D SHALLOW WATER equations
c     with topography:
c     #        h_t + (hu)_x + (hv)_y = 0                           #
c     #        (hu)_t + (hu^2 + 0.5gh^2)_x + (huv)_y = -ghb_x      #
c     #        (hv)_t + (huv)_x + (hv^2 + 0.5gh^2)_y = -ghb_y      #

c On input, ql contains the state vector at the left edge of each cell
c     qr contains the state vector at the right edge of each cell
c
c This data is along a slice in the x-direction if ixy=1
c     or the y-direction if ixy=2.

c  Note that the i'th Riemann problem has left state qr(i-1,:)
c     and right state ql(i,:)
c  From the basic clawpack routines, this routine is called with
c     ql = qr
c
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                           !
!      # This Riemann solver is for the shallow water adjoint               !
!             equations. It is modified from rpn2_geoclaw.f.                !
!                                                                           !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

      implicit none

      !input
      integer maxm,meqn,maux,mwaves,mbc,mx,ixy

      double precision  fwave(meqn, mwaves, 1-mbc:maxm+mbc)
      double precision  s(mwaves, 1-mbc:maxm+mbc)
      double precision  ql(meqn, 1-mbc:maxm+mbc)
      double precision  qr(meqn, 1-mbc:maxm+mbc)
      double precision  apdq(meqn,1-mbc:maxm+mbc)
      double precision  amdq(meqn,1-mbc:maxm+mbc)
      double precision  auxl(maux,1-mbc:maxm+mbc)
      double precision  auxr(maux,1-mbc:maxm+mbc)

      !local only
      integer m,i,mw,maxiter
      double precision wall(2)
      double precision fw(2,2)
      double precision sw(2)
      double precision delta(2)

      double precision hR,hL,huR,huL
      double precision bR,bL,cL,cR,uhat,chat,grav
      double precision s1m,s2m
      double precision hstar,hstartest,hstarHLL,sLtest,sRtest
      double precision tw,dxdc
      double precision beta1, beta2, beta3, hRhat, hLhat

      logical rare1,rare2

!     # Gravity constant set in the setprob.f
      common /cparam/ grav

      !loop through Riemann problems at each grid cell
      do i=2-mbc,mx+mbc

!-----------------------Initializing-----------------------------------
         !inform of a bad riemann problem from the start
         if((qr(1,i-1).lt.0.d0).or.(ql(1,i) .lt. 0.d0)) then
            write(*,*) 'Negative input: hl,hr,i=',qr(1,i-1),ql(1,i),i
         endif

        !Initialize Riemann problem for grid interface
        do mw=1,mwaves
            s(mw,i)=0.d0
            fwave(1,mw,i)=0.d0
            fwave(2,mw,i)=0.d0

            fw(1,mw)=0.d0
            fw(2,mw)=0.d0
        enddo

         !zero (small) negative values if they exist
         if (qr(1,i-1).lt.0.d0) then
           qr(1,i-1)=0.d0
           qr(2,i-1)=0.d0
         endif

        if (ql(1,i).lt.0.d0) then
          ql(1,i)=0.d0
          ql(2,i)=0.d0
        endif

        !Riemann problem variables
        hL = qr(1,i-1)
        hR = ql(1,i)
        bL = auxr(1,i-1)
        bR = auxl(1,i)

        huL = qr(2,i-1)
        huR = ql(2,i)

        ! Linearizing
        hLhat = -bL
        hRhat = -bR

c       ! Check for wet/dry boundary
        if (hR <= 0.d0) then
            hR = 0.d0
            huR = 0.d0
            hRhat = 0.d0
        endif
        if (hL <= 0.d0) then
            hL = 0.d0
            huL = 0.d0
            hLhat = 0.d0
        endif

        wall(1) = 1.d0
        wall(2) = 1.d0

         !determine wave speeds
         cL=sqrt(grav*hLhat) ! 1 wave speed of left state
         cR=sqrt(grav*hRhat) ! 2 wave speed of right state

         !--------------------end initializing----------
         !solve Riemann problem.

c       # f-wave splitting
        delta(1) = -huR*cR**2 + huL*cL**2
        delta(2) = -(hR+bR) + (hL+bL)

        beta1 = (delta(1) + cR*delta(2))/(cL + cR)
        beta2 = (-delta(1) + cL*delta(2))/(cL + cR)

        if (cL + cR == 0.d0) then
            beta1 = (delta(1) + cR*delta(2))
            beta2 = (-delta(1) + cL*delta(2))
        endif

c       # Compute the waves.
        fw(1,1) = cL*beta1
        fw(2,1) = beta1
        sw(1) = -cL

        fw(1,2) = -cR*beta2
        fw(2,2) = beta2
        sw(2) = cR

c        !eliminate ghost fluxes for wall
         do mw=1,2
            sw(mw)=sw(mw)*wall(mw)

            fw(1,mw)=fw(1,mw)*wall(mw)
            fw(2,mw)=fw(2,mw)*wall(mw)
         enddo

         do mw=1,mwaves
            s(mw,i)=sw(mw)
            fwave(1,mw,i)=fw(1,mw)
            fwave(2,mw,i)=fw(2,mw)
         enddo

 30      continue
      enddo

 !        write(*,*) "Starting"
c============= compute fluctuations=============================================
         amdq(1:2,:) = 0.d0
         apdq(1:2,:) = 0.d0
         do i=2-mbc,mx+mbc
             do  mw=1,mwaves
!               write(*,*) "1", fwave(1:2,mw,i)
               if (s(mw,i) < 0.d0) then
                 amdq(1:2,i) = amdq(1:2,i) + fwave(1:2,mw,i)
               else if (s(mw,i) > 0.d0) then
                 apdq(1:2,i)  = apdq(1:2,i) + fwave(1:2,mw,i)
               else
                 amdq(1:2,i) = amdq(1:2,i) + 0.5d0 * fwave(1:2,mw,i)
                 apdq(1:2,i) = apdq(1:2,i) + 0.5d0 * fwave(1:2,mw,i)
               endif
             enddo
         enddo

         do i=2-mbc, mx+mbc
!             write(*,*) "2", fwave(1:meqn,1,i), fwave(1:meqn,2,i)
             amdq(1:meqn,i) = fwave(1:meqn,1,i)
             apdq(1:meqn,i) = fwave(1:meqn,2,i)
         enddo
!         write(*,*) "Finished"

      return
      end subroutine
