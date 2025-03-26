from scipy import optimize
from numpy import array
from random import randint


def demand(x1,x2,b):
    return 1-x1-b*x2


def cost(x,c):
    if x == 0:
     cost = 0
    else:
     cost = c*x
    return cost


def profit(x1,x2,c1,b):
    return demand(x1,x2,b)*x1-cost(x1,c1)


def reaction(x2,c1,b):
    x1 = optimize.brute(lambda x: -profit(x,x2,c1,b), ((0,1,),))
    return x1[0]


def vector_reaction(x,param):
    return array(x)-array([reaction(x[1],param[1],param[0]),reaction(x[0],param[2],param[0])])


def init_matrix_tables(values, stats):

    industry_total = values[0]
    c1 = values[2]
    c2 = values[3]

    firm_one_optimal = stats[0]
    firm_two_optimal = stats[1]

    firm_one_full_output = firm_one_optimal * industry_total
    firm_two_full_output = firm_two_optimal * industry_total

    demand_nash = industry_total - (firm_one_full_output + firm_two_full_output)

    p1 = demand_nash

    firm_one_profit = demand_nash * firm_one_full_output - cost(firm_one_full_output, c1)
    firm_two_profit = demand_nash * firm_two_full_output - cost(firm_two_full_output, c2)

    matrix_one = [[firm_one_full_output, firm_one_profit], [firm_two_full_output, firm_two_profit]]

    mc_one = industry_total - 2 * firm_one_full_output - firm_two_full_output
    mc_two = industry_total - 2 * firm_two_full_output - firm_one_full_output

    cartel_output = (industry_total - mc_one) / 2
    cartel_output_firm = cartel_output / 2

    cartel_demand = industry_total - cartel_output

    p2 = cartel_demand

    cartel_profit_one = cartel_demand * cartel_output_firm - cost(cartel_output_firm, c1)
    cartel_profit_two = cartel_demand * cartel_output_firm - cost(cartel_output_firm, c2)

    matrix_two = [[cartel_output_firm, cartel_profit_one], [cartel_output_firm, cartel_profit_two]]

    cartel_break_output = (industry_total - mc_one - cartel_output_firm) / 2
    cartel_break_demand = industry_total - (cartel_output_firm + cartel_break_output)

    p3 = cartel_break_demand

    cartel_break_profit_one = cartel_break_demand * cartel_break_output - cost(cartel_break_output, c1)
    cartel_break_profit_two = cartel_break_demand * cartel_break_output - cost(cartel_break_output, c2)

    cartel_stay_profit_one = cartel_break_demand * cartel_output_firm - cost(cartel_output_firm, c1)
    cartel_stay_profit_two = cartel_break_demand * cartel_output_firm - cost(cartel_output_firm, c2)

    p4 = cartel_break_demand

    matrix_three = [[cartel_break_output, cartel_break_profit_one], [cartel_output_firm, cartel_stay_profit_two]]
    matrix_four = [[cartel_output_firm, cartel_stay_profit_one], [cartel_break_output, cartel_break_profit_two]]
    m5 = [p1, p2, p3, p4]

    states = [matrix_one, matrix_two, matrix_three, matrix_four, m5]

    return states


def init_nash_states(initial_values):

    x0 = [0.0, 0.0]

    c1_func = float(initial_values[2] / initial_values[0])
    c2_func = float(initial_values[3] / initial_values[0])

    params = [initial_values[1], c1_func, c2_func]

    stats = optimize.fsolve(vector_reaction, x0, args=params)

    return stats


def matrix_states(matrix_reaction):

    nash_state = matrix_reaction[0]
    cartel_state = matrix_reaction[1]
    cartel_break_one_state = matrix_reaction[2]
    cartel_break_two_state = matrix_reaction[3]
    price = matrix_reaction[4]

    output_matrix = [[nash_state[0][0], nash_state[1][0]], [cartel_state[0][0], cartel_state[1][0]],
                     [cartel_break_one_state[0][0], cartel_break_one_state[1][0]], [cartel_break_two_state[0][0],
                                                                                    cartel_break_two_state[1][0]]]

    profit_matrix = [[nash_state[0][1], nash_state[1][1]], [cartel_state[0][1], cartel_state[1][1]],
                     [cartel_break_one_state[0][1], cartel_break_one_state[1][1]], [cartel_break_two_state[0][1],
                                                                                    cartel_break_two_state[1][1]]]

    return output_matrix, profit_matrix, price


def load_states(initial_values):

    nash_states = init_nash_states(initial_values)
    matrix_reactions = init_matrix_tables(initial_values, nash_states)
    output_m, profit_m, price_m = matrix_states(matrix_reactions)

    return output_m, profit_m, price_m