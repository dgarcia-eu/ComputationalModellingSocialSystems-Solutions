import matplotlib.pyplot as plt
import pandas as pd
import statistics
import os.path
import numpy as np


def init_fig(x_max, x_step):
    f = plt.figure(figsize=(4.5, 2))  # , dpi=100)
    font = {'family': 'normal',
            'weight': 'regular',
            'size': 7}
    plt.rc('font', **font)

    ax_left = plt.subplot2grid((1, 3), (0, 0), colspan=2)
    ax_left.set_xlabel('time step')
    ax_left.set_ylabel("Number of opinion -1, $β(\%)$")
    ax_left.set_ylabel("Mean and SD of $β$ (%)")
    ax_left.set_ylim((-8, 105))
    ax_left.set_yticks(range(0, 101, 10))
    ax_left.grid(True)

    ax_right = plt.subplot2grid((1, 3), (0, 2), sharey=ax_left)
    ax_right.set_xlabel('Initial $β(\%)$')
    ax_right.set_ylabel("Mean, SD, MinMax,\n and Median of $β_{final}(\%)$")
    ax_right.set_ylim((-8, 105))
    ax_right.set_xticks(range(0, x_max + 1, x_step))
    ax_left.set_yticks(range(0, 101, 10))
    ax_right.grid(True)
    return f, ax_right, ax_left


