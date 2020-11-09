""" Framework layout to run SAO - Sequential Approximate Optimizaion."""
from sao_opt.doe import RandomDoE
from sao_opt.trust_region import TrustRegion
from sao_opt.opt_problem import OptimizationProblem, Simulation
from sao_opt.surrogate import RadialBasisSurrogate
from sao_opt.solver import TrustConstrSolver
from sao_opt.sequence import Sequence
from sao_opt.converge import Converge
from sao_opt.results import Results

# ---------- Problem Layer -----------------
# Create problem
simulation = Simulation()
problem = OptimizationProblem()

# Initial guess
x_init = simulation.nominal


# ---------- Init Routine Layer ----------------
# Trust region
trust_region = TrustRegion(x_init, problem)

# Lhs sample
doe = RandomDoE(trust_region.lower, trust_region.upper)

# Evaluate in High fidelity model
breakpoint()
samples_output = simulation.high_fidelity(doe.samples)

# Surrogate model
surrogate = RadialBasisSurrogate(doe.samples, samples_output)

# Optimizer Solver
solver = TrustConstrSolver(surrogate, x_init, problem.bounds, problem.linear)

# Results
results = Results(simulation, solver, surrogate, trust_region)

# Converge
converge = Converge(results, problem)


# ---------- Sequence Layer -----------------
sequence = Sequence(trust_region, surrogate, solver, converge, results)
sequence.run()

# ----------- Final Resusts ------------------
