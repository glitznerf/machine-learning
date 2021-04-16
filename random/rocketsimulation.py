# Note that this code is based on NAROM/Andoya Space educational material for
# the ESA Fly a Rocket! campaign


#### Imports ####
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt



#### Constants ####
g = 9.81            # gravitational acceleration [m/s^2]
rho_0 = 1.225       # air density at sea level [kg/m^3]
H = 8800            # scale height [m]
c_D = 0.54          # drag coefficient for the rocket [-]
A = 0.0103          # rocket body frontal area [m^2]
m_i = 19.100        # "wet" mass of the rocket [kg]
m_f = 10.604        # "dry" mass of the rocket [kg]
T_avg = 2501.8      # average rocket engine thrust [N]
t_burn = 6.09       # burn time [s]
H = 8800            # scale height [m]

# Saving some parameters to optimize run time
m = (m_i+m_f)/2     # average mass of the rocket
k = 0.5*c_D*A*rho_0 # constant factor in the drag function



#### Calculation functions ####
def Thrust(t):
    """ The thrust curve of the rocket engine.
    Parameter:
        t time [s]
    """
    if t < t_burn:
        return T_avg
    return 0

def Drag(h, v):
    """ Air drag
    Parameters:
        h altitude [m]
        v speed [m/s]
    """
    if v == 0: # This test avoids division by zero.
        return 0
    return -k*np.exp(-h/H)*v*abs(v)

def f(t, w):
    """ The right-hand side of the equations of motion, i.e. (3) and (4).
    Parameters:
        t time [s]
        w vector with the needed coordinates and velocities.
            In the one-dimensional case, w = (r, v)
    """
    temp_vector = np.zeros(2)
    # Eq. (3) (1D)
    temp_vector[0] = w[1]
    # Eq. (4). In the 1D-case, r_y = r = h
    temp_vector[1] = (Thrust(t) + Drag(w[0],w[1]))/m - g
    return temp_vector

def trajectory(dt, t_f):
    """ Calculates the rocket trajectory using the ODE-solver solve_ivp
    from the scipy package.
    Parameters:
        dt time step [s]
        t_f termination time [s]
    Returns:
        solution.t array of calculated time values
        solution.y[0] array of the rocket’s y-position (altitude)
        solution.y[1] array of the rocket’s y-velocity
    """
    t_span = [0, t_f] # interval of integration
    w_0 = [0, 0] # initial values [in 1D: w = (r, v)]
    t_val = np.arange(0, t_f, dt) # time values
    solution = solve_ivp(f, t_span, w_0, t_eval=t_val)
    # Remember to unpack all values when calling this function!
    return solution.t, solution.y[0], solution.y[1]



#### Simulation ####
# Arguments
dt = 0.01 # Time step
t_f = 500 # Calculation end time

# Runs the simulation
t, y, v_y = trajectory(dt, t_f)
max_height, max_height_time = max(y), 0
max_speed = max(v_y)

# Keep only positive altitude simulations
tp, yp, v_yp, density = [], [], [], []
i = 0
while y[i] >= 0:
    if y[i] == max_height:
        max_height_time = t[i]
    tp.append(t[i])
    yp.append(y[i])
    v_yp.append(v_y[i])
    density.append(rho_0**(-(y[i]/H)))
    i+=1

# Plot the resulting trajectory
plt.plot(tp, yp)
plt.title("Trajectory")
plt.xlabel("$t$ [s]")
plt.ylabel("altitude [m]")
plt.show()

# Calculate (max) dynamic pressure
q = []
for i in range(0, len(density)):
    d = density[i]
    v = v_yp[i]
    q.append(1/2*d*v**2)
max_q = max(q)

# Print metrics
print(f'Apogee reached at t = {max_height_time:.2f}s with y = {max_height:.2f}m.')
print(f'Splashdown at t = {tp[-1]:.2f}s with speed v = {v_yp[-1]:.2f}m/s.')
print(f'Maximum speed during flight is v = {max_speed:.2f}m/s.')
print(f'Maximum dynamic pressure maxq = {max_q:.2f}N/m^2.')
