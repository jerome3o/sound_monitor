# Sound Monitor

Big Bunnings Brother mandates no sound above regulation dB levels. Calibrated to Jerome's cheapo headset.


# Setup

```bash
python -m venv venv
. venv/bin/activate
pip install -r frontend/requirements.txt
```

# Usage

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```
 Then the navigate to `localhost:8000` and you should have the UI displaying the sound data
