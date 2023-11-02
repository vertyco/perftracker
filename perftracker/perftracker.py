"""A Python performance tracking package"""
import logging
import typing as t
from datetime import datetime, timedelta
from functools import wraps
from time import perf_counter

from pydantic import BaseModel

_log = logging.getLogger("perftracker")


class FTime(BaseModel):
    exe_time: float  # milliseconds
    timestamp: datetime  # UTC


class Performance(BaseModel):
    function_times: dict[str, list[FTime]] = {}

    def add(self, func: t.Callable[..., t.Any] | str, exe_time: float, max_entries: int = None) -> None:
        """Add a function execution time record.

        Args:
            func (t.Callable[..., t.Any] | str): function or the module.name of the function.
            exe_time (float): The execution time of the function in milliseconds.
            max_entries (int, optional): The maximum number of records to keep for the function.
                                          Older records are discarded. Defaults to None, meaning all records are kept.
        """
        key = func if isinstance(func, str) else f"{func.__module__}.{func.__name__}"

        if key not in self.function_times:
            self.function_times[key] = []

        ftime = FTime(exe_time=exe_time, timestamp=datetime.utcnow())
        self.function_times[key].append(ftime)

        if max_entries:
            self.function_times[key] = self.function_times[key][-max_entries:]

    def get(self, func: t.Callable[..., t.Any] | str) -> list[FTime] | None:
        """Get the execution time records of a function.

        Args:
            func (t.Callable[..., t.Any] | str): function or the module.name of the function.

        Returns:
            list[FTime] | None: A list of execution time records, or None if no records exist for the function.
        """
        key = func if isinstance(func, str) else f"{func.__module__}.{func.__name__}"
        return self.function_times.get(key)

    def cpm(self, func: t.Callable[..., t.Any] | str, time_delta: timedelta = None) -> float:
        """Get the "calls per minute" of a function.

        Args:
            func (t.Callable[..., t.Any] | str): function or the module.name of the function.
            time_delta (timedelta, optional): Timespan of data to use. Defaults to None.

        Returns:
            float: Calls per minute for the given function.
        """
        key = func if isinstance(func, str) else f"{func.__module__}.{func.__name__}"
        function_times = self.get(key)
        if not function_times:
            return 0.0

        if time_delta is None:
            # Calculate CPM using all function times
            return len(function_times) / (len(function_times) / 60)

        # Find the oldest entry
        oldest_entry = min(function_times, key=lambda ftime: ftime.timestamp)

        if time_delta >= datetime.utcnow() - oldest_entry.timestamp:
            # Calculate CPM using all function times
            return len(function_times) / (len(function_times) / 60)

        # Filter function times based on the provided time delta
        recent_calls = [ftime for ftime in function_times if ftime.timestamp >= datetime.utcnow() - time_delta]
        if not recent_calls:
            return 0.0
        return len(recent_calls) / (time_delta.total_seconds() / 60)

    def avg_time(self, func: t.Callable[..., t.Any] | str, time_delta: timedelta = None) -> float:
        """Get the average execution time of a function

        Args:
            func (t.Callable[..., t.Any] | str): function or the module.name of the function.
            time_delta (timedelta, optional): Timespan of data to use. Defaults to None.

        Returns:
            float: average time the function takes to execute in milliseconds
        """
        key = func if isinstance(func, str) else f"{func.__module__}.{func.__name__}"
        function_times = self.get(key)
        if not function_times:
            return 0.0
        if time_delta is None:
            # Calculate average execution time of all entries
            return sum(i.exe_time for i in function_times) / len(function_times)

        # Find the oldest entry
        oldest_entry = min(function_times, key=lambda ftime: ftime.timestamp)
        if time_delta >= datetime.utcnow() - oldest_entry.timestamp:
            # Calculate average execution time of all entries
            return sum(i.exe_time for i in function_times) / len(function_times)

        recent_calls = [ftime for ftime in function_times if ftime.timestamp >= datetime.utcnow() - time_delta]
        if not recent_calls:
            return 0.0
        return sum(i.exe_time for i in recent_calls) / len(recent_calls)


_perf = Performance()


def perf(max_entries: int = 100):
    """Decorator to measure and record the execution time of a function.

    Args:
        max_entries (int, optional): The maximum number of execution time records to keep for the function.
                                      Older records are discarded. Defaults to 100, meaning only 100 records are kept.

    Returns:
        function: The decorated function.
    """

    def decorator(func: t.Callable[..., t.Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = perf_counter()
            result = func(*args, **kwargs)
            end_time = perf_counter()
            delta_ms = (end_time - start_time) * 1000

            global _perf
            _perf.add(func, delta_ms, max_entries)

            _log.debug(f"{func.__module__}.{func.__name__} took {delta_ms}ms to complete.")
            return result

        return wrapper

    return decorator


def get_stats() -> Performance:
    """Get the current Performance instance.

    Returns:
        Performance: The current Performance instance.
    """
    global _perf
    return _perf
