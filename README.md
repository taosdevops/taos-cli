# taos

[![Actions Status](https://github.com/taosdevops/taos-cli/workflows/Test/badge.svg)](https://github.com/taosdevops/taos-cli/actions)
[![Actions Status](https://readthedocs.org/projects/taos-cli/badge/?version=latest)](https://github.com/taosdevops/taos-cli/actions)

Taos command line utility.

## The Taos Bot

*Note:* You must have a slack token exposed at environment variable
`SLACK_API_TOKEN`.

The bot has been created and can be ran by:
- `pip install taos`
- `export SLACK_API_TOKEN=SOMETOKEN`
- `python -m taos.bot`

Alternatively you can run the docker container by using:
`docker run --rm -it -e "SLACK_API_TOKEN=$env:SLACK_API_TOKEN" --name taosbot amcchesneytaos/taosbot:latest`
