import requests
import json
from api_config import API_KEY, API_KEY2
# import os 

# dir_path = os.path.dirname(os.path.realpath(__file__))

def get_kcl(food_name):
    base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    param = {
        'query': food_name,
        'api_key': API_KEY
    }
    data = requests.get(base_url, params=param)
    if data.status_code != 200:
        print(f"Error: {data.status_code} - {data.reason}")
        return None
    data = json.loads(data.text)
    # with open('nutritious_food.json', 'a+') as file:
    #      json.dump(data, file, indent = 2, sort_keys=True)
    if 'foods' in data and len(data['foods']) > 0:
        nutrients = data['foods'][0].get('foodNutrients', [])
        for nutrient in nutrients:
            if nutrient.get('unitName') == 'KCAL':
                kcl = nutrient.get('value', 0)
                return kcl

def get_burnt_kcl(sport_name):
    base_url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}'.format(sport_name)
    data = requests.get(base_url, headers={'X-Api-Key':API_KEY2}) 
    if data.status_code != 200:
        print(f"Error: {data.status_code} - {data.reason}")
        return None
    data = json.loads(data.text)
    if len(data) > 0:
        for i in data:
            if i['total_calories']:
                kcl_burnt = i['total_calories']
                return kcl_burnt


if __name__=='__main__':
    get_burnt_kcl('skiing')