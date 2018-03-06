import numpy as np
import scr.StatisticalClasses as Stat


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, id, prob_head, n_games):
        self._id = id
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._gameLoss = []

        for n in range(n_games):
            # create a new game
            game = Game(id=self._id*1000+n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards

    def get_probability_loss(self):
        """ returns the probability of a loss """
        count_loss = 0
        for value in self._gameRewards:
            if value < 0:
                count_loss += 1
                self._gameLoss.append(1)
            else:
                self._gameLoss.append(0)
        return count_loss / len(self._gameRewards)




class MultiCohort:
    """ simulates multiple cohorts with different parameters """

    def __init__(self, ids, pop_sizes):

        self._ids = ids
        self._popSizes = pop_sizes
        self._get_all_rewards =[]

    def simulate(self):
        """ simulates all cohorts """
        for i in range(len(self._ids)):
            cohort = SetOfGames(i,prob_head=0.5,n_games=self._popSizes)
            self._get_all_rewards.append(cohort.get_ave_reward())



trial = SetOfGames(1,prob_head=0.5, n_games=1000)
print("The average expected reward is:", trial.get_ave_reward())

# problem 1
Stat_sumStat_reward = Stat.SummaryStat('Game Rewards', trial.get_reward_list())
CI_of_Expected = Stat_sumStat_reward.get_t_CI(0.05)

trial.get_probability_loss()
a=trial._gameLoss
Stat_sumStat_loss = Stat.SummaryStat('Game Loss', a)
CI_of_Loss = Stat_sumStat_loss.get_t_CI(0.05)

# Print the 95% t-based confidence intervals for the expected reward and the probability of loss
print("the 95% t-based confidence intervals for the expected reward is", CI_of_Expected)
print("the 95% t-based confidence intervals for the probability of loss", CI_of_Loss)


# problem 2
print("95% CI of expected rewards means that if we simulate many times of 1000 games and get a confidence interval in each time, 95% of these intervals will cover true mean.")

print("95% CI of probability means that if we simulate multiple times of 1000 games and get a confidence interval of probability in each time, 95% of  these intervals will cover true probability of losing.")


# problem 3

print("Casino owner is a steady state simulation, while gambler is a transient state simulation.")
print("Therefore, casino owner should use 95% confidence interval, while gambler should use 95% prediction interval.")


print("for the casino owner, the 95% confidence interval for the expected reward is", CI_of_Expected)
print("for the casino owner, the 95% confidence interval for the probability of loss", CI_of_Loss)

# now simulate 10 times 1000 set of games for the gambler and get the prediction interval
# create multiple cohorts
simulation_number = 1000
popsizefinal =10
b = MultiCohort(range(simulation_number),popsizefinal)
b.simulate()
m = b._get_all_rewards

Stat_sumStat_gambler = Stat.SummaryStat('Game Gambler', m)
CI_of_Gambler = Stat_sumStat_gambler.get_PI(0.05)
print("for the gambler, the 95% confidence interval for the expected reward is", CI_of_Gambler)
