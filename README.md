# NS Travel randomizer

This CLI allows you to randomly select stations on the Nederlandse Spoorwegen (NS) network.

## Run script

To run the script, use:

```sh
python3 ns-randomizer.py
```

## Dependencies

Before starting the script, make sure to install the following dependencies in your venv:

* `pandas`
* `yaml`

## Tracking visited stations

To track the station you already visited, the program uses the `visited.yaml` file structured as follows:

```yaml
visited:
- code: XXX
```

In the example above, the only visited station is marked by a three-letter code. 

> By default, the Amsterdam Centraal station (`ASD`) is included in the list of visited stations by default.

When you select the option `Mark the station as visited` in the program, it adds the `-code` entry with the station code from the `code` column in the CSV.
