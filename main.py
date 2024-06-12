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
    logged_in_user = None
    #tracker.load_data()
    
    menu = {
            1: 'Edit User Info',  #from loaded df
            2: 'Add Workout',   #from workout list ()
            3: 'Edit Workout',  #
            4: 'View Workouts',
            5: 'Set Goals',
            6: 'Track Progress',
            7: 'Log out'
            }
    
    #In both case user will be logged in automatically
    log = {1: 'Log in', 
           2: 'Register', #create_user 
           3: 'Exit'}
    
    #Main big loop
    while True:
        
        #Printing menu for login
        for key, value in log.items():
            print(key, value)
        
        #Function input loop
        while True:
            function = input('\nChoose functionality: ')
            is_valid, function = validators.number_validator(function, int)
            if is_valid:
                break
        
        #Login    
        if function == 1:
            while True:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if tracker.authenticate_user(username, password):
                    logged_in_user = username
                    print('Successful log in!\n')
                    break
                else:
                    print("Incorrect username or password. Please try again.")
                    
        #Register +login
        elif function == 2:
            name = input('\nEnter your name: ')
            age = loops.num_loop('your age', validators.number_validator, num_type=int)
            weight = loops.num_loop('your weight', validators.number_validator, num_type = float)
            height = loops.num_loop('your height', validators.number_validator, num_type = int)
        
            #Creating new user
            username = tracker.create_user(name, age, weight, height)
              
        #Exit
        elif function == 3:
            tracker.save_data()
            print('Exiting...\nGoodbye\n')
            break
        
        #Goes to inner loop (menu)
        while True:
            
            #Printing menu
            for key, value in menu.items():
                print(key, value)
            
            #Function choosing loop
            while True:
                function = input('\nChoose functionality: ')
                is_valid, function = validators.number_validator(function, int)
                if is_valid:
                    break
                  
            #Edit user info
            if function == 1: 
                #user = loops.user_loop('your username', validators.user_validator, tracker.users)
                
                while True:    
                    fields = input('Enter variable (comma separated, e.g., weight,height): ').split(',')
                    for field in fields:
                        if field not in ['name', 'age', 'weight','height', 'goal']:
                            print('\nInvalid variables provided! Please enter from these - [name, age, weight, height, goal]\n')
                            break
                    else:
                        break
                    
                #fields = input('Enter the fields to edit (comma separated, e.g., weight,height): ').split(',')
                updates = {field: input(f'Enter new value for {field}: ') for field in fields}
                
                tracker.edit_user_info(username, **updates)
                #edit_user 
            
            #Add Workout
            elif function == 2: #Add Workout
                
                #user = loops.user_loop('your username', validators.user_validator, tracker.users) 
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
                
                tracker.add_workout(username, date, duration, calories_burned, type_, distance, reps, sets, description)
                
            #Edit Workout
            elif function == 3: #Edit Workout
                #user = loops.user_loop('your username', validators.user_validator, tracker.users) 
                date = loops.date_loop('workout date (in format dd/mm/yyyy)', validators.date_validator)
                description = input('Enter description: ')
                
                while True:    
                    fields = input('Enter variable (comma separated, e.g., duration,calories_burned): ').split(',')
                    for field in fields:
                        if field not in ['date', 'duration', 'calories_burned','type', 'distance', 'reps', 'sets', 'description']:
                            print('\nInvalid variables provided! Please enter from these - [date, duration, calories_burned, distance, reps, sets, description]\n')
                            break
                    else:
                        break
                    
                updates = {field: input(f'Enter new value for {field}: ') for field in fields}
                
                tracker.edit_workout(username, date, description, **updates)
                
            #View Workouts
            elif function == 4:
                #user = loops.user_loop('your username', validators.user_validator, tracker.users)
                tracker.view_workouts(username)
                
            #Set Goal
            elif function == 5: 
                #user = loops.user_loop('your username', validators.user_validator, tracker.users)
                goal = loops.num_loop('goal (in kg)', validators.number_validator, float)
    
                tracker.set_goal(username, goal)
                
            #Track Progress
            elif function == 6:
                #user = loops.user_loop('your username', validators.user_validator, tracker.users)
                
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
                tracker.track_progress(username, type_, variables)
                
            #Logout
            elif function == 7: 
                print('Logged out...\nGoodbye!\n')
                break
            
            #Invalid choice
            else:
                print("Invalid choice, number not in (1-8). Please try again.")
            
if __name__ == "__main__":
    main()
    
        