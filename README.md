# ladxr-ui
A simple UI for daid/LADXR

## Usage

### With git

1. Run `git clone https://github.com/spicefather/ladxr-ui` to clone this repo.
2. Run `cd ladxr-ui` and `git submodule update --init` to install LADXR and Z4Randomizer (used for custom sprites).

### Without git

1. Download https://github.com/spicefather/ladxr-ui/archive/master.zip and extract it to a folder.
2. Download https://github.com/daid/LADXR/archive/master.zip and extract it inside of that folder.
3. If you want custom sprites, also download https://github.com/CrystalSaver/Z4Randomizer/archive/master.zip and extract it to the same folder.

Regardless of method, your folder should look like this:

```.
|-LADXR
|-Z4Randomizer
|-LICENSE
|-README.md
|-ui.py
```

You can now open `ui.py` with Python 3 to generate seeds.