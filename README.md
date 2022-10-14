# Welcome to "Tidecast"!

This is a very simple web scraper built as part of the Gridium interview process. It polls tide-forecast.com for a few hardcoded locations and finds the low tides that occur during daylight hours over the course of the next month and prints them to stdout.~~~~

# Instructions for Running

To run this project, you must have, Git, Docker and docker-compose installed locally.

To build the project, clone this repository and navigate to it in a shell and run

```shell
docker-compose build tidecast
```

To run the scraper, run

```shell
docker-compose run tidecast
```

To run the test suite, run

```shell
docker-compose run test
```

# Future improvements

### Dev UX

* A few more unit tests, ensuring that non-200 responses are handled correctly
* Configurable log levels
* Ability to run linting and testing separately
* Branch protection rules, merging only with high enough test coverage

### Features

* Scraping from CDATA section is flaky, since it relies on an implementation detail of the page. Web scrapers are generally a bit flaky, but there are other ways to collect this data. We could fall back to parsing the table entity itself, for example. 
* Auto-discovering location pages through searching on the home page
* No hardcoded locations, input via a CSV or similar file
* Parallelized requests to load page content