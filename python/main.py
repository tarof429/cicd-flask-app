# A simple Python app that manages events

import sys
from datetime import datetime

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
    event_name = input('Event: ').strip()
    event_location = input('Location: ').strip()

    while True:
        event_date = input('Date (mm/dd/yyyy): ').strip()
        try:
            datetime.strptime(event_date, '%m/%d/%Y')
            break
        except ValueError:
            print('Invalid date format, try again')

    event = {
        'name': event_name,
        'location': event_location,
        'date': event_date
    }
    events.append(event)

def list_events():
    if len(events) == 0:
        print('No events!')
        return
    
    print('Events')
    for event in events:
        event_name = event['name']
        event_location = event['location']
        event_date = event['date']
        print(f"{event_name}\t{event_location}\t{event_date}")

def update_event():
    prev_event_name = input('Event: ').strip()
    new_event_name = input('New event name: ').strip()
    
    for event_index in range(len(events)):
        if prev_event_name == events[event_index]['name']:
            events[event_index]['name'] = new_event_name
            break  

def delete_event():
    event_name = input('Event: ').strip()
    for event in events:
        if event['name'] == event_name:
            events.remove(event)
            break

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
