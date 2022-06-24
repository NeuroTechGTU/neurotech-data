import json
import requests

URL = 'https://neurotech-model.azurewebsites.net/api/HttpTrigger1?code=H_b77QaGW6eeF8UvewZONUSBFuBUfZ1R9yGftNQKHKXEAzFuGLjiqQ=='

data = [0, 23, 0.0, 24, 57, 10, 28, 55, 10, 37, 57, 10, 32, 57, 10]

body = {'data':data, 'model_num': 0}

res = requests.post(URL,json=body)

print(res.content)