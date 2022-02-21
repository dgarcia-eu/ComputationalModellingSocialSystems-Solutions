# model.py
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
import random
import numpy as np
import math
import networkx as nx


def get_step_list(model):
    return model.step_list


def get_beta_final_num_list(model):
    return model.beta_final_num_list


class OpinionModel(Model):
    """A model with some number of agents."""
    def __init__(self, Ag, distribution, beta, rand_seed, hi_param):
        self.Ag_num = Ag
        self.pers_sup_dist = distribution
        self.hi = hi_param  # to generate uniform(-hi,hi)

        random.seed(rand_seed*9 +3)  # Generate different random seeds
        np.random.seed(rand_seed*9 + 3)  # Generate different random seeds
        self.running = True

        self.self_distance = 1
        self.pers_sup_max = 100
        self.distance = 1

        self.step_counter = 0
        self.step_list = []
        self.beta_final_num_list = []

        self.set_opinions_degrees(beta)

        self.schedule = SimultaneousActivation(self)

        # Create agents
        for x in range(Ag):
            pers, sup = self.set_pers_sup(x)
            a = OpinionAgent(x, self, pers, sup)
            a.opinion = self.opinion_array[x]
            self.schedule.add(a)

    def set_opinions_degrees(self, beta):
        self.opinion_array = np.ones(self.Ag_num, int)
        self.dmax = 0

        self.G = nx.barabasi_albert_graph(self.Ag_num, 2)  # barabasi_albert parameter = 2
        self.degree = self.G.degree()
        node_degree = [self.degree[i] for i in range(len(self.degree))]
        sort_index = np.argsort(node_degree)  # Ascending, needed for 'BA_most_deg'
        sort_index = [sort_index[-i] for i in range(1, len(sort_index) + 1)]  # Descending
        self.dmax = node_degree[sort_index[0]] # I debugged it, node-degree was forgotted
        for i in range(int(self.Ag_num * beta / 100)):
            self.opinion_array[i] = -1
        self.minus_opinion = int(self.Ag_num * beta / 100)
        self.plus_opinion = self.Ag_num - self.minus_opinion
        np.random.shuffle(self.opinion_array)

    def set_pers_sup(self, i):
        if self.pers_sup_dist == 'uniform':
            return random.uniform(0, self.pers_sup_max), random.uniform(0, self.pers_sup_max)
        elif self.pers_sup_dist == 'deg_ratio':
            return round(self.pers_sup_max * self.degree[i] / self.dmax), \
                   round(self.pers_sup_max * self.degree[i] / self.dmax)
        else:
            print("incorrect parameter for set_pers_sup")

    def distance_func(self, d_agent, s_agent):
        if d_agent.unique_id == s_agent.unique_id:
            return self.self_distance
        elif self.G.has_edge(s_agent.unique_id, d_agent.unique_id):
            return self.distance # distance between two connected nodes is supposed 1
        else:
            return -1 # means no connection

    def step(self):
        self.schedule.step()
        self.step_counter += 1
        self.step_list.append(self.step_counter)
        self.beta_final_num_list.append(self.minus_opinion)


class OpinionAgent(Agent):
    def __init__(self, unique_id, model, pers, sup):
        super().__init__(unique_id, model)
        self.persuad = pers #np.random.randint(0, max_persuad)
        self.support = sup #np.random.randint(0, max_support)
        self.sigma_s = 0
        self.sigma_p = 0

    def interact(self):
        agent_list = self.model.schedule.agents
        agent_opinion = self.opinion
        sigma_p = 0
        sigma_s = 0
        n = 0
        for source_agent in agent_list:
            immediacy = self.model.distance_func(self, source_agent)
            if (source_agent.opinion == agent_opinion) and (immediacy != -1):  # -1 is for no connected
                sigma_s += source_agent.support * 2 / (immediacy ** 2)  # 2 for (1+sig_i*sig_j
            elif (source_agent.opinion != agent_opinion) and (immediacy != -1):
                sigma_p += source_agent.persuad * 2 / (immediacy ** 2)  # 2 for (1-sig_i*sig_j
            n += 1
        return sigma_s, sigma_p

    def step(self):
        self.sigma_s, self.sigma_p = self.interact()

    def advance(self):
#        print(self.unique_id, ': Advance:')
        rand_hi = random.uniform(-self.model.hi, self.model.hi)
        if (self.sigma_p - self.sigma_s + rand_hi) > 0:
            if self.opinion == 1:
                self.opinion = -1
                self.model.minus_opinion += 1
                self.model.plus_opinion -= 1
            elif self.opinion == -1:
                self.opinion = +1
                self.model.minus_opinion -= 1
                self.model.plus_opinion += 1
            else:
                print("Incorrect opinion")
                exit(1)
