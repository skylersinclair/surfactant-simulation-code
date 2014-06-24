subroutine qinit(maxmx, maxmy, meqn, mbc, mx, my, x_low, y_low, dx, dy, q)

! Sets initial conditions for:
!     film height = q(:,:,1);
!     surfactant concentration = q(:,:,2).

    implicit none

    integer, intent(in) :: maxmx, maxmy, meqn, mbc, mx, my
    double precision, intent(in) :: x_low, y_low, dx, dy
    double precision, intent(out) :: q(1-mbc:maxmx+mbc, 1-mbc:maxmy+mbc, meqn)

    integer :: i, j, imode, k(4)
    double precision :: x, y,r, a, b, big_b, c(4), pi=dacos(-1.d0)
    double precision :: heaviside_1mr

    a = 1.d-2
    b = 5.d-2
    big_b = 5.d0

    c(1) = 1.d0
    c(2) = 1.d0
    c(3) = 1.d0
    c(4) = 0.5d0

    k(1) = 2
    k(2) = 5
    k(3) = 7
    k(4) = 20

! Shreyas' old meniscus code

!    do j = 1,my
!       y = y_low + (j-0.5d0)*dy
!        do i = 1,mx
!            x = x_low + (i-0.5d0)*dx
!            r = sqrt(x**2 + y**2)
!           if (abs(r) >1.5) then
!              q(i,j,1) = 1.d0
!              q(i,j,2) = 0.8d0
!           end if
!           if (1.5 >r .and. r > 1.25) then
!              q(i,j,2) = 0.8d0 + 0.4d0*sin(12.37d0*x - 3.5d0)
!              q(i, j, 1) = 1 + 0.25d0*sin(12.37d0*x - 3.5d0)
!           end if
!           if (r < 0.75) then
!              q(i, j, 2) = 0.d0
!              q(i, j, 1) = 1.d0
!           end if
!           if (1 < r .and. r < 1.25) then
!                   q(i, j, 2) = 0.8 + 0.4d0*sin(7*x  - 4)
!                   q(i, j, 1) = 1  + 0.4*sin(7*x-4.d0)
!           end if
!           if (0.75 < r .and. r <= 1) then
!                   q(i, j, 2) = 0
!                   q(i, j, 1) = 1 + 0.4*sin(7*x - 4.d0)
!           end if

! Testing timestep convergencs using constant height, conc
do j = 1,my
    do i = 1,mx 
        q(i,j,1) = 1.0
        q(i,j,2) = 0.5
    end do
end do

           ! heaviside_1mr = 0.5d0*(3.d0 + 3.d0*tanh(20*(1-r)))
           ! q(i,j,1) = 1.d0
            !q(i,j,2) = heaviside_1mr  tanh IC
            !if (abs(r) >  1) then
            !   q(i,j,2) = 0.80d0*(1 - (1/r)**10)
            !else 
            !   q(i,j,2) = 0.d0
            !end if
!        end do
!    end do
  
end subroutine qinit
