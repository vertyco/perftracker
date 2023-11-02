# PerfTracker

PerfTracker is a Python performance tracking package. It allows you to measure and record the execution time of your functions. The package provides a decorator you can add to any function to track its performance.

## Features

- Easy to use: Simply add a decorator to your functions.
- Flexible: Set a maximum number of entries to keep for each function.
- Detailed statistics: Get the execution times and calculate the average calls per minute over a certain period.

## Installation

Install PerfTracker with pip:

```bash
pip install perftracker
```

## Usage

Here is a quick example:

```python
from perftracker import perf, get_stats

@perf(max_entries=100)
def my_function():
    # Your code here...

# Get performance statistics
stats = get_stats()
```

### Methods

- `perf(max_entries=None)`: A decorator to measure and record the execution time of a function. If `max_entries` is set, it will limit the number of records kept for the function to this value.
- `get_stats()`: Returns the current Performance instance, which contains all recorded performance data.
- `Performance.add(function, exe_time, max_entries=None)`: Adds an execution time record for a function.
- `Performance.get(function)`: Returns the execution time records for a function.
- `Performance.cpm(function, time_delta)`: Calculates the average calls per minute (CPM) of a function over a certain period.
- `Performance.avg_tme(function, time_delta)`: Calculate the average time a function takes to execute over a certain period.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the MIT license.
