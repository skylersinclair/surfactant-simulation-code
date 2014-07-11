subroutine qinit(maxmx, maxmy, meqn, mbc, mx, my, x_low, y_low, dx, dy, q)

! Sets initial conditions for:
!     film height = q(:,:,1);
!     surfactant concentration = q(:,:,2).

! INPUT VARIABLES:
! maxmx, maxmy, meqn,mbc are only used in intent(out), which does(?)
! mbc could be the number of ghost cells (specified in setrun.py)
! mx,my = the number of grid cells along the x,y axis respectively
! x_low,y_low = the lowest numbered grid cell along the x,y axis  
! dx,dy = the size of grid cells along the x,y axis

    implicit none

    integer, intent(in) :: maxmx, maxmy, meqn, mbc, mx, my
    double precision, intent(in) :: x_low, y_low, dx, dy
    double precision, intent(out) :: q(1-mbc:maxmx+mbc, 1-mbc:maxmy+mbc, meqn)

    integer :: i, j, imode, k(4)
    double precision :: x, y,r, pi=dacos(-1.d0), INSIDE, OUTSIDE
    double precision :: heaviside_1mr

    !INSIDE and OUTSIDE define surfactant concentrations in/outside ring
    INSIDE = 1.2d0
    OUTSIDE = 1.6d0

! Testing timestep convergencs using constant height, conc
!do j = 1,my
!    do i = 1,mx 
!        q(i,j,1) = 1.0
!        q(i,j,2) = 0.5
!    end do
!end do

    !Surfactant different in/outside ring, but const height profile
    do j = 1,my
       y = y_low + (j-0.5d0)*dy
        do i = 1,mx
            x = x_low + (i-0.5d0)*dx
            r = sqrt(x**2 + y**2)

           !Set surfactant concentration
           if (abs(r) > 1.0) then
               q(i,j,2) = OUTSIDE
           else
               q(i,j,2) = INSIDE
           end if

           !Set constant height
           q(i,j,1) = 1.d0

        end do
    end do

end subroutine qinit
