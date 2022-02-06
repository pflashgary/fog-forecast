from asyncio.log import logger
import numpy as np
import os
import logging

logger = logging.getLogger("example_logger")


def stack_ntiers(stack, years, prog):
    stack_list = []
    stack_shape = {}
    for key, value in stack.items():
        to_append = all_years(value, years, prog)
        stack_list.append(to_append)
        stack_shape.update({key: to_append.shape[1:]})
    return stack_shape, stack_list


def all_years(filename, years, prog):
    years_list = []
    for year in years:
        pred_year = np.load(filename.format(prog=prog, year=year), mmap_mode="r")[
            "arr_0"
        ]
        pred_year = np.expand_dims(pred_year, axis=-1)
        logger.info("Array shape to stack is: ", pred_year.shape)
        years_list.append(pred_year)
    return np.concatenate(years_list)
