import logging
from typing import List


class Bench:
    class Rating:
        def __init__(self, rating_id=None, user_id=None, username=None, rating=None):
            self.rating_id = id(self) if rating_id is None else rating_id
            self.user_id = user_id
            self.username = username
            self.rating = rating

        def __add__(self, other):
            return self.rating + other

        def __radd__(self, other):
            if other == 0:
                return self.rating
            else:
                return self.__add__(other)

    def __init__(self, bench_id=None, ratings=None, message_id=None):
        self.bench_id = id(self) if bench_id is None else bench_id
        self.ratings: List[Bench.Rating] = ratings
        self.message_id = message_id

    def serialize(self):
        return {
            'bench_id': str(self.bench_id),
            'ratings': [{'rating_id': str(i.rating_id),
                         'user_id': str(i.user_id),
                         'username': str(i.username),
                         'rating': i.rating,
                         } for i in self.ratings] if self.ratings is not None else None,
            'message_id': str(self.message_id)
        }

    @staticmethod
    def deserialize(json):
        try:
            bench_id = json['bench_id']
        except KeyError as e:
            bench_id = None
            logging.error(e)
        try:
            ratings = [Bench.Rating(i['rating_id'], i['user_id'], i['username'], i['rating']) for i in
                       json['ratings']] if json['ratings'] is not None else []
        except KeyError as e:
            ratings = None
            logging.error(e)
        try:
            message_id = json['message_id']
        except KeyError as e:
            message_id = None
            logging.error(e)
        bench = Bench(bench_id=bench_id,
                      ratings=ratings,
                      message_id=message_id)
        return bench
