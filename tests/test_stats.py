import numpy as np
from subcipher.stats import transition_matrix

def test_matrix_sum_one():
    text = "ABCD_EFGHIJKL"
    tm = transition_matrix(text)
    np.testing.assert_allclose(tm.sum(), 1.0)
