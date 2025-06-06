import operator
import numpy as np
import cmath
from typing import List
from collections import namedtuple
import traceback
import sys


basis = np.array(
    [1, cmath.exp(2j * cmath.pi * 1 / 3), cmath.exp(2j * cmath.pi * 2 / 3)]
)


HistMatchResult = namedtuple("HistMatchResult", "idx length")


def find_all_longest(seq, max_len=None) -> List[HistMatchResult]:
    """
    Find all indices where end of `seq` matches some past.
    """
    result = []

    i_search_start = len(seq) - 2

    while i_search_start > 0:
        i_sub = -1
        i_search = i_search_start
        length = 0

        while i_search >= 0 and seq[i_sub] == seq[i_search]:
            length += 1
            i_sub -= 1
            i_search -= 1

            if max_len is not None and length > max_len:
                break

        if length > 0:
            result.append(HistMatchResult(i_search_start + 1, length))

        i_search_start -= 1

    result = sorted(result, key=operator.attrgetter("length"), reverse=True)

    return result


def probs_to_complex(p):
    return p @ basis


def _fix_probs(probs):
    """
    Put probs back into triangle. Sometimes this happens due to rounding errors or if you
    use complex numbers which are outside the triangle.
    """
    if min(probs) < 0:
        probs -= min(probs)

    probs /= sum(probs)

    return probs


def complex_to_probs(z):
    probs = (2 * (z * basis.conjugate()).real + 1) / 3
    probs = _fix_probs(probs)
    return probs


def z_from_action(action):
    return basis[action]


def sample_from_z(z):
    probs = complex_to_probs(z)
    return np.random.choice(3, p=probs)


def bound(z):
    return probs_to_complex(complex_to_probs(z))


def norm(z):
    return bound(z / abs(z))


class Pred:
    def __init__(self, *, alpha):
        self.offset = 0
        self.alpha = alpha
        self.last_feat = None

    def train(self, target):
        if self.last_feat is not None:
            offset = target * self.last_feat.conjugate()   # fixed

            self.offset = (1 - self.alpha) * self.offset + self.alpha * offset

    def predict(self, feat):
        """
        feat is an arbitrary feature with a probability on 0,1,2
        anything which could be useful anchor to start with some kind of sensible direction
        """
        feat = norm(feat)

        # offset = mean(target - feat)
        # so here we see something like: result = feat + mean(target - feat)
        # which seems natural and accounts for the correlation between target and feat
        # all RPSContest bots do no more than that as their first step, just in a different way

        result = feat * self.offset

        self.last_feat = feat

        return result


class BaseAgent:
    def __init__(self):
        self.my_hist = []
        self.opp_hist = []
        self.my_opp_hist = []
        self.outcome_hist = []
        self.step = None

    def __call__(self, obs, conf):
        try:
            if obs.step == 0:
                action = np.random.choice(3)
                self.my_hist.append(action)
                return action

            self.step = obs.step

            opp = int(obs.lastOpponentAction)
            my = self.my_hist[-1]

            self.my_opp_hist.append((my, opp))
            self.opp_hist.append(opp)

            outcome = {0: 0, 1: 1, 2: -1}[(my - opp) % 3]
            self.outcome_hist.append(outcome)

            action = self.action()

            self.my_hist.append(action)

            return action
        except Exception:
            traceback.print_exc(file=sys.stderr)
            raise

    def action(self):
        pass


class Agent(BaseAgent):
    def __init__(self, alpha=0.01):
        super().__init__()

        self.predictor = Pred(alpha=alpha)

    def action(self):
        self.train()

        pred = self.preds()

        return_action = sample_from_z(pred)

        return return_action

    def train(self):
        last_beat_opp = z_from_action((self.opp_hist[-1] + 1) % 3)
        self.predictor.train(last_beat_opp)

    def preds(self):
        hist_match = find_all_longest(self.my_opp_hist, max_len=20)

        if not hist_match:
             return 0

        feat = z_from_action(self.opp_hist[hist_match[0].idx])

        pred = self.predictor.predict(feat)

        return pred


agent = Agent()


def call_agent(obs, conf):
    return agent(obs, conf)
