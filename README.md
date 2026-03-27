# PyPSA-UK
A PyPSA-based framework for modelling energy storage integration, renewable energy resources and power system optimisation.

 ## 📖Overview

This repository contains Python code for power system modelling and optimisation using [PyPSA] (Python for Power System Analysis). 
The project focuses on:

- GB grid simulation and optimisation
- Optimal energy storage allocation
- Battery degradation modelling economically and physically
- Energy storage investment expansion planning
- Renewable integration studies
- Scenario-based optimal power flow analysis


## GB 29 Bus with Interconnectors 2040
![GB 29 Bus with Interconnectors 2040](https://github.com/EPSRC-DIGEST/PyPSA-UK/blob/main/img/GB%2029%20Bus%20with%20Interconnectors%202040.png)


## Renewable Generation for 2040 with Optimal Energy Storage Allocation
![Renewable Generation for 2040 with Optimal Energy Storage Allocation](https://github.com/EPSRC-DIGEST/PyPSA-UK/blob/main/img/Renewable%20Generation%20for%202040%20with%20Optimal%20Energy%20Storage%20Allocation.png)


## Installation
To use this code you need to install [PyPSA] as follows: 
```sh
pip install pypsa
```


and then the following requirments:
- CPLEX - Adcademic version a high-performance, commercial software package for mathematical optimization
- numpy – numerical computing and array operations
- scipy – scientific computing and sparse matrix calculations
- pandas – data structures for time series and component data
- xarray – labeled multidimensional data handling
- linopy – optimization modeling interface used by PyPSA
- networkx – network graph calculations
- matplotlib – plotting and visualization
- seaborn – statistical plotting utilities
- plotly – interactive plotting
- netcdf4 – reading and writing NetCDF data files
- validators – validation utilities
- deprecation – API deprecation warnings
- highspy – HiGHS optimization solver interface

Create a virtual environment and activate it (optional but recommended)

```sh
python -m venv pypsa-env
```
then run following code: 

```sh
Investment_GB29Ed_2040_Whole_Year_All_Storage.py
```

## Licence
PyPSA-UK is released under the MIT License.

## Cite Us
If you use PyPSA for your research, we would appreciate it if you would cite the following paper:
- Sobhan Naderian, Marko Aunedi, “Optimal Energy Storage Deployment in GB Transmission Grid Using Open-Source Software” MDPI Energies, 2026, under review

[PyPSA]: <https://docs.pypsa.org/latest/>

