import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

@dataclass
class State:
    time: float
    yaw_angle: float      # radians
    yaw_rate: float       # radians/s
    steering_angle: float # radians

    deltaT = 0.1  # Time step
    L = 2.5       # Wheelbase (m)
    v = 10.0      # Constant forward velocity (m/s)

def step(state: State) -> State:
    # Simple bicycle yaw rate model: yaw_rate = v / L * tan(steering_angle)
    yaw_rate = state.v / state.L * np.tan(state.steering_angle)
    
    # Update yaw angle
    new_yaw_angle = state.yaw_angle + yaw_rate * state.deltaT
    new_time = state.time + state.deltaT

    # Simulate steering input pattern
    if new_time < 3:
        steering_angle = np.radians(10)  # turn left
    elif new_time < 6:
        steering_angle = np.radians(-10) # turn right
    else:
        steering_angle = 0               # straight

    return State(time=new_time, yaw_angle=new_yaw_angle, yaw_rate=yaw_rate, steering_angle=steering_angle)

# Initialize
s0 = State(time=0, yaw_angle=0, yaw_rate=0, steering_angle=0)

# Data storage
time_data = []
yaw_data = []
yaw_rate_data = []

def animate(i):
    global s0
    s0 = step(s0)
    time_data.append(s0.time)
    yaw_data.append(np.degrees(s0.yaw_angle))   # convert to degrees
    yaw_rate_data.append(np.degrees(s0.yaw_rate))

    ax1.clear()
    ax2.clear()

    ax1.plot(time_data, yaw_data, color='blue')
    ax1.set_ylabel("Yaw Angle (°)")
    ax1.set_title("Yaw Model (Turning Simulation)")

    ax2.plot(time_data, yaw_rate_data, color='red')
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Yaw Rate (°/s)")

    ax1.grid(True)
    ax2.grid(True)

    return ax1, ax2

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 6))
ani = animation.FuncAnimation(fig, animate, interval=100)

plt.tight_layout()
plt.show()
