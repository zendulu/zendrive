# Customization Guide

This guide explains how to modify the pacenotes and create your own custom co-drivers for zendrive.

## Editing Pace Notes

Pacenotes define what the co-driver says and when they say it. They are stored in JSON format.

### Quick Start: Your First Custom Note
1. **Find the stage:** Locate the JSON file for the stage you want to edit in the `pacenotes` directory.
2. **Override it:** Copy that file into the `custom_pacenotes` directory. The mod always prioritizes files in `custom_pacenotes` over the defaults.
3. **Edit:** Open the file in a text editor, modify a phrase or distance, and save.
4. **Test:** Launch the game and run the stage to hear your changes.

### Anatomy of a Pacenote
Each pacenote is an array consisting of a distance, a series of phrases, and an optional conditional rule.

Example:
```json
[16, ["slight right", "40", "over bumps"]],
[64, ["ice now"], {"winter": true}],
```

- **Distance (e.g., `16`)**: The distance in meters from the start of the stage. The note is triggered approximately X seconds (default 4s) before this mark.
- **Phrases (e.g., `["slight right", "40"]`)**: A list of audio phrases to play in sequence. 
    - *Pro Tip:* Using multiple small phrases (e.g., `["slight right", "40"]`) allows for better phrase reuse across different co-drivers. Using one long phrase (e.g., `["slight right 40"]`) can sound more natural but is harder to maintain.
- **Conditions (e.g., `{"winter": true}`)**: Optional rules. The "winter" condition only triggers if the Season is set to "Winter" in the mod settings.

### JSON Safety
JSON is extremely strict. A single missing character can prevent the mod from loading the notes.
- **The Comma Rule:** Every pacenote line must end with a comma `,` **except for the very last pacenote in the file**.
- **Validation:** If your notes aren't loading, copy the file content into an online validator like [JSONLint](https://jsonlint.com/) to find syntax errors.

---

## Adding Co-drivers

A co-driver is simply a folder of MP3 files named after the phrases they use.

### Co-driver Creation Checklist
- [ ] **Review Vocabulary**: Check [./vocabulary.txt](vocabulary.txt) for the 193 required phrases and [./vocabulary-supplemental.txt](vocabulary-supplemental.txt) for optional ones.
- [ ] **Prepare Audio**: Create MP3 files.
    - **Format**: 44.1kHz, Stereo.
- [ ] **Name Files**: Use the `PHRASE-suffix.mp3` convention.
- [ ] **Organize**: Place all files in `codrivers/YourCoDriverName/`.

### Naming Convention
The mod identifies the phrase by everything before the first hyphen `-`.

**Example:** `and acute hairpin right-v1-take2.mp3`
- **Phrase**: `and acute hairpin right`
- **Suffix**: `v1-take2` (ignored by the mod)

If multiple files match the same phrase (e.g., `left-1.mp3` and `left-2.mp3`), the mod will pick one at random for each occurrence.

### Validation for Power Users
If you are familiar with Python, you can use the provided script to verify your co-driver folder is missing any required phrases:
```bash
python check-codriver-vocabulary.py path/to/your/codriver_folder
```

---

## Special and Dynamic Calls

Some calls are triggered by game events rather than distance.

### System Events
Ensure your co-driver has audio for these specific phrases:
- **Punctures/Bursts**: `puncture rear left`, `puncture rear right`, `puncture front left`, `puncture front right`, `burst rear left`, `burst rear right`, `burst front left`, `burst front right`.
- **Penalties**:
    - `penalty maybe cut`: 5-15 second penalty.
    - `penalty maybe big reset`: 15-85 second penalty.
    - `penalty maybe tire repair`: >85 second penalty.

### Filler and Stage Calls
- **Fillers**: Add files prefixed with `pre-filler-` or `post-filler-` for random atmospheric sounds (currently 20% chance to play).
- **Stage Bounds**: 
    - `pre-stage`: Called before the stage begins.
    - `post-stage`: Called after the stage ends.
