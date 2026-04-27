# ==========================================
# Advanced Solar PV Parameter Extraction & Thermal Prediction
# ==========================================
# This script extracts the 5 parameters of a solar cell/module using 
# the single-diode model, Lambert W-function, and Differential Evolution.
# It also projects performance at different temperatures using Varshni's Eq.
# ==========================================

import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution
from scipy.special import lambertw  
import matplotlib.pyplot as plt
import io

# Optional: For Google Colab file upload
try:
    from google.colab import files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# ==========================================
# 1. Physical Constants & Functions
# ==========================================
q = 1.602176634e-19  # Electron charge (C)
k = 1.380649e-23     # Boltzmann constant (J/K)

def calc_Eg(T_Kelvin):
    """Calculate Silicon Bandgap energy using Varshni's equation."""
    Eg0 = 1.166        # Bandgap at 0 K (eV)
    alpha = 4.73e-4    # eV/K
    beta = 636.0       # K
    return Eg0 - (alpha * T_Kelvin**2) / (T_Kelvin + beta)

# ==========================================
# 2. User Input & Smart Data Loader
# ==========================================
print("--- Solar PV Analyzer Setup ---")
try:
    T_C = float(input("Enter measured temperature in °C (e.g., 25, 33, 45): "))
except ValueError:
    T_C = 25.0
    print("Invalid input. Defaulting to 25 °C.")

T_ref = T_C + 273.15  # Reference Temperature in Kelvin

try:
    Ns = int(input("Enter Number of cells in series (Ns) (e.g., 1 for cell, 36 for module): "))
except ValueError:
    Ns = 1
    print("Invalid input. Defaulting to Ns = 1.")

# Data Loading
V_exp, I_exp = None, None

if IN_COLAB:
    print("\nPlease upload your CSV data file (V in col 1, I in col 2):")
    uploaded = files.upload()
    if uploaded:
        file_name = list(uploaded.keys())[0]
        try:
            df = pd.read_csv(io.BytesIO(uploaded[file_name]), sep=None, engine='python')
        except:
            df = pd.read_csv(io.BytesIO(uploaded[file_name]))
        
        # Clean data: convert to string, fix malformed minus signs (?), convert to float, drop NaNs
        df = df.astype(str).apply(lambda x: x.str.replace('?', '-')).astype(float).dropna()
        V_exp = df.iloc[:, 0].values
        I_exp = df.iloc[:, 1].values
        print(f"\n✅ Successfully loaded '{file_name}'.")
else:
    # For local Python execution
    file_path = input("Enter the path to your CSV file: ")
    try:
        df = pd.read_csv(file_path, sep=None, engine='python')
        df = df.astype(str).apply(lambda x: x.str.replace('?', '-')).astype(float).dropna()
        V_exp = df.iloc[:, 0].values
        I_exp = df.iloc[:, 1].values
        print(f"\n✅ Successfully loaded file.")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        exit()

if V_exp is None or I_exp is None:
    print("No data available. Exiting...")
    exit()

# ==========================================
# 3. Solar Cell Model (Lambert W)
# ==========================================
def solar_residual(params, V, I_exp, T, Ns):
    Rs, Rsh, n, I0, Iph = params
    Vt = (Ns * k * T) / q
    Rs = max(Rs, 1e-6) 
    
    term1 = (Rsh * (Iph + I0) - V) / (Rs + Rsh)
    arg = (I0 * Rs * Rsh) / (n * Vt * (Rs + Rsh))
    exponent = (Rsh * (V + Rs * (Iph + I0))) / (n * Vt * (Rs + Rsh))
    
    exponent = np.clip(exponent, None, 700) # Prevent math overflow
    X = arg * np.exp(exponent)
    W = np.real(lambertw(X))
    I_calc = term1 - (n * Vt / Rs) * W
    
    return I_calc - I_exp 

# ==========================================
# 4. Global Optimization (RMSRE Objective)
# ==========================================
print("\nRunning Global Optimization (Differential Evolution)...")

def objective_function(params, V, I_exp, T, Ns):
    Rs, Rsh, n, log_I0, Iph = params
    I0 = 10 ** log_I0 
    
    res = solar_residual([Rs, Rsh, n, I0, Iph], V, I_exp, T, Ns)
    
    # Root Mean Square Relative Error (RMSRE)
    # Epsilon prevents division by zero near Voc
    epsilon = 0.05 * np.max(np.abs(I_exp)) 
    relative_res = res / (np.abs(I_exp) + epsilon)
    
    return np.mean(relative_res**2)  

