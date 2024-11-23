import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import requests

# ORS API Key
API_KEY = '5b3ce3597851110001cf6248fb737de2190642038aaa41bd0441db21'  # Replace with your OpenRouteService API key

# Available locations
locations = [
    "Bhadradri Kothagudem", "Hyderabad", "Adilabad", "Jagtial", "Warangal",
    "Mulugu", "Khammam", "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad",
    "Peddapalli", "Rajanna Sircilla", "Rangareddy", "Suryapet", "Vikarabad"
]

# Route-to-bus mapping
route_to_bus = {
    ("Bhadradri Kothagudem", "Hyderabad"): 150,
    ("Hyderabad", "Bhadradri Kothagudem"): 123,
    ("Bhadradri Kothagudem", "Adilabad"): 170,
    ("Adilabad", "Bhadradri Kothagudem"): 120,
    ("Bhadradri Kothagudem", "Jagtial"): 98,
    ("Jagtial", "Bhadradri Kothagudem"): 260,
    ("Bhadradri Kothagudem", "Warangal"): 195,
    ("Warangal", "Bhadradri Kothagudem"): 150,
    ("Bhadradri Kothagudem", "Mulugu"): 194,
    ("Mulugu", "Bhadradri Kothagudem"): 180,
    ("Bhadradri Kothagudem", "Khammam"): 126,
    ("Khammam", "Bhadradri Kothagudem"): 220,
    ("Bhadradri Kothagudem", "Nalgonda"): 119,
    ("Nalgonda", "Bhadradri Kothagudem"): 300,
    ("Bhadradri Kothagudem", "Narayanpet"): 118,
    ("Narayanpet", "Bhadradri Kothagudem"): 200,
    ("Bhadradri Kothagudem", "Nirmal"): 231,
    ("Nirmal", "Bhadradri Kothagudem"): 240,
    ("Bhadradri Kothagudem", "Nizamabad"): 76,
    ("Nizamabad", "Bhadradri Kothagudem"): 210,
    ("Bhadradri Kothagudem", "Peddapalli"): 68,
    ("Peddapalli", "Bhadradri Kothagudem"): 230,
    ("Bhadradri Kothagudem", "Rajanna Sircilla"): 148,
    ("Rajanna Sircilla", "Bhadradri Kothagudem"): 310,
    ("Bhadradri Kothagudem", "Rangareddy"): 143,
    ("Rangareddy", "Bhadradri Kothagudem"): 230,
    ("Bhadradri Kothagudem", "Suryapet"): 154,
    ("Suryapet", "Bhadradri Kothagudem"): 280,
    ("Bhadradri Kothagudem", "Vikarabad"): 213,
    ("Vikarabad", "Bhadradri Kothagudem"): 180,
    
    ("Hyderabad", "Adilabad"): 162,
    ("Adilabad", "Hyderabad"): 160,
    ("Hyderabad", "Jagtial"): 203,
    ("Jagtial", "Hyderabad"): 220,
    ("Hyderabad", "Warangal"): 132,
    ("Warangal", "Hyderabad"): 340,
    ("Hyderabad", "Mulugu"): 96,
    ("Mulugu", "Hyderabad"): 290,
    ("Hyderabad", "Khammam"): 224,
    ("Khammam", "Hyderabad"): 280,
    ("Hyderabad", "Nalgonda"): 198,
    ("Nalgonda", "Hyderabad"): 200,
    ("Hyderabad", "Narayanpet"): 197,
    ("Narayanpet", "Hyderabad"): 190,
    ("Hyderabad", "Nirmal"): 136,
    ("Nirmal", "Hyderabad"): 330,
    ("Hyderabad", "Nizamabad"): 298,
    ("Nizamabad", "Hyderabad"): 290,
    ("Hyderabad", "Peddapalli"): 214,
    ("Peddapalli", "Hyderabad"): 210,
    ("Hyderabad", "Rajanna Sircilla"): 228,
    ("Rajanna Sircilla", "Hyderabad"): 275,
    ("Hyderabad", "Rangareddy"): 186,
    ("Rangareddy", "Hyderabad"): 180,
    ("Hyderabad", "Suryapet"): 177,
    ("Suryapet", "Hyderabad"): 170,
    ("Hyderabad", "Vikarabad"): 254,
    ("Vikarabad", "Hyderabad"): 250,

    ("Adilabad", "Jagtial"): 214,
    ("Jagtial", "Adilabad"): 210,
    ("Adilabad", "Warangal"): 123,
    ("Warangal", "Adilabad"): 310,
    ("Adilabad", "Mulugu"): 227,
    ("Mulugu", "Adilabad"): 200,
    ("Adilabad", "Khammam"): 246,
    ("Khammam", "Adilabad"): 240,
    ("Adilabad", "Nalgonda"): 183,
    ("Nalgonda", "Adilabad"): 180,
    ("Adilabad", "Narayanpet"): 179,
    ("Narayanpet", "Adilabad"): 250,
    ("Adilabad", "Nirmal"): 211,
    ("Nirmal", "Adilabad"): 210,
    ("Adilabad", "Nizamabad"): 231,
    ("Nizamabad", "Adilabad"): 310,
    ("Adilabad", "Peddapalli"): 193,
    ("Peddapalli", "Adilabad"): 198,
    ("Adilabad", "Rajanna Sircilla"): 212,
    ("Rajanna Sircilla", "Adilabad"): 240,
    ("Adilabad", "Rangareddy"): 189,
    ("Rangareddy", "Adilabad"): 180,
    ("Adilabad", "Suryapet"): 229,
    ("Suryapet", "Adilabad"): 220,
    ("Adilabad", "Vikarabad"): 269,
    ("Vikarabad", "Adilabad"): 260,
    ("Nalgonda","Suryapet") :192 ,
    ("Suryapet","Nalgonda") :90 ,
   
    ("Jagtial", "Warangal"): 107,
    ("Warangal", "Jagtial"): 310,
    ("Jagtial", "Mulugu"): 237,
    ("Mulugu", "Jagtial"): 245,
    ("Jagtial", "Khammam"): 191,
    ("Khammam", "Jagtial"): 190,
    ("Jagtial", "Nalgonda"): 209,
    ("Nalgonda", "Jagtial"): 200,
    ("Jagtial", "Narayanpet"): 204,
    ("Narayanpet", "Jagtial"): 285,
    ("Jagtial", "Nirmal"): 203,
    ("Nirmal", "Jagtial"): 205,
    ("Jagtial", "Nizamabad"): 186,
    ("Nizamabad", "Jagtial"): 180,
    ("Jagtial", "Peddapalli"): 172,
    ("Peddapalli", "Jagtial"): 170,
    ("Jagtial", "Rajanna Sircilla"): 262,
    ("Rajanna Sircilla", "Jagtial"): 260,
    ("Jagtial", "Rangareddy"): 252,
    ("Rangareddy", "Jagtial"): 250,
    ("Jagtial", "Suryapet"): 203,
    ("Suryapet", "Jagtial"): 270,
    ("Jagtial", "Vikarabad"): 219,
    ("Vikarabad", "Jagtial"): 210,
}

