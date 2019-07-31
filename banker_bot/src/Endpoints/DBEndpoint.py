from Entities import Bench
import src.State as State


def insert_new_bench(bench: Bench.Bench):
    bench_serialized = bench.serialize()
    return State.State.bench_col.insert_one(bench_serialized)


def get_bench(bench_id: int):
    query = {"bench_id": bench_id}
    result = State.State.bench_col.find(query)
    if result.count() is 1:
        return Bench.Bench.deserialize(result.next())
    else:
        return None


def update_bench(bench_id: int, update: dict):
    query = {"bench_id": str(bench_id)}
    State.State.bench_col.update_one(query, update)
