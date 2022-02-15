# Program by Alireza Mansouri
# This model is discussed in a manuscript under review by JASSS
# The manuscript title is:
# Phase Transition in the Social Impact Model of Opinion Formation in Scale-Free Networks: The Social Power Effect
#
# This program generate output files of simulations.
# The output files are input of another program named "Diagram-NoThresh" to generate diagrams
#

from model import OpinionModel, get_beta_final_num_list, get_step_list
from result import show_batch_result
from mesa.batchrunner import BatchRunner
import time

ag_num = 1000  # Number of agents
run_max_steps = 1000  # Simulation time steps
rand_num = 30  # iterations with different random seeds for every combination of input values

beta_min = 0
beta_max = 50
beta_step = 10
beta = list(range(beta_min, beta_max+1, beta_step))

hi_min = 0  # minimum value for noise (social temperature)
hi_max = 2000  # maximum moise
hi_step = 200  # steps for changing noise level
hi = list(range(hi_min, hi_max+1, hi_step))

pers_sup_dist= 'uniform',  # or 'deg_ratio', to generate two scenarios

variable_params = { "hi_param":hi, \
                    "beta": beta, "rand_seed": range(rand_num)}

def run_scenario():
    start_time = time.time()
    print('\n===================== current time:', time.ctime())
    fixed_params = {"Ag": ag_num,
                    "distribution": pers_sup_dist}
    print('total it =', total_it(variable_params))
    param_vals = {"Ag": ag_num,
                  "distribution": pers_sup_dist,
                  "hi_param": hi,
                  "beta": beta,
                  "rand_seed": range(rand_num)}
    batch_run = BatchRunner(OpinionModel,
                            fixed_parameters=fixed_params,
                            variable_parameters=variable_params,
                            # parameter_values = param_vals,
                            # iterations = iter_num,
                            max_steps = run_max_steps,
                            model_reporters={"beta_final": get_beta_final_num_list, "steps": get_step_list})
    batch_run.run_all()
    run_data = batch_run.get_model_vars_dataframe()
    show_batch_result(ag_num, pers_sup_dist, run_data, beta_min, beta_max, beta_step, hi_min, hi_max, hi_step, rand_num, run_max_steps)
    end_time = time.time()
    hours, minutes, seconds = calc_H_M_S(start_time, end_time)
    print('Finished, elapsed time:', hours, ':', minutes, ':', seconds, '(H:M:S)')


def calc_H_M_S(start, end):
    m = (end - start) // 60
    h = m // 60
    m = m % 60
    s = round((end - start) % 60)
    return(h, m, s)


def total_it(var_p):
    total = 1
    for x in var_p.keys():
        total *= len(var_p.get(x))
    return total


# The First Scenario (UDBS: Uniform distribution based strengths)
pers_sup_dist = 'uniform'
run_scenario()

# The Second Scenario (NCBS: Node centrality based strength)
pers_sup_dist = 'deg_ratio'
run_scenario()

