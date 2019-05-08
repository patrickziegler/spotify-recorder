# SpotifyRecorder

### Features

This software allows for **recording currently played music** on the Spotify desktop client in real time.

The generated files are **tagged with ID3-tags** and also **contain the album artwork** as seen in Spotify.

As the information about currently played music is gathered by what the Spotify client broadcasts on the [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/), this software **only runs on Linux** based operating systems.

## Getting started

### Prerequisites

The following packages are needed:

* `python` (>= 3.5)
* `setuptools`
* `virtualenv` (for local deployment)
* `ffmpeg`

### :hammer: Build and Install

1. Clone this repository
```bash
git clone https://github.com/patrickziegler/SpotifyRecorder.git && cd SpotifyRecorder
```

2. Create and activate a virtual environment
```bash
python3 -m virtualenv .venv --system-site-packages
source .venv/bin/activate
```

3. Build and install the package and its dependencies (in virtual environment). You may need to install the development files of `dbus-1` and `portaudio` for this
```bash
pip install -r requirements.txt
python setup.py install
```

4. Instead of a virtual deployment, you can also do a system wide installation after installing the packages stated in `requirements.txt`

### Usage

After the installation is finished, the command `spotify-rec` should be available at your terminal.

After starting the Spotify client, run `spotify-rec` with your desired output location. Then just start playing the songs to be recorded, everything else is done automatically.

## Authors

*  Patrick Ziegler

## License

This project is licensed under the GPL - see the [LICENSE](LICENSE) file for details
