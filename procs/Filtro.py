from pandasql import sqldf
from procs.console import console
import pandas as pd
import timeit


def filtro(df, num):
    # Count the number of cars per person
    count = df.groupby(df.index).size()
    # Get the unique indexes of people with more than x things
    result_index = count[count > num].index
    # Filter the DataFrame using the valid indexes
    result = df.loc[result_index]
    # result_index = pd.DataFrame(result_index, columns=["id_persona"])
    return result
