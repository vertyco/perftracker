import time
from datetime import timedelta

from perftracker import get_stats, perf


def test_perf_decorator():
    @perf()
    def test_func():
        time.sleep(0.1)  # Sleep for 100ms

    test_func()

    stats = get_stats()
    function_times = stats.get("test_func")

    assert function_times is not None
    assert len(function_times) == 1
    assert 100 <= function_times[0].exe_time <= 150  # Allow some leeway


def test_max_entries():
    @perf(max_entries=2)
    def test_func():
        pass

    test_func()
    test_func()
    test_func()  # This should evict the first entry

    stats = get_stats()
    function_times = stats.get("test_func")

    assert len(function_times) == 2


def test_cpm():
    @perf()
    def test_func():
        pass

    # Call the function twice
    test_func()
    time.sleep(1)  # Sleep for 1 second
    test_func()

    stats = get_stats()

    # Test against all entries
    cpm = stats.cpm("test_func", time_delta=None)
    assert cpm == 60

    # Test against delta
    cpm = stats.cpm("test_func", timedelta(seconds=1))
    assert cpm == 60

    # Test against overly large delta
    cpm = stats.cpm("test_func", timedelta(days=1))
    assert cpm == 60

    # Test when function doesnt exist yet
    assert stats.cpm("non-existant-function") == 0.0
