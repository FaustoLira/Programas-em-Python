# This is a program that stores books in a user library. This program presents a loop menu where the user:
#
# 1) Includes books to the user library.
# 2) Excludes books to the user library.
# 3) Prints two tables on the screen: read and unread books. The tables include: title, author, year of publication.
# 4) Manually switch the status of a specific book: from unread to read, and vice versa.
# 5) Search by book and print the result.
# 6) Quit the program.

# written by Fausto Lira

########################################################################
# modules
########################################################################

import pandas as pd

########################################################################
# global variables
########################################################################

columns = ['Title', 'Author', 'Year of publication', 'Read']

########################################################################
# books DataFrame
########################################################################

# extracting books DataFrame from 'books.csv'
# creating 'books.csv' if the file does not exist
try:
    books = pd.read_csv('books.csv')
except FileNotFoundError:
    with open('books.csv', 'w') as books_file:
        books_file.write(','.join(columns))
    books = pd.read_csv('books.csv')


########################################################################
# functions
########################################################################


# 'a' in menu - Add user book to the auxiliary list of book
def add_book(df):
    # storing the user input as a list
    user_book = input('Please, enter [book title,Author,year of publication]: ').split(',')
    read = input('Did you read it [y/n]? ').strip().lower()
    while True:
        if read == 'y':
            user_book.append('yes')
            break
        elif read == 'n':
            user_book.append('no')
            break
        else:
            read = input('Error! Did you read it [y/n]? ').strip().lower()

    # updating books DataFrame
    bool_1 = df['Title'] != user_book[0]
    bool_2 = df['Author'] != user_book[1]
    bool_3 = df['Year of publication'] != int(user_book[2])
    bool_all = bool_1 & bool_2 & bool_3

    df = df[bool_all]
    df = df.append(dict(zip(columns, user_book)), ignore_index=True)
    # update 'books.csv'
    df.to_csv('books.csv', index=False)
    return df


# 'd' in menu - Del a book from the list
def dell_book(df):
    user_input = input('Enter the book title to be deleted: ').strip()
    # updating books DataFrame
    bool_del = df['Title'] != user_input
    df = df[bool_del]
    # update 'books.csv'
    df.to_csv('books.csv', index=False)
    print('')
    return df


# 'p' in menu - Print book list
def print_books(df):
    # expand output display with pandas
    pd.set_option('display.expand_frame_repr', False)

    print('----------------------------------------------------------------------------------------------')
    print('Books Read\n')
    if df[df['Read'] == 'yes'].shape[0]:
        # creating df_read Dataframe with just books marked as read
        df_read = df.loc[df['Read'] == 'yes', columns[:-1]].copy().sort_values(by=['Title'])
        # start index by 1
        df_read.reset_index(drop=True, inplace=True)
        df_read.index += 1
        print(df_read)
    else:
        print('There is no read book!')
    print('----------------------------------------------------------------------------------------------')
    print('Books Unread:\n')
    if df[df['Read'] == 'no'].shape[0]:
        # creating df_unread Dataframe with just books marked as unread
        df_unread = df.loc[df['Read'] == 'no', columns[:-1]].copy().sort_values(by=['Title'])
        df_unread.sort_values(by=['Title'])
        # start index by 1
        df_unread.reset_index(drop=True, inplace=True)
        df_unread.index += 1
        print(df_unread)
    else:
        print('There is no unread book!')
    print('----------------------------------------------------------------------------------------------')
    input('Press ENTER to continue...')
    print('')


# 'r' in menu - Mark a book as read
def mark_read(df):
    user_input = input('Enter the book title: ').strip()
    df.loc[df['Title'] == user_input, 'Read'] = 'yes'
    # update 'books.csv'
    df.to_csv('books.csv', index=False)
    print('')
    return df


# 's' in menu - Search function
def search_book(df):
    user_input = input("Enter the book title: ")

    # Extracting books_read and books_unread DataFrame from books DataFrame
    df_read = df[df['Read'] == 'yes'].copy().sort_values(by=['Title'])
    df_read.reset_index(drop=True, inplace=True)
    df_read.index += 1

    df_unread = df[df['Read'] == 'no'].copy().sort_values(by=['Title'])
    df_unread.reset_index(drop=True, inplace=True)
    df_unread.index += 1

    print('----------------------------------------------------------------------------------------------')
    if df_read[df_read['Title'] == user_input].shape[0]:
        print(f'''This book appears in Books Read list.\n''')
        print(df_read[df_read['Title'] == user_input])
    elif df_unread[df_unread['Title'] == user_input].shape[0]:
        print(f'''This book appears in Books Unread list.\n''')
        print(df_unread[df_unread['Title'] == user_input])
    else:
        print('Book not found.')
    print('----------------------------------------------------------------------------------------------')
    input('Press ENTER to continue...')
    print('')


####################################
# menu
####################################

prompt_menu = """Chose one of the following options. 
'a' to add a book;  
'd' to delete a book;
'p' to print the list;
'r' tom mark a book as read;
's' to search;
'q' to quit.
What do you would like to do? """

# print(f"\n{books_list}\n")

while True:
    option = input(prompt_menu).strip().lower()
    print(' ')
    if option == 'a':
        books = add_book(books)
        print('')
    elif option == 'd':
        books = dell_book(books)
    elif option == 'p':
        print_books(books)
    elif option == 'r':
        books = mark_read(books)
    elif option == 's':
        search_book(books)
    elif option == 'q':
        break
    else:
        print('Error!\n')

########################################################################
# Input suggestions
########################################################################

# Alice in Wonderland,Lewis Carroll,1865
# Animal Farm,George Orwell,1945
# Auto da Compadecida,Ariano Suassuna,1955
# Dom Casmurro,Machado de Assis,1899
# Frankenstein,Mary Shelley,1823
# Strange Case of Dr Jekyll and Mr Hyde,Robert Louis Stevenson,1886
# The Book Thief,Markus Zusak,2005
# The Fault in Our Stars,John Green,2012
# The Shack,William P. Young,2007
