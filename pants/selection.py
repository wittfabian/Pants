import numpy as np
import random
import operator

class SelectionMechanism:

    def __init__(self, weights):
        self.weights = weights
        self._probabilities = [x / sum(self.weights) for x in self.weights]


    def roulette_wheel_selection(self):
        '''performs weighted selection or roulette wheel selection on a list
            and returns the index selected from the list'''

        # sort the weights in ascending order
        sorted_indexed_weights = sorted(enumerate(self.weights))
        indices, sorted_weights = zip(*sorted_indexed_weights)

        # calculate the cumulative probability
        tot_sum = sum(sorted_weights)
        prob = [x / tot_sum for x in sorted_weights]
        cum_prob = np.cumsum(prob)

        # select a random a number in the range [0,1]
        random_num = random.random()

        for index_value, cum_prob_value in zip(indices, cum_prob):
            if random_num < cum_prob_value:
                return index_value

    def tournament_selection(self, q=2, relate=operator.gt):
        '''
        Ant randomly choose q < Lambda actions form the action set (usually q = 2) and than select the best one.
        This selection mechanism relies on an ordering relation that can rank two (or q) actions.
        Selective pressure is much stronger than for proportional selection (except the random walk setting q = 1,
        which corresponds to p_j = 1 / Lambda, for all j)

        :param q:
        :param relate:
        :return:
        '''
        if q is None or q > len(self._probabilities):
            q = len(self._probabilities)

        best = None
        for i in range(q):
            ind = random.randint(0, len(self._probabilities)-1)
            # if best is None or self._probabilities[ind] < self._probabilities[i]:
            if best is None or relate(self._probabilities[ind], self._probabilities[best]):
                best = ind

        return best

    def uniform_selection(self):
        '''
        We ignore the probabilities for action and do a random search.
        All actions have equal probability to be selected
        :return:
        '''
        return random.randint(0, len(self._probabilities)-1)
