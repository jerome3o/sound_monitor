# Sound Monitor

Big Bunnings Brother mandates no sound above regulation dB levels. Calibrated to Jerome's cheapo headset.

# Setup

## Docker

docker build . -t soundmonitor
docker run -d --device /dev/snd:/dev/snd -p "8000:8000" soundmonitor

## From source

This will require portaudio19-dev

For ubuntu:
```
sudo apt-get install -y portaudio19-dev
```

```bash
python -m venv venv
. venv/bin/activate
pip install -r frontend/requirements.txt

# run
uvicorn server:app --host 0.0.0.0 --port 8000
```

# Usage

Then the navigate to `localhost:8000` and you should have the UI displaying the sound data
