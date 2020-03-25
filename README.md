# Personalized surf app

Personalized surf reports based on swell, wind, tide, location, skill level, and availability.

## Current state

Returns whether El Porto is small, not blown out, and not high tide. Sends me a text every night with wave conditions if the surf looks good at sunrise the next morning or a message explaining why the surf conditions are forecasted to be poor. Example: 

*Surf's up tomorrow. Waves are 2 to 3 feet with 1 mile per hour winds. Tide is 1.2 feet. First light is at 6:23 AM.*

## Future work

* Integrate surfline or an [aggregate surf forecast](https://github.com/swrobel/meta-surf-forecast) to augment MSW
* Return forecast for one week instead of daily.
* Extend to multiple surf spots.
* Create frontend for entering user preferences.
* Create backend database for saving and updating user preferences.
* Add water quality check.
* Add unit tests.
* Add continuous integration and deployment.

## Acknowledgments

Sunrise time taken from [sunrise-sunset.org](https://sunrise-sunset.org/api).

![](https://im-1-uk.msw.ms/msw_powered_by.png)
