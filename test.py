import requests

url = 'http://localhost:8000/api/v1/auth/volunteer/registration/'  # Replace with the actual URL where your API is located

data = {
    'email': 'abc@gmail.com',
    'password': 'abc@123',  # Replace with a valid password that meets the minimum length requirement
    'full_name': 'abc',
}

# Replace 'path-to-your-image-file.jpg' with the actual path to the image file you want to upload
files = {'image': open('media/agile.jfif', 'rb')}

response = requests.post(url, data=data, files=files)

print(response.json())
