module adjoint_module

    implicit none

    ! Adjoint data type definition
    type adjointData_type
        real(kind=8) :: time
        integer :: igrid, level, mx, my, meqn
        real(kind=8) :: xlow,ylow, dx, dy
        double precision, allocatable :: q(:,:,:)
    end type adjointData_type

    type(adjointData_type), allocatable :: adjoints(:)
    integer :: num_adjoints
    real(kind=8) :: trange_start, tfinal

contains

    subroutine read_adjoint_data(adjointFolder)

        implicit none

        ! Function Arguments
        character(len=364) :: fname1, fname2
        character(len=*), intent(in) :: adjointFolder
        integer :: iunit, iframe, k, i, j, m
        logical :: fileExists
        double precision :: finalT

        fileExists = .true.
        num_adjoints = -1
        do while (fileExists)
            num_adjoints = num_adjoints + 1
            fname1 = '../' // adjointFolder // '/_output/fort.q' &
                // char(ichar('0') + mod(num_adjoints/1000,10)) &
                // char(ichar('0') + mod(num_adjoints/100,10)) &
                // char(ichar('0') + mod(num_adjoints/10,10)) &
                // char(ichar('0') + mod(num_adjoints,10))

            inquire(file=fname1, exist=fileExists)
        end do

        num_adjoints = num_adjoints - 1

        iunit = 16
        allocate(adjoints(num_adjoints+1))

        do k = 1,num_adjoints+1

            iframe = num_adjoints - k + 1
            ! Read initial time in from fort.tXXXX file.
            fname2 = '../' // adjointFolder // '/_output/fort.t' &
                // char(ichar('0') + mod(iframe/1000,10)) &
                // char(ichar('0') + mod(iframe/100,10)) &
                // char(ichar('0') + mod(iframe/10,10)) &
                // char(ichar('0') + mod(iframe,10))
            open(iunit,file=fname2)
            read(iunit,*) adjoints(k)%time
            read(iunit,*) adjoints(k)%meqn
            close(iunit)

            ! first create the file name and open file
            fname1 = '../' // adjointFolder // '/_output/fort.q' &
                // char(ichar('0') + mod(iframe/1000,10)) &
                // char(ichar('0') + mod(iframe/100,10)) &
                // char(ichar('0') + mod(iframe/10,10)) &
                // char(ichar('0') + mod(iframe,10))
            open(iunit,file=fname1)

            ! Read grid parameters.
            read(iunit,*) adjoints(k)%igrid
            read(iunit,*) adjoints(k)%level
            read(iunit,*) adjoints(k)%mx
            read(iunit,*) adjoints(k)%my
            read(iunit,*) adjoints(k)%xlow
            read(iunit,*) adjoints(k)%ylow
            read(iunit,*) adjoints(k)%dx
            read(iunit,*) adjoints(k)%dy
            read(iunit,*)

            allocate(adjoints(k)%q(adjoints(k)%meqn,adjoints(k)%mx,adjoints(k)%my))
            ! Read variables in from old fort.qXXXX file.
            do j = 1,adjoints(k)%my
                do i = 1,adjoints(k)%mx
                    read(iunit,*) (adjoints(k)%q(m,i,j),m=1,adjoints(k)%meqn)
                enddo
            end do
            close(iunit)
        end do

        ! Reverse time
        finalT = adjoints(1)%time
        do k = 1,num_adjoints+1
            adjoints(k)%time = finalT - adjoints(k)%time
        end do

    end subroutine read_adjoint_data

    subroutine set_time_window(t1, t2)

        implicit none

        ! Function Arguments
        real(kind=8), intent(in) :: t1, t2

        write(*,*) ' '
        write(*,*) 'TIME WINDOW:'

        tfinal = t2
        trange_start = t1

        write(*,*) 'Initial time: ', trange_start, ', Final time: ', tfinal

    end subroutine set_time_window

    function interpolate_adjoint(k, xc, yc) result(q_value)
        implicit none

        integer, intent(in) :: k
        integer :: y_cell, x_cell, y_adjacent, x_adjacent
        real(kind=8), intent(in) :: xc, yc
        real(kind=8) :: x_main, x_side, y_main, y_side
        real(kind=8) :: h_current, eta_current, h_adjacent, eta_adjacent
        real(kind=8) :: aux_current, aux_adjacent
        double precision :: q_value(adjoints(k)%meqn)
        double precision :: q_temp1(adjoints(k)%meqn), q_temp2(adjoints(k)%meqn)
        logical :: y_interp

        y_cell = floor(((yc-adjoints(k)%ylow)/adjoints(k)%dy))
        x_cell = floor(((xc-adjoints(k)%xlow)/adjoints(k)%dx))

        ! Finding correct grid cell to interpolate with
        y_adjacent = floor(((yc-adjoints(k)%ylow)/adjoints(k)%dy) + 0.5d0)
        x_adjacent = floor(((xc-adjoints(k)%xlow)/adjoints(k)%dx) + 0.5d0)

        if (y_cell == y_adjacent .and. y_adjacent /= 0) then
            y_adjacent = y_adjacent - 1
        endif
        if (x_cell == x_adjacent .and. x_adjacent /= 0) then
            x_adjacent = x_adjacent - 1
        endif

        if (y_adjacent >= adjoints(k)%my) then
            y_adjacent = y_adjacent - 1
        endif
        if (x_adjacent >= adjoints(k)%mx) then
            x_adjacent = x_adjacent - 1
        endif

        ! Interpolating in y
        y_main = adjoints(k)%ylow + (y_cell + 0.5d0) * adjoints(k)%dy
        if (y_cell /= y_adjacent) then
            y_interp = .true.
            y_side = adjoints(k)%ylow + (y_adjacent + 0.5d0) * adjoints(k)%dy

            q_temp1 = ((y_side - yc)/(y_side - y_main))*adjoints(k)%q(:,x_cell+1,y_cell+1)&
                    + ((yc - y_main)/(y_side - y_main))*adjoints(k)%q(:,x_cell+1,y_adjacent+1)
            q_temp2 = ((y_side - yc)/(y_side - y_main))*adjoints(k)%q(:,x_adjacent+1,y_cell+1)&
                    + ((yc - y_main)/(y_side - y_main))*adjoints(k)%q(:,x_adjacent+1,y_adjacent+1)
        else
            y_interp = .false.
        endif

        ! Interpolating in x
        x_main = adjoints(k)%xlow + (x_cell + 0.5d0) * adjoints(k)%dx
        if (x_cell /= x_adjacent) then
            x_side = adjoints(k)%xlow + (x_adjacent + 0.5d0) * adjoints(k)%dx

            if(y_interp) then
                q_value = ((x_side - xc)/(x_side - x_main))*q_temp1&
                    + ((xc - x_main)/(x_side - x_main))*q_temp2
            else
                q_value = ((x_side - xc)/(x_side - x_main))*adjoints(k)%q(:,x_cell+1,y_cell+1)&
                    + ((xc - x_main)/(x_side - x_main))*adjoints(k)%q(:,x_adjacent+1,y_cell+1)
            endif
        else
            if (y_interp) then
                q_value = q_temp1
            else
                q_value = adjoints(k)%q(:,x_cell+1,y_cell+1)
            endif
        endif

    end function interpolate_adjoint

    function calculate_max_innerproduct(t,x_c,y_c,q1,q2,q3,tolsp) result(max_innerprod)

        real(kind=8), intent(in) :: t, tolsp
        integer :: r
        real(kind=8) :: q_innerprod1, q_innerprod2, q_innerprod, max_innerprod
        double precision, allocatable :: q_interp(:)
        real(kind=8) :: x_c,y_c,q1,q2,q3
        real(kind=8) :: aux_interp1, aux_interp2, aux1

        max_innerprod = 0.d0
        ! Select adjoint data
        aloop: do r=1,num_adjoints+1

          if (t <= adjoints(r)%time .and. &
              min((t + (tfinal - trange_start)),tfinal) >= adjoints(r-1)%time) then

            q_interp = interpolate_adjoint(r, x_c, y_c)
            q_innerprod1 = abs( q1 * q_interp(1) &
                  + q2 * q_interp(2) + q3 * q_interp(3))

            q_innerprod2 = 0.d0
            q_innerprod = q_innerprod1
            if (r .ne. 1) then
                q_interp = interpolate_adjoint(r-1, x_c, y_c)

                q_innerprod2 = abs(q1 * q_interp(1) &
                    + q2 * q_interp(2) + q3 * q_interp(3))

                ! Assign max value to q_innerprod
                q_innerprod = max(q_innerprod1, q_innerprod2)
            endif

            if (q_innerprod > max_innerprod .and. abs(q1) > tolsp) then
                max_innerprod = q_innerprod
            endif

          endif
        enddo aloop

    end function calculate_max_innerproduct

end module adjoint_module
