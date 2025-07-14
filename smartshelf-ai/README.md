# SmartShelf AI

A low-cost AI system to prevent product spoilage and improve transparency in retail shops using Raspberry Pi, OCR, and smart alerts.

## Features

* Camera-based expiry date detection
* Identification of expired and fake products
* NFC tap-to-check expiry
* LED visual alerts (Red/Green)
* Mobile dashboard for staff
* SMS/WhatsApp expiry notifications
* Early alerts for near-expiry products to prevent losses
* Predictive analytics (future upgrade)
* Blockchain expiry verification (future upgrade)
* Augmented Reality expiry visualization (future upgrade)

## Purpose

SmartShelf AI not only detects expiry dates but also helps identify expired or counterfeit products. By alerting sellers early about soon-to-expire items, it allows them to take timely action (discounts, promotions) so products are consumed instead of wasted, and losses are minimized.

## Project Structure

```
smartshelf-ai/
  backend/                # All Python logic (Flask app, camera, OCR, LED, notifications, upgrades)
  frontend/
    templates/            # HTML templates (dashboard UI)
    static/               # CSS and JavaScript assets
  hardware/               # Camera and LED control modules
  ocr/                    # OCR and date parsing modules
  notifications/          # SMS and WhatsApp notification modules
  dashboard/              # (Legacy) Simple Flask dashboard
  tests/                  # Test scripts
  blockchain.py           # Future upgrade module
  flash_sale.py           # Future upgrade module
  ar_overlay.py           # Future upgrade module
  main.py                 # Main Flask app (serves frontend and API)
  requirements.txt        # Python dependencies
  README.md               # Project documentation
```

## Dashboard (Frontend)

- Staff login interface
- Table of products with expiry dates
- Color-coded status: **Red** (expired), **Yellow** (near expiry), **Green** (safe)
- Buttons to rescan products and send notifications
- Mark products as checked
- Data updates dynamically via API

## Backend (Flask API)

- Serves the dashboard UI and static assets
- Handles product scanning, expiry extraction, LED control, and notifications
- Stores product data in memory (for demo)
- API Endpoints:
  - `GET /api/products` — List all products and expiry statuses
  - `POST /api/products/<id>/check` — Mark a product as checked
  - `POST /api/scan` — Trigger a rescan (simulate OCR)
  - `POST /api/alerts` — Send notifications for expired/near-expiry products

## Hardware Setup

1. Raspberry Pi 4 (brain of the system)
2. Pi Camera (label scanning)
3. NFC Stickers (optional tap-to-check)
4. LED Strips (visual shelf alerts)
5. Power Bank/Battery (portability)

## Software Workflow

* OCR reads expiry dates from labels
* Sorting logic prioritizes products by shelf life
* LEDs and dashboard highlight urgency
* Notifications sent to staff

## Running the Project

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the backend Flask app:
   ```bash
   python main.py
   ```
3. Open your browser and go to `http://localhost:5000` to access the dashboard.

## Prototype Timeline

* Hardware Assembly: 2 days
* Software Setup: 3 days
* Testing: 1 day

**Total Estimated Budget:** ₹5,000

## Future Enhancements

* Blockchain expiry records
* Flash Sale auto-discounts
* AR expiry visualization
