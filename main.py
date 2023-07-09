from multiprocessing import Pool
import os
import sys
import requests
import cv2
import numpy as np

def remove_background(image_path):
    your_api_key = 'L8sdeVvsBcxZmfq3aF9bVmKd'  # Paste your API key here

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

def save_output(content, image_path):
    new_file_path="./result/"+"output_"+str(image_path)+".jpg"
    with open(new_file_path, 'wb') as output_file:
        output_file.write(content)
    print("Output image saved as", new_file_path)
    return new_file_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path1> <image_path2> ... <image_pathN>")
        sys.exit(1)

    paths = sys.argv[1:]
    num=0
    for path in paths:
        image = remove_background(path)
        save_output(image, num)
        num=num+1
    print(num) 
    

    