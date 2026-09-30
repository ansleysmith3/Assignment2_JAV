from pyomo.environ import *
from pyomo.opt import SolverFactory

model = AbstractModel()

# Sets and parameters
model.M = Set(ordered = True)       # months
model.d = Param(model.M)            # demand
model.ci = Param()                  # cost to increase output by one unit
model.cd = Param()                  # cost to decrease output by one unit
model.h = Param()                   # monthly holding cost per unit
model.Imax = Param()                # warehouse capacity
model.P0 = Param()                  # December production
model.I0 = Param()                  # starting inventory
model.Iend = Param()                # required ending inventory

# Variables
model.P = Var(model.M, domain = NonNegativeReals)
model.INC = Var(model.M, domain = NonNegativeReals)
model.DEC = Var(model.M, domain = NonNegativeReals)
model.I = Var(model.M, domain = NonNegativeReals)

def obj(model):
    return sum(model.ci*model.INC[j] + model.cd*model.DEC[j] + model.h*model.I[j] for j in model.M)
model.objfn = Objective(rule = obj, sense = minimize)

def prodbal(model, j):
    if j == model.M.first():
        return model.P[j] == model.P0 + model.INC[j] - model.DEC[j]
    return model.P[j] == model.P[j-1] + model.INC[j] - model.DEC[j]
model.prodbalcons = Constraint(model.M, rule = prodbal)

def invbal(model, j):
    if j == model.M.first():
        return model.I[j] == model.I0 + model.P[j] - model.d[j]
    return model.I[j] == model.I[j-1] + model.P[j] - model.d[j]
model.invbalcons = Constraint(model.M, rule = invbal)

def storage(model, j):
    return model.I[j] <= model.Imax
model.storagecons = Constraint(model.M, rule = storage)

def endinv(model):
    return model.I[model.M.last()] == model.Iend
model.endinvcons = Constraint(rule = endinv)


instance = model.create_instance("JAV_Production.dat")
opt = SolverFactory('glpk')
results = opt.solve(instance)
instance.solutions.store_to(results)
results.write(filename = "JAV_Production_results.yml")

print("Month  Prod    INC     DEC     Inv")
for j in instance.M:
    print(j, value(instance.P[j]), value(instance.INC[j]), value(instance.DEC[j]), value(instance.I[j]))
print("Total cost:", value(instance.objfn))
