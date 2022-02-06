import numpy as np
import os


def stack_ntiers(stack, years, prog):
    stack = []
    for value in STACK.values():
        stack.append(all_years(value, years, prog))
    return stack


def all_years(value, years, prog):
    years_list = []
    for year in years:
        years.append(np.load(value.format(prog=prog, year=year))["arr_0"])
    return np.stack(years_list, axis=0)
