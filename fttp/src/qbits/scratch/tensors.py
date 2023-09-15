import torch

from torch import tensor


def indices(shape: list) -> list:
    if len(shape) == 1:
        return list(range(shape[0]))

    elif len(shape) > 1:
        result = []
        for a in range(shape[0]):
            for b in indices(shape[1:]):
                result.append(a)
                result.append(b)

        return result


def tmm(A: tensor, B: tensor) -> tensor:
    """
    :param A: a tensor
    :param B: a tensor
    :return: R = tensor product of A and B; size(R) = (size(A), size(B))
    result[x, y] = A[x] * B[y]
    where x and y are multi-dim indices of A and B
    """

    R = torch.empty(A.size() + B.size)


if __name__ == '__main__':
    sz = [3, 4, 5]
    print(indices(sz))
    print(len(indices(sz)))