def plot_mean_beta_as_x(path_name, r_data, ag_num, max_step, prefix, rand_seed):
    np.random.seed(1234567)
    r_data = r_data[['beta', 'hi_param', 'rand_seed', 'beta_final', 'steps']]

    fig_beta_50 = plt.figure(figsize=(5, 3.4))  # , dpi=100)
    font = {'family': 'normal',
            'weight': 'regular',
            'size': 7}
    plt.rc('font', **font)
    ax_list = [None] * 6

    ax_list[0] = plt.subplot2grid((2, 3), (0, 0))
    ax_list[1] = plt.subplot2grid((2, 3), (0, 1))
    ax_list[2] = plt.subplot2grid((2, 3), (0, 2))
    ax_list[3] = plt.subplot2grid((2, 3), (1, 0))
    ax_list[4] = plt.subplot2grid((2, 3), (1, 1))
    ax_list[5] = plt.subplot2grid((2, 3), (1, 2))

    ax_list[0].set_ylabel("$β(\%)$")
    ax_list[3].set_ylabel("$β(\%)$")

    ax_list[0].set_xlabel("Time steps\n($h$=0, initial $β=50\%$)")
    ax_list[1].set_xlabel("Time steps\n($h$=200, initial $β=50\%$)")
    ax_list[2].set_xlabel("Time steps\n($h$=400, initial $β=50\%$)")
    ax_list[3].set_xlabel("Time steps\n($h$=600, initial $β=50\%$)")
    ax_list[4].set_xlabel("Time steps\n($h$=1000, initial $β=50\%$)")
    ax_list[5].set_xlabel("Time steps\n($h$=2000, initial $β=50\%$)")

    for i in range(0, 6):
        ax_list[i].set_ylim([-5, 105])
        ax_list[i].set_yticks(range(0, 101, 10))
        ax_list[i].set_xticks(range(0, max_step + 1, int(max_step / 5)))
        ax_list[i].grid(True)
    for i in range(3):
        ax_list[i].set_xticklabels([])
    for i in [1, 2, 4, 5]:
        ax_list[i].set_yticklabels([])

    ax_counter = 0

    for hi in [0, 200, 400, 600, 1000, 2000]:  # for Figures for some hi values
        print("= = = = = = = = = = = = hi: %i = = = = = = = = = = = =" % hi)
        fig1, ax_right, ax_left = init_fig(100, 10)
        beta_list = []
        beta_last_step_mean_arr = []
        beta_last_step_stdv_arr = []
        beta_last_step_max_arr = []
        beta_last_step_min_arr = []
        beta_last_step_median_arr = []
        for beta in [0, 10, 20, 30, 40, 50]:
            beta_trend_mean_arr = [beta]
            beta_trend_stdv_arr = [0]
            beta_list.append(beta)
            temp = r_data[(r_data.hi_param == hi) & (r_data.beta == beta)]['beta_final'].get_values()
            for t_step_counter in range(max_step):
                this_time_step_beta = []
                for rand_counter in range(rand_seed):
                    this_time_step_beta.append(temp[rand_counter][t_step_counter] * 100 / ag_num)
                mean_value = statistics.mean(this_time_step_beta)
                stdv_value = statistics.stdev(this_time_step_beta)
                beta_trend_mean_arr.append(mean_value)
                beta_trend_stdv_arr.append(stdv_value)

            ax_left.plot(range(max_step + 1), beta_trend_mean_arr, linewidth=1)
            ax_left.fill_between(range(max_step + 1), [a - b for a, b in zip(beta_trend_mean_arr, beta_trend_stdv_arr)], [a + b for a, b in zip(beta_trend_mean_arr, beta_trend_stdv_arr)],
                                 alpha=0.3, linewidth=2, antialiased=True)
            beta_last_step_mean_arr.append(beta_trend_mean_arr[-1])
            beta_last_step_stdv_arr.append(beta_trend_stdv_arr[-1])
            beta_last_step_min_arr.append(min(this_time_step_beta))
            beta_last_step_max_arr.append(max(this_time_step_beta))
            beta_last_step_median_arr.append(statistics.median(this_time_step_beta))

            if beta == 50:
                for rand_counter in range(rand_seed):
                    t = [beta]
                    t.extend([x * 100 / ag_num for x in temp[rand_counter]])
                    ax_list[ax_counter].plot(range(max_step + 1), t, linewidth=1)
        ax_counter += 1
        min_arr = [a - b for a, b in zip(beta_last_step_mean_arr, beta_last_step_min_arr)]
        max_arr = [a - b for a, b in zip(beta_last_step_max_arr, beta_last_step_mean_arr)]
        min_max_arr = [min_arr, max_arr]
        ax_right.errorbar(beta_list, beta_last_step_mean_arr, min_max_arr, fmt="o", linewidth=1, color='r', markersize=1, solid_capstyle='projecting', capsize=3, elinewidth=1, markeredgewidth=1)
        ax_right.errorbar(beta_list, beta_last_step_mean_arr, beta_last_step_stdv_arr, fmt="o", linewidth=1, color='k', markersize=1, solid_capstyle='projecting', capsize=2, elinewidth=1, markeredgewidth=1)
        ax_right.errorbar(beta_list, beta_last_step_median_arr, yerr=0, fmt="none", color='b', capsize=4, elinewidth=1, markeredgewidth=1)
        fig1.show()
        fig1.savefig(path_name + prefix + "_hi_" + str(hi), dpi=150, bbox_inches='tight', pad_inches=0)
    fig_beta_50.show()
    fig_beta_50.savefig(path_name + prefix + "_hi_All_beta_50", dpi=150, bbox_inches='tight', pad_inches=0)


