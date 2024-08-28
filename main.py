import requests
import json

url = "https://api.metalpriceapi.com/v1/latest"

# Define the query parameters, including the API key, base currency, and target currencies
params = {
    'api_key': '075d3c357273e653671d9760ad42f7fe',
    'base': 'USD',
    'currencies': 'XAG,XAU,XPD,XPT'
}

# Make the GET request to the API with the parameters
output_response = requests.get(url, params=params)

if output_response.status_code == 200:                   

    output_data = output_response.json()  
    

    formatted_json = json.dumps(output_data, indent=4)

                        
    lines = formatted_json.split('\n')                   

    file_add = './api_data.json'    
    with open(file_add,'w') as file:                    
        file.write( formatted_json)                      
    print('Your data is save successfully!')
else:
    print("API request failed with status code:", output_response.status_code)
