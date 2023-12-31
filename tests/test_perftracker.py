import datetime
import time

from perftracker import Performance, Record, get_stats, perf


def test_record():
    now = datetime.datetime.utcnow()
    record = Record(exe_time=10.0, timestamp=now)
    assert record.exe_time == 10.0
    assert isinstance(record.timestamp, datetime.datetime)
    assert str(record) == f"{round(record.exe_time, 4)}ms @ {record.timestamp} UTC"


def test_add():
    perf = Performance()
    perf.add("test_func", 10.0)
    assert "test_func" in perf.function_times
    assert len(perf.function_times["test_func"]) == 1
    assert perf.function_times["test_func"][0].exe_time == 10.0


def test_add_with_max_entries():
    perf = Performance()
    for i in range(10):
        perf.add("test_func", i, max_entries=5)
    assert len(perf.function_times["test_func"]) == 5
    assert perf.function_times["test_func"][0].exe_time == 5.0


def test_get():
    perf = Performance()
    perf.add("test_func", 10.0)
    assert perf is not None
    assert len(perf.get("test_func")) == 1
    if p := perf.get("test_func"):
        assert p[0].exe_time == 10.0


def test_cpm():
    perf = Performance()
    for _ in range(10):
        perf.add("test_func", 0)
        time.sleep(0.1)
    assert 600 <= perf.cpm("test_func") <= 700
    assert 600 <= perf.cpm("test_func", datetime.timedelta(seconds=1)) <= 700
    assert 600 <= perf.cpm("test_func", datetime.timedelta(minutes=1)) <= 700
    time.sleep(1)
    assert perf.cpm("test_func", datetime.timedelta(seconds=0.1)) == 0.0


def test_cpm_timespans():
    perf = Performance()
    record = Record(0, datetime.datetime.utcnow())
    perf.function_times["test"] = [record, record]
    assert perf.cpm("test") == 0.0
    assert perf.cpm("test", datetime.timedelta(minutes=1)) == 0.0
    perf.function_times["test"].append(Record(0, datetime.datetime.utcnow()))
    time.sleep(0.1)
    perf.function_times["test"].append(Record(0, datetime.datetime.utcnow()))
    assert perf.cpm("test", datetime.timedelta(seconds=0.1)) == 0.0


def test_avg_time():
    perf = Performance()
    # Add 5 function calls with execution times from 1 to 5 milliseconds
    for i in range(1, 6):
        perf.add("test_func", i)
    # The average time should be 3.0 ms
    assert perf.avg_time("test_func") == 3.0


def test_avg_time_no_calls():
    perf = Performance()
    # No function calls were added, so the average time should be 0.0 ms
    assert perf.avg_time("test_func") == 0.0


def test_avg_time_with_time_delta():
    perf = Performance()
    # Add 5 function calls with execution times from 1 to 5 milliseconds
    for i in range(1, 6):
        perf.add("test_func", i)
        time.sleep(0.3)
    assert perf.avg_time("test_func", datetime.timedelta(minutes=1)) == 3
    assert perf.avg_time("test_func", datetime.timedelta(seconds=1)) == 4
    time.sleep(1)
    assert perf.avg_time("test_func", datetime.timedelta(seconds=1)) == 0.0


@perf()
def test_func():
    time.sleep(0.01)


def test_perf():
    stats = get_stats()
    stats.function_times.clear()
    test_func()
    assert "test_perftracker.test_func" in stats.function_times
    assert len(stats.get("test_perftracker.test_func")) == 1


def test_perf_repr():
    perf = Performance()
    assert str(perf) == "0 functions currently tracked"


def test_max_entries():
    @perf(max_entries=2)
    def test_func():
        pass

    test_func()
    test_func()
    test_func()  # This should evict the first entry

    stats = get_stats()
    function_times = stats.get(test_func)

    assert len(function_times) == 2


def test_null_cpm():
    stats = get_stats()
    assert stats.cpm("test") == 0.0
