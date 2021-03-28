# SpotifyRecorder

### Features

- This tool allows for **recording currently played music** on the Spotify desktop or web client in real time
- The generated files are **tagged with ID3-tags** and contain **album artwork** as seen in Spotify
- The information about currently played music is gathered by [what is broadcasted](https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/) on the [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/)

## Installation

- Use the following commands to install `spotify-rec` for the current user

  ```sh
  pip3 install -r requirements.txt --user
  python3 setup.py install --user
  ```

- You can repeat this also for updating the repo with `git pull`

## Usage

- After the installation is finished, the command `spotify-rec` should be available at your terminal.
- After starting the Spotify desktop or web client, run `spotify-rec` with your desired output location
- Then just start playing the songs to be recorded, everything else is done automatically
- Use `spotify-rec -h` to get more information about the interface

## Example

The output of an example session can be seen below:

```sh
$ spotify-rec ./rec
Watchdog is monitoring 'org.mpris.MediaPlayer2.firefox.instance1680'
New track 'Soopertrack' is playing
Start recording 'Soopertrack'
Cached album cover '/tmp/spotify-rec_album_cover_676ee20be59b46918cc091ceeb025843.png'
New track 'Schmedding' is playing
Start recording 'Schmedding'
Cached album cover '/tmp/spotify-rec_album_cover_9e6c322441b14a18b3a0428d8edd3820.png'
Successfully exported './rec/Soopertrack - Soopertrack.mp3'
^CSuccessfully exported './rec/Schmedding 8000 - Schmedding.mp3'
```

## Authors

*  Patrick Ziegler

## License

This project is licensed under the GPL - see the [LICENSE](LICENSE) file for details
