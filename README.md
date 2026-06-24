# Welcome to zendrive

This is a custom mod for EA Sports WRC to let you edit the pacenotes as well as run custom co-drivers. The game exposes just enough telemetry information to make this work but we don't have any way to impact the base game itself. As a result in order to get editable pacenotes we also need to implement our own co-driver and capture the base game notes. The mod currently ships with notes for all 264 stages that are intended to align with the games default notes. However due to the manual process and tremendous amount of work required I'm sure there are inaccuracies, please create an issue for any problems you see so we can integrate the fixes for everyone's benefit.

[![Video preview of the pacenote mod in action](https://img.youtube.com/vi/G3aY9JkA0p4/0.jpg)](https://www.youtube.com/watch?v=G3aY9JkA0p4)

## Setup

### WebView2 Runtime (Windows)

The new version renders its UI using Microsoft WebView2 — the same engine that powers Microsoft Edge. Most Windows 10/11 machines already have WebView2 installed. If you get an error about a missing runtime when launching Zendrive, install it:

- **Download:** https://developer.microsoft.com/en-us/microsoft-edge/webview2/

If you already use Edge, Chromium, or any modern browser, WebView2 is almost certainly already present.

### EA WRC Telemetry Setup

Zendrive listens for UDP telemetry on `127.0.0.1:20666`. EA WRC's telemetry system uses a custom packet structure file (`wrc_zen.json`) that defines what data is sent.

**Step 1: Install the packet structure**

Copy `wrc_zen.json` from this repo to your game's telemetry udp folder:

```
wrc_zen.json → Documents/My Games/WRC/telemetry/udp/wrc_zen.json
```
*(Note: If you use OneDrive, your path may be `OneDrive/Documents/My Games/WRC/...`)*

This file defines all five packet types Zendrive needs:
- `session_update` — continuous telemetry (speed, position, progress, etc.)
- `session_start` — fired when a stage begins
- `session_end` — fired when a stage ends
- `session_pause` — fired when the game is paused
- `session_resume` — fired when the game is resumed

**Step 2: Update the game config**

Open `Documents/My Games/WRC/telemetry/config.json` in a text editor (like Notepad or VS Code).

**⚠️ Backup first:** Before making any changes, create a copy of the file (e.g., make a copy to `config.json.bak`). If the game fails to launch or telemetry stops working, you can simply delete the broken file and rename the backup back to `config.json`.

You need to add the Zendrive configurations into the `udp.packets` array. **Do not replace the entire file**; simply add the `wrc_zen` entries alongside your existing configurations.

**⚠️ Important:** JSON is very strict. Ensure every block is separated by a comma, but **do not** put a comma after the very last block in the array.

**Example of the change:**

*Before:*
```json
{
    "schema": 2,
    "udp": {
        "packets": [
            {
                "structure": "some_other_mod",
                "packet": "session_update",
                "ip": "127.0.0.1",
                "port": 12345,
                "frequencyHz": 60,
                "bEnabled": true
            }
        ]
    }
}
```

*After (adding wrc_zen entries):*
```json
{
    "schema": 2,
    "udp": {
        "packets": [
            {
                "structure": "some_other_mod",
                "packet": "session_update",
                "ip": "127.0.0.1",
                "port": 12345,
                "frequencyHz": 60,
                "bEnabled": true
            },
            {
                "structure": "wrc_zen",
                "packet": "session_start",
                "ip": "127.0.0.1",
                "port": 20666,
                "frequencyHz": 0,
                "bEnabled": true
            },
            {
                "structure": "wrc_zen",
                "packet": "session_end",
                "ip": "127.0.0.1",
                "port": 20666,
                "frequencyHz": 0,
                "bEnabled": true
            },
            {
                "structure": "wrc_zen",
                "packet": "session_pause",
                "ip": "127.0.0.1",
                "port": 20666,
                "frequencyHz": 0,
                "bEnabled": true
            },
            {
                "structure": "wrc_zen",
                "packet": "session_resume",
                "ip": "127.0.0.1",
                "port": 20666,
                "frequencyHz": 0,
                "bEnabled": true
            },
            {
                "structure": "wrc_zen",
                "packet": "session_update",
                "ip": "127.0.0.1",
                "port": 20666,
                "frequencyHz": 120,
                "bEnabled": true
            }
        ]
    }
}
```


If you used zendrive prior to 0.2.0 your `config.json` should already have the `session_update` entry so just add the first 4 additional configurations.


## Using the mod

### Quick Start
1. Launch **EA WRC**.
2. Run `zendrive.exe`.
3. Position the UI on your screen.

**Note:** When running `zendrive.exe` for the first time, Windows may show a "Windows protected your PC" warning. Click **"More info"** and then **"Run anyway"**.

### First Launch
After completing the steps above:
1. Launch EA WRC.
2. Run `zendrive.exe`.
3. A thin control bar will appear with a visual pace notes display below it. You can resize this but the drag handles are difficult to see. Double clicking the header will set it to full screen width you can then move it to wherever you like. Note that there is a known interaction issue with the header not allowing click through on areas where it is not visible. I've made the menu as unobstructive as possible visually but it does take up the full width and does not allow clickthrough as such it may create a scenario where the UI appears like you can click interfaces below the window.
4. Click the hamburger menu (☰) to access settings that were previously keyboard shortcuts (season, co-driver, timing, etc.).
5. Drag the control bar to reposition the entire app.


### Options

The following options are not currently saved so you will need to reset to your preference on each startup of the mod.

#### Codriver

You can change your codriver the mod will automatically scan the codrivers directory at startup so add your own co-drivers do this directory.

#### Note timing

**Default**: 4s

Notes are triggered based on stage progress and are attempted to be queued approximately X seconds before you arrive to the marked location in the notes. Note that timing is approximate based on the vehicle's current speed and will obviously vary from the intended timing if the car is accelarating or braking rapidly. The `-` and `+` buttons will adjust the timing in 0.250 second increments. The default is 6s and will need to be adjusted to your preference.

#### Season

**Default**: "Normal"

Note that this is necessary as the game telemetry does not indicate what season it is and Monte stages have calls for ice in winter. You need to set the season to Winter if you are running Monte in winter, or for any custom winter calls you may add in other locations to work properly.

#### Easter

You can enable/disable some additional calls by adjusting this setting.

#### Filler

You can enable/disable pre and post filler calls by adjusting this setting. These are random sounds that play in between pacenotes. These are only present on Beavis and Butthead.

#### Penalty

You can enable/disable codriver responses to penalties.

#### Icon

You can adjust the visual pacenote display size. `small`, `medium`, or `large`

#### Always On Top

This adjusts how the window displays if you don't want visual pacenotes and want just the audio you may prefer this off.

#### Stage Info

Toggles whether or not the current location and stage (left side) as well as current stage distance and total stage distance (right) render.

#### Pace Notes

This enables/disables the visual pacenotes.


## Customization

Want to tweak the notes or add your own co-driver? Check out the [Customization Guide](CUSTOMIZATION.md) for a detailed walkthrough on editing JSON pacenotes and creating audio packs.


# Bugs!

I'm sure there are bugs in the pacenote and codriver mod as well as innaccuracies in the pacenotes I captured. I used a combination of manual recording of the recce, AI assisted transcription, automated alignment of notes to distances and then lots of hybrid manual and automated cleanup to align both the phrasing and timing. I'm sure due to punctures, time penalties, AI hallucinations, human error, and other details that occurred during my recce the automated portions may be off and I have not re-ran every stage to ensure the notes are aligned with the in game notes. If you notice that any pacenotes or timings are insonsistent with the base game pacenotes. Please create an issue and flag which pacenotes are inaccurate if just a few. Or if a whole route is wildly inaccurate feel free to flag the entire stage.

For the co-drivers the audio is all generated with AI and it is generally not great quality but with some curation and cleanup I've been able to create a subset that seems passable. These certainly need more work but I wanted to share this system earlier rather than later so that others can start contributing improvements or their own pacenotes and co-drivers.

# Help & Troubleshooting

## Common Issues
- **No audio?** Ensure `zendrive.exe` is in the same directory as the `codrivers` and `pacenotes` folders.
- **Notes not updating?** Double-check your `config.json` for syntax errors (missing commas) and ensure you restarted the game after saving.
- **UI issues?** If the window is not appearing, check if it's hidden behind other windows or off-screen.

Feel free to create issues or pull requests for any issues you find. Also if you struggle through something and find a solution please make sure to share the details somehow; I'm sure it will help someone else.

