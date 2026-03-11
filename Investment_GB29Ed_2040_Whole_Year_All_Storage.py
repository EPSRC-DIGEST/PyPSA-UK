import pypsa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cplex

#Create Network object
network = pypsa.Network()

# Read the Network data
data_folder = "Investment_GB29Ed_2040_Whole_Year_All_Storage"
network.import_from_csv_folder(data_folder)

# # Plot the network
# network.plot()
# plt.show()

#Show the network details
print(network.buses)
print(network.lines)
print(network.loads)
print(network.generators)

print(network.generators.type)

# Renewable_DF = network.generators[type == 'Wind Offshore']


print(network.lines.s_nom)
#Run Linear Optimal Power Flow 
#https://pypsa.readthedocs.io/en/v0.28.0/api_reference.html#pypsa.Network.lopf

# # Solver options for HiGHS
# solver_options = {
#     "presolve": "on",
#     "solver": "simplex",
#     "mip_max_nodes": 100000,
#     "time_limit": 600,
#     "parallel": "on",
#     "mip_gap": 0.01
# }
# network.optimize(solver_name="highs" , solver_options=solver_options)
#Grubi Solver
# network.optimize(solver_name="gurobi" ,solver_options = {"MIPGap": 0.01})

#CPLEX Solver
solver_options={       
        "threads": 8,  # the number of parallel threads for the optimization
        "lpmethod": 4, # 4 for Barrier optimizer https://www.ibm.com/docs/en/cofz/12.9.0?topic=problem-overview-lp-optimizers
        "parallel": -1, # -1 for Opportunistic https://www.ibm.com/docs/en/icos/22.1.1?topic=parameters-parallel-mode-switch
        "solutiontype": 2, #2 for NONBASIC_SOLN https://www.ibm.com/docs/en/icos/22.1.1?topic=parameters-solution-type-lp-qp
        "timelimit": 600,    # time limit in seconds for running the optimization    
    }
network.optimize(solver_name="cplex", solver_options=solver_options)


#Calculate the curtailment
print(network.statistics().round(1))
curtailment = network.statistics.curtailment()
print("Curtailment")
print(network.statistics.curtailment())
# print(network.statistics.supply(comps=["Generator"]))
print("Installed Capacity")
print(network.statistics.installed_capacity())
print("Optimal Capacity")
print(network.statistics.optimal_capacity())

#Run Power Flow
# network.pf()

#Network flows #network.lines_t.{p0, q0, p1, q1}
print('Lines Flow for Active and Reactive Power____________: \n\n')
print(network.lines_t.p0) # Active power flow on each line
print(network.lines_t.q0) # Reactive power flow on each line

# Calculate the P.U. Power exchange of lines
Line_Capacity_pu = network.lines_t.p0/network.lines.s_nom
print (Line_Capacity_pu)
Line_Capacity_pu_DF = pd.DataFrame(Line_Capacity_pu)
Line_Capacity_pu_DF.to_csv(f"{data_folder}/Line_Capacity_pu_DF.csv")

# Count occurrences of 1 and -1 to find congested lines
count_1 = ((Line_Capacity_pu_DF >= 0.9)&(Line_Capacity_pu_DF <= 1)).sum().sum()
count_neg1 = (Line_Capacity_pu_DF >= -1 & (Line_Capacity_pu_DF <= -0.9)).sum().sum()

Congested_Hours = count_1 + count_neg1
print("____Congested Hours____")
print(Congested_Hours)

#Bus voltage and angle #network.buses_t.{v_mag_pu, v_ang, p, q}
# print('Bus Voltage and Angle____________: \n\n')
# print(network.buses_t.v_mag_pu)
# print(network.buses_t.v_ang)

# Generators output #network.generators.{p, q}
print('Generator Active and Reactive Power____________: \n\n')
print(network.generators_t.p)
print(network.generators_t.q)

# Check storage state of charge (SoC) over time and storage dispatch(charging/discharging)
print(network.storage_units_t.state_of_charge)
print(network.storage_units_t.p)

#Links usage
print(network.links_t.p0)
print(network.links_t.p1)

# Save the Generator Dispatch
Generators_DF = pd.DataFrame(network.generators_t.p)
Generators_DF.to_csv(f"{data_folder}/Generators_DF.csv")
Total_Gen=Generators_DF.sum(axis=1)


# Save the Storage Dispatch
Storage_DF = pd.DataFrame(network.storage_units_t.p)
Storage_DF.to_csv(f"{data_folder}/Storage_DF.csv")
Total_Storage=Storage_DF.sum(axis=1)

Storage_Charge_DF = pd.DataFrame(network.storage_units_t.state_of_charge)
Storage_Charge_DF.to_csv(f"{data_folder}/Storage_Charge_DF.csv")
Total_Storage_Charge=Storage_Charge_DF.sum(axis=1)

#Calculate and save statistics data
Curtailment_DF = pd.DataFrame(network.statistics().round(1))
Curtailment_DF.to_csv(f"{data_folder}/Curtailment_DF.csv")

#Save the Demand data
Demand_DF = pd.DataFrame(network.loads_t.p_set)
Demand_DF.to_csv(f"{data_folder}/Demand_DF.csv")
Total_Demand = Demand_DF.sum(axis=1)

#Demand Generation Storage DataFrame
Network_DF = pd.concat([Total_Gen, Total_Storage, Total_Demand] , axis=1 )
Network_DF.columns = ['Generation','Storage','Demand']
Network_DF.to_csv(f"{data_folder}/Network_DF.csv")


# Calculate total generation cost
Total_Cost = (network.generators_t.p * network.generators.marginal_cost).sum().sum()
print(Total_Cost)
# np.savetxt("generator_t.csv", network.generators_t, delimiter=",")


# Calculate Total Renewable Capacity

# #Generators status
# print('Generator Status____________: \n\n')
# print(network.generators_t.status)


# print(network.generators_t.p)
# print(network.generators_t.p.values)
# m = network.optimize.create_model()
# gen_p = m.variables["Generator-p"]
# bus = network.generators.bus.to_xarray()
# total_generation = gen_p.groupby(bus).sum().sum()
total_generations = network.generators_t.p.values.sum()
total_demand = network.loads_t.p_set.sum().sum() #Loads don't change while I change the csv file

print(total_demand, total_generations)
#Run Linear (DC) Optimal Power Flow
# network.lopf(pyomo=False)

#Run Linear Optimal Power Flow 
#https://pypsa.readthedocs.io/en/v0.28.0/api_reference.html#pypsa.Network.lopf
# network.optimize(solver_name="highs" , solver_options={"solver": "ipm"})

# Generators optimal output #network.generators.{p, q}
# print(network.generators_t.p)

print(1)