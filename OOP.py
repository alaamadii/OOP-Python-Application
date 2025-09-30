from abc import ABC,abstractmethod

import json
class ItemNotAvailableError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class ItemNotFoundError(Exception):
    pass
class libraryItem(ABC):
    def __init__(self, title,author):
        self.title = title
        self.author = author
        self.available = True
    @abstractmethod
    def display_info(self):
        pass
    @abstractmethod
    def cheack_avilability(self):
        pass
class Reservable(ABC):
    @abstractmethod
    def reserve(self,user):
        pass

class Book(libraryItem, Reservable):
    def __init__(self,title,author):
        super().__init__(title,author)

    def display_info(self):
        print(f"Book: {self.title}, Author: {self.author}")
    def cheack_avilability(self):
        return self.available
    def reserve(self,user):
        print(f'{user} reserved the Book {self.title}')


class Magazine(libraryItem):
    def __init__(self,title,author):
        super().__init__(title,author)

    def display_info(self):
        print(f'This magazine: {self.title}, author: {self.author}')
    def cheack_avilability(self):
      return self.available


class DVD(libraryItem, Reservable):
    def __init__(self, title, author):
        super().__init__(title,author)

    def display_info(self):
        print(f' DVD: {self.title},author: {self.author}')
    def cheack_avilability(self):
       return self.available
    def reserve(self,user):
        print(f'{user} reserved the DVD {self.title}')

class User:
    def __init__(self,name, user_id, borrowed_items):
        self.name = name
        self.user_id= user_id
        self.borrowed_items = borrowed_items if borrowed_items else []



class library:
    def __init__(self):
        self.item =[]
        self.users = []
    def load_data(self):
        try:
            with open("item.json", "r") as f:
                item_data = json.load(f)
                for item in item_data:
                    item_type = item.get("type")
                    if item_type == "Book":
                        self.item.append(Book(item["title"], item["author"]))
                    elif item_type == "DVD":
                        self.item.append(DVD(item["title"], item["author"]))
                    elif item_type == "Magazine":
                        self.item.append(Magazine(item["title"], item["author"]))
        except FileNotFoundError:
            print("items.json not found. starting with empty items list")

        try:
            with open("user.json", "r") as f:
                user_data = json.load(f)
                for user in user_data:
                    self.users.append(User(user["name"], user["user_id"],user.get("borrowed_items",[])))
        except FileNotFoundError:
            print(f"user.json not found. starting with empty users list")
    def save_data(self):
        items_data = []
        for item in self.item:
            items_data.append({
                "type": item.__class__.__name__,
                "title":item.title,
                "author": item.author
            })

        with open("item.json", "w")as f:
            json.dump(items_data, f, indent=4)
        user_data =[]
        for user in self.users:
            user_data.append({
                "user_id": user.user_id,
                "name": user.name,
                "borrowed_item": user.borrowed_items
            })
        with open("user.json", "w") as f:
            json.dump(user_data, f, indent=4)
    def add_user(self,user):
        self.users.append(user)

    def add_item(self, item):
        self.item.append(item)

    def find_user(self,user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user

        raise UserNotFoundError(f"user with ID {user_id} not founded")

    def find_item(self, title):
        for item in self.item:
            if item.title == title:
                return item
        raise ItemNotFoundError(f"item with title {title} not found")

    def borrow_item(self, user_id,title):
        user = self.find_user(user_id)
        item = self.find_item(title)
        if not item.cheack_avilability():
            raise ItemNotAvailableError(f'item {title} is not available for borwing')
        item.available = False
        user.borrowed_items.append(title)
    def return_item(self, user_id, title):
        user = self.find_user(user_id)
        item = self.find_item(title)
        if title in user.borrowed_items:
            user.borrowed_items.remove(title)
            item.available = True
        else:
            print(f"User {user_id} has not borrowed item {title}")

    def reserve_item(self, user_id, title):
        user = self.find_user(user_id)
        item = self.find_item(title)
        if hasattr(item, "reserve"):
            item.reserve(user.name)
        else:
            print(f"Item {title} can not be reserved")
lib = library()
lib.load_data()
while True:
       print("\n1.View all available itmes\n 2.Search item by title or type\n 3.Register a new user\n 4.Borrow an item\n 5.Reserve an item\n 6.Return an item\n 7.Exit and Save\n >..")
       choice =input("> ").strip()
       if choice  == "1":
            for item in lib.item:
                item.display_info()
                print("Avilable:"if item.available else "Not Available")
       elif choice =="2":
             b= input("enter the item title or type").strip()
             found = False
             for item in lib.item:
                 if item.title.lower() == b.lower() or item.__class__.__name__.lower() == b.lower():
                     item.display_info()
                     print("Available: " if item.available else "Not Avilable")
                     found = True
             if not found:
                 print("item not found")
       elif choice == "3":
           name= str(input("enter the user name: "))
           user_id= int(input("enter the user ID: "))
           lib.add_user(User(name, user_id,[]))
           print("User registerd.")
       elif choice == "4":
           user_id = int(input("enter the user ID: "))
           title = input("enter the title")
           try:
              lib.borrow_item(user_id, title)
              print("Item borrowed.")
           except Exception as e:
              print(e)

       elif choice == "5":
           user_id = int(input("enter the user id"))
           title = str(input("enter the title"))
           try:
               lib.reserve_item(user_id,title)
           except Exception as e:
               print(e)

       elif choice  == "6" :
            user_id = int(input("enter the user id"))
            title = input("enter the title")
            try:
                lib.return_item(user_id,title)
                print("Item returned.")

            except Exception as e:
                print(e)
       elif choice == "7":
          lib.save_data()
          print("Data saved")
          break

       else:
          print("Invalid choice")





