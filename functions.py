import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'goal': self.goal
            }

class User(Person):
    def __init__(self, name, age, weight, height, goal=None):
        super().__init__(name, age)
        self.__weight = weight
        self.__height = height
        self.__goal = goal
        self.__password = None

    def get_weight(self):
        return self.__weight

    def set_weight(self, weight):
        self.__weight = weight

    def get_height(self):
        return self.__height

    def set_height(self, height):
        self.__height = height

    def get_goal(self):
        return self.__goal

    def set_goal(self, goal):
        self.__goal = goal
        
    def set_password(self, password):
        self.__password = password
        
        
class validators:
    @staticmethod
    def number_validator(n, num_type):
        is_number=False
        try:
            n=num_type(n)
            is_number=True
        except:
            print('\nInvalid input! Please enter a numeric value.\n')
        return is_number, n
    
    def user_validator(user, users):
        return user in users
        
    def date_validator(date):
        is_date=False
        try:
            date=pd.to_datetime(date, dayfirst=True)
            is_date=True
        except:
            print('\nInvalid input! Please enter date in correct format\n')
        return is_date, date


class Workout:
    def __init__(self, user, date, duration, calories_burned, type_, description, distance=0, reps=0, sets=0 ):
        self.user = user
        self.date = date
        self.duration = duration
        self.calories_burned = calories_burned
        self.type = type_
        self.distance = distance
        self.reps = reps
        self.sets = sets
        self.description = description

    def details(self):
        return vars(self)
    
    def to_dict(self):
        return {
            'user': self.user,
            'date': self.date,
            'duration': self.duration,
            'calories_burned': self.calories_burned,
            'type': self.type,
            'distance': self.distance,
            'reps': self.reps,
            'sets': self.sets,
            'description': self.description
            }

class StrengthWorkout(Workout):
    def __init__(self, user, date, duration, calories_burned, description, reps, sets):
        super().__init__(user, date, duration, calories_burned, type_='strength', reps=reps, sets=sets, description=description)

class CardioWorkout(Workout):
    def __init__(self, user, date, duration, calories_burned, description):
        super().__init__(user, date, duration, calories_burned, type_='cardio', description=description)

class RunWorkout(Workout):
    def __init__(self, user, date, duration, calories_burned, description, distance):
        super().__init__(user, date, duration, calories_burned, type_='run', distance=distance, description=description)



class FitnessTracker:
    def __init__(self):
        self.users = {}
        self.workouts = []
        self.df_workouts=pd.DataFrame(self.workouts)
        self.df_users=pd.DataFrame(self.users).T
        
        
    def authenticate_user(self, username, password):
        if validators.user_validator(username, self.users):
            user = self.users[username]
            if user.get_password() == password:
                return True
        return False    
    
    #Generating unique username for each person
    def unique_username(self, name):
        while True:
            #Creating name+ random 4-digit number combination as username
            username=name+''.join(random.choice('0123456789') for _ in range(4))
            #Makes sure each username is unique
            if username in self.users:
                continue
            else:
                break
        return username
    
    #Adding user info in users dict
    def create_user(self,  name, age, weight, height):
        self.username=self.unique_username(name)
        new_user=User(name, age, weight, height)
        while True:     
            password=input('Set a password for the new user: ')
            if len(password)<8:
                print('\nPassword length is less than 8.')
            else:
                break
        new_user.set_password(password)    
        self.users[self.username] = new_user.to_dict()
        print(f"\nUser {self.username} created successfully.\n")
        self.df_users=pd.DataFrame(self.users).T
        return self.users
    
    #
    def edit_user(self, username, **kwargs):
        for user in self.users:
            if user==username:
                for key,value in kwargs.items:
                    self.users[username][key]=value
    
    #Appending each workout dictionary in workout list            
    def add_workout(self, user, date, duration, calories_burned, type_, distance, reps, sets, description):
        
        if type_ == 'strength':
            self.workouts.append(StrengthWorkout(user, date, duration, calories_burned, description, reps, sets).to_dict())
            print('\n', pd.DataFrame(StrengthWorkout(user, date, duration, calories_burned, description, reps, sets).to_dict(), index=[0]).to_string(index=False))
        elif type_ == 'cardio':
            self.workouts.append(CardioWorkout(user, date, duration, calories_burned, description).to_dict())
            print('\n',pd.DataFrame(CardioWorkout(user, date, duration, calories_burned, description).to_dict(), index=[0]).to_string(index=False))
        else:
            self.workouts.append(RunWorkout(user, date, duration, calories_burned, description, distance).to_dict())
            print('\n',pd.DataFrame(RunWorkout(user, date, duration, calories_burned, description, distance).to_dict(), index=[0]).to_string(index=False))    
        
        self.df_workouts = pd.DataFrame(self.workouts)    
        print(f"\nWorkout added for user {user}\n")


    def edit_workout(self, username, date, description, **kwargs):
        for workout in self.workouts:
            if workout['user']==username and workout['date']==date and workout['description']==description:
                for key, value in kwargs.items():
                    workout[key]=value
                    print(f'\n{key.capitalize()} successfully updated with {value}\n')
                    break
            elif workout == self.workouts[-1]:
                print('\nNo changes have been made!\n')
                
        self.df_workouts = pd.DataFrame(self.workouts)
        return self.workouts


    def view_workouts(self, username):
        print('\n', self.df_workouts[self.df_workouts['user']==username].iloc[:,1:].to_string(index=False), '\n')


    def set_goal(self, username, goal):
        self.users[username]['goal'] = goal
        print(f'\nGoal set for user {username}\n')

    def track_progress(self, username, type_, variables):
        
        #Filtering data for specific user
        user_data = self.df_workouts[(self.df_workouts['user']==username) & (self.df_workouts['type']==type_)]
        user_data['date'] = pd.to_datetime(user_data['date'], format='%d/%m/%Y')
        user_data = user_data.sort_values('date')
        grouped = user_data.groupby(by=['date']).sum(numeric_only=True) #Grouping numerical values for same date
        dates = grouped.index
        
        plt.figure(figsize=(10, 6))
        
        #plotting line for each variable
        for variable in variables:
            values = grouped[variable]
            plt.plot(dates, values, marker='o', linestyle='-', label=variable.capitalize())

        plt.xticks(dates)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.xticks(rotation=0)

        #Indicating labels
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Progress Over Time')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        #Saving and displaying plot
        plt.savefig(f'{username}_{type_}_{variables}.png') 
        plt.show()
        
        
    def save_data(self, users_file="users.csv", workouts_file="workouts.csv"):
        self.df_users.to_csv(users_file, mode='w')
        print(f'Transformed data saved to {users_file}')
        
        self.df_workouts.to_csv(workouts_file, mode='w')
        print(f'Transformed data saved to {workouts_file}\n')
        
        
    def load_data(self, users_file="users.csv", workouts_file="workouts.csv"):
        
        try:
            with open(users_file, 'r'):
                
                print(f'Users data loaded from {users_file}\n')
        except FileNotFoundError:
            print(f'File {users_file} not found\n')
        except Exception as e:
            print(f'An error occurred: {e}\n')

        try:
            with open(workouts_file, 'r'):
                print(f'Workouts data loaded from {workouts_file}\n')
        except FileNotFoundError:
            print(f'File {workouts_file} not found.\n')
        except Exception as e:
            print(f"An error occurred: {e}")