bounds = [
    (0.0001, 5.0),               # Rs
    (5.0, 5000.0),               # Rsh
    (0.5, 4.0),                  # n (per cell)
    (-15.0, -3.0),               # log_I0
    (0.0, np.max(I_exp) * 1.5)   # Iph
]

result = differential_evolution(
    objective_function, bounds, args=(V_exp, I_exp, T_ref, Ns),
    strategy='best1bin', popsize=40, tol=1e-8, mutation=(0.5, 1.5), recombination=0.7, seed=42
)

Rs_opt, Rsh_opt, n_opt, log_I0_opt, Iph_opt = result.x
I0_opt = 10 ** log_I0_opt 

# Calculate standard RMSE for reference
final_res = solar_residual([Rs_opt, Rsh_opt, n_opt, I0_opt, Iph_opt], V_exp, I_exp, T_ref, Ns)
final_rmse = np.sqrt(np.mean(final_res**2))

# ==========================================
# 5. Output Results
# ==========================================
print("\n" + "="*50)
print("📊 Extracted Parameters (Global Optimum):")
print("="*50)
print(f"Rs  (Series Resistance):      {Rs_opt:.5f} Ω")
print(f"Rsh (Shunt Resistance):       {Rsh_opt:.2f} Ω")
print(f"n   (Ideality Factor / cell): {n_opt:.4f}")
print(f"I0  (Saturation Current):     {I0_opt:.4e} A")
print(f"Iph (Photo-current):          {Iph_opt:.4f} A")
print(f"Standard RMSE:                {final_rmse:.5e}")
print("="*50)

# ==========================================
# 6. Advanced Physical Temperature Prediction
# ==========================================
print("\n🌡️ Generating Advanced Predictive Models (25, 33, 45, 60 °C)...")

T_list_C = [25, 33, 45, 60]
alpha_Iph = 0.0005  # Temp coeff for Photocurrent (~0.05%/°C)
alpha_Rs  = 0.003   # Temp coeff for Series Res (~0.3%/°C increase)
beta_Rsh  = 0.02    # Temp coeff for Shunt Res (Exponential decay)

Eg_ref = calc_Eg(T_ref)
V_sim = np.linspace(0, np.max(V_exp) * 1.25, 200)

plt.figure(figsize=(12, 7))

for T_val in T_list_C:
    T_new = T_val + 273.15
    Eg_new = calc_Eg(T_new) 
    delta_T = T_new - T_ref
    
    # 1. Update Iph
    Iph_new = Iph_opt * (1 + alpha_Iph * delta_T)
    
    # 2. Update I0 using Varshni's equation
    factor1 = (T_new / T_ref)**3
    factor2 = (q / k) * ((Eg_ref / T_ref) - (Eg_new / T_new))
    I0_new = I0_opt * factor1 * np.exp(factor2)
    
    # 3. Update Resistances dynamically
    Rs_new = Rs_opt * (1 + alpha_Rs * delta_T)
    Rsh_new = Rsh_opt * np.exp(-beta_Rsh * delta_T)
    
    # 4. Thermal Voltage
    Vt_new = (Ns * k * T_new) / q
    
    # Recalculate curve with Lambert W
    term1_new = (Rsh_new * (Iph_new + I0_new) - V_sim) / (Rs_new + Rsh_new)
    arg_new = (I0_new * Rs_new * Rsh_new) / (n_opt * Vt_new * (Rs_new + Rsh_new))
    exponent_new = (Rsh_new * (V_sim + Rs_new * (Iph_new + I0_new))) / (n_opt * Vt_new * (Rs_new + Rsh_new))
    exponent_new = np.clip(exponent_new, None, 700)
    
    X_new = arg_new * np.exp(exponent_new)
    W_new = np.real(lambertw(X_new))
    I_calc = term1_new - (n_opt * Vt_new / Rs_new) * W_new
    
    plt.plot(V_sim, I_calc, label=f'Pred: {T_val}°C (Eg={Eg_new:.3f}eV)', linewidth=2.5)

plt.scatter(V_exp, I_exp, color='black', label=f'Exp Data ({T_C} °C)', alpha=0.7, zorder=10)

plt.title(f'Advanced Physical Temp Prediction | Ns = {Ns}', fontsize=14, fontweight='bold')
plt.xlabel('Voltage (V)', fontsize=13)
plt.ylabel('Current (A)', fontsize=13)
plt.xlim(0, np.max(V_sim))
plt.ylim(0, np.max(I_exp) * 1.15)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
