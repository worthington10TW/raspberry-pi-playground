# Build monitor

Now the world is remote, do you struggle to keep track of you builds?

Do you want to decouple your build monitor from your machine?

Get yourself a raspberry pi, some LEDs and clone this repo!

## Signals

- Blue light: Fetching data
- Green light: **All** builds pass
- Red light: **Any** builds fail
- Yellow pulse: **Any** builds are running

## Setup

Setup is stored within `src/integrations.json`

```json
{
    "poll_in_seconds": 30,
    "integrations": [
            {
                "type": "",
                "username": "",
                "repo": "",
                "excluded_workflows": [ "" ]
            }
        ]
}
```

### Current integrations

- CircleCI
- GitHub Actions
  
Personal API tokens are read from environment variables

```shell
export GITHUB_TOKEN=<TOKEN>
export CIRCLE_CI_TOKEN<TOKEN>
```

## Pin setup

- Pin constants can be found in `src/gpio/constants.py`

## TODO

- [ ] Feedback when connection is unsuccessful.
- [ ] Allow multiple access tokens for integrations.



