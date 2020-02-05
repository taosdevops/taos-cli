# taos

[![Actions Status](https://github.com/taosdevops/taos-cli/workflows/Test/badge.svg)](https://github.com/taosdevops/taos-cli/actions)
[![Actions Status](https://readthedocs.org/projects/taos-cli/badge/?version=latest)](https://github.com/taosdevops/taos-cli/actions)

[Read The Docs](https://taos-cli.readthedocs.io/en/latest/?)


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


### Contributing

- create pr
- ???
- profit!


## The Taos Bot

*Note:* You must have a slack token exposed at environment variable
`SLACK_API_TOKEN`.

The bot has been created and can be ran by:
- `pip install taos`
- `export SLACK_API_TOKEN=SOMETOKEN`
- `python -m taos.bot`

Alternatively you can run the docker container by using:
`docker run --rm -it -e "SLACK_API_TOKEN=$env:SLACK_API_TOKEN" --name taosbot amcchesneytaos/taosbot:latest`


## Document Generation

In order to generate the docs, make sure you have the `dev.requirements.txt` set of pips installed.

- `pipenv install --dev`
- `pipenv shell`
- `python -m sphinx docs .docs`

There is a catch that unless you have a `SLACK_API_TOKEN` set, the
[bot.py](./taos/bot.py) documentation will not generate. This is due to the
blind call to test authentications. One can either set the token or catch the
error.
