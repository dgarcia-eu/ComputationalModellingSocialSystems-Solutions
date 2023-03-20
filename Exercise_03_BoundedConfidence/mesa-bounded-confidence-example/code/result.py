def show_batch_result(ag_num, pers_sup_dist, r_data, beta_min, beta_max, beta_step, hi_min, hi_max, hi_step,
                      rand_num, max_steps):
    r_data.head()
    file_name = ''
    file_name += 'Ag_' + str(ag_num) + \
                 '-MaxStep_' + str(max_steps) + \
                 "-" + pers_sup_dist + \
                 '-Rnd_' + str(rand_num) + \
                 '-Hi_' + str(hi_min) + '_' + str(hi_max) + '_' + str(hi_step) + \
                 '-beta_' + str(beta_min) + '_' + str(beta_max) + '_' + str(beta_step)
    print(file_name)
    r_data.to_pickle(file_name+'.pkl') # save the result
