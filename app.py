from flask import Flask, render_template, request, jsonify
from PIL import Image
import cv2
import os
import requests

app = Flask(__name__)

def remove_background(image_path):
    your_api_key = 'Cpzme64xtg7E8RYPZp4s48Yt'  # Paste your API key here

    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': image_file},
                data={'size': 'auto'},
                headers={'X-Api-Key': your_api_key}
            )
            if response.status_code == requests.codes.ok:
                return response.content
            else:
                print("Error: " + str(response.status_code))
    except requests.exceptions.ConnectionError:
        print("Connection Error")
    except FileNotFoundError:
        print("No valid file found.")

    return None

def arrange_family_photo(background_image_path, individual_photos_paths, spacing, x_offset, y_offset, image_width, image_height):
    # Load the background image
    background_image = Image.open(background_image_path)

    # Create a new blank image with the same size as the background
    family_photo = Image.new("RGBA", background_image.size)

    # Process individual photos
    for photo_path in individual_photos_paths:
        # Load the individual photo
        individual_photo = Image.open(photo_path)

        # Remove the background from the individual photo
        individual_photo_content = remove_background(photo_path)
        if individual_photo_content is not None:
            individual_photo_path = f'./individual_photo_removed.png'
            with open(individual_photo_path, 'wb') as output_image:
                output_image.write(individual_photo_content)
            # Load the individual photo with removed background
            individual_photo = Image.open(individual_photo_path)

        # Resize the individual photo if necessary
        individual_photo = individual_photo.resize((image_width, image_height))

        # Calculate the y-offset to center the individual photo vertically
        y_offset = (background_image.height - individual_photo.height) // 2

        # Position the individual photo on the family photo
        # Adjust the coordinates based on the calculated offsets
        family_photo.paste(individual_photo, (x_offset, y_offset), mask=individual_photo)

        # Update the x-offset for the next photo
        x_offset += spacing

        # Delete the temporary individual photo with removed background
        if individual_photo_content is not None:
            os.remove(individual_photo_path)

    # Blend the images
    final_photo = Image.alpha_composite(background_image.convert("RGBA"), family_photo)

    # Save the resulting family photo as PNG
    output_path = './output/family_photo.png'
    final_photo.save(output_path, "PNG")
    result_image = cv2.imread(output_path)
    cv2.imwrite('./static/family_photo.png', result_image)

    return output_path

@app.route('/', methods=['GET', 'POST'])
def create_family_photo():
    if request.method == 'POST':
        # Get form data
        background_image = request.files['background_image']
        individual_photos = request.files.getlist('individual_photos')
        spacing = int(request.form['spacing'])
        x_offset = int(request.form['x_offset'])
        y_offset = int(request.form['y_offset'])
        image_width = int(request.form['image_width'])
        image_height = int(request.form['image_height'])

        # Save the background image
        background_image_path = './background.jpg'
        background_image.save(background_image_path)

        # Save the individual photos
        individual_photos_paths = []
        for idx, photo in enumerate(individual_photos):
            photo_path = f'./individual_photo_{idx}.jpg'
            photo.save(photo_path)
            individual_photos_paths.append(photo_path)

        output_path = arrange_family_photo(background_image_path, individual_photos_paths, spacing, x_offset, y_offset, image_width, image_height)

        # Delete the temporary files
        os.remove(background_image_path)
        for photo_path in individual_photos_paths:
            os.remove(photo_path)

        return jsonify({'result': output_path})

    # Return the initial version of the family photo when the page is loaded
    output_path = './static/family_photo.png'  # Path to the initial photo
    return render_template('index.html', result=output_path)

@app.route('/update_image', methods=['POST'])
def update_image():
    data = request.get_json()

    background_image_path = './background.jpg'
    individual_photos_paths = []
    for idx, photo in enumerate(data['individual_photos']):
        photo_path = f'./individual_photo_{idx}.jpg'
        with open(photo_path, 'wb') as f:
            f.write(photo.encode('base64'))
        individual_photos_paths.append(photo_path)

    output_path = arrange_family_photo(background_image_path, individual_photos_paths, data['spacing'], data['x_offset'], data['y_offset'], data['image_width'], data['image_height'])

    for photo_path in individual_photos_paths:
        os.remove(photo_path)

    return jsonify({'result': output_path})

if __name__ == '__main__':
    app.run(debug=True)