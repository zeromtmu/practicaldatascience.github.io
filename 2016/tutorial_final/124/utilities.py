'''
Methods shared by the other modules.
'''
import collections
import numpy as np

# pylint: disable=fixme, no-member

def remove_rare_values_inplace(df_frame, column_list, threshold):
    """ Remove rare values to speed up computation.

    Args:
        df_frame -- A pandas data frame.
        column_list -- A list of columns.
        threshold -- The threshold, below which a value is removed.
    """
    insignificant_population = int(np.floor(threshold * len(df_frame)))
    for cat in column_list:
        freqs = collections.Counter(df_frame[cat])
        other = [i for i in freqs if freqs[i] < insignificant_population]
        for i in other:
            df_frame[cat].replace(i, 'other', inplace=True)

def calculate_final_accuracy(output_result, actual_result):
    """
    Args:
        output_result -- a numpy array.
        actual_result -- a numpy array.
    """
    return 1 - float(np.sum(output_result is not actual_result)) / len(output_result)