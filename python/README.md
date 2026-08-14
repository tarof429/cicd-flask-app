# Python Event App

## Introduction

This is a Python console application to manage events. A list is used to manage the events, and CRUD operations are supported.

## Sample Output

Below is the main menu:

```sh
$ python ./main.py
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
```

Events can be created.

```sh
> 1
Event: Listen to music
Location: Home
Date (mm/dd/yyyy): 08/14/2026
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
```

Events can be listed.

```sh
> 2
Events
Listen to music	Home	08/14/2026
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
```

More events can be added.

```sh
> 1
Event: Go to work
Location: Work
Date (mm/dd/yyyy): 08/15/2026
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
> 2
Events
Listen to music	Home	08/14/2026
Go to work	Work	08/15/2026
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
```

Event names can be updated.

```sh
> 3
Event: Go to work
New event name: Play tennis
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
> 2
Events
Listen to music	Home	08/14/2026
Play tennis	Work	08/15/2026
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
```

Events can be deleted.

```sh
> 4
Event: Listen to music
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
> 2
Events
Play tennis	Work	08/15/2026
Welcome to the event app!
Enter from the choice below: 
1) Create an event
2) List events
3) Update an event
4) Delete an event
5) Exit
```

Press 5 to quit.

```sh
> 5
Goodbye!
```