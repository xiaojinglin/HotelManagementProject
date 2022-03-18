from models import initialize,cur,Customer,Room
from get_input import clean_date, get_customer,get_room,get_phone,check_in,check_out,menu,show_menu


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
        print(f'Check in: {room[2]}')
        choice = int(show_menu('Edit or Skip')[0])
        if choice == 1:
            room[2] = check_in()
        print(f'Check out: {room[3]}')
        choice = int(show_menu('Edit or Skip')[0])
        if choice == 1:
            room[3] = check_out(room[2])
        Room(customer_id).update(customer_id,room[2],room[3])
    print('Update successfully')


def check_customer(customer_id):
    customer = Customer(customer_id)
    rooms = Room.get_rooms(customer_id)  
    print('******Customer Information******')
    print(customer)
    for room in rooms:
        print(f'ID: {room[0]}, Room NO: {room[1]}, Check In: {room[2]}, Check Out: {room[3]}')
    choice = int(show_menu('What do you want to do?')[0])
    if choice == 1:
        update_customer(customer)
    elif choice == 2:
        customer.delete()
        for room in rooms:
            Room(room[0]).update(None,None,None)
        print('Customer Delete successfully')
    elif choice == 3:
        update_rooms(rooms,customer_id)
    elif choice == 4:
        cancel_rooms(rooms)
        
    



if __name__ == '__main__':
    initialize()
    booking()
    check_customer(1)

    cur.close()

