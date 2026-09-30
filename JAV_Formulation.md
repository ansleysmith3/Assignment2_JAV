JAV Manufacturing - Production Planning

Sets
M = {1,...,6} months (1 = January, 6 = June)

Parameters
d_j = demand in month j (1000, 2000, 5000, 7000, 4000, 3000)
ci = cost to increase output by one unit = 10
cd = cost to decrease output by one unit = 5
h = monthly holding cost per unit = 4
Imax = warehouse capacity = 2000
P0 = December production = 1000
I0 = inventory at start of January = 1500
Iend = required inventory at end of June = 500

Decision variables
P_j = units produced in month j
INC_j = increase in production from month j-1 to month j
DEC_j = decrease in production from month j-1 to month j
I_j = inventory at end of month j

Objective
min Z = sum over j of (10*INC_j + 5*DEC_j + 4*I_j)

Constraints
P_j = P_(j-1) + INC_j - DEC_j    for all j (P_0 = 1000)
I_j = I_(j-1) + P_j - d_j        for all j (I_0 = 1500)
I_j <= 2000                      for all j
I_6 = 500
P_j, INC_j, DEC_j, I_j >= 0      for all j

Optimal solution: total cost = 71,500

Month  Demand  Production  INC   DEC   Inventory
Jan    1000    1000        0     0     1500
Feb    2000    2500        1500  0     2000
Mar    5000    5000        2500  0     2000
Apr    7000    5000        0     0     0
May    4000    4000        0     1000  0
Jun    3000    3500        0     500   500

Increases: 4000 x 10 = 40,000
Decreases: 1500 x 5 = 7,500
Holding: 6000 x 4 = 24,000
