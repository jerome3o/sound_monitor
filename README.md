# Sound Monitor

Big Bunnings Brother mandates no sound above regulation dB levels. Calibrated to Jerome's cheapo headset.


# Setup

## Backend

```bash
python -m venv venv
. venv/bin/activate
pip install -r frontend/requirements.txt
```

## Frontend

Add you need is a static server, I use `browser-sync` for development:

```bash
npm install -g browser-sync
```


# Running

## Backend

```bash
uvicorn backend.server:app --host 0.0.0.0
```

## Frontend

```bash
cd frontend
browser-sync start -s -f . --no-notify --host 0.0.0.0 --port 9000
```