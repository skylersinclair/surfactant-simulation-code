subroutine compute_surface_tension(nx, ny, surfactant, surface_tension)
    
    ! This file contains the equation of state. 
    ! compute_surface_tension contains the eos
    ! compute_surface_tension_d1 contains the first derivative of the eos
    ! make sure the two match!
    ! uncomment the one you want and comment out the rest.

    implicit none
    double precision :: beta, kappa, delta, mu, right_film_height
    common /surfactant_config/ beta, kappa, delta, mu, right_film_height

    integer, intent(in) :: nx, ny
    double precision, dimension(nx, ny), intent(in) :: surfactant
    double precision, dimension(nx, ny), intent(out) :: surface_tension

    integer :: ix, iy
    character :: EOS

    ! variable that keeps track of what EoS is being used
    EOS = 'a'
    
    do iy = 1, ny
        do ix = 1, nx
        
            !MULTILAYER EQU
            if (EOS == 'm')
              surface_tension(ix, iy) = (1.d0 + mu * surfactant(ix, iy))**(-3)
            end if
            
            !LINEAR EQU
            if (EOS == 's')
              surface_tension(ix, iy) = 1.d0 - surfactant(ix, iy)
            end if
            
            !SHREYAS NEW EOS 1
            !surface_tension(ix, iy) = 0.5d0*(1.2d0 - tanh(9*(surfactant(ix, iy) - 0.5d0)))
            !SHREYAS NEW EOS 2
            ! surface_tension(ix, iy) = (51.633d0 - 13.85d0*tanh(22.593d0*0.2d0*surfactant(ix,iy) - 3.2046d0))/27
            
            !DINA NEW EOS 1 (Piecewise Linear/Tanh)
            if (EOS == 'm')
              if (surfactant(ix,iy) < .4183d0) then
                 surface_tension(ix,iy) = 1.d0
              else if (surfactant(ix,iy) < 1.d0) then
                 surface_tension(ix,iy) =  (1.d0/63.d0)*(50.52d0 + 15.59d0 * tanh(2.739d0 - 3.918d0 * surfactant(ix,iy)))
              else
                 surface_tension(ix,iy) = (1.d0/63.d0)*(37.87d0 - 0.239d0 * surfactant(ix,iy))
              end if
            end if
            
            !DINA NEW EOS 2 (Piecewise Linear)
            if (EOS == 'l')
              if (surfactant(ix,iy) < .4183d0) then
                 surface_tension(ix,iy) = (1.d0/63.d0)*(63.0d0 - 0.2399d0 * surfactant(ix,iy))
              else if (surfactant(ix,iy) < 1.d0) then
                 surface_tension(ix,iy) =  (1.d0/63.d0)*(81.07d0 - 43.44d0 * surfactant(ix,iy))
              else
                 surface_tension(ix,iy) = (1.d0/63.d0)*(37.87d0 - 0.2399d0 * surfactant(ix,iy))
              end if
            end if
            
            !DINA NEW EOS 3 (Tanh)
            if (EOS == 't')
              surface_tension(ix,iy) = (1.d0/63.d0)*(51.13d0 + 13.85d0 * tanh(3.20d0 - 4.67d0 * surfactant(ix,iy)))
            end if
            
        end do
    end do
end subroutine compute_surface_tension


subroutine compute_surface_tension_d1(nx, ny, surfactant, surface_tension_d1)
    implicit none
    double precision :: beta, kappa, delta, mu, right_film_height
    common /surfactant_config/ beta, kappa, delta, mu, right_film_height

    integer, intent(in) :: nx, ny
    double precision, dimension(nx, ny), intent(in) :: surfactant
    double precision, dimension(nx, ny), intent(out) :: surface_tension_d1

    integer :: ix, iy

    do iy = 1, ny
        do ix = 1, nx
            !MULTILAYER EQU
            !surface_tension_d1(ix, iy) = -3.d0 * mu * (1.d0 + mu * surfactant(ix, iy))**(-4)
            
            !LINEAR EQU
            !surface_tension_d1(ix, iy) = -1.d0
            
            !SHREYAS NEW EOS 1
            !surface_tension_d1(ix, iy) = -9.d0*(1/(cosh(9*(surfactant(ix, iy) - 0.5d0))))**2
            !SHREYAS NEW EOS 2
            !surface_tension_d1(ix, iy) = -2.31787d0*(1/(cosh(3.2046d0 - 4.5186d0*surfactant(ix, iy))))**2
            
            !DINA NEW EOS 1 (Piecewise Linear/Tanh)
            if (surfactant(ix,iy) < .4183d0) then
               surface_tension_d1(ix,iy) = 0.d0
            else if (surfactant(ix,iy) < 1.d0) then
               surface_tension_d1(ix,iy) = -.9693d0 * (1/(cosh(2.739d0 - 3.918d0 * surfactant(ix,iy))))**2
            else
               surface_tension_d1(ix,iy) = -.003798d0
            end if
            
            !DINA NEW EOS 2 (Piecewise Linear)
            
            !DINA NEW EOS 3 (Tanh)
            
        end do
    end do
end subroutine compute_surface_tension_d1
