import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

@dataclass
class State:
    xpos : float
    ypos : float
    xvel : float
    yvel : float

    deltaT = 1
    bounceCoefficient = 1.01

def step (state:State) -> State:
    new_xpos = state.xpos + state.xvel * state.deltaT
    new_ypos = state.ypos + state.yvel * state.deltaT
    new_yvel = state.yvel - 9.81 * state.deltaT

    if new_ypos < 0:
        new_yvel = new_yvel * -1 * state.bounceCoefficient
    sNew = State(
        xpos = new_xpos,
        ypos = new_ypos,
        xvel = state.xvel,
        yvel = new_yvel
    )
    return sNew

def animate (i):
    global s0
    s0 = step(s0)
    ax.clear()
    ax.scatter([s0.xpos], [s0.ypos], s = 50)
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 1000)
    return ax,

s0 = State(
    xpos = 0,
    ypos = 5,
    xvel = 0,
    yvel = 0
)

fig = plt.figure(figsize=(3,3), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
plt.pause(5)
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()