def plot_mean_hi_as_x(path_name, r_data, ag_num, prefix, rand_seed):
    np.random.seed(1234567)
    fig = plt.figure(figsize=(5, 3.2))  # , dpi=100)
    font = {'family': 'normal',
            'weight': 'regular',
            'size': 7}
    plt.rc('font', **font)
    ax_list = [None] * 6

    ax_list[0] = plt.subplot2grid((2, 3), (0, 0))
    ax_list[1] = plt.subplot2grid((2, 3), (0, 1))
    ax_list[2] = plt.subplot2grid((2, 3), (0, 2))
    ax_list[3] = plt.subplot2grid((2, 3), (1, 0))
    ax_list[4] = plt.subplot2grid((2, 3), (1, 1))
    ax_list[5] = plt.subplot2grid((2, 3), (1, 2))

    ax_list[0].set_ylabel("Mean and SD of $β_{final}(\%)$")
    ax_list[3].set_ylabel("Mean and SD of $β_{final}(\%)$")

    ax_list[0].set_xlabel("$h$  (Initial $β=0\%$)")
    ax_list[1].set_xlabel("$h$  (Initial $β=10\%)$")
    ax_list[2].set_xlabel("$h$  (Initial $β=20\%)$")
    ax_list[3].set_xlabel("$h$  (Initial $β=30\%)$")
    ax_list[4].set_xlabel("$h$  (Initial $β=40\%)$")
    ax_list[5].set_xlabel("$h$  (Initial $β=50\%)$")

    for i in range(0, 6):
        ax_list[i].set_ylim([-5, 105])
        ax_list[i].set_yticks(range(0, 101, 10))

        for tick in ax_list[i].get_xticklabels():
            tick.set_rotation(90)
        ax_list[i].set_xticks(range(0, 2001, 200))
        ax_list[i].grid(True)
    for i in range(3):
        ax_list[i].set_xticklabels([])
    for i in [1, 2, 4, 5]:
        ax_list[i].set_yticklabels([])

    ax_counter = 0
    hi_list = range(0, 2001, 200)
    for beta in range(0, 51, 10):
        beta_final_list_mean = []
        beta_final_list_stdv = []
        for hi in hi_list:
            beta_final_list = []
            for rand_counter in range(rand_seed):
                temp = r_data[(r_data.hi_param == hi) & (r_data.beta == beta) & (r_data.rand_seed == rand_counter)]['beta_final'].get_values()
                t = temp[0]
                beta_final_list.append(t[-1] * 100 / ag_num)
            mean_value = statistics.mean(beta_final_list)
            stdv_value = statistics.stdev(beta_final_list)

            beta_final_list_mean.append(mean_value)
            beta_final_list_stdv.append(stdv_value)

        ax_list[ax_counter].plot(hi_list, beta_final_list_mean, linewidth=1, color='k')
        ax_list[ax_counter].fill_between(hi_list, [a - b for a, b in zip(beta_final_list_mean, beta_final_list_stdv)],
                                         [a + b for a, b in zip(beta_final_list_mean, beta_final_list_stdv)],
                                         alpha=0.3, linewidth=1, antialiased=True, facecolor='k')
        ax_counter += 1
    fig.show()
    # fig.savefig(path_name + prefix + "_percent_" + str(beta) , dpi=400, bbox_inches='tight',pad_inches=0)
    fig.savefig(path_name + prefix + "_percent_all", dpi=150, bbox_inches='tight', pad_inches=0)


def get_value(param, full_string):
    ix = full_string.find(param) + len(param)
    while full_string[ix] == '-' or full_string[ix] == '_':
        ix += 1
    ix2 = ix
    while '0' <= full_string[ix2] <= '9':
        ix2 += 1
    value = int(full_string[ix:ix2])
    return value


def get_value_ix_fromIx(index, full_string):
    end_ix = index
    while '0' <= full_string[end_ix] <= '9':
        end_ix += 1
    return int(full_string[index:end_ix]), end_ix


def get_Hi_values(full_string):
    ix = full_string.find('Hi-')
    if ix == -1:
        ix = full_string.find('Hi_')
    ix += 3;
    hi_min, ix = get_value_ix_fromIx(ix, full_string)
    ix += 1
    hi_max, ix = get_value_ix_fromIx(ix, full_string)
    ix += 1
    hi_step, ix = get_value_ix_fromIx(ix, full_string)
    return hi_min, hi_max, hi_step


def aggregate_files(path_name, file_name_list):
    # in case the input is segmented in different files, this function aggregates them
    if os.path.exists(path_name + file_name_list[0]):
        r_data = pd.read_pickle(path_name + file_name_list[0])
    else:
        print(path_name + file_name_list[0], " does NOT Exist")
        exit(-1)
    for i in range(1, len(file_name_list)):
        if os.path.exists(path_name + file_name_list[i]):
            # print(path_name + file_name_list[i], " Exists")
            pass
        else:
            print(path_name + file_name_list[i], " does NOT Exist")
            exit(-1)
        to_add = pd.read_pickle(path_name + file_name_list[i])
        r_data = r_data.append(to_add, ignore_index=True)
    return r_data
