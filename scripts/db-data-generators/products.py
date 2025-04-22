import random

# Sample product names and corresponding descriptions
product_data = [
    ("Wireless Mouse", "Ergonomic wireless mouse with adjustable DPI and silent clicks."),
    ("Bluetooth Speaker", "Compact Bluetooth speaker with 360-degree sound and waterproof design."),
    ("LED Monitor", "27-inch full HD LED monitor with ultra-thin bezels and vivid colors."),
    ("Mechanical Keyboard", "Mechanical keyboard with RGB lighting and programmable keys."),
    ("USB-C Charger", "Fast-charging USB-C wall adapter compatible with laptops and smartphones."),
    ("Noise Cancelling Headphones", "Wireless headphones with hybrid noise cancellation and long battery life."),
    ("Smart Watch", "Smartwatch with AMOLED display, GPS, and health tracking features."),
    ("External SSD", "Portable 1TB SSD with shock-resistant casing and USB-C support."),
    ("Webcam", "1080p HD webcam with wide-angle lens and auto light correction."),
    ("Laptop Stand", "Foldable and adjustable laptop stand with cooling design."),
    ("Graphic Tablet", "Drawing tablet with 8192 pressure sensitivity levels and USB connection."),
    ("Smart LED Bulb", "Smart bulb with voice control and customizable color scenes."),
    ("Portable Projector", "Portable projector with 720p resolution and HDMI input."),
    ("Wireless Earbuds", "True wireless earbuds with noise isolation and sweat resistance."),
    ("Gaming Chair", "Adjustable gaming chair with headrest and lumbar pillows."),
    ("Action Camera", "4K action camera with waterproof housing and WiFi connectivity."),
    ("Fitness Tracker", "Fitness band with heart rate monitor and step tracking."),
    ("Smart Plug", "Compact smart plug with timer and energy monitoring features."),
    ("Digital Photo Frame", "WiFi-enabled photo frame with cloud storage and slideshow mode."),
    ("Standing Desk", "Electric height adjustable standing desk with memory presets."),
    ("Smart Thermostat", "WiFi-enabled thermostat with remote app control and scheduling."),
    ("Robot Vacuum", "Smart robot vacuum with mapping and voice assistant compatibility."),
    ("Wireless Router", "Dual-band wireless router with MU-MIMO and parental controls."),
    ("Streaming Stick", "HD streaming stick with voice remote and multiple app support."),
    ("USB Hub", "Multi-port USB hub with fast charging and data transfer capabilities."),
    ("Laptop Backpack", "Water-resistant laptop backpack with multiple compartments and USB port."),
    ("Bluetooth Keyboard", "Slim Bluetooth keyboard with rechargeable battery and multi-device pairing."),
    ("Smart Doorbell", "Video doorbell with two-way audio and motion detection."),
    ("E-reader", "Lightweight e-reader with adjustable brightness and glare-free screen."),
    ("Webcam Cover", "Privacy webcam cover with slide design for laptops and tablets."),
    ("Portable Charger", "10,000mAh portable power bank with dual USB outputs."),
    ("Desk Lamp", "LED desk lamp with dimmable brightness and USB charging port."),
    ("VR Headset", "Virtual reality headset with immersive 3D experience and adjustable lenses."),
    ("3D Printer", "Compact 3D printer with easy bed leveling and filament detection."),
    ("Air Purifier", "HEPA air purifier with quiet operation and smart sensor."),
    ("Bluetooth Tracker", "Item tracker with app alerts and replaceable battery."),
    ("USB Microphone", "Condenser microphone with cardioid pickup pattern and stand."),
    ("Streaming Webcam", "HD webcam with ring light and tripod mount for streaming."),
    ("Electric Scooter", "Foldable electric scooter with LED display and long-range battery."),
    ("Smart Lock", "Keyless smart lock with app access and auto-lock feature."),
    ("WiFi Extender", "Signal booster with dual-band support and easy setup."),
    ("Laptop Cooling Pad", "Cooling pad with adjustable fans and USB connectivity."),
    ("Portable Monitor", "USB-C portable monitor with full HD resolution and slim design."),
    ("Wireless Presenter", "Presentation remote with laser pointer and slideshow control."),
    ("Digital Alarm Clock", "LED alarm clock with USB charging and snooze function."),
    ("Smart Light Strip", "Color-changing light strip with music sync and app control."),
    ("Bluetooth Car Adapter", "FM transmitter with Bluetooth and hands-free calling."),
    ("Desk Organizer", "Multi-functional desk organizer with drawer and pen holder."),
    ("Surge Protector", "Power strip with surge protection and USB charging ports."),
    ("Cable Management Box", "Box for organizing and hiding power strips and cables."),
    ("Keyboard Cover", "Silicone keyboard cover with spill protection and soft touch."),
    ("Monitor Stand", "Ergonomic monitor riser with drawer and phone holder."),
    ("Smart Scale", "Body scale with Bluetooth connectivity and health metrics tracking."),
    ("Label Maker", "Portable label maker with Bluetooth and app customization."),
    ("Smart Remote", "Universal smart remote with customizable scenes and voice control."),
    ("WiFi Camera", "Indoor security camera with night vision and motion alerts."),
    ("Pet Camera", "Interactive pet camera with treat dispenser and two-way audio."),
    ("USB Flash Drive", "64GB USB 3.0 flash drive with swivel design and keychain loop."),
    ("Smartwatch Charger", "Magnetic charger for smartwatches with fast charging support."),
    ("Bluetooth Adapter", "USB Bluetooth adapter with wide compatibility and stable connection."),
    ("Solar Power Bank", "Solar-powered charger with LED flashlight and dual USB ports."),
    ("Phone Tripod", "Flexible phone tripod with remote shutter and universal mount."),
    ("Wireless Charging Pad", "Qi-enabled charging pad with fast charging support."),
    ("LED Strip Connector", "Set of connectors for LED light strip extensions and corners."),
    ("VR Controller", "Wireless controller for VR games with precise tracking."),
    ("Mini Projector Screen", "Foldable projector screen with stand for portable use."),
    ("Gaming Mouse Pad", "Extended mouse pad with anti-slip base and stitched edges."),
    ("USB Desk Fan", "Compact USB fan with adjustable angle and quiet operation."),
    ("Phone Stand", "Adjustable phone stand with anti-slip base and cable slot."),
    ("Tablet Stand", "Aluminum tablet holder with multi-angle adjustment and cable management."),
    ("Memory Card Reader", "Multi-card reader with USB 3.0 and SD/TF support."),
    ("Bluetooth Headset", "Mono Bluetooth headset with noise reduction and long battery life."),
    ("Power Strip Tower", "Vertical power strip with rotating outlets and surge protection."),
    ("HDMI Switch", "3-port HDMI switch with remote and 4K support."),
    ("Screen Protector Kit", "Tempered glass screen protectors with installation tools."),
    ("Ergonomic Mouse Pad", "Mouse pad with wrist support and smooth surface."),
    ("Wireless Charging Stand", "Stand for wireless charging with vertical and horizontal support."),
    ("Cable Clips", "Adhesive cable clips for organizing charging cords and wires."),
    ("Monitor Light Bar", "LED light bar for monitor top with adjustable brightness."),
    ("USB Docking Station", "Docking station with multiple USB ports, HDMI, and Ethernet."),
    ("Digital Notepad", "Electronic notepad for digital writing and note saving."),
    ("Gaming Controller", "Wireless gaming controller with vibration and customizable buttons."),
    ("Foldable Bluetooth Keyboard", "Portable keyboard with tri-fold design and Bluetooth connectivity."),
    ("Smartphone Gimbal", "3-axis gimbal stabilizer for smooth smartphone video recording."),
    ("Portable Hard Drive", "2TB external hard drive with USB 3.0 and rugged design."),
    ("WiFi Smart Switch", "Smart switch with remote app control and energy monitoring."),
    ("Electric Air Duster", "Cordless air duster for cleaning electronics and keyboards."),
    ("Privacy Screen Filter", "Laptop screen filter for privacy and glare reduction."),
    ("Gaming Headset", "Over-ear headset with surround sound and noise-canceling mic."),
    ("USB Reading Light", "Flexible USB LED light for reading and keyboard illumination."),
    ("HDMI Cable", "High-speed HDMI cable with 4K support and braided design."),
    ("Bluetooth Transmitter", "Audio transmitter for TVs and headphones with aptX support."),
    ("Smartphone Lens Kit", "Clip-on lens set with wide-angle, macro, and fisheye lenses."),
    ("Laptop Privacy Filter", "Privacy filter for laptops with easy installation and screen clarity."),
    ("Portable Whiteboard", "Dry erase whiteboard for desks and portable meetings."),
    ("USB LED Strip", "USB-powered LED light strip for ambient lighting and decoration."),
    ("Digital Timer", "Compact digital timer with magnetic back and loud alarm."),
    ("Wireless Barcode Scanner", "Handheld barcode scanner with Bluetooth and USB support."),
    ("Smart IR Blaster", "Universal IR blaster to control appliances via smartphone app."),
    ("Laptop Sleeve", "Protective laptop sleeve with padded interior and zipper closure.")
]

# Generate product list with ID, name, description, and price
products = [
    {
        "id": i + 1,
        "name": name,
        "description": description,
        "price": random.randint(15, 230),
    }
    for i, (name, description) in enumerate(product_data)
]

# Generate SQL INSERT statements
sql_statements = [
    f'INSERT INTO Product (id, name, description, price) VALUES ({p["id"]}, "{p["name"]}", "{p["description"]}", {p["price"]});'
    for p in products
]

# Print product list
print("Generated product data:")
print(products)

# Print SQL statements
print("\nGenerated SQL statements:")
print("\n".join(sql_statements))
