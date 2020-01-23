# taos
taos command line

## Development

Checkout the project

`git clone git@github.com:taosdevops/taos-cli.git`

Create a branch

`git checkout ?`

### Branching
- bug/    - random bugfixes
- feat/    - random feature requests
- trash/  - for just playing around
- ticket/ - for working an assigned jira ticket


create pr
???
profit!


[Read The Docs](https://taos-cli.readthedocs.io/en/latest/?)

[![Actions Status](https://github.com/taosdevops/taos-cli/workflows/Test/badge.svg)](https://github.com/taosdevops/taos-cli/actions)
[![Actions Status](https://readthedocs.org/projects/taos-cli/badge/?version=latest)](https://github.com/taosdevops/taos-cli/actions)

Taos command line utility.


## Document Generation

In order to generate the docs, make sure you have the `dev.requirements.txt` set of pips installed.

After installing them
- `cd docs`
- `make html`


There is a catch that unless you have a `SLACK_API_TOKEN` set, the [bot.py](./taos/bot.py)
documentation will not generate. This is due to the blind call to test authentications.
One can either set the token or catch the error.
