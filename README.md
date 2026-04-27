<div align="center">
  
  <h1>🌞 Advanced Solar PV Parameter Extraction & Thermal Predictor</h1>
  <p><i>A Research-Grade Python Tool for Photovoltaic Cell/Module Analysis</i></p>

  [![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
  [![SciPy](https://img.shields.io/badge/SciPy-Ecosystem-lightgrey.svg)](https://scipy.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📑 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Installation & Usage](#-installation--usage)
- [Data Format](#-data-format-requirements)
- [Scientific Methodology](#-scientific-methodology)
- [License](#-license)

---

## 📖 Overview
This project is a highly accurate Python tool designed to extract the five fundamental parameters of solar cells and photovoltaic modules using the **Single-Diode Model (SDM)**. 

Going beyond standard extraction, this tool acts as a **Thermal Predictor**, incorporating advanced physical models (like Varshni's Equation) to predict the I-V curve behavior under varying and extreme temperatures.

*(Note: Add a screenshot of your Colab plot here later to make it look awesome!)*
---

## 🚀 Key Features

* **🎯 Exact Analytical Solution:** Utilizes the **Lambert W-function** to solve the implicit diode equation, completely eliminating algebraic approximation errors.
* **🌐 Global Optimization:** Employs the **Differential Evolution** algorithm coupled with logarithmic scaling for the saturation current ($I_0$) to avoid local minima traps.
* **⚖️ Unbiased Objective Function:** Uses **Root Mean Square Relative Error (RMSRE)** instead of standard MSE. This ensures the algorithm gives equal weight to the open-circuit voltage ($V_{oc}$) region and the short-circuit current ($I_{sc}$) region.
* **🌡️ Advanced Thermal Prediction:** * Integrates **Varshni's Equation** to dynamically calculate the silicon bandgap energy ($E_g$) at different temperatures.
  * Applies dynamic temperature coefficients to both series ($R_s$) and shunt ($R_{sh}$) resistances.
* **🧹 Smart Data Loader:** Automatically cleans messy CSV datasets (fixes malformed signs, drops empty rows, and auto-detects delimiters). Supports both Single Cells and full PV Modules ($N_s \ge 1$).

---

## 🛠️ Installation & Usage

You can run this tool either on the cloud (Google Colab) or locally on your machine.

### Option 1: Google Colab (Recommended)
Google Colab provides a ready-to-use, powerful environment.
1. Download `solar_analyzer.py` from this repository.
2. Upload it to a new [Google Colab](https://colab.research.google.com/) notebook.
3. Ensure you have the required libraries by running this command in the first cell:
   ```python
   !pip install numpy pandas scipy matplotlib
