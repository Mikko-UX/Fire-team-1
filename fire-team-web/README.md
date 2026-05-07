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

## API Endpoints

- `GET /`: Main web interface
- `GET /api/weapons`: Get list of all weapons
- `POST /api/vehicle-combat`: Calculate vehicle combat results
- `POST /api/infantry-combat`: Calculate infantry combat results

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Templates**: Jinja2

## Original System

This web app is based on the FIRE TEAM 6.5 wargame rules and replaces the original Tkinter-based calculator with a web interface for better accessibility and usability.