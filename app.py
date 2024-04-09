from classes import Record, Name, Birthday, Phone, Email, Address, Group
from address_book import AddressBook
from colorama import init, Fore

book = AddressBook()
commands = dict()

def error_handler(func):
    """Error handler for program runtime."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f'{Fore.RED}Oops! {e}{Fore.RESET}')
    return wrapper

@error_handler
def input_command(value: str = None):
    """Prompt the user to input a command with error handling."""
    if not value:
        print(f'{Fore.GREEN}Enter a command to execute: {Fore.RESET}', end='')
        user_input = input()
    else:
        user_input = value

    user_input = user_input.split(maxsplit=1)
    command = user_input[0].casefold()

    if not (command in commands):
        raise ValueError(f'InputCommand - Command "{command}" not recognized.')

    command_info = commands[command]

    if command_info['param']:
        if len(user_input) == 1:
            raise ValueError(f'InputCommand - No arguments provided for command execution.')

        params = user_input[1].split()
        params_count = len(params)
        func_params_count = len(command_info['param'].split(' '))
        
        if params_count != func_params_count:
            raise ValueError(f'InputCommand - Incorrect number of arguments - "{params_count}". Expected arguments - "{func_params_count}"')

    func = command_info['func']

    if command_info['param']:
        func(*params) if not command_info['print'] else print(f'{Fore.YELLOW}{func(*params)}{Fore.RESET}')
    else:
        func() if not command_info['print'] else print(f'{Fore.YELLOW}{func()}{Fore.RESET}')

def hello_bot() -> str:
    """Greetings message."""
    print(f'{Fore.GREEN}Greetings, my mentor!{Fore.GREEN}')

commands.update({
    'hello': {
        'desc': 'Greetings message.', 
        'func': hello_bot, 
        'param': None, 
        'print': False
    }
})

def help() -> str:
    """Return a string with a list of all commands and their descriptions."""
    result = f'{"Command":<10}{"Parameters":<40}{"Description":<50}\n'
    for key, value in commands.items():
        param = value['param'] if value['param'] is not None else 'No parameters'
        desc = value['desc']
        result += f'{key:<10}{param:<40}{desc:<50}\n'
    result = result.rstrip('\n')
    return result

commands.update({
    'help': {
        'desc': 'Help with commands.', 
        'func': help, 
        'param': None,
        'print': True
    },
})

def add_value_contact(name: str, obj_type: type, value: str) -> None:
    """Add a contact field."""
    contact = book.find_contact(Record(name))
    book.change_contact('add', contact, eval(obj_type.capitalize()), value)

commands.update({
    'add': {
        'desc': 'Add a contact field.', 
        'func': add_value_contact, 
        'param': '[name] [type] [value]', 
        'print': False
    }
})

def del_value_contact(name: str, obj_type: type, value: str) -> None:
    """Delete a contact field."""
    contact = book.find_contact(Record(name))
    book.change_contact('delete', contact, eval(obj_type.capitalize()), value)

commands.update({
    'del': {
        'desc': 'Delete a contact field.', 
        'func': del_value_contact, 
        'param': '[name] [type] [value]', 
        'print': False
    }
})

def change_value_contact(name: str, obj_type: type, new_value: str, old_value: str = None) -> None:
    """Change a contact field."""
    contact = book.find_contact(Record(name))
    book.change_contact('change', contact, eval(obj_type.capitalize()), new_value, old_value)

commands.update({
    'change': {
        'desc': 'Change a contact.', 
        'func': change_value_contact, 
        'param': '[name] [type] [new_value] [old_value]', 
        'print': False
    }
})

def show_birthdays_week():
    """Show birthdays in the current week."""
    return book.get_upcoming_birthdays()

commands.update({
    'birthday': {
        'desc': 'Show birthdays for the week.', 
        'func': show_birthdays_week, 
        'param': None, 
        'print': True
    }
})

def delete_contact(name: str) -> None:
    """Delete a contact by name."""
    book.delete_contact(Record(name))

commands.update({
    'delete': {
        'desc': 'Delete a contact.', 
        'func': delete_contact, 
        'param': '[name]', 
        'print': False
    }
})

def find_contact(name: str) -> Record:
    """Find a contact by name."""
    print('Contact found:')
    return book.find_contact(Record(name))

commands.update({
    'find': {
        'desc': 'Find a contact.', 
        'func': find_contact, 
        'param': '[name]', 
        'print': True
    }
})

def add_new_contact(name: str) -> None:
    """Create a new contact in the address book."""
    book.add_contact(Record(name))

commands.update({
    'new': {
        'desc': 'Create a new contact.', 
        'func': add_new_contact, 
        'param': '[name]', 
        'print': False
    }
})

def show_all_contacts() -> AddressBook:
    """Show all contacts."""
    return book

commands.update({
    'all': {
        'desc': 'Show all contacts.', 
        'func': show_all_contacts, 
        'param': None, 
        'print': True
    }
})

def exit_bot() -> None:
    """Exit the program."""
    print(f'{Fore.GREEN}Farewell, my mentor!{Fore.GREEN}')
    exit()

commands.update({
    'exit': {
        'desc': 'Close the program.', 
        'func': exit_bot, 
        'param': None,
        'print': False
    }
})

def main():
    """Main program function."""
    init()
    input_command('hello')
    while True:
        input_command()

if __name__ == "__main__":
    main()