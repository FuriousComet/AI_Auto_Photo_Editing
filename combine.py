from PIL import Image, ImageTk
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def create_family_photo():
    # Load the background image
    background_image_path = background_image_path_var.get()
    background_image = Image.open(background_image_path)

    # Get the individual photo paths
    individual_photos_paths = individual_photos_paths_var.get().split(",")

    # Get the spacing, x_offset, y_offset, and image size values
    spacing = spacing_var.get()
    x_offset = x_offset_var.get()
    y_offset = y_offset_var.get()
    image_width = image_width_var.get()
    image_height = image_height_var.get()

    # Create a new blank image with the same size as the background
    family_photo = Image.new("RGBA", background_image.size)

    for photo_path in individual_photos_paths:
        # Load the individual photo with removed background
        individual_photo = Image.open(photo_path)

        # Resize the individual photo if necessary
        individual_photo = individual_photo.resize((image_width, image_height))

        # Calculate the y-offset to center the individual photo vertically
        y_offset = (background_image.height - individual_photo.height) // 2

        # Position the individual photo on the family photo
        # Adjust the coordinates based on the calculated offsets
        family_photo.paste(individual_photo, (x_offset, y_offset), mask=individual_photo)

        # Update the x-offset for the next photo
        x_offset += spacing

    # Blend the images
    final_photo = Image.alpha_composite(background_image.convert("RGBA"), family_photo)

    # Save the resulting family photo as PNG
    output_path = output_path_var.get()
    final_photo.save(output_path, "PNG")
    result_image = cv2.imread(output_path)
    cv2.imshow('Combined Image', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def browse_background_image():
    filename = filedialog.askopenfilename(title="Select Background Image")
    background_image_path_var.set(filename)

def browse_individual_photos():
    filenames = filedialog.askopenfilenames(title="Select Individual Photos")
    individual_photos_paths_var.set(",".join(filenames))

def update_spacing_label(value):
    spacing_label.config(text="Spacing: " + str(value))

def update_x_offset_label(value):
    x_offset_label.config(text="X Offset: " + str(value))

def update_y_offset_label(value):
    y_offset_label.config(text="Y Offset: " + str(value))

def update_image_width_label(value):
    image_width_label.config(text="Image Width: " + str(value))

def update_image_height_label(value):
    image_height_label.config(text="Image Height: " + str(value))

# Create the main window
window = tk.Tk()
window.title("Family Photo Creator")

# Create and position the control buttons and labels
background_image_label = ttk.Label(window, text="Background Image:")
background_image_label.grid(row=0, column=0)
background_image_path_var = tk.StringVar()
background_image_entry = ttk.Entry(window, textvariable=background_image_path_var, width=50)
background_image_entry.grid(row=0, column=1)
background_image_button = ttk.Button(window, text="Browse", command=browse_background_image)
background_image_button.grid(row=0, column=2)

individual_photos_label = ttk.Label(window, text="Individual Photos:")
individual_photos_label.grid(row=1, column=0)
individual_photos_paths_var = tk.StringVar()
individual_photos_entry = ttk.Entry(window, textvariable=individual_photos_paths_var, width=50)
individual_photos_entry.grid(row=1, column=1)
individual_photos_button = ttk.Button(window, text="Browse", command=browse_individual_photos)
individual_photos_button.grid(row=1, column=2)

spacing_label = ttk.Label(window, text="Spacing:")
spacing_label.grid(row=2, column=0)
spacing_var = tk.IntVar(value=240)
spacing_scale = ttk.Scale(window, variable=spacing_var, from_=0, to=500, orient=tk.HORIZONTAL, command=update_spacing_label)
spacing_scale.grid(row=2, column=1)

x_offset_label = ttk.Label(window, text="X Offset:")
x_offset_label.grid(row=3, column=0)
x_offset_var = tk.IntVar(value=0)
x_offset_scale = ttk.Scale(window, variable=x_offset_var, from_=0, to=500, orient=tk.HORIZONTAL, command=update_x_offset_label)
x_offset_scale.grid(row=3, column=1)

y_offset_label = ttk.Label(window, text="Y Offset:")
y_offset_label.grid(row=4, column=0)
y_offset_var = tk.IntVar(value=0)
y_offset_scale = ttk.Scale(window, variable=y_offset_var, from_=0, to=500, orient=tk.HORIZONTAL, command=update_y_offset_label)
y_offset_scale.grid(row=4, column=1)

image_width_label = ttk.Label(window, text="Image Width:")
image_width_label.grid(row=5, column=0)
image_width_var = tk.IntVar(value=400)
image_width_scale = ttk.Scale(window, variable=image_width_var, from_=100, to=1000, orient=tk.HORIZONTAL, command=update_image_width_label)
image_width_scale.grid(row=5, column=1)

image_height_label = ttk.Label(window, text="Image Height:")
image_height_label.grid(row=6, column=0)
image_height_var = tk.IntVar(value=550)
image_height_scale = ttk.Scale(window, variable=image_height_var, from_=100, to=1000, orient=tk.HORIZONTAL, command=update_image_height_label)
image_height_scale.grid(row=6, column=1)

output_path_label = ttk.Label(window, text="Output Path:")
output_path_label.grid(row=7, column=0)
output_path_var = tk.StringVar()
output_path_entry = ttk.Entry(window, textvariable=output_path_var, width=50)
output_path_entry.grid(row=7, column=1)

create_button = ttk.Button(window, text="Create Family Photo", command=create_family_photo)
create_button.grid(row=8, column=0, columnspan=3)

# Start the main event loop
window.mainloop()