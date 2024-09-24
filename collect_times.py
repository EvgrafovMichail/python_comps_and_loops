import multiprocessing as mp
import os

from utils.times_utils import (
    collect_times,
    timers,
)


MAX_WORKERS = 3


def main():
    path_to_data = os.path.join(".", "data")

    if not os.path.exists(path_to_data):
        os.mkdir(path_to_data)

    size_range_config = 10, 10 ** 7 + 1, 10000

    args = [
        (timer_id, size_range_config, path_to_data)
        for timer_id in timers
    ]

    with mp.Pool(processes=MAX_WORKERS) as pool:
        pool.starmap(collect_times, args)


if __name__ == "__main__":
    main()
