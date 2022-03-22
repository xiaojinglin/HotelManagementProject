from models import Room, Customer, initialize

from datetime import date
from datetime import datetime


menu = {'Choose your next step': ['Booking','Check customer','All customers','All rooms','Exit'],
        'Choose a room type': ['single','double'],
        'Search type': ['ID','Name','Phone'],
        'What do you want to do?': ['Edit customer information','Delete customer',
                                    'Edit customer booking','Cancel customer booking','Back to the main menu'],
        'Edit or Skip': ['Edit','Skip']}


def show_menu(menu_key):
    menu_items = menu[menu_key]
    while True:
        for index,item in enumerate(menu_items,1):
            print(f'{index}. {item}')
        choice = input(f'{menu_key}: ')
        if not choice.isnumeric() or int(choice) not in range(1,len(menu_items)+1):
            print(f'Invalid {menu_key}, try again')
            continue
        else:
            return choice,menu_items[int(choice)-1]


def get_phone():
    while True:
        phone = input('Phone NO(eg: 5022222222): ')
        if len(phone) != 10:
            print('Invalid phone number, try again')
        else:
            return phone


def get_customer():
    first_name = input('First Name:')
    last_name = input('Last Name:')
    phone = get_phone()
    return first_name,last_name,phone


def get_room():
    room_type = show_menu('Choose a room type')[1]
    rooms = Room.get_room_nos(room_type)
    while True:
        print(f"Rooms: {','.join(rooms)}")
        choice = input('Choose a room number: ')
        if choice not in rooms:
            print('Invalid room number, try again')
            continue
        else:
            return choice


def clean_date():
    while True:
        good_date = input('Enter a valid date(eg:2022-1-5): ')
        try:
            good_date = datetime.strptime(good_date,'%Y-%m-%d')
        except ValueError:
            print('Please enter a valid date according the example: ')
            continue
        else:
            return good_date.date()


def check_in():
    today = date.today()
    print('DATE CHECK IN')
    while True:
        date_in = clean_date()
        if date_in < today:
            print('The check in date should not be earlier than today.')
            continue
        else:
            return date_in

        
def check_out(date_in):
    print('DATE CHECK OUT')
    while True:
        date_out = clean_date()
        if date_out < date_in:
            print('The check out date should not be earlier than check in date.')
            continue
        else:
            return date_out


def search_by(search_type):
    result = input(f'Enter the {search_type} you want to search: ')
    return result


def search_get_customer(customers):
    customer_ids = []
    for customer in customers:
        customer_ids.append(str(customer[0]))
        print(Customer(customer[0]))
    while True:
        choice = input('Choose a customer Id from the search result: ')
        if choice not in customer_ids:
            print('The customer id is not in the searching result list,try again')
            continue
        else:
            return int(choice)