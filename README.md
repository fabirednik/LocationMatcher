# Location Matcher using coordinates

---

A program made in python that matches locations to their corresponding regions and vice versa - to each location the appropriate regions it applies to.

---
### Usage: `python main.py --mode=mode --regions=path --locations=path --output=path`

| Option        | Required | Description                                                                                                                    |
|---------------|----------|--------------------------------------------------------------------------------------------------------------------------------|
| `--mode`      | NO       | Set the mode of program. Use **1 for regions with locations** or **2 for locations with regions**. If not specified, selects 1 |
| `--regions`   | YES      | Path to the regions file in JSON format.                                                                                       |
| `--locations` | YES      | Path to the locations file in JSON format.                                                                                     |
| `--output`    | YES      | Path to the output file.                                                                                                       |

Example usage: `python main.py --mode=1 --regions=input/regions.json --locations=input/locations.json --output=output/results.json`

---
### Input files:
[Locations](input/locations.json):
```js
[
  {
    "name": "<unique identifier>",
    "coordinates": [<longitude>, <latitude>]
  },
  // more locations
]
```
[Regions](input/regions.json):
```js
[
  {
    "name": "<unique identifier>",
    "coordinates": [
      [[<longitude>, <latitude>], [<longitude>, <latitude>]], 
        // more polygons    
    ] - array of polygons, where each polygon is an array of coordinates.
  },
  // more regions
]
```
---
### Output file (for mode 1):

[Results](output/results.json):
```js
[
  {
    "region": "<region identifier>",
    "matched_locations": [
      "<location identifier>",
      "<location identifier>",
    ]
  },
  // more regions
]
```
### Output file (for mode 2):
[Results](output/results.json):
```js
[
  {
    "location": "<location identifier>",
    "matched_regions": [
      "<region identifier>",
      "<region identifier>",
    ]
  },
  // more locations
]
```
---
