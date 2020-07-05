import os
import sys
import time


def text_animation(any_text, direction, wait_sec):
    """This function creates animation from a string. The string is
    animated horizontally or vertically given parameter, and speed is
    controlled by given waiting seconds.
    :param any_text: String to be animated.
    :type any_text: String.
    :param direction: 'horizontal' or 'vertical' animation direction.
    :type direction: String.
    :param wait_sec: Animation speed by seconds.
    :type wait_sec: float.
    :return: Animated string.
    :rtype: String.
    """
    for char in any_text:
        # Write vertical lines.
        if direction == 'vertical':
            sys.stdout.write(char + '\n')
        # Write horizontal in line.
        elif direction == 'horizontal':
            sys.stdout.write(char)
        sys.stdout.flush()
        # Waiting seconds.
        time.sleep(wait_sec)
    return ''


def game_opening_screen():
    """In this function the maximum number of tries is defined and
    returned, it is the limit (not included) number of guess failures
    in the game. The function prints game's animated opening screen,
    including welcome photo and statement of maximum number of failures.
    :return MAX_TRIES: Number of maximum tries.
    :rtype MAX_TRIES: Integer.
    """
    WELCOME_PHOTO = r"""
     _    _
    | |  | |    WELCOME TO GAME
    | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
    |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
    | |  | | (_| | | | | (_| | | | | | | (_| | | | |
    |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                         __/ |
                        |___/"""
    # Define maximum tries.
    MAX_TRIES = 7
    split_welcome = WELCOME_PHOTO.split('\n')
    # Animate the split welcome.
    animated_welcome = text_animation(split_welcome, 'vertical', .07)
    # Opening screen.
    data = {'a': animated_welcome, 'b': MAX_TRIES - 1}
    format_string = "{a}\nMax number of failures is {b}"
    OPENING_SCREEN = format_string.format(**data)
    # Show the animated opening screen.
    print(OPENING_SCREEN)
    time.sleep(.7)
    return MAX_TRIES


def get_valid_path():
    """This function asks the user for a file path, and return it if
    valid. The function repeats asking should file path not found, in
    this case also notification is shown.
    :return user_input: A valid file path.
    :rtype user_input: String.
    """
    file_path = False
    while not file_path:
        # Ask user for a file path and remove spaces.
        user_input = input("Specify file path for words "
                           "container: ").strip()
        # If path is found, flag to stop loop and return path.
        if os.path.exists(user_input):
            file_path = True
            return user_input
        else:
            # If path is not found, show animated error notification and
            # continue the loop.
            error_notification = "File Path Not Found"
            print(text_animation(error_notification, 'horizontal', .02))


def get_counting_number():
    """This function asks user for a 'counting number' and return it.
    The function asks repeatedly until a valid value is received, and
    show animated error notifications accordingly.
    :return user_input: Counting number (positive int, not zero).
    :rtype user_input: Integer.
    """
    counting_number = False
    while not counting_number:
        # Ask user for a counting number, and test convert to integer.
        try:
            user_input = int(input("Write a number for word to be "
                                   "chosen: "))
            # If received integer is positive and not zero,
            # flag to stop loop and return value.
            if user_input > 0:
                counting_number = True
                return user_input
            else:
                zero_or_negative = "Choose only a whole number " \
                                   "greater than 0"
                # Show animated error notification if integer <= 0.
                print(text_animation(zero_or_negative,
                                     'horizontal', .02))
        # Show animated error notification if failed to convert
        # to integer.
        except ValueError:
            error_notification = "This is not a whole number"
            print(text_animation(error_notification, 'horizontal', .02))


def choose_word(file_path):
    """This function returns a word according to its index position
    asked by the user, in received file path. The words in the file are
    separated by spaces. If user specifies an index greater than the
    number of words, the count continues circular from the start,
    meaning at first word position.
    :param file_path: Location of the file, directory path.
    :type file_path: String.
    :return chosen_word: A word from the file.
    :rtype chosen_word: String.
    """
    # Ask user for index position, a counting number.
    word_index = get_counting_number()
    # Open file and close automatically.
    with open(r"%s" % file_path, 'r') as input_file:
        input_str = input_file.read()
        # Create list from string split by spaces.
        words_list = input_str.split(' ')
        # If num of words is equal or greater than index number.
        if word_index <= len(words_list):
            # Word position is at list position, not counting zero.
            chosen_word = words_list[word_index - 1]
        else:
            # Word position is at calculated remainder of num of words
            # from index, not counting zero.
            chosen_word = words_list[(word_index % len(words_list)) - 1]
    return chosen_word


