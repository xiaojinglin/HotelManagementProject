
from prettytable import PrettyTable
from models import initialize,cur,Customer,Room
from get_input import (clean_date, get_customer,get_room,
                       get_phone,check_in,check_out,menu,
                       show_menu,search_by,search_get_customer)


room_table = PrettyTable(['ID','Room NO','Cusomtomer id','Room Type','Price','Check in','Check out'])


def booking():
    customer = get_customer()
    room = get_room()
    room_id = Room.get_id(room)
    date_in = check_in()
    date_out = check_out(date_in)
    if not Customer.exist_customer(customer):
        Customer.add(customer)
    customer_id = Customer.exist_customer(customer)[0]
    Room(room_id).update(customer_id,date_in,date_out)
    print('Booking successfully!')


def update_customer(customer):
    info = {'First Name': customer.first_name,
                'Last Name': customer.last_name,
                'Phone': customer.phone}
    for key,value in info.items():
            print(f'{key}: {value}')
            choice = int(show_menu('Edit or Skip')[0])
            if choice == 2:
                continue
            if key == 'Phone':
                info[key] = get_phone()
            else:
                info[key] = input(f'New {key}: ')
    customer.update(info['First Name'],info['Last Name'],info['Phone'])


def cancel_rooms(rooms):
    room_nos = [room[1] for room in rooms]   
    while True:
        choice = input(f"Choose the room No you want to cancel ({','.join(room_nos)}): ")
        if choice not in room_nos:
            print('The room NO is not in the option')
            continue
        else:
            break
    room_id = Room.get_id(choice)
    Room(room_id).update(None,None,None)
    print('Room Reversation Cancelled')


def update_rooms(rooms,customer_id):
    for room in rooms:
        room = list(room)
        print(f'Room NO: {room[1]}')
        print(f'Check in: {room[5]}')
        choice = int(show_menu('Edit or Skip')[0])
        if choice == 1:
            room[5] = check_in()
        print(f'Check out: {room[6]}')
        choice = int(show_menu('Edit or Skip')[0])
        if choice == 1:
            room[6] = check_out(room[5])
        Room(customer_id).update(customer_id,room[5],room[6])
    print('Update successfully')


def show_customer(customer,rooms): 
    room_table.clear_rows()
    total = 0 
    print('\n',customer)
    for room in rooms:
        room_table.add_row(room)
        days = 1 if room[6]==room[5] else (room[6]-room[5]).days
        total += room[4]*days
    print(room_table)
    print(f'Total amount: ${total}')


def search_customer():
    print('Search By:')
    choice = int(show_menu('Search type')[0])
    search_dict = {1:'id', 2:'name', 3:'phone'}
    search_type = search_dict.get(choice)
    search_value = search_by(search_type)
    customers = Customer.search_customers(search_type,search_value)
    return customers


def check_customer():
    check_running = True
    while check_running:
        customers = search_customer()
        if not customers:
            print('The customer you searched is not exist, press enter to try again')
            continue
        the_customer_id = search_get_customer(customers)
        the_customer = Customer(the_customer_id)
        rooms = Room.get_rooms(the_customer_id)
        print('******Customer Information******')
        show_customer(the_customer,rooms)
        choice = int(show_menu('What do you want to do?')[0])
        if choice == 1:
            update_customer(the_customer)
        elif choice == 2:
            the_customer.delete()
            for room in rooms:
                Room(room[0]).update(None,None,None)
            print('Customer Delete successfully')
        elif choice == 3:
            update_rooms(rooms,the_customer_id)
        elif choice == 4:
            cancel_rooms(rooms)
        check_running = False


def all_customers():
    customers = Customer.get_all_customers()
    for customer in customers:
        c = Customer(customer[0])
        rooms = Room.get_rooms(customer[0])
        show_customer(c,rooms)


def all_rooms():
    rooms = Room.get_all_rooms()
    room_table.clear_rows()
    for room in rooms:
        room_table.add_row(room)
    print(room_table)


def app():
    app_running = True
    while app_running:
        print('\n****************HOTEL SYSTEM****************\n')
        choice = int(show_menu('Choose your next step')[0])
        if choice == 1:
            booking()
        elif choice == 2:
            check_customer()
        elif choice == 3:
            all_customers()
        elif choice == 4:
            all_rooms()
        else:
            app_running = False
        input('Press enter to continue')


if __name__ == '__main__':
    initialize()
    app()
    cur.close()

