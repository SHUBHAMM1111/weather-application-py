# 🌤️ Atmosphere — Modern Weather Application

A sleek, responsive desktop weather application built with Python and CustomTkinter. It provides real-time global weather conditions, accurate local timezone data, dynamic condition icons, and precise location lookup via OpenStreetMap reverse-geocoding.

---

## ✨ Features

- **Global Coverage:** Search for any city, town, or country worldwide.
- **Real-Time Data:** Instant updates on Temperature, Wind Speed, Humidity, Pressure, and "Feels Like" metrics.
- **Dynamic Icons:** Condition-specific weather icons loaded live from OpenWeatherMap.
- **Responsive Threading:** Network requests run in background threads to keep the UI smooth and responsive.
- **Dark Mode UI:** Modern, slate-themed interface with rounded card layouts.

---

## 🛠️ Built With

- [Python 3.x](https://www.python.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern GUI Library
- [OpenWeatherMap API](https://openweathermap.org/api) — Weather Data
- [GeoPy](https://geopy.readthedocs.io/) & [Nominatim](https://nominatim.org/) — Geocoding Engine
- [TimezoneFinder](https://github.com/gboeing/timezonefinder) & [pytz](https://pythonhosted.org/pytz/) — Local Time Processing
- [Pillow (PIL)](https://python-pillow.org/) — Image Processing

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8 or higher installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SHUBHAMM1111/weather-application-py.git](https://github.com/SHUBHAMM1111/weather-application-py.git)
   cd weather-application-py

 Install required dependencies:
 py -m pip install customtkinter pillow geopy timezonefinder requests pytz

 Run the application:
 python main.py

 🔑 Environment Variables & API Keys
To use your own OpenWeatherMap API key, update the api_key variable inside the script:
api_key = "YOUR_OPENWEATHERMAP_API_KEY"

