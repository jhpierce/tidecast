# Welcome to "Tidecast"!

This is a very simple web scraper built as part of the Gridium interview process.

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

* Configurable log levels
* Ability to run linting and testing separately
* Branch protection rules, merging only with high enough test coverage

### Features

* Auto-discovering location pages through searching on the home page
* No hardcoded locations, input via a CSV or similar file
* Parallelized requests to load page content