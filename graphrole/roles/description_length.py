from typing import Tuple

import numpy as np

from graphrole.types import FactorTuple, MatrixLike


def get_description_length_costs(
    V: MatrixLike,
    model: FactorTuple,
    n_bits: int,
) -> Tuple[float, float]:
    """
    Compute description length for encoding the model tuple (factor matrices)
     using the specified number of bits
    :param V: original matrix of features from which factors were computed
    :param model: tuple of encoded NMF factors
    :param n_bits: number of bits used for encoding
    """
    G_encoded, F_encoded = model
    V_approx = G_encoded @ F_encoded
    try:
        V_orig = V.values
    except AttributeError:
        # V was already np.ndarray
        V_orig = V

    return (
        get_encoding_cost(model, n_bits),
        get_error_cost(V_orig, V_approx)
    )


def get_encoding_cost(
    model: FactorTuple,
    n_bits: int,
) -> float:
    G_encoded, F_encoded = model
    return n_bits * (G_encoded.size + F_encoded.size)


def get_error_cost(
    V: np.ndarray,
    V_approx: np.ndarray
) -> float:
    """
    Compute error cost of encoding for description length
    :param V: original matrix
    :param V_approx: reconstructed matrix from encoded factors
    """
    # KL divergence as given in section 2.3 of RolX paper
    vec1 = V.ravel()
    vec2 = V_approx.ravel()
    kl_div = np.sum(np.where(vec1 != 0, vec1 * np.log(vec1 / vec2) - vec1 + vec2, 0))
    return kl_div
