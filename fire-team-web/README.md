# FIRE TEAM Web Calculator

A web-based calculator for the FIRE TEAM 6.5 wargame system, replacing the Tkinter GUI with a modern web interface.

## Features

- **Vehicle Combat Calculator**: Calculate kill numbers for vehicle-to-vehicle combat
- **Infantry Combat Calculator**: Determine infantry fire results using the fire table
- **Complete Weapon Database**: All weapons from US, Soviet, and Finnish forces
- **Responsive Web Interface**: Works on desktop and mobile devices

## Installation

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python main.py
   ```

3. Open your browser and go to `http://localhost:8000`

## Project Structure

- `www/` – the whole app as static files (also the source for the iOS app):
  - `index.html` – UI (vehicle, infantry and command point calculators)
  - `engine.js` – weapon data and all combat calculations, run in the browser
  - `sw.js`, `manifest.webmanifest`, `static/` – PWA service worker, manifest and icons
- `main.py` – FastAPI server that serves `www/`; it still exposes the original Python API below,
  but the app no longer uses it. Weapon or table changes belong in `www/engine.js`.

## API Endpoints (legacy, not used by the app)

- `GET /`: Main web interface
- `GET /api/weapons`: Get list of all weapons
- `POST /api/vehicle-combat`: Calculate vehicle combat results
- `POST /api/infantry-combat`: Calculate infantry combat results

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla); calculations in `www/engine.js`

## Original System

This web app is based on the FIRE TEAM 6.5 wargame rules and replaces the original Tkinter-based calculator with a web interface for better accessibility and usability.