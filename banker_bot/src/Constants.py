from enum import Enum


class NC_MSG_States(Enum):
    INFO = 0
    USERNAME = 1
    DISPLAY_EDIT_NAME = 2


class CALLBACK:
    # BENCH CALLBACKS
    BENCH_NEW = 'bench-new'

    # BAG CALLBACKS
    @staticmethod
    def BENCH_RATING(bench_id, stars: float): return 'bench-rating%' + str(bench_id) + '%' + str(stars)