def clear_screen():
    """This function clears the screen.
    :rtype: None.
    """
    # Clear screen command.
    os.system('cls' if os.name == 'nt' else 'clear')


def print_hangman(num_of_tries):
    """In this function the photos of Hangman game are defined and
    printed to represent user guessing level, according to a given
    number. Each photo, set of characters, is associated to index
    number in dictionary, and printed according to the number of tries.
    :param num_of_tries: Level number of user guesses.
    :rtype: None.
    """
    # Note: No line space in photo2, according CampusIL example.
    HANGMAN_PHOTOS = {
        1: """Let’s start!\n
x-------x""", 2: """:(
x-------x
|
|
|
|
|\n""", 3: """:(\n
x-------x
|       |
|       0
|
|
|\n""", 4: """:(\n
x-------x
|       |
|       0
|       |
|
|\n""", 5: """:(\n
x-------x
|       |
|       0
|      /|\\
|
|\n""", 6: """:(\n
x-------x
|       |
|       0
|      /|\\
|      /
|\n""", 7: """:(\n
x-------x
|       |
|       0
|      /|\\
|      / \\
|\n"""}
    print(HANGMAN_PHOTOS[num_of_tries])


def show_hidden_word(secret_word, old_letters_guessed):
    """This function accepts the secret word and a list of already
    guessed letters, and prints an output as follows: correct guessed
    letters are shown in word's position, and letters not yet guessed
    appear as underscore.
    :param secret_word: The word to guess by user.
    :type secret_word: String.
    :param old_letters_guessed: List of valid letters already guessed.
    :type old_letters_guessed: List.
    :rtype: None.
    """
    # Create a string output.
    result = ''
    # For each letter in word.
    for letter in secret_word:
        # Check if exist in the already guessed letters' list.
        if letter in old_letters_guessed:
            # Add letter to output.
            result += (letter + ' ')
        else:
            # Add underscore to output.
            result += '_ '
    print(result)


def check_error_notification(letter_guessed, old_letters_guessed):
    """This function checks error type for a given invalid letter
    guessed, and return notification accordingly.
    :param letter_guessed: A user guess.
    :type letter_guessed: String.
    :param old_letters_guessed: List of valid letters already guessed.
    :type old_letters_guessed: List.
    :return error_notification: Error notification.
    :rtype error_notification: String.
    """
    # Check if guess is more than single char, and alphabet letters.
    if len(letter_guessed) > 1 and letter_guessed.isalpha():
        error_notification = "X\nOnly one letter is allowed"
    # Check if guess is more than single char, and not alphabet letters.
    elif len(letter_guessed) > 1 and not letter_guessed.isalpha():
        error_notification = "X\nOnly one alphabet A-Z letter is " \
                             "allowed"
    # Check if guess is a single char, and not alphabet letter.
    elif len(letter_guessed) == 1 and not letter_guessed.isalpha():
        error_notification = "X\nOnly type alphabet A-Z letter is " \
                             "allowed"
    # Check if guess exist in the already guessed letters' list.
    elif letter_guessed in old_letters_guessed:
        error_notification = "X\nThis letter was guessed already"
    else:
        error_notification = "Un-resolved letter"
    return error_notification


