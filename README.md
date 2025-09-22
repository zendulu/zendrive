# Welcome to zendrive

This is a custom mod for EA Sports WRC to let you edit the pacenotes as well as run custom co-drivers. The game exposes just enough telemetry information to make this work but we don't have any way to impact the base game itself. As a result in order to get editable pacenotes we also need to implement our own co-driver and capture the base game notes. The mod currently ships with notes for all 264 stages that are intended to align with the games default notes. However due to the manual process and tremendous amount of work required I'm sure there are inaccuracies, please create an issue for any problems you see so we can integrate the fixes for everyone's benefit.

[![Video preview of the pacenote mod in action](https://img.youtube.com/vi/G3aY9JkA0p4/0.jpg)](https://www.youtube.com/watch?v=G3aY9JkA0p4)

## Setup

### UDP Configuration

You should only need to do this UDP setup the first time you use the mod. Once UDP is configured and working you only need to double click the executable to have the mod running. 

1. Download the zip in the releases section. Currently [v0.1.4-beta](https://github.com/zendulu/zendrive/releases/tag/v0.1.2-beta) is the latest release.
2. Extract the zip file.
3. Copy `wrc_zen.json` from the extracted files to `Documents\My Games\WRC\telemetry\udp`
4. Go up one directory to `Documents\My Games\WRC\telemetry`
5. Make a backup copy of `config.json`
6. Edit config.json to add the following section to the packets data structure of that file. Note that the last comma chould be omitted if you add this as the last entry. 

The following is what we need to add:
```json
      {
        "structure": "wrc_zen",
        "packet": "session_update",
        "ip": "127.0.0.1",
        "port": 20666,
        "frequencyHz": 120,
        "bEnabled": true
      },
```

## Using the mod

## Running the program.

After you have setup the UDP settings as detailed above, in theory you should be able to double click the executable and as long as it is in the same directory as the codrivers and pacenotes it should be working and look something like the following

![A computer interface for the zendrive mod showing configuration including: Note Timing, Season, and Co-driver settings. Also shown on the right side are status details like the current location, route, distance and app version. At the bottom is a section showing log information.](./screenshot.png)

### Options

The following options are not currently saved so you will need to reset to your preference on each startup of the mod.

#### Note timing

**Default**: 4s

Notes are triggered based on stage progress and are attempted to be queued approximately X seconds before you arrive to the marked location in the notes. Note that timing is approximate based on the vehicle's current speed and will obviously vary from the intended timing if the car is accelarating or braking rapidly. The left and right arrow keys will adjust the timing in 0.250 second increments. The default is 6s and will need to be adjusted to your preference.

#### Season

**Default**: "Normal"

You can press the 's' key to change the season. Note that this is necessary as the game telemetry does not indicate what season it is and Monte stages have calls for ice in winter. You need to set the season to Winter if you are running Monte in winter, or for any custom winter calls you may add in other locations to work properly.

#### Easter

You can enable/disable some additional calls for some stages by pressing the 'e' key..

#### Filler

You can enable/disable pre and post filler calls by pressing the 'f' key.

#### Penalty

You can enable/disable codriver responses to penalties by pressing the 'p' key.

#### Codriver

You can change your codriver at any time by pressing the 'c' key. The mod will automatically scan the codrivers directory at startup so add your own co-drivers do this directory.


## Editing pace notes

Pacenote files are in a json format. You must ensure that your pacenotes are valid json. Use one of the many online JSON validators if you are unfamilar with the format to ensure your edits are valid JSON. As a helpful hint every pacenote line should end with a ',' except for the last pacenote in a file.

### Anatomy of a pacenote

Each pacenote consists of a distance, a series of phrases, and an optional conditional rule which currently only allows for a "winter" conditional.

An example excerpt is as follows:

```json
  [16, ["slight right", "40", "over bumps"]],
  [64, ["ice now"], {"winter": true}],
  [106, ["six left", "100"]],
  [258, ["five left"]],
  [327, ["and four right", "short", "100"]],
```

Let's take a closer look at the first pace note:
```json
  [16, ["slight right", "40", "over bumps"]],
```

What this pacenote does is indicate that when we are approximately 6s (default timing) prior to the 16 meter mark the game will queue the phrases "slight right", "40" and "over bumps". This could have also been written as
```json
  [16, ["slight right 40 over bumps"]],
```
In which case the system would queue the single phrase "slight right 40 over bumps". There are tradeoffs between the two options. The many smaller phrases create more flexbility and allow for more phrase re-use which makes creating new co-drivers less cumbersome. However it can lead to canned or robotic sounding pacenotes as the notes don't necessarily flow from one to the next. I have done my best to find a right balance with the base notes to minimize the amount of calls while also creating some flow. The base notes have 518 unique phrases which is heavily reduced from the approximate 7500 or so calls that would be if the second format was used. Please review `vocabulary.txt` for the list of base note files that are supported.

### Adding your own pacenotes

The directory `custom_pacenotes` will always be consulted first and any matching notes for the current stage will be prioritized over the default pacenotes found in the `pacenotes` directory. You can either create your own notes from scratch or copy the existing notes into the `custom_pacenotes` directory and edit as prefer.


## Adding co-drivers

### vocabulary

Review [./vocabulary.txt](vocabulary.txt) which is the vocabulary of the default pacenotes. Custom co-drivers will need to implement those 193 phrases as a minimum; there is an additional set of supplemental calls not used by the default notes and are covered in [./vocabulary-supplemental.txt](vocabulary-supplemental.txt). In addition there are several system notes that are used for various in game dynamic events those are currently limited to the following calls.

- "puncture rear left": called when the rear left receives a puncture.
- "puncture rear right": called when the rear right receives a puncture.
- "puncture front left": called when the front left receives a puncture.
- "puncture front right": called when the front right receives a puncture.
- "burst rear left": called when the rear left bursts.
- "burst rear right": called when the rear right bursts.
- "burst front left": called when the front left bursts.
- "burst front right": called when the front right bursts.
- "penalty maybe cut": called when a 5-15 second penalty happens.
- "penalty maybe big reset": called when the vehicle is likely reset and a penalty between 15 and 85 seconds is applied. Note that the game has several issues with vehicle resets, penalties and when the game state is updated so this behavior is approximate.
- "penalty maybe tire repair": called when called when the vehicle is likely reset and a penalty greater than 85 seconds is applied. Note that the game has several issues with vehicle resets, penalties and when the game state is updated so this behavior is approximate.

When the above penalty times trigger they may also create a scenario where the notes are repeated, if this occurs the codriver will say "repeating" and then repeat notes for corners not yet reached based on the reset position.

In addition to the tire puncture and burst calls there are also dynamic filler samples that you can add. These calls are randomly included at a rate currently 20%. Currently supported are two prefixes:

- pre-filler: possibly called before a note entry
- post-filler: possibly called after a note entry

Additional fixed point calls:

- pre-stage: called before a stage
- post-stage: called after a stage

### naming convention

Co driver call files are named with the following convention.

```PHRASE-(ANYTHING YOU WANT).mp3```

Where `PHRASE` is a phrase that is used in the pacenots. For instance the call file `and acute hairpin right-123-2.mp3` has the `PHRASE` "and acute hairpin right" meaning that in the pacenotes the phrase "and acute hairpin right" will potentially use this file when that call comes up. Everything after the `-` will be essentially ignored and can be whatever is helpful for your naming convention. When the mod needs to pick a sound file any file matching the `PHRASE` for the currently selected co-driver will be picked at random.

### file formats

mp3 files should be 44.1k stereo samples.

# Bugs!

I'm sure there are bugs in the pacenote and codriver mod as well as innaccuracies in the pacenotes I captured. I used a combination of manual recording of the recce, AI assisted transcription, automated alignment of notes to distances and then lots of hybrid manual and automated cleanup to align both the phrasing and timing. I'm sure due to punctures, time penalties, AI hallucinations, human error, and other details that occurred during my recce the automated portions may be off and I have not re-ran every stage to ensure the notes are aligned with the in game notes. If you notice that any pacenotes or timings are insonsistent with the base game pacenotes. Please create an issue and flag which pacenotes are inaccurate if just a few. Or if a whole route is wildly inaccurate feel free to flag the entire stage.

For the co-drivers the audio is all generated with AI and it is generally not great quality but with some curation and cleanup I've been able to create a subset that seems passable. These certainly need more work but I wanted to share this system earlier rather than later so that others can start contributing improvements or their own pacenotes and co-drivers.

# Help

Feel free to create issues or pull requests for any issues you find. Also if you struggle through something and find a solution please make sure to share the details somehow; I'm sure it will help someone else.
