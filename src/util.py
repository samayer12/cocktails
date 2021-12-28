"""
Dumping ground for useful functions that don't have
enough related functions to justify their own file.
"""

import logging
import os
import pandas as pd


def extract_nested_values(iterable_data):
    """
    Given a dict of dicts, this unpacks the values in the iterable.
    From stackoverflow, I should find the link for posterity.
    """
    if isinstance(iterable_data, list):
        for sub_iterable_data in iterable_data:
            yield from extract_nested_values(sub_iterable_data)
    elif isinstance(iterable_data, dict):
        for value in iterable_data.values():
            yield from extract_nested_values(value)
    else:
        yield iterable_data


def create_directories(directories: list) -> None:
    """Create the specified list of directories and log the result to an existing logger"""
    for directory in directories:
        try:
            os.makedirs(directory)
            logging.debug('%s created.', directory)
        except FileExistsError:
            logging.debug('%s already exists.', directory)


def reformat_yield_column(yields: pd.Series) -> str:
    """
    Convert the ORF-parsed yield data into a tuple for easier use with Pandas
    """
    drink_yield = []
    for item in yields:
        drink_yield.append(tuple(extract_nested_values(item)))
    return drink_yield


def create_ingredient_set(ingredients: pd.Series) -> pd.Series:
    """
    Convert the ORF-parsed ingredient data to a set of ingredients without amounts for easier use with Pandas
    """
    result = []
    for ingredient_set in ingredients:
        result.append({key for d in ingredient_set for key in d.keys()})
    return pd.Series(result)
