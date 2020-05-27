import typing as t

from abc import abstractmethod, ABC


def expected_win_rate(rating: int, versus_rating: int) -> float:
    return 1 / (1 + 10 ** ((versus_rating - rating) / 400))


def adjusted_values(rating: int, versus_rating: int, score: float, k: int = 32) -> t.Tuple[int, int]:
    gain = int(k * (score - expected_win_rate(rating, versus_rating)))
    return rating + gain, versus_rating - gain


class Eloed(ABC):

    @property
    @abstractmethod
    def elo(self) -> int:
        pass


def rescale(
    eloeds: t.Sequence[Eloed],
    average_rating: int = 1500,
    reset_factor: float = 0.,
) -> t.Iterable[t.Tuple[Eloed, int]]:
    old_average_rating = sum(eloed.elo for eloed in eloeds) / len(eloeds)
    for eloed in eloeds:
        yield eloed, int(
            round(
                (average_rating + eloed.elo - old_average_rating) * (1 - reset_factor)
                + reset_factor * average_rating,
                0,
            )
        )
