from functions import validators, FitnessTracker

#Creating loop class for incorrect input values
class loops:
    def num_loop(variable_name, validator, num_type):
        while True:
            variable = input(f'Enter {variable_name}: ')
            is_valid, variable = validator(variable, num_type)
            if is_valid:
                break 
        return variable
    
    def date_loop(variable_name, validator):
        while True:
            variable = input(f'Enter {variable_name}: ')
            is_valid, variable = validator(variable)
            if is_valid:
                break 
        return variable
    
    def user_loop(variable_name, validator, users):
        while True:
            variable = input(f'Enter {variable_name}: ')
            if validator(variable, users):
                break 
            else:
                print('\nInvalid input! Please enter valid username\n')
        return variable
    
    
def main():
    
    tracker = FitnessTracker()
    tracker.load_data()
    
    menu = {1: 'Create User', # +edit user info
            2: 'Add Workout',  #აქ არ დაგავიწყდეს დაამატე, თუ იუზერი ემპტია
            3: 'Edit Workout',
            4: 'View Workouts',
            5: 'Set Goals',
            6: 'Track Progress',
            7: 'Save Data to File',
            8: 'Exit'}
    

    while True:
        #Prints menu iteratively after every function
        for key, value in menu.items():
            print(key, value)
        
        while True:
            function = input('\nChoose functionality: ')
            is_valid, function = validators.number_validator(function, int)
            if is_valid:
                break
              
        if function == 1: #Create User
            name = input('\nEnter your name: ')
            age = loops.num_loop('your age', validators.number_validator, num_type=int)
            weight = loops.num_loop('your weight', validators.number_validator, num_type = float)
            height = loops.num_loop('your height', validators.number_validator, num_type = int)
        
            #Creating new user
            tracker.create_user(name, age, weight, height)
                
        elif function == 2: #Add Workout
            
            user = loops.user_loop('your username', validators.user_validator, tracker.users) 
            date = loops.date_loop('workout date (in format dd/mm/yyyy)', validators.date_validator)
            duration = loops.num_loop('workout duration (in minutes)', validators.number_validator, float)
            calories_burned = loops.num_loop('calories you burned', validators.number_validator, int)
            
            while True:
                type_ = input('Enter workout type (Cardio, Run, Strength): ').lower()
                if type_ not in ['cardio', 'run', 'strength']:
                    print('Invalid workout type')
                else:
                    break
                
            distance = loops.num_loop('distance (if applicable, else 0)', validators.number_validator, float)
            reps = loops.num_loop('reps (if applicable, else 0)', validators.number_validator, int)
            sets = loops.num_loop('sets (if applicable, else 0)', validators.number_validator, int)
            description = input('Enter description: ')
            
            tracker.add_workout(user, date, duration, calories_burned, type_, distance, reps, sets, description)
            
        elif function == 3: #Edit Workout
            user = loops.user_loop('your username', validators.user_validator, tracker.users) 
            date = loops.date_loop('workout date (in format dd/mm/yyyy)', validators.date_validator)
            description = input('Enter description: ')
            fields = input('Enter the fields to edit (comma separated, e.g., duration,calories_burned): ').split(',')
            updates = {field: input(f'Enter new value for {field}: ') for field in fields}
            
            tracker.edit_workout(user, date, description, **updates)
            
        elif function == 4: #View Workouts
            user = loops.user_loop('your username', validators.user_validator, tracker.users)
            tracker.view_workouts(user)
            
        elif function == 5: #Set Goals
            user = loops.user_loop('your username', validators.user_validator, tracker.users)
            goal = loops.num_loop('goal (in kg)', validators.number_validator, float)

            tracker.set_goal(user, goal)
            
        elif function == 6: #Track Progress
            user = loops.user_loop('your username', validators.user_validator, tracker.users)
            
            #makes sure type is correctly inputted
            while True:
                type_ = input('Enter workout type (Cardio, Run, Strength): ').lower()
                if type_ not in ['cardio', 'run', 'strength']:
                    print('Invalid workout type')
                else:
                    break
                
            #makes sure variables provided actually exist    
            while True:    
                variables = input('Enter variable (comma separated, e.g., duration,calories_burned): ').split(',')
                for variable in variables:
                    if variable not in ['duration', 'calories_burned', 'distance', 'reps', 'sets']:
                        print('\nInvalid variables provided! Please enter from these - [duration, calories_burned, distance, reps, sets]\n')
                        break
                else:
                    break
            
            #Displays and saves line chart of input variables
            tracker.track_progress(user, type_, variables)
            
        elif function == 7: #Save Data to File
            tracker.save_data()
            
        elif function == 8: #Exit
            print('Saving data...')
            tracker.save_data() #Saving data even in case of exit
            print('Succesfully saved, exiting...\nGoodbye!')
            break
        
        else:
            print("Invalid choice, number not in (1-8). Please try again.")
        
if __name__ == "__main__":
    main()
    
        