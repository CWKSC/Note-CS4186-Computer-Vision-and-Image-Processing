from typing import Any
import math

import numpy as np

import Util.Array2DUtil as Array2DUtil


def applyKernal(image: list[list[int]], kernal: list[list[int]]) -> list[list[int]]:
    (row, col) = Array2DUtil.getRowCol(image)
    k = Array2DUtil.getRadius(kernal)
    result = Array2DUtil.zero(row - 2 * k, col - 2 * k)
    for (paddingRow, paddingCol), (resultRow, resultCol) in zip(
        Array2DUtil.paddingIter(image, k), Array2DUtil.iter(result)
    ):
        sum: int = 0
        for (kernalRow, kernalCol), (offsetRow, offsetCol) in zip(
            Array2DUtil.iter(kernal), Array2DUtil.centerAlignOffsetIter(kernal)
        ):
            sum += (
                image[paddingRow + offsetRow][paddingCol + offsetCol]
                * kernal[kernalRow][kernalCol]
            )
        result[resultRow][resultCol] = sum
    return result


def genMeanKernal(k: int = 1):
    length = 2 * k + 1
    return np.full((length, length), 1 / (length * length))


def gaussianFunc(x: int, y: int, sd: float = 1.0) -> float:
    return math.exp(-(x**2 + y**2) / (2 * sd**2)) / (2 * math.pi * sd**2)


def genGaussianKernel(k: int = 1, sd: float = 1.0) -> list[list[float]]:
    result = list(Array2DUtil.centerAlignOffsetArray2D(k))
    result = Array2DUtil.map(result, lambda ele, r, c: gaussianFunc(ele[0], ele[1], sd))
    sum = Array2DUtil.sum(result)
    result = Array2DUtil.map(result, lambda ele, r, c: ele / sum)
    return result
