# Add Cost Constaint# Set working directory to downloaded csv from draft kings
import os
os.chdir("C:\\Users\\kyles\\Downloads") # windows

import numpy as np
import pandas as pd
players = pd.read_csv("DKSalaries.csv")


players.dtypes
players["RB"] = (players["Position"] == 'RB').astype(float)
players["WR"] = (players["Position"] == 'WR').astype(float)
players["QB"] = (players["Position"] == 'QB').astype(float)
players["TE"] = (players["Position"] == 'TE').astype(float)
players["DST"] = (players["Position"] == 'DST').astype(float)
players["Salary"] = players["Salary"].astype(float)

from pulp import *
# Initialize Model 
model = pulp.LpProblem("Draft Kings", pulp.LpMaximize)


# Define Objective Function
total_points = {}
# Subject to cost constraint
cost = {}
# Subject to limited number of slots for each position
QBs = {}
RBs = {}
WRs = {}
TEs = {}
DST = {}
number_of_players = {}


for i, player in players.iterrows():
    var_name = 'x' + str(i) # Create variable name
    decision_var = pulp.LpVariable(var_name, cat='Binary') # Initialize Variables

    total_points[decision_var] = player["AvgPointsPerGame"] # Create PPG Dictionary
    cost[decision_var] = player["Salary"] # Create Cost Dictionary
    
    # Create Dictionary for Player Types
    QBs[decision_var] = player["QB"]
    RBs[decision_var] = player["RB"]
    WRs[decision_var] = player["WR"]
    TEs[decision_var] = player["TE"]
    DST[decision_var] = player["DST"]
    number_of_players[decision_var] = 1.0
    
# Define ojective function and add it to the model
objective_function = pulp.LpAffineExpression(total_points)
model += objective_function

#Define cost constraint and add it to the model
total_cost = pulp.LpAffineExpression(cost)
model += (total_cost <= 50000)


# Add player type constraints
QB_constraint = pulp.LpAffineExpression(QBs)
RB_constraint = pulp.LpAffineExpression(RBs)
WR_constraint = pulp.LpAffineExpression(WRs)
TE_constraint = pulp.LpAffineExpression(TEs)
DST_constraint = pulp.LpAffineExpression(DST)
total_players = pulp.LpAffineExpression(number_of_players)

model += (QB_constraint <= 1)
model += (RB_constraint <= 3)
model += (WR_constraint <= 4)
model += (TE_constraint <= 2)
model += (DST_constraint <= 1)
model += (total_players <= 9)

# Write the LP to a file and solve
model.writeLP("modelfile.lp")
model.status
model.solve()

# Now that the LP is solved we can look at the variables
# There are 569 variable, 1 for each player, 
# We will loop through the vars to put them
# back into the data frame
players["is_drafted"] = 0.0
for var in model.variables():
    # Set is drafted to the value determined by the LP
    players.iloc[int(var.name[1:]),9] = var.varValue

my_team = players[players["is_drafted"] == 1.0]
my_team["Salary"].sum()



