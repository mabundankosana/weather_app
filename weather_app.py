import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Function to fetch weather data
def get_weather_data(city):
    api_key = "64a48fd8b07e6d945ff444912da864f5"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Unable to fetch weather data: {e}")
        return None

# Function to update the UI with weather data
def display_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return

    weather_data = get_weather_data(city)
    if weather_data and "main" in weather_data:
        city_name = weather_data["name"]
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"].capitalize()
        icon_code = weather_data["weather"][0]["icon"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        # Update labels
        city_label.config(text=f"Weather in {city_name}")
        temp_label.config(text=f"Temperature: {temperature}°C")
        desc_label.config(text=f"Description: {description}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")

        # Update weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url, stream=True)
        if icon_response.status_code == 200:
            img_data = icon_response.content
            with open("weather_icon.png", "wb") as img_file:
                img_file.write(img_data)
            weather_icon = ImageTk.PhotoImage(Image.open("weather_icon.png"))
            icon_label.config(image=weather_icon)
            icon_label.image = weather_icon
    else:
        messagebox.showerror("Error", "City not found or invalid response.")

# GUI Setup
root = tk.Tk()
root.title("Stylish Weather App")
root.geometry("400x500")
root.resizable(False, False)
root.config(bg="#87CEEB")

# City input
city_label_entry = tk.Label(root, text="Enter city name:", font=("Helvetica", 12), bg="#87CEEB", fg="#FFFFFF")
city_label_entry.pack(pady=10)
city_entry = tk.Entry(root, font=("Helvetica", 14), width=20)
city_entry.pack(pady=5)
search_button = tk.Button(root, text="Get Weather", command=display_weather, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
search_button.pack(pady=10)

# Weather details
icon_label = tk.Label(root, bg="#87CEEB")
icon_label.pack(pady=10)
city_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), bg="#87CEEB", fg="#FFFFFF")
city_label.pack(pady=5)
temp_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#87CEEB", fg="#FFFFFF")
temp_label.pack(pady=5)
desc_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#87CEEB", fg="#FFFFFF")
desc_label.pack(pady=5)
humidity_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#87CEEB", fg="#FFFFFF")
humidity_label.pack(pady=5)
wind_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#87CEEB", fg="#FFFFFF")
wind_label.pack(pady=5)

# Footer
footer_label = tk.Label(root, text="Powered by OpenWeatherMap", font=("Helvetica", 10), bg="#87CEEB", fg="#FFFFFF")
footer_label.pack(pady=20)

# Run the GUI
root.mainloop()

# Cleanup: Remove the downloaded icon
if os.path.exists("weather_icon.png"):
    os.remove("weather_icon.png")
