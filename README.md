# XKCD Excuse Generator

Generate your own excuse in a nifty comic style!

[![CircleCI](https://circleci.com/gh/mislavcimpersak/xkcd-excuse-generator/tree/master.svg?style=svg)](https://circleci.com/gh/mislavcimpersak/xkcd-excuse-generator/tree/master)

-----

Created for [Python Hrvatska meetup](https://www.meetup.com/Python-Hrvatska/events/242639630/) held on September 12, 2017 and for [Python Belgrade meetup](https://www.meetup.com/PythonBelgrade/events/243547584/) held on September 29, 2017 on which I gave [a talk](https://mislavcimpersak.github.io/serverless-talk/) on serverless technology.


![](example.png)

## Usage

Send `first_text` and `second_text` with desired text as GET parameters to function's root URL.

### Using curl:

```
curl -X GET https://xzmc1m2dgb.execute-api.eu-central-1.amazonaws.com/prod/\?first_text\=my%20function%20is%20uploading\&second_text\=uploading > excuse.png
```

### Using browser

Visit [function](https://xzmc1m2dgb.execute-api.eu-central-1.amazonaws.com/prod/) in browser and follow instructions.

## Original image

[Original image](https://xkcd.com/303/) created by Randall Munroe from XKCD.

Released under [Creative Commons Attribution-NonCommercial 2.5 License](https://creativecommons.org/licenses/by-nc/2.5/).

## Font

[XKCD-Font](https://github.com/ipython/xkcd-font) created by iPython team.

Released under [Creative Commons Attribution-NonCommercial 3.0 License](https://creativecommons.org/licenses/by-nc/3.0/).

