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

## 🛠️ Usage / Installation

The script is standalone and highly optimized for **Google Colab** and local Jupyter/Python environments.

1. Clone the repository:
   ```bash
   git clone [https://github.com/almelbi50/solar-pv-extractor.git](https://github.com/almelbi50/solar-pv-extractor.git)
