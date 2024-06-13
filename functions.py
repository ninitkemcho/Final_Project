import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.errors import EmptyDataError


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
            'goal': self.goal,
            'password': self._password}

class User(Person):
    def __init__(self, name, age, weight, height, goal=None, password=None):
        super().__init__(name, age)
        self.weight = weight
        self.height = height
        self.goal = goal
        self._password = password

    def get_password(self, password):
        return self._password
    
    def set_password(self, password):
        self._password = password
       
        
        
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
        self.df_users, self.df_workouts, self.df_operations = self.load_data()

    def authenticate_user(self, username, password):
        if username in self.df_users.index and self.df_users.at[username,'password']==password:
            return True
        return False    
    
    def operations(self, username, time, operation, description):
        self.df_operations = self.df_operations.append({'user': username, 'time': time, 'operation': operation, 'description': description}, ignore_index = True)
        return self.df_operations
        
    #Generating unique username for each person
    def unique_username(self, name):
        while True:
            #Creating name+ random 4-digit number combination as username
            username=name+''.join(random.choice('0123456789') for _ in range(4))
            #Makes sure each username is unique
            if username in self.df_users.index:
                continue
            else:
                break
        return username
    
    #Adding user info in users dict
    def create_user(self,  name, age, weight, height):
        
        #Generating username
        self.username=self.unique_username(name)
        
        #Validating password length
        while True:     
            password=input('Set a password for the new user: ')
            if len(password)<8:
                print('\nPassword length is less than 8.')
            else:
                break
        #Appending new user info
        new_user=User(name, age, weight, height, password=password)
        self.users[self.username] = new_user.to_dict()
        
        if self.df_users.shape == (0,0):
            self.df_users = pd.DataFrame(self.users).T
        else:
            self.df_users.loc[self.username]=self.users[self.username]
    
        print(f"\nUser {self.username} created successfully.\n")
        
        return self.username #To use in main
    
    #Edits user info in case of mistake
    def edit_user_info(self, username, **kwargs):
        for key,value in kwargs.items():
            self.df_users.at[username,key] = value
            print(f'Succesfully edited {key}')
    
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
        
        #Appending new row to dataframe
        self.df_workouts = self.df_workouts.append(self.workouts[-1], ignore_index=True)
    
        print(f"\nWorkout added for user {user}\n")

    def edit_workout(self, username, date, description, **kwargs):
        
        for index, row in self.df_workouts.iterrows():
            if row['user'] == username and row['date'] == date and row['description'] == description:
                for key, value in kwargs.items():
                    self.df_workouts.at[index,key] = value
                    print(f'\n{key.capitalize()} successfully updated with {value}\n')
                    return True
                    break
            elif index+1 == len(self.df_workouts):
                print('\nNo changes have been made!\n')
                return False
        
    

    def view_workouts(self, username):
        print('\n', self.df_workouts[self.df_workouts['user']==username].iloc[:,1:].to_string(index=False), '\n')


    def set_goal(self, username, goal):
        self.df_users.at[username, 'goal'] = goal
        print(f'\nGoal set for user {username}\n')

    def track_progress(self, username, type_, variables):
        
        #Filtering data for specific user
        user_data = self.df_workouts[(self.df_workouts['user']==username) & (self.df_workouts['type']==type_)]
        user_data['date'] = pd.to_datetime(user_data['date'], format='%Y/%m/%d')
        user_data = user_data.sort_values('date')
        grouped = user_data.groupby(by=['date']).sum(numeric_only=True) #Grouping numerical values for same date
        dates = grouped.index
        
        plt.figure(figsize=(10, 6))
        
        #plotting line for each variable
        for variable in variables:
            values = grouped[variable]
            plt.plot(dates, values, marker='o', linestyle='-', label=variable.capitalize())

        plt.xticks(dates)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
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
        
        
    def save_data(self, users_file="users.csv", workouts_file="workouts.csv", operations_file = 'operations.csv'):
        
        #Users data
        self.df_users.to_csv(users_file)
        print(f'Transformed data saved to {users_file}')
        
        #Workouts data
        self.df_workouts.to_csv(workouts_file)
        print(f'Transformed data saved to {workouts_file}\n')
        
        #Operations data
        self.df_operations.to_csv(operations_file)
        
    def load_data(self, users_file="users.csv", workouts_file="workouts.csv", operations_file = 'operations.csv'):
        #Users data
        try:
            df_users = pd.read_csv(users_file, index_col = [0])
            print(f'Users data loaded from {users_file}')
        except FileNotFoundError:
            print(f'File {users_file} not found')
        except EmptyDataError:
            df_users = pd.DataFrame()
            print(f'Empty dataframe generated for {users_file}')
        except Exception as e:
            print(f"An error occurred: {e}")
            
        #Workouts data
        try:
            df_workouts = pd.read_csv(workouts_file, index_col = [0])
            print(f'Workouts data loaded from {workouts_file}')
        except FileNotFoundError:
            print(f'File {workouts_file} not found.')
        except EmptyDataError:
            df_workouts = pd.DataFrame() 
            print(f'Empty dataframe generated for {workouts_file}')
        except Exception as e:
            print(f"An error occurred: {e}")
            
        #Operations data
        try:
            df_operations = pd.read_csv(operations_file, index_col = [0])
            print(f'Operations data loaded from {operations_file}')
        except FileNotFoundError:
            print(f'File {operations_file} not found.')
        except EmptyDataError:
            df_operations = pd.DataFrame() 
            print(f'Empty dataframe generated for {operations_file}')
        except Exception as e:
            print(f"An error occurred: {e}")
            
            
        return df_users, df_workouts, df_operations