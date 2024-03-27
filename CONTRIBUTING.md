# Contributing to AST-Monitor
:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

## Code of Conduct
This project and everyone participating in it is governed by the [AST-Monitor Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [iztok.fister1@um.si](mailto:iztok.fister1@um.si).

## How Can I Contribute?

### Reporting Bugs
Before creating bug reports, please check existing issues list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible in the [issue template](.github/templates/ISSUE_TEMPLATE.md).

### Suggesting Enhancements

Open new issue using the [feature request template](.github/templates/FEATURE_REQUEST.md).

### Pull requests

Fill in the [pull request template](.github/templates/PULL_REQUEST.md) and make sure your code is documented.

## Setup development environment

### Requirements

* Poetry: [https://python-poetry.org/docs](https://python-poetry.org/docs)

After installing Poetry and cloning the project from GitHub, you should run the following command from the root of the cloned project:

```sh
poetry install
```

All of the project's dependencies should be installed and the project ready for further development. **Note that Poetry creates a separate virtual environment for your project.**

### Dependencies

| Package                   | Version | Platform |
|---------------------------|:-------:|:--------:|
| matplotlib                | *       |   All    |
| geopy                     | *       |   All    |
| tcx-reader                | ^0.4.2  |   All    |
| sport-activities-features | ^0.3.12 |   All    |
| openant                   | ^1.2.0  |   All    |
| PyQt6                     | 6.4.2   |   All    |
| PyQt6-WebEngine           | ^6.5.0  |   All    |
| pyqt-feedback-flow        | ^0.3.0  |   All    |

#### Development dependencies

| Package               | Version  | Platform |
|-----------------------|:--------:|:--------:|
| pytest                | ^7.2.2   |   All    |
| Sphinx                | ^5.0     |   All    |
| sphinx-rtd-theme      | ^1.0.0   |   All    |
| sphinxcontrib-bibtex  | ^2.4.1   |   All    |

## Development Tasks

### Testing

Manually run the tests:

```sh
poetry run pytest
```