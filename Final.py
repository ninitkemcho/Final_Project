import csv
import random
import pandas as pd

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
            'target_value': self.target_value,
            'goal': self.goal
            }

class User(Person):
    def __init__(self, name, age, weight, height, target_value=None, goal=None):
        super().__init__(name, age)
        self.weight = weight
        self.height = height
        self.target_value = target_value
        self.goal = goal


class validators:
    
    @staticmethod
    def number_validator(n, num_type):
        is_number=False
        try:
            n=num_type(n)
            is_number=True
        except:
            print('\nInvalid input! Please enter a numeric value.')
        return is_number
    
    def user_validator(user, users):
        return user in users
        



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
        super().__init__(user, date, duration, calories_burned, type_='Strength', reps=reps, sets=sets, description=description)

class CardioWorkout(Workout):
    def __init__(self, user, date, duration, calories_burned, description):
        super().__init__(user, date, duration, calories_burned, type_='Cardio', description=description)

class RunWorkout(Workout):
    def __init__(self, user, date, duration, calories_burned, description, distance):
        super().__init__(user, date, duration, calories_burned, type_='Cardio', distance=distance, description=description)



class FitnessTracker:
    def __init__(self):
        self.users = {}
        self.workouts = []
        self.df_workouts=pd.DataFrame(workouts)
        self.df_users=pd.DataFrame(users).T

    #Generating unique username for each person
    def unique_username(self, name):
        while True:
            username=name+''.join(random.choice('0123456789') for _ in range(4))
            if username in self.users:
                continue
            else:
                break
        return username
    
    #Adding user info in users dict
    def create_user(self,  name, age, weight, height):
        self.username=self.unique_username(name)
        if self.username in self.users:
            print(f"\nUser {self.username} already exists.")
        else:
            self.users[self.username] = User(name, age, weight, height).to_dict()
            print(f"\nUser {self.username} created successfully.")

    def add_workout(self, user, date, duration, calories_burned, type_, distance, reps, sets, description):
        if type_ == 'strength':
            self.workouts.append(StrengthWorkout(user, date, duration, calories_burned, description, reps, sets).to_dict())
        elif type_ == 'cardio':
            self.workouts.append(CardioWorkout(user, date, duration, calories_burned, description).to_dict())
        else:
            self.workouts.append(RunWorkout(user, date, duration, calories_burned, description, distance).to_dict())
                
        print(self.workouts)
        print(f"\nWorkout added for user {user}.")

    def edit_workout(self, username, date, description, **kwargs):
        
        for workout in self.workouts:
            if workout['user']==username and workout['date']==date and workout['description']==description:
                for key, value in kwargs.items():
                    workout[key]=value
                    print(f'\n{key} successfully updated with {value}')
        return self.workouts

    def view_workouts(self, username):
        print(self.df_workouts[self.df_workouts['user']==username].iloc[:,1:].to_string(index=False))

    def set_goals(self, username, target_value, goal):
        self.users[username].target_value = target_value
        self.users[username].goal = goal
        print(f"Goal set for user {username}.")

    def track_progress(self, username):
        if username not in self.users:
            print(f"User {username} does not exist.")
        else:
            user = self.users[username]
            print(f"User {username} progress: Target - {user.target_value}, Goal - {user.goal}")

    def save_data(self, users_file="users.csv", workouts_file="workouts.csv"):
        with open(users_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'name', 'age', 'weight', 'height', 'target_value', 'goal'])
            for user in self.users.values():
                writer.writerow([user.username, user.name, user.age, user.weight, user.height, user.target_value, user.goal])
        print(f"Users data saved to {users_file}")

        with open(workouts_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user', 'date', 'duration', 'calories_burned', 'type', 'distance', 'reps', 'sets', 'description'])
            for workout in self.workouts:
                writer.writerow([workout.user, workout.date, workout.duration, workout.calories_burned, workout.type, workout.distance, workout.reps, workout.sets, workout.description])
        print(f"Workouts data saved to {workouts_file}")

    def load_data(self, users_file="users.csv", workouts_file="workouts.csv"):
        try:
            with open(users_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.users[row['username']] = User(row['username'], row['name'], int(row['age']), float(row['weight']), float(row['height']), row['target_value'], row['goal'])
            print(f"Users data loaded from {users_file}")
        except FileNotFoundError:
            print(f"File {users_file} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            with open(workouts_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['type'] == 'Cardio':
                        workout = CardioWorkout(row['user'], row['date'], float(row['duration']), float(row['calories_burned']), float(row['distance']), row['description'])
                    elif row['type'] == 'Strength':
                        workout = StrengthWorkout(row['user'], row['date'], float(row['duration']), float(row['calories_burned']), int(row['reps']), int(row['sets']), row['description'])
                    self.workouts.append(workout)
            print(f"Workouts data loaded from {workouts_file}")
        except FileNotFoundError:
            print(f"File {workouts_file} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    tracker = FitnessTracker()
    tracker.load_data()

    while True:
        print("\nFitness Progress Tracker")
        print("1. Create User")
        print("2. Add Workout")
        print("3. Edit Workout")
        print("4. View Workouts")
        print("5. Set Goals")
        print("6. Track Progress")
        print("7. Save Data to File")
        print("8. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            weight = float(input("Enter weight: "))
            height = float(input("Enter height: "))
            tracker.create_user(name, age, weight, height)
            print(tracker.users)
            
        elif choice == '2':
            username = input("Enter username: ")
            date=input('Enter date: ')
            duration = float(input("Enter duration (minutes): "))
            calories_burned = float(input("Enter calories burned: "))
            type_ = input("Enter workout type: ")
            distance = float(input("Enter distance (if applicable, else 0): "))
            reps = int(input("Enter reps (if applicable, else 0): "))
            sets = int(input("Enter sets (if applicable, else 0): "))
            description = input("Enter description: ")
            
            tracker.add_workout(username, date, duration, calories_burned, type_, distance, reps, sets, description)
            print(tracker.workouts)
            
        elif choice == '3':
            
            username = input("Enter username: ")
            date=input('Enter date: ')
            description=input('Enter description: ')
            fields = input("Enter the fields to edit (comma separated, e.g., duration,calories_burned): ").split(',')
            updates = {field: input(f"Enter new value for {field}: ") for field in fields}
            tracker.edit_workout(username, date, description, **updates)
            
        elif choice == '4':
            username = input("Enter username: ")
            tracker.view_workouts(username)
            
        elif choice == '5':
            username = input("Enter username: ")
            target_value = input("Enter target value (e.g., weight): ")
            goal = float(input("Enter goal: "))
            tracker.set_goals(username, target_value, goal)
            
        elif choice == '6':
            username = input("Enter username: ")
            tracker.track_progress(username)
            
        elif choice == '7':
            tracker.save_data()
            
        elif choice == '8':
            tracker.save_data()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    
workouts=[{'user': 'nini79115', 'date': '16', 'duration': 90.0, 'calories_burned': 20.0, 'type': 'Cardio', 'distance': 0, 'reps': 0, 'sets': 0, 'description': 'cycling'}, {'user': 'nini79115', 'date': '16', 'duration': 90.0, 'calories_burned': 90.0, 'type': 'Cardio', 'distance': '90', 'reps': '12', 'sets': '4', 'description': 'biking'}, {'user': 'nini1717', 'date': '18', 'duration': 90.0, 'calories_burned': 90.0, 'type': 'Cardio', 'distance': 90.0, 'reps': 0, 'sets': 0, 'description': '90'}]

df=pd.DataFrame(workouts)
username='nini79115'
print(df[df['user']==username].iloc[:,1:].to_string(index=False))

users={'nini4456': {'name': 'nini', 'age': 20, 'weight': 50.0, 'height': 172.0, 'target_value': None, 'goal': None}}
df_users=pd.DataFrame(users).T

print(df.to_string(index=False))
fields = input("Enter the fields to edit (comma separated, e.g., duration,calories_burned): ").split(',')
updates = {field: input(f"Enter new value for {field}: ") for field in fields}
for key, value in updates.items():
    print(key,value)
    
import matplotlib.pyplot as plt

# Sample data
time = [1, 2, 3, 4, 5]
duration = [30, 45, 50, 40, 55]

# Plotting
plt.plot(time, duration)
plt.xlabel('Time')
plt.ylabel('Duration')
plt.title('Duration over Time')
plt.show()
