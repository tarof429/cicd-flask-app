# A simple Python app that manages events

import sys

events = []

def print_menu():
    print('Welcome to the event app!')
    print('Enter from the choice below: ')
    print('1) Create an event')
    print('2) List events')
    print('3) Update an event')
    print('4) Delete an event')
    print('5) Exit')

def create_new_event():
    event = input('Event: ').strip()
    events.append(event)

def list_events():
    if len(events) == 0:
        print('No events!')
    for event in events:
        print(event)

def update_event():
    prev_event_name = input('Event: ').strip()
    new_event_name = input('New event name: ').strip()
    
    for event_index in range(len(events)):
        if prev_event_name == events[event_index]:
            events[event_index] = new_event_name
            break  

def delete_event():
    event_name = input('Event: ').strip()
    for event in events:
        if event == event_name:
            events.remove(event)

def exit_app():
    sys.exit('Goodbye!')

if __name__ == '__main__':
    choice = ''

    while True:
        print_menu()
        choice = input('> ').strip()

        if choice == '1':
            create_new_event()
        elif choice == '2':
            list_events()
        elif choice == '3':
            update_event()
        elif choice == '4':
            delete_event()
        elif choice == '5':
            exit_app()
