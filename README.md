# Route to contact or location
This workflow calculates the route from the current location, a contact from your address book or a specified location to either the current location, a contact from your address book or a specified location. The scripts are written in python and use the pre-installed objective-c bridge pyobjc to search the address book and determine the current location with CoreLocation. Because of this, OS X will display messages that ask for the permission to use CoreLocation and AddressBook.
 
## Requirements:
The scripts use the shipped python version and the nice alfred module by nikipore (included). Because of the usage of OS X APIs there are requirements for the OS X version. I developed and tested the workflow on 10.8.4 and 10.9.1, but perhaps older versions are also working (feedback?).
 
## Installation:
You could either download the alfredworkflow file from Packal or clone the repository to your Alfred workflow folder:

```bash
git clone https://github.com/abyth/alfred-route-contact-workflow.git\
  ~/Library/Application\ Support/Alfred\ 2/Alfred.alfredpreferences/workflows/
```

## Usage:
Simply type "route" followed by the first or last name of a contact or a custom location and choose the right one from the list. You can also specify two addresses in the same manner to calculate a route between the two. If your custom address or the contact name include spaces, you'll need to put quotes around it.
