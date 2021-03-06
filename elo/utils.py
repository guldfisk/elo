import typing as t
import random

from abc import abstractmethod


def expected_win_rate(rating: int, versus_rating: int) -> float:
    return 1 / (1 + 10 ** ((versus_rating - rating) / 400))


def adjusted_values(rating: int, versus_rating: int, score: float, k: int = 32) -> t.Tuple[int, int]:
    gain = min(max(int(k * (score - expected_win_rate(rating, versus_rating))), 1), versus_rating)
    return rating + gain, versus_rating - gain


class Eloed(t.Protocol):

    @property
    @abstractmethod
    def elo(self) -> int:
        pass

    @elo.setter
    @abstractmethod
    def elo(self, value: int) -> int:
        pass


def adjust_eloeds(winner: Eloed, loser: Eloed, k: int = 32) -> None:
    winner.elo, loser.elo = adjusted_values(winner.elo, loser.elo, 1, k = k)


E = t.TypeVar('E', bound = Eloed)


def rescale(
    eloeds: t.Sequence[E],
    average_rating: t.Optional[int] = None,
    reset_factor: float = .5,
) -> t.List[t.Tuple[E, int]]:
    old_average_rating = sum(eloed.elo for eloed in eloeds) / len(eloeds)
    average_rating = old_average_rating if average_rating is None else average_rating

    new_ratings = [
        [
            eloed,
            int(
                round(
                    (average_rating + eloed.elo - old_average_rating) * (1 - reset_factor)
                    + reset_factor * average_rating,
                    0,
                )
            )
        ] for eloed in
        eloeds
    ]

    new_sum = sum(r for _, r in new_ratings)

    total_target = int(average_rating * len(eloeds))

    if new_sum > total_target:
        for p in random.sample(new_ratings, new_sum - total_target):
            p[1] -= 1
    elif new_sum < total_target:
        for p in random.sample(new_ratings, total_target - new_sum):
            p[1] += 1

    return new_ratings


def rescale_eloeds(
    eloeds: t.Sequence[E],
    average_rating: t.Optional[int] = None,
    reset_factor: float = .5,
) -> None:
    for eloed, new_rating in rescale(eloeds, average_rating, reset_factor):
        eloed.elo = new_rating
