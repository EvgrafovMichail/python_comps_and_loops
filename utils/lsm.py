from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class TrendInfo:
    """
    Структура данных для описания построенного тренда.

    Attrs:
        abscissa: абсциссы точек.
        ordinates: ординаты точек, полученных в эксперименте.
        ordinates_trend: ординаты значений, рассчитанных с помощью МНК.
            По умолчанию None.
        ordinates_above: ординаты верхней границы коридора ошибок.
            По умолчанию None.
        ordinates_under: ординаты нижней границы коридора ошибок.
            По умолчанию None.
    """

    abscissa: np.ndarray
    ordinates: np.ndarray
    ordinates_trend: Optional[np.ndarray] = None
    ordinates_above: Optional[np.ndarray] = None
    ordinates_under: Optional[np.ndarray] = None


def get_trend(abscissa: np.ndarray, ordinates: np.ndarray) -> TrendInfo:
    """
    Рассчитывает тренд на основе экспериментальных данных, используя МНК.

    Args:
        abscissa: абсциссы точек.
        ordinates: ординаты точек, полученных в эксперименте.

    Returns:
        Структуру данных для описания построенного тренда.
    """
    abscissa_mean = abscissa.mean()
    abscissa_var = np.var(abscissa)
    ordinates_mean = ordinates.mean()

    incline = (
        (np.mean(abscissa * ordinates) - abscissa_mean * ordinates_mean)
        / abscissa_var
    )
    shift = ordinates_mean - incline * abscissa_mean
    incline_std = (np.var(ordinates) / (ordinates.size * abscissa_var)) ** 0.5
    shift_std = incline_std * (np.mean(abscissa ** 2) ** 0.5)

    return TrendInfo(
        abscissa=abscissa,
        ordinates=ordinates,
        ordinates_trend=incline * abscissa + shift,
        ordinates_above=(
            (incline + incline_std) * abscissa + (shift + shift_std)
        ),
        ordinates_under=(
            (incline - incline_std) * abscissa + (shift - shift_std)
        ),
    )