def check_valid_input(letter_guessed, old_letters_guessed):
    """This function validates given guess, should be a single alphabet
    letter and not exist in given already guessed letters' list.
    If all conditions are met the function returns True, else- False.
    :param letter_guessed: A user guess.
    :type: letter_guessed: String.
    :param: old_letters_guessed: List of valid letters already guessed.
    :type old_letters_guessed: List.
    :return: True if guess is valid, else- False.
    :rtype: Boolean.
    """
    # Check if guess is a single char, and is an alphabet letter,
    # and if not exist in the already guessed letters' list.
    if len(letter_guessed) == 1 and letter_guessed.isalpha() \
            and letter_guessed not in old_letters_guessed:
        # If all conditions are met, return True.
        return True
    else:
        # If not all conditions are met, return False.
        return False


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """This function accepts a guess and already guessed letters' list.
    If guess is valid it is added to that list, and function returns
    True. Else, if a guess is not valid, the function returns False,
    prints an animated error notification and a string of previous
    guesses, sorted and arrow separates each letter.
    :param letter_guessed: A user guess.
    :type letter_guessed: String.
    :param old_letters_guessed: List of valid letters already guessed.
    :type old_letters_guessed: List
    :return: True if guess is valid, else False.
    :rtype: Boolean.
    """
    # Check if guess is valid.
    if check_valid_input(letter_guessed, old_letters_guessed):
        # Add valid to already guessed letters' list.
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        # Create letters' list string, sorted and arrow separated.
        previous_guesses = " -> ".join(sorted(old_letters_guessed))
        # Check error notification type.
        error_notification = check_error_notification(
            letter_guessed, old_letters_guessed)
        # If first time invalid guess.
        if len(old_letters_guessed) == 0:
            # Print animated error notification.
            print(text_animation(error_notification, 'horizontal', .02))
        else:
            # Print animated error notification and previous guesses.
            print(text_animation(error_notification, 'horizontal', .02)
                  + '\n' + previous_guesses)
        return False


def check_win(secret_word, old_letters_guessed):
    """This function checks if all letters of given secret word appear
    in given guessed letters' list, and return True. If at-least one
    letter does not appear, the function returns False.
    :param secret_word: The word to guess by user.
    :type secret_word: String.
    :param old_letters_guessed: List of valid letters already guessed.
    :type old_letters_guessed: List
    :return: True if all word's letters appear in list, else- False.
    :rtype: Boolean.
    """
    # Create counter for counting letters.
    count = 0
    for letter in secret_word:
        # If letter appear in list.
        if letter in old_letters_guessed:
            count += 1
            # If counting reached the num of secret word's letters.
            if count == len(secret_word):
                return True
        else:
            return False


def end_game(end_game_status):
    """This function ends the program, printing given status after a
    short pause, and waits for any user input in order to freeze the
    screen.
    :param end_game_status: Ending game status 'WIN' or 'LOSE'.
    :type end_game_status: String.
    :rtype: None.
    """
    # Wait 0.4 seconds.
    time.sleep(0.4)
    # Print given status.
    print(end_game_status)
    # Wait for user input.
    input()


def main():
    """This is the main function of Hangman game. Opening screen is
    displayed and play starts after a secret word is selected by user
    specifying a path and a number. The secret word is presented with
    it's letters hidden. The player starts letters guessing and program
    responds to each try. Correct guess reveals hidden letters. Wrong
    guess is being counted, showing the hangman photo in progress. The
    player wins if succeed to reveal all secret word's letters, however
    if fails in 6 guesses the game ends.
    :rtype: None.
    """
    # Show opening screen and define Max Tries.
    MAX_TRIES = game_opening_screen()
    # Create already guessed letters' list.
    old_letters_guessed = []
    # Define tries counter.
    num_of_tries = 1
    # Receive file path.
    file_path = get_valid_path()
    # Receive secret word in file path.
    secret_word = choose_word(file_path)
    clear_screen()
    # Show first guessing level photo.
    print_hangman(num_of_tries)
    # Show secret word letters hidden.
    show_hidden_word(secret_word, old_letters_guessed)
    print('\n')
    # Loop as long as num of tries is less than maximum defined.
    while num_of_tries < MAX_TRIES:
        # Receive user guess.
        letter_guessed = input("Guess a letter: ").strip().lower()
        clear_screen()
        # If guess is valid, add to guessed letters' list.
        if try_update_letter_guessed(letter_guessed,
                                     old_letters_guessed):
            # If guess is not a correct guess.
            if letter_guessed not in secret_word:
                # Increase tries counter by 1.
                num_of_tries += 1
                # Show hangman relevant photo.
                print_hangman(num_of_tries)
            # Show secret word, letters hidden/revealed accordingly.
            show_hidden_word(secret_word, old_letters_guessed)
            # If all secret word's letters are guessed.
            if check_win(secret_word, old_letters_guessed):
                # Show end game as win.
                end_game('WIN')
                # exit loop.
                break
    # If num of tries reached maximum defined.
    else:
        # Show end game as lose.
        end_game('LOSE')


if __name__ == "__main__":
    main()