# Cost per kilometer
cost_per_km = 2

# Function to fetch coordinates using ORS Geocoding API
def get_coordinates(location):
    url = f"https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": API_KEY,
        "text": location
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['features']:
            coordinates = data['features'][0]['geometry']['coordinates']
            return coordinates[1], coordinates[0]  # Return as (latitude, longitude)
        else:
            raise ValueError("No results found for the location.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch coordinates for {location}: {e}")
        return None

# Main GUI setup
root = tk.Tk()
root.title("QR Code Fare Generator with ORS")
root.geometry("800x600")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Background image setup with reduced opacity
try:
    bg_image = Image.open(r"C:\Users\nampa\Downloads\tsrtca.jpg")  # Update with your image path
    bg_image = bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)

    # Reduce opacity by blending with a white overlay (opacity = 150)
    overlay = Image.new("RGBA", bg_image.size, (255, 255, 255, 150))  # Opacity value set to 150
    bg_image = Image.alpha_composite(bg_image.convert("RGBA"), overlay).convert("RGB")

    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

except Exception as e:
    messagebox.showerror("Error", f"Failed to load background image: {e}")
    # Fallback to a solid pastel background if image loading fails
    pastel_bg_color = "#F2F2F2"
    bg_label = tk.Label(root, bg=pastel_bg_color)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Container Frame for alignment with widgets
