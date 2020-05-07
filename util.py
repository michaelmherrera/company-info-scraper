def get_yes_no(prompt):
    """Prompts user with prompt and request a [Y/N] response

    """

    print(prompt, end=" ")
    proceed = ""
    while(True):
        proceed = input("[Y/N]")
        if proceed == 'Y':
            return True
        elif proceed == 'N':
            return False
        print("Invalid option. Please choose", end=" ")