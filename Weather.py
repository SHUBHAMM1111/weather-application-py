import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image
from io import BytesIO
import threading

# Global Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PremiumWeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Atmosphere — Global Weather")
        self.geometry("880x520")
        self.resizable(False, False)
        self.configure(fg_color="#0F172A")  # Deep Slate background

        # Header Search Frame
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(pady=25, padx=30, fill="x")

        self.textfield = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search any city or country (e.g., London, Tokyo, Cairo)...",
            width=650,
            height=48,
            corner_radius=24,
            font=("Inter", 15),
            fg_color="#1E293B",
            text_color="#F8FAFC",
            border_color="#334155",
            border_width=1
        )
        self.textfield.pack(side="left", padx=(0, 15), expand=True, fill="x")
        self.textfield.bind("<Return>", lambda event: self.start_weather_thread())
        self.textfield.focus()

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=140,
            height=48,
            corner_radius=24,
            font=("Inter", 14, "bold"),
            fg_color="#38BDF8",
            hover_color="#0284C7",
            text_color="#0F172A",
            command=self.start_weather_thread
        )
        self.search_btn.pack(side="right")

        # Main Display Card
        self.main_card = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=20, border_color="#334155", border_width=1)
        self.main_card.pack(padx=30, pady=(0, 20), fill="x")

        # Left Info Sub-Frame
        self.info_left = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.info_left.pack(side="left", padx=30, pady=25)

        self.city_label = ctk.CTkLabel(self.info_left, text="Search a Location", font=("Inter", 26, "bold"), text_color="#F8FAFC")
        self.city_label.pack(anchor="w")

        self.time_label = ctk.CTkLabel(self.info_left, text="--:-- --", font=("Inter", 16), text_color="#94A3B8")
        self.time_label.pack(anchor="w", pady=(2, 0))

        self.desc_label = ctk.CTkLabel(self.info_left, text="Enter a city to get weather metrics", font=("Inter", 14), text_color="#38BDF8")
        self.desc_label.pack(anchor="w", pady=(15, 0))

        # Right Info Sub-Frame (Icon + Temperature)
        self.info_right = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.info_right.pack(side="right", padx=30, pady=25)

        self.icon_label = ctk.CTkLabel(self.info_right, text="", width=80, height=80)
        self.icon_label.pack(side="left", padx=(0, 15))

        self.temp_label = ctk.CTkLabel(self.info_right, text="--°C", font=("Inter", 54, "bold"), text_color="#F8FAFC")
        self.temp_label.pack(side="right")

        # Metrics Grid (4 Stat Boxes)
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.pack(padx=30, pady=5, fill="x")
        self.metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")

        self.card_wind = self.create_metric_card(self.metrics_frame, 0, "WIND SPEED", "-- m/s")
        self.card_humidity = self.create_metric_card(self.metrics_frame, 1, "HUMIDITY", "-- %")
        self.card_feels = self.create_metric_card(self.metrics_frame, 2, "FEELS LIKE", "--°C")
        self.card_pressure = self.create_metric_card(self.metrics_frame, 3, "PRESSURE", "-- hPa")

    def create_metric_card(self, parent, column, title, default_val):
        """Helper to construct uniform metric cards"""
        card = ctk.CTkFrame(parent, fg_color="#1E293B", corner_radius=16, border_color="#334155", border_width=1)
        card.grid(row=0, column=column, padx=8, pady=0, sticky="ew")

        lbl_title = ctk.CTkLabel(card, text=title, font=("Inter", 11, "bold"), text_color="#64748B")
        lbl_title.pack(pady=(15, 2))

        lbl_val = ctk.CTkLabel(card, text=default_val, font=("Inter", 18, "bold"), text_color="#F8FAFC")
        lbl_val.pack(pady=(0, 15))

        return lbl_val

    def start_weather_thread(self):
        """Thread wrapper to ensure UI remains responsive while fetching network data"""
        city = self.textfield.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return

        self.search_btn.configure(state="disabled", text="Searching...")
        threading.Thread(target=self.fetch_weather_data, args=(city,), daemon=True).start()

    def fetch_weather_data(self, city):
        try:
            # 1. Look up location coordinates worldwide via Nominatim
            geolocator = Nominatim(user_agent="premium_weather_app")
            location = geolocator.geocode(city, addressdetails=True, language="en")

            if not location:
                self.show_error(f"Location '{city}' could not be found.")
                return

            # 2. Parse detailed location information (City/Town/Village + Country)
            raw_address = location.raw.get('address', {})
            detected_city = (
                raw_address.get('city') or 
                raw_address.get('town') or 
                raw_address.get('village') or 
                raw_address.get('municipality') or 
                raw_address.get('county') or 
                location.address.split(',')[0]
            )
            country = raw_address.get('country', '')
            state = raw_address.get('state', '')

            location_parts = [p for p in [detected_city, state, country] if p]
            display_location = ", ".join(location_parts[:2]) if len(location_parts) > 1 else location_parts[0]

            # 3. Calculate local time by coordinates
            obj = TimezoneFinder()
            tz_str = obj.timezone_at(lng=location.longitude, lat=location.latitude)
            
            time_formatted = "--:--"
            if tz_str:
                home = pytz.timezone(tz_str)
                local_time = datetime.now(home)
                time_formatted = local_time.strftime("%I:%M %p")

            # 4. Fetch weather by exact lat/lon coordinates to ensure accuracy
            api_key = "d0e233dc5fae0770c88e3df9f860cd2d"
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api_key}"
            res = requests.get(url).json()

            if str(res.get("cod")) != "200":
                self.show_error(res.get("message", "Error fetching weather data.").capitalize())
                return

            # Parse Weather Data
            condition = res['weather'][0]['main']
            description = res['weather'][0]['description'].capitalize()
            icon_code = res['weather'][0]['icon']
            temp = int(res['main']['temp'] - 273.15)
            feels_like = int(res['main']['feels_like'] - 273.15)
            pressure = res['main']['pressure']
            humidity = res['main']['humidity']
            wind = res['wind']['speed']

            # 5. Fetch Weather Icon Image
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            img_res = requests.get(icon_url)
            img_data = Image.open(BytesIO(img_res.content))
            ctk_icon = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(80, 80))

            # 6. Safely update GUI on the main thread
            self.after(0, self.update_ui, display_location, time_formatted, condition, description, 
                       temp, feels_like, pressure, humidity, wind, ctk_icon)

        except Exception as e:
            self.show_error(f"Unexpected error: {str(e)}")

    def update_ui(self, city_name, time_str, condition, description, temp, feels_like, pressure, humidity, wind, icon_img):
        self.city_label.configure(text=city_name)
        self.time_label.configure(text=f"Local Time: {time_str}")
        self.desc_label.configure(text=f"{condition} • {description}")
        self.temp_label.configure(text=f"{temp}°C")

        self.card_wind.configure(text=f"{wind} m/s")
        self.card_humidity.configure(text=f"{humidity}%")
        self.card_feels.configure(text=f"{feels_like}°C")
        self.card_pressure.configure(text=f"{pressure} hPa")

        self.icon_label.configure(image=icon_img)

        # Reset button state
        self.search_btn.configure(state="normal", text="Search")

    def show_error(self, message):
        self.after(0, lambda: messagebox.showerror("Error", message))
        self.after(0, lambda: self.search_btn.configure(state="normal", text="Search"))


if __name__ == "__main__":
    app = PremiumWeatherApp()
    app.mainloop()