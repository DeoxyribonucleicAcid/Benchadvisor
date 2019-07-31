import logging


class Bench:
    def __init__(self, bench_id=None, ratings=None, message_id=None):
        self.bench_id = id(self) if bench_id is None else bench_id
        self.ratings = ratings
        self.message_id = message_id

    def serialize(self):
        return {
            'bench_id': str(self.bench_id),
            'ratings': [i for i in self.ratings] if self.ratings is not None else None,
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
            ratings = [i for i in json['ratings']] if json['ratings'] is not None else []
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
