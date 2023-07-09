import requests
import os

def remove_background(image_path):
    your_api_key = 'k9FXgDpDP57nhSe3eXyVks8o'  # Paste your API key here

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
        

# if __name__ == '__main__':
#     image_path = input("Enter the path to the input image: ")
#     output_path = remove_background(image_path)
#     print("Output image saved as", output_path)