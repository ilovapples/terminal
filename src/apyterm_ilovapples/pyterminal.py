#!/usr/bin/env python3
print("Importing modules...")
import os
from platform import system as getos

# Try to import 'getkey' from 'getkey', prompt to install if not installed
try:
    from getkey import getkey
except ModuleNotFoundError:
    print("You need to install the 'getkey' module. Run 'pip install getkey' in your pyterminal.")
    install = input("Automatically install 'getkey'? (Y/n): ").lower()
    if install.lower() == 'y':
        os.system('pip3 install getkey')
        print("The program will now restart to continue.\n")
        if getos() == 'Windows':
            os.system('py pyterminal.py')
        else:
            os.system('python3 pyterminal.py')
    quit()
# Try to import 'tim' from 'pytermgui', prompt to install if not installed
try:
    from pytermgui import tim
except ModuleNotFoundError:
    print("You need to install the 'pytermgui' module. Run 'pip install pytermgui' in your pyterminal.")
    install = input("Automatically install 'pytermgui'? (Y/n): ").lower()
    if install.lower() == 'y':
        os.system('pip3 install pytermgui')
        print("The program will now restart to continue.\n")
        if getos() == 'Windows':
            os.system('py pyterminal.py')
        else:
            os.system('python3 pyterminal.py')
    quit()
import yaml

print("Finished importing modules!")


class OpenFiles:
    def __init__(self):
        self.files = []

    def open(self, file_name, mode='r'):
        f = open(file_name, mode)
        self.files.append(f)
        return f

    def close(self):
        list(map(lambda f: f.close(), self.files))


file = OpenFiles()

fileLocation_file = file.open('dir.txt', 'r')
fileLocation = fileLocation_file.read().replace('\n', '').strip()
if fileLocation == 'default':
    if getos() == 'Windows':
        print("Setting base directory...\n")
        os.system('set_dir.bat')
        print("The program will now restart to continue.\n")
        os.system('python3 pyterminal.py')
        quit()
    else:
        print("Setting base directory...\n")
        os.system('bash set_dir.sh')
        print("The program will now restart to continue.\n")
        os.system('python3 pyterminal.py')
        quit()
else:

    backslash = '\\'

    # ANSI Color Codes
    codes = {
        'black_fore': '\033[30m',
        'red_fore': '\033[31m',
        'green_fore': '\033[32m',
        'yellow_fore': '\033[33m',
        'blue_fore': '\033[34m',
        'magenta_fore': '\033[35m',
        'cyan_fore': '\033[36m',
        'white_fore': '\033[37m',
        'bold': '\033[1m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'strikethrough': '\033[9m',
        'reset': '\033[0m',
        'blue_bold': '\033[34;1m',
    }

    # Console Commands
    with open('cmds.yaml', 'r') as cmds:
        commands = yaml.safe_load(cmds.read())

    user_file = file.open(fileLocation + "/.users.txt", 'r')
    usersList = user_file.read()


    def runcmd(cmd: str, user: str):
        a_cmd = [False]
        cmds_list = [cmd.strip()]
        if " && " in cmd:
            cmds_list = [i.strip() for i in cmd.split(" && ")]
            a_cmd = [False for _ in cmds_list]
        # iterate over all commands in command
        for index, cur_cmd in enumerate(cmds_list):
            if cur_cmd.startswith("ls"):
                args = cmd.split(' ')[1:]
                exec(commands['ls'])
                a_cmd[index] = True
            else:
                # check if the chosen command exists, and if so, run it
                for i in commands:
                    if cur_cmd.startswith(i):
                        args = cmd.split(' ')[1:]
                        exec(commands[i])
                        a_cmd[index] = True

        for index, i in enumerate(a_cmd):
            if not i:
                if ' ' in cmds_list[index]:
                    print(f"Error: Command '{cmds_list[index][:cmds_list[index].index(' ')]}' does not exist.")
                else:
                    print(f"Error: Command '{cmds_list[index]}' does not exist.")


    def create_account(username, password):
        if f'{username} {password}' not in usersList and not os.path.isdir(f'{fileLocation}/data/{username}'):
            with open(fileLocation + "/.users.txt", 'a') as users_append:
                users_append.write(f'{username} {password}\n')
            os.chdir(fileLocation)

            try:
                os.mkdir(f'{fileLocation}/data/{username}')
                print()
            except:
                print('')
            if getos() != 'Windows':
                os.system(f'cp -r {fileLocation}/default_data/* {fileLocation}/data/{username}')
                os.system(f'cp -r {fileLocation}/default_data/.startup {fileLocation}/data/{username}')
                os.system(f'wget https://github.com/ilovapples/terminal/tree/main/README.md {fileLocation}/data/{username}')
        else:
            print("That account already exists.")


    def create_account_screen():
        print(f"{codes['bold']}\nCreate Account Screen{codes['reset']}")
        username = input("Username for New Account: ")
        password = input("Password for New Account: ")
        create_account(username, password)
        print("You created a new account!")
        login_screen()


    def login(username, password):
        with open(fileLocation + "/.users.txt", "r") as user_list:
            user_password_list = [i.split(' ') for i in user_list.read().strip().split('\n')]

            for pair in user_password_list:
                if username == pair[0]:
                    if password == pair[1]:
                        # return status code 0 if password is correct and user exists (successful login)
                        return 0
                    else:
                        # return status code 1 if password is incorrect
                        return 1

                else:
                    # return status code 2 if user does not exist
                    return 2
            user_list.close()


    def login_screen():
        users = file.open(fileLocation + "/.users.txt")
        if users.read().strip() == '':
            print("You don't currently have any accounts, so you are being redirected to the account creation screen.")
            create_account_screen()
        else:
            print("\nLog in to a user: ")
            username = input("Username: ")
            password = input("Password: ")
            if login(username, password) == 0:
                print(f"You are successfully logged in to the '{username}' account!")
                runterminal(username)
            elif login(username, password) == 1:
                print("\nEither The username or password you inputted is incorrect.")
                login_screen()
            else:
                print(f"The user '{username}' does not exist! Do you want to create an account? (Y/n): ")
                key = ""
                while key != 'y' or key != 'n':
                    key = getkey()
                    if key.lower() == 'y':
                        create_account_screen()
                    elif key.lower() == 'n':
                        login_screen()
        users.close()


    def runterminal(user):
        # run startup commands
        # startupfile = file.open(fileLocation + f'data/{user}/.startup', 'r')
        # startup = startupfile.read()
        # for i in startup.split('\n'):
        #     runcmd(i, user)
        file.close()
        

        startdir = os.getcwd().replace(backslash, "/").replace(user, '~', 1).split("/")
        cmd = ''
        os.chdir(fileLocation + f'/data/{user}')
        
        runcmd('run .startup', user)
        while cmd != 'logout':
            directory = (os.getcwd().replace(backslash, "/").replace(user, '~', 1).split("/"))[len(startdir):]
            usingdir = ""
            for i in directory:
                usingdir += i + '/'
            usingdir = usingdir.replace('data/', '')

            # DEFINE TERMINAL PROMPT
            prompt = tim.parse(f'[royalblue]{user}: {usingdir} $ ')

            user_file.close()

            cmd = input(prompt)

            runcmd(cmd, user)
        file.close()
        login_screen()


    if __name__ == '__main__':
        login_screen()

    file.close()
