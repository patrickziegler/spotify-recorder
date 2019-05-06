# AudioSpy

### Prerequisites

The following packages are needed

* `python` (>= 3.5)
* `setuptools`
* `virtualenv` (optional)
* `dbus-1-devel`
* `portaudio-devel`
* `ffmpeg`

### Build and Install

1. Clone this repository
```bash
git clone https://github.com/patrickziegler/AudioSpy.git && cd AudioSpy
```

2. Create and activate a virtual environment
```bash
export PREFIX=.
python3 -m virtualenv "${PREFIX}/env" --system-site-packages
source "${PREFIX}/env/bin/activate"
```

3. Install dependencies (in virtual environment) and create symbolic links to this package
```bash
pip install -r requirements.txt
python setup.py develop --prefix "${PREFIX}/env"
```

4. System-wide installation
```bash
python setup.py install
```

## Authors

*  Patrick Ziegler

## License

This project is licensed under the GPL - see the [LICENSE](LICENSE) file for details
