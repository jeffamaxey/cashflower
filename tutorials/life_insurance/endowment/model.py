from cashflower import assign, ModelVariable

from tutorials.life_insurance.endowment.input import policy

INTEREST_RATE = 0.005
DEATH_PROB = 0.003


survival_rate = ModelVariable()
expected_benefit = ModelVariable()
net_single_premium = ModelVariable()


@assign(survival_rate)
def survival_rate_formula(t):
    if t == 0:
        return 1 - DEATH_PROB
    else:
        return survival_rate(t-1) * (1 - DEATH_PROB)


@assign(expected_benefit)
def expected_benefit_formula(t):
    sum_assured = policy.get("sum_assured")
    remaining_term = policy.get("remaining_term")

    if t < remaining_term:
        return survival_rate(t-1) * DEATH_PROB * sum_assured
    elif t == remaining_term:
        return survival_rate(t) * sum_assured
    else:
        return 0


@assign(net_single_premium)
def net_single_premium_formula(t):
    return expected_benefit(t) + net_single_premium(t+1) * 1/(1+INTEREST_RATE)
