import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------
# PARAMETERS (tuned for Murata VTC5A-like behavior)
# -------------------------------------------------------
Q_rated = 2.5 * 3600      # cell capacity [Coulombs] (2.5Ah)
R0 = 0.015                # Ohmic resistance [Ohms]
R1 = 0.02                 # RC branch resistance [Ohms]
C1 = 200.0                # RC branch capacitance [Farads]
dt = 1.0                  # time step [seconds]
N = 300                   # number of time steps

lambda_hyst = 0.98        # hysteresis memory decay
gamma_hyst = 0.03         # hysteresis voltage scaling [V]
T_ref = 25.0              # reference temp [°C]
alpha_R = 0.004           # resistance temp coefficient [/°C]
beta_V = 0.0008           # OCV temperature coefficient [V/°C]
m, c, hA = 0.045, 1000.0, 0.6   # mass [kg], specific heat [J/kgK], cooling term [W/K]

# -------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------
def f_OCV(SOC):
    """Open-circuit voltage vs SOC curve (simple polynomial fit)"""
    # Approximate Li-ion OCV curve shape (Murata-like)
    return 3.0 + 1.2*SOC - 0.3*(SOC**2) + 0.1*(SOC**3)

def R_int(T):
    """Internal resistance vs temperature"""
    return R0 * (1 + alpha_R * (T - T_ref))

# -------------------------------------------------------
# TIME SERIES INPUTS (synthetic)
# -------------------------------------------------------
time = np.arange(N) * dt

# Create simple current profile: discharge/charge pulses [A]
I = np.zeros(N)
I[20:80]  = 5.0    # discharge
I[100:150] = 2.5   # partial discharge
I[170:220] = -3.0  # small charge
I[250:280] = 6.0   # strong discharge

# -------------------------------------------------------
# INITIAL CONDITIONS
# -------------------------------------------------------
SOC = np.zeros(N)
V_RC = np.zeros(N)
H = np.zeros(N)
T = np.zeros(N)
V_model = np.zeros(N)

SOC[0] = 1.0   # start at 100% charge
T[0] = 25.0    # ambient start
V_RC[0] = 0.0
H[0] = 0.0

# -------------------------------------------------------
# SIMULATION LOOP
# -------------------------------------------------------
for t in range(1, N):
    # 1. SOC update (Coulomb counting)
    SOC[t] = SOC[t-1] - (I[t-1] * dt / Q_rated)
    SOC[t] = max(0, min(1, SOC[t]))  # bound between 0–1

    # 2. OCV lookup
    V_OCV = f_OCV(SOC[t])

    # 3. RC voltage update (polarization)
    exp_factor = np.exp(-dt / (R1 * C1))
    V_RC[t] = V_RC[t-1] * exp_factor + R1 * (1 - exp_factor) * I[t-1]

    # 4. Hysteresis update
    H[t] = lambda_hyst * H[t-1] + (1 - lambda_hyst) * I[t-1]

    # 5. Thermal update
    T[t] = T[t-1] + (dt / (m * c)) * (I[t-1]**2 * R_int(T[t-1]) - hA * (T[t-1] - T_ref))

    # 6. Temperature corrections
    R0_eff = R0 * (1 + alpha_R * (T[t] - T_ref))
    V_OCV_T = V_OCV + beta_V * (T[t] - T_ref)

    # 7. Total terminal voltage
    V_model[t] = V_OCV_T - I[t] * R0_eff - V_RC[t] + gamma_hyst * H[t]

# -------------------------------------------------------
# PLOTS
# -------------------------------------------------------
plt.figure(figsize=(10, 6))

plt.subplot(3,1,1)
plt.plot(time, I, label='Current [A]')
plt.ylabel('Current (A)')
plt.grid(True)
plt.legend()

plt.subplot(3,1,2)
plt.plot(time, V_model, label='Modeled Voltage [V]', color='tab:red')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.legend()

plt.subplot(3,1,3)
plt.plot(time, SOC*100, label='State of Charge [%]', color='tab:green')
plt.xlabel('Time (s)')
plt.ylabel('SOC (%)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
