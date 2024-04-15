import statistics

import numpy as np


class SequenceFunctions:
    @staticmethod
    def get_arth_mean(sequence):
        """
        Count the average arithmetical mean of row
        """
        return np.mean(sequence)

    @staticmethod
    def get_median(sequence):
        """
        Count the median of row
        """
        return np.median(sequence)

    @staticmethod
    def get_mode(sequence):
        """
        Count the mode of row
        """
        return statistics.mode(sequence)

    @staticmethod
    def get_dispersion(sequence):
        """
        Count the dispersion of row
        """
        return np.var(sequence)

    @staticmethod
    def get_sko(sequence):
        """
        Count the RMS of row
        """
        return np.std(sequence)