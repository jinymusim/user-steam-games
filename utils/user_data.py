import os

MANAGER_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'manager.private'))       

DEFAULT_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , 'data' , 'keys.private'))
DATA_KEYS = ['API_KEY', 'USER_ID', 'USER']


class UserData:
    
    def __init__(self, data_file: str = DEFAULT_DATA_FILE) -> None:
        self.data_file = data_file
        if os.path.exists(data_file) and os.path.isfile(data_file) and data_file != MANAGER_FILE:
            print("User data file found")
            self.load_user_data_file()
        else:
            print("User data file is missing! Input user data!")
            self.query_user()
            
    
    def load_user_data_file(self):
        with open(self.data_file, 'r') as file:
            for line in file.readlines():
                key_line = line.split('=')
                if len(key_line) == 2:
                    setattr(self, key_line[0], key_line[1].strip())
                    
    def query_user(self):
        with open(self.data_file, 'w+') as file:
            for key in DATA_KEYS:
                key_value = input(key + ">")
                setattr(self, key, key_value)
                print(f"{key}={key_value}", file=file)
      

class UserDataManager:
    
    def __init__(self, manager_file:str = MANAGER_FILE) -> None:
        self.manager_file = MANAGER_FILE
        self.user_datafile_dict = {}
        if os.path.exists(manager_file) and os.path.isfile(manager_file):
            print("Manger data file found")
            self.load_manager_file()
        else:
            open(self.manager_file, 'x')
            
    def load_manager_file(self):
        with open(self.manager_file, 'r') as file:
            for line in file.readlines():
                user_userfile = line.split('=')
                # Check that the files exists
                if len(user_userfile) == 2 and os.path.exists(user_userfile[1].strip()) and os.path.isfile(user_userfile[1].strip()):
                    self.user_datafile_dict[user_userfile[0]] = user_userfile[1].strip()
    
    def get_user_data(self, user, input_if_missing: bool=True):
        if user in self.user_datafile_dict.keys():
            return UserData(self.user_datafile_dict[user])
        elif input_if_missing:
            head, tail = os.path.split(DEFAULT_DATA_FILE)
            user_data_file = os.path.join(head, f"{user}_keys.private")
            self.user_datafile_dict[user] = user_data_file
            self._write_user(user, user_data_file)
            return UserData(self.user_datafile_dict[user])
        else:
            raise AttributeError("Users datafile not found!")
        
    def _write_user(self, user, path):
        with open(self.manager_file, 'a+') as file:
            print(f"{user}={path}", file=file)
            
            
if __name__ == "__main__":
    manager = UserDataManager()
    jinymusims_data = manager.get_user_data(user='jinymusim')
    print(jinymusims_data.USER)