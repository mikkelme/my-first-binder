import numpy as np

def simulator(MB_start, OB_start, MB_end, OB_end, T = 10, dt = 0.1):
    K = int(T/dt + 1)         #Steps
    MB_pos = np.zeros((K,2))  #MB = Main Boat
    OB_pos = np.zeros((K,2))  #OB = Other Boat
    t = np.zeros(K)           #Time

    #Initial position
    MB_pos[0] = MB_start
    OB_pos[0] = OB_start

    #Calculate constant velocity
    MB_vel = (MB_end - MB_pos[0])/T
    OB_vel = (OB_end - OB_pos[0])/T

    #Main update loop
    for k in range(K - 1):
        MB_pos[k+1] = MB_pos[k] + MB_vel*dt
        OB_pos[k+1] = OB_pos[k] + OB_vel*dt
        t[k+1] = t[k] + dt
    return MB_pos, OB_pos
