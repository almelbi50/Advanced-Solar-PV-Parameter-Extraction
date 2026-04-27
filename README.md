# Advanced Solar PV Parameter Extraction & Thermal Predictor

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![SciPy](https://img.shields.io/badge/SciPy-Ecosystem-lightgrey.svg)](https://scipy.org/)

A research-grade Python tool designed to accurately extract the five parameters of solar cells and photovoltaic modules using the Single-Diode Model (SDM). It goes beyond standard extraction by incorporating advanced physical and mathematical models to predict the I-V curve behavior under varying temperatures.

## 🚀 Key Features

- **Exact Analytical Solution:** Utilizes the **Lambert W-function** to solve the implicit diode equation, eliminating algebraic approximation errors.
- **Global Optimization:** Employs the **Differential Evolution** algorithm coupled with logarithmic scaling for the saturation current ($I_0$) to avoid local minima traps.
- **Unbiased Objective Function:** Uses **Root Mean Square Relative Error (RMSRE)** instead of standard MSE. This ensures the algorithm gives equal weight to the open-circuit voltage ($V_{oc}$) region and the short-circuit current ($I_{sc}$) region, resulting in true physical parameters.
- **Advanced Thermal Prediction:** - Integrates **Varshni's Equation** to dynamically calculate the silicon bandgap energy ($E_g$) at different temperatures.
  - Applies dynamic temperature coefficients to both series ($R_s$) and shunt ($R_{sh}$) resistances for highly accurate high-temperature predictions.
- **Smart Data Loader:** Automatically cleans messy CSV datasets (fixes malformed signs, drops empty rows, and auto-detects delimiters). Supports both Single Cells and full PV Modules (Ns > 1).

## 🛠️ Installation & Usage

You can run this tool either on the cloud (Google Colab) or locally on your machine.

### Option 1: Google Colab (Recommended)
Google Colab provides a ready-to-use environment.
1. Upload the `solar_analyzer.py` script to a new Google Colab notebook.
2. Ensure you have the required libraries by running this command in a code cell at the top:
   ```python
  
   !pip install numpy pandas scipy matplotlib
3.Run the script. A prompt will appear asking you to input the temperature, number of cells, and upload your .csv dataset.
Option 2: Local Python Environment
If you prefer running the script on your own computer (Windows / Mac / Linux):
1.Clone the repository:
git clone [https://github.com/almelbi50/solar-pv-extractor.git](https://github.com/almelbi50/solar-pv-extractor.git)
cd solar-pv-extractor
2.Install the required dependencies: Open your terminal or command prompt and run:
pip install numpy pandas scipy matplotlib
3.Run the script:
python solar_analyzer.py
Follow the on-screen prompts to enter the parameters and provide the path to your CSV file.
Data Format RequirementsYour .csv file should contain two columns (without headers, or with headers that can be safely ignored):Column 1: Voltage (V)Column 2: Current (A)Note: The script's Smart Data Loader will automatically detect the delimiter (comma or semicolon) and clean any malformed negative signs.
🔬 Scientific Methodology
1. The Lambert W-Function ModelThe tool transforms the implicit I-V equation:
 I = Iph - I0 * [exp((V + I*Rs) / (Ns*n*k*T/q)) - 1] - (V + I*Rs)/Rsh
into an explicit form using scipy.special.lambertw to compute the exact theoretical current without iterative approximations inside the objective function.
2. Relative Error ObjectiveStandard Mean Squared Error (MSE) biases the curve fitting towards high-current regions. By minimizing the RMSRE (with a protective epsilon), the algorithm correctly captures the "knee" of the curve and the $V_{oc}$ region, yielding highly accurate Ideality Factors ($n$) and Shunt Resistances ($R_{sh}$).
3. Thermal DynamicsWhen
 projecting the curve for temperatures (e.g., 45°C, 60°C), the tool adjusts:
Bandgap ($E_g$): Decreases via Varshni's empirical relation.Saturation Current ($I_0$):
 Increases exponentially driven by the new $E_g$ and thermal voltage.
Resistances: $R_s$ increases linearly (lattice scattering), while $R_{sh}$ decreases exponentially (thermal generation).

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