container = tk.Frame(root, bg="#F2F2F2", bd=2, relief="solid")
container.place(relx=0.5, rely=0.5, anchor="center", width=300, height=500)

# Start and End Point dropdowns
tk.Label(container, text="Select Start Point:", font=("Helvetica", 14, "bold"), bg="#F2F2F2", fg="#333333").pack(pady=(20, 5))
start_var = tk.StringVar(value=locations[0])
start_dropdown = tk.OptionMenu(container, start_var, *locations)
start_dropdown.config(width=20, font=("Helvetica", 14), bg="#A1C4D1", fg="#333333", borderwidth=0)
start_dropdown.pack(pady=5)

tk.Label(container, text="Select End Point:", font=("Helvetica", 14, "bold"), bg="#F2F2F2", fg="#333333").pack(pady=(10, 5))
end_var = tk.StringVar(value=locations[1])
end_dropdown = tk.OptionMenu(container, end_var, *locations)
end_dropdown.config(width=20, font=("Helvetica", 14), bg="#A1C4D1", fg="#333333", borderwidth=0)
end_dropdown.pack(pady=5)

# Number of People dropdown
tk.Label(container, text="Select Number of People:", font=("Helvetica", 14, "bold"), bg="#F2F2F2", fg="#333333").pack(pady=(10, 5))
people_var = tk.IntVar(value=1)
people_dropdown = tk.OptionMenu(container, people_var, *[i for i in range(1, 11)])
people_dropdown.config(width=20, font=("Helvetica", 14), bg="#A1C4D1", fg="#333333", borderwidth=0)
people_dropdown.pack(pady=5)

# Label to display fare
fare_label = tk.Label(container, text="Fare: ", font=("Helvetica", 14, "bold"), bg="#F2F2F2", fg="#333333")
fare_label.pack(pady=10)

# Label to display QR code image
qr_label = tk.Label(container, bg="#F2F2F2")
qr_label.pack(pady=10)

# Function to calculate fare and generate QR code
def generate_qr():
    start = start_var.get()
    end = end_var.get()

    if start == end:
        messagebox.showerror("Error", "Start and End points cannot be the same")
        return

    bus_number = route_to_bus.get((start, end), "No Bus Available")

    coords_start = get_coordinates(start)
    coords_end = get_coordinates(end)

    if not coords_start or not coords_end:
        return

    try:
        # Request distance data from ORS API
        client_url = f"https://api.openrouteservice.org/v2/directions/driving-car"
        payload = {
            "coordinates": [[coords_start[1], coords_start[0]], [coords_end[1], coords_end[0]]],
            "radiuses": [1000, 1000]
        }
        headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

        response = requests.post(client_url, json=payload, headers=headers)
        response.raise_for_status()

        route = response.json()
        distance_km = route['routes'][0]['summary']['distance'] / 1000
        x =(distance_km * cost_per_km)
        fare=(x-(x%5))

        num_people = people_var.get()
        fare=fare*num_people
        fare_label.config(text=f"Fare: ₹{fare}\nBus Number: {bus_number}")

        qr_text = f"From {start} to {end}\nBus: {bus_number}\nFare: ₹{fare}\nDistance: {distance_km:.2f} km\nPeople: {num_people}"
        qr = qrcode.make(qr_text)
        qr_image = qr.resize((150, 150))
        tk_image = ImageTk.PhotoImage(qr_image)

        qr_label.config(image=tk_image)
        qr_label.image = tk_image

        messagebox.showinfo("Fare", f"The fare from {start} to {end} is ₹{fare} on {bus_number} for {distance_km:.2f} km.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate route: {e}")

# Generate QR Code Button
generate_button = tk.Button(container, text="Generate QR Code", command=generate_qr, font=("Helvetica", 14), bg="#A1C4D1", fg="#333333", borderwidth=0)
generate_button.pack(pady=(20, 10), ipadx=20, ipady=10)

root.mainloop()