import api_client as ap
from setup_bdd import link_to_bdd
import json

class myFitPlanner:
    def __init__(self):
        self.basal_metabolism = 0
        self.kcl_absorb = 0
        self. kcl_consume = 0


    def cal_basal_metabolism(self):
        print('Are you a man or a woman ?')
        gender = input('I a am a: ').lower()
        height = float(input('What is your height in cm?:'))
        weight = float(input('What is your weight in kg?:'))
        age = float(input('What is your age in year?:'))
        if gender == 'man':
            self.basal_metabolism = round(88.362 + (13.397*weight)+(4.799*height)-(5.677*age), 2)
            mb = self.basal_metabolism
            print(f'\033[4;36mYour basal metabolism is {mb} calories\033[0m')
            return mb
        elif gender == 'woman':
            self.basal_metabolism = round(447.593 + (9.247*weight) + (3.098 *height)-(4.330*age), 2)
            mb = self.basal_metabolism
            print(f'\033[4;36mYour basal metabolism is {mb} calories\033[0m')
            return mb
        else:
            print('We do not calculate basal metabolisme for tractor')
            return None

    def add_dish(self):
        try:
            connection, cursor = link_to_bdd()
            if connection is None or cursor is None:
                return None, None
            dish = input('\033[1;32mWhat dish do you want to add ?:\033[0m ')
            kcl = ap.get_kcl(dish)
            query = '''insert into meals (meal_name, calories) values (%s, %s)'''
            cursor.execute(query, (dish, kcl))
            print(f'\033[45mYou have absorbed {kcl} Calories.\033[0m')
            print("Your Dish has been add to the database.")
            self.kcl_absorb += kcl
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def add_workout(self):
        try:
            connection, cursor = link_to_bdd()
            if connection is None or cursor is None:
                return None, None
            workout = input('\033[1;32mWhat workout do you want to add ?:\033[0m ')
            kcl_burnt = ap.get_burnt_kcl(workout)
            query = '''insert into workout (workout_name, calories) values (%s, %s)'''
            cursor.execute(query, (workout, kcl_burnt))
            print(f'\033[45mYou have burned {kcl_burnt} Calories\033[0m')
            print('Your workout has been add to the database')
            self.kcl_consume += kcl_burnt
        except Exception as e:
            print(f'ERROR: {e}')
        finally:
            cursor.close()
            connection.close()

    def export_data(self):
        try:
            connection, cursor = link_to_bdd()
            if connection is None or cursor is None:
                return None, None
            query = '''select meal_name, calories from meals where date = current_date'''
            query2 = '''select workout_name, calories from workout where date = current_date'''
            cursor.execute(query)
            data1 = cursor.fetchall()
            cursor.execute(query2)
            data2 = cursor.fetchall()
            data = {
            "meals": [{"meal_name": meal, "calories": cal} for meal, cal in data1],
            "workouts": [{"workout_name": workout, "calories": cal} for workout, cal in data2],
            }
            with open("exported_data.json", "w") as file:
                json.dump(data, file, indent=4)
            print("Data has been exported to 'exported_data.json'.")
        except Exception as e:
            print(f'ERROR: {e}')
        finally:
            cursor.close()
            connection.close()
    
    def display(self):
        try:
            connection, cursor = link_to_bdd()
            if connection is None or cursor is None:
                return None, None
            query = '''select meal_name, calories from meals where date = current_date'''
            query2 = '''select workout_name, calories from workout where date = current_date'''
            cursor.execute(query)
            result = cursor.fetchall()
            print(f'Basal methabolism: {self.basal_metabolism}')
            print('today you have eat: ')
            for meal, kcl in result:
                print(f'- Meal: {meal} - KCL: {kcl}')
            print(f'\033[41;30mYou have absorbed a total of {self.kcl_absorb} calories.\033[0m')
            cursor.execute(query2)
            result2 = cursor.fetchall()
            print('today you have burned: ')
            for workout, kcl in result2:
                print(f'-Workout: {workout} - KCL: {kcl}')
            print(f'\033[41;30mYou have burned a total of {self.kcl_consume} calories.\033[0m')
            if self.basal_metabolism != 0:
                print(f'\033[1;32myou can still absorb {(self.basal_metabolism + self.kcl_consume) - self.kcl_absorb } calories for today.\033[0m')
            else:
                print('You need to calculate your basal metabolism first (c)')
        except Exception as e :
            print(f'ERROR: {e}')
        finally:
            cursor.close()
            connection.close()