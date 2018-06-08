#!/usr/bin/python3

import glob
import os
import sys
from configparser import ConfigParser
from utils import Utils
import shutil


class FileMaintenance:
    """
    This class will provide a way to Rename files or directories, Move those files or directories
    or Delete files or directories
    """

    def __init__(self):
        util = Utils()
        conf_file_name = util.get_program_name_no_extension() + '.conf'
        print(conf_file_name)
        self.config = ConfigParser()
        self.config.read(conf_file_name)

        self.script_dir = os.getcwd()
        self.source_dir_to_use = self.config.get('settings', 'source_dir')

    def main(self):

        print('Rename/Move/Delete Data Program')
        print()
        print('What would you like to do?')
        print('Rename Data, Move Data or Delete Data?')
        print()
        answer = input('Enter "r" for Rename, "m" for Move or "d" for Delete or "q" for Quit : ')
        print('You\'ve selected ' + answer)

        if answer == 'm' or answer == 'M':
            self.process_move_data()
        elif answer == 'd' or answer == 'D':
            self.process_delete_data()
        elif answer == 'r' or answer == 'R':
            self.process_rename_data()
        elif answer == 'q' or answer == 'Q':
            print('Exiting program...')
            sys.exit()
        else:
            self.main()

    def process_rename_data(self):
        """
        This function will process the renaming of data
        :return:
        """

        selected_data_to_rename = self.get_selected_data(self.source_dir_to_use)

        self.rename_data(selected_data_to_rename)

    def process_move_data(self):
        """
        This function will process the moving of data
        :return:
        """
        selected_data_to_move = self.get_selected_data(self.source_dir_to_use)

        self.move_data(selected_data_to_move)

    def get_selected_data(self, dir_to_use):
        """
        Function to call so that you can get the selected data from the directory being passed
        :param dir_to_use:
        :return:
        """

        dirs = self.get_dirs(dir_to_use)

        dirs_available = self.create_dir_dict(dirs)

        if len(dirs_available) > 0:
            selected_data_to_move = self.display_dir_dict_info(dirs_available)
        else:
            print('There are no more sub directories to use')
            len_dir_to_use = len(dir_to_use) - 2
            use_dir = dir_to_use[:len_dir_to_use]
            print('Will use ' + use_dir)
            selected_data_to_move = use_dir

        return selected_data_to_move

    def process_delete_data(self):
        """
        This function will process the deletion of data selected
        :return:
        """

        dirs = self.get_dirs(self.source_dir_to_use)

        dirs_available = self.create_dir_dict(dirs)

        selected_data_to_delete = self.display_dir_dict_info(dirs_available)

        self.delete_data(selected_data_to_delete)

    def get_dirs(self, path):
        """
        Provides you with the dirs and files from
        the path being passed
        """

        dirs = glob.glob(path)

        return dirs

    def create_dir_dict(self, dir_list):

        counter = 0
        dir_dict = {}

        for data in dir_list:
            dir_dict[str(counter)] = data
            counter = counter + 1

        return dir_dict

    def display_dir_dict_info(self, dir_dict):

        print()
        print('(Key) - Dir/FileName - [Type]')

        for key, value in dir_dict.items():
            if os.path.isdir(value):
                value_type = '[Dir]'
            else:
                value_type = '[File]'
            print('(' + key + ') - ' + value + ' - ' + value_type)

        print()
        print('Please enter the number of the file or directory you would like to use')
        selected = input('Enter number : ')

        print('You have selected')
        print(dir_dict[selected])

        data_to_mod = dir_dict[selected]
        return str(data_to_mod)

    def display_move_dir_dict_info(self, dir_dict):

        print()
        print('(Key) - Dir/FileName - [Type]')

        for key, value in dir_dict.items():
            if os.path.isdir(value):
                value_type = '[Dir]'
            else:
                value_type = '[File]'
            print('(' + key + ') - ' + value + ' - ' + value_type)

        print()
        print('Please enter the number of the file or directory you would like to use')
        selected = input('Enter number : ')

        data_to_mod = dir_dict[selected]
        print('You have selected')
        print(data_to_mod)

        print('Would you like to select a sub directory of ' + data_to_mod + '?')

        return str(data_to_mod)

    def move_data(self, data_to_move):
        """
        Function to move data
        :param data_to_move:
        :return:
        """

        print('You\'ve selected to move : ' + data_to_move)
        print('You can move to the availble directories:')

        dest_dir = self.config.get('settings', 'dest_dir')

        move_to_dir = self.get_selected_data(dest_dir)

        keep_looking = True

        while keep_looking:
            print()
            print('Would you like to select a subdirectory from ' + move_to_dir + '?')
            answer = input('Please enter "y" for Yes or "n" for No : ')
            if answer == 'y' or answer == 'Y':
                keep_looking = True
                move_to_dir = self.get_selected_data(os.path.join(move_to_dir, '*'))
            else:
                keep_looking = False
                break

        print()
        print('You are about to move the data.')
        answer = input('Please enter "y" to proceed, or "n" to select a different option : ')

        if answer == 'y' or answer == 'Y':
            try:
                print()
                print('Moving ' + data_to_move)
                print('to')
                print(move_to_dir)
                shutil.move(data_to_move, move_to_dir)
                print('File or Directory move was successful!')
                print()
                self.ask_to_continue('move')
            except ValueError as e:
                print('Could not move ' + data_to_move)
                print('to')
                print(move_to_dir)
                print(e.args[0])
        else:
            self.ask_to_continue('move')

    def rename_data(self, data_to_modify):

        len_last_fwd_slash = data_to_modify.rfind('/')

        dir_path = data_to_modify[:len_last_fwd_slash]

        print()
        new_name = input('Enter new name :')

        new_name_with_path = os.path.join(dir_path, new_name)

        # Do a rename of the folder here
        # Ask first though
        print()
        print('Would you like to rename :')
        print(data_to_modify)
        print('With : ' + new_name_with_path)
        answer = input('Enter y for Yes or n for No : ')

        if answer == 'y' or answer == 'Y':
            try:
                print()
                print('Attempting to rename to...')
                print(new_name_with_path)
                os.rename(data_to_modify, new_name_with_path)
                print('Renaming was succesful!')
            except ValueError as e:
                print('Could not rename')
                print(e)

            # Lets call the section that deletes uneeded data here
            # if the data is in a directory
            # Lets call it with a try/except to capture errors

            if os.path.isdir(new_name_with_path):

                print('')
                print('Would you like to rename sub files and directories of : ')
                print(new_name_with_path)
                answer = input('Enter "y" for Yes or "n" for "No" : ')
                print()

                if answer == 'y' or answer == 'Y':
                    print('Attempting to rename valid sub files and directories...')
                    look_for = os.path.join(new_name_with_path, '*')
                    files_in_dir = self.get_dirs(look_for)

                    for data in files_in_dir:
                        # Gonna delete the files that we don't need
                        self.delete_excluded_files(data)
                        self.rename_included_files(data, new_name)
                else:
                    print('Sub files and directories will not be renamed.')

            # Add logic here to ask if you would like
            # to rename another file or quit
            self.ask_to_continue('rename')

        else:
            print('No worries, you can run program at a later time.')
            print('Exiting...')
            sys.exit()

    def delete_data(self, data_to_delete):
        """
        Function to deleted data being passed
        :param data_to_delete:
        :return:
        """

        print('Attempting to delete :')
        print(data_to_delete)

        try:

            if os.path.isdir(data_to_delete):
                print()
                shutil.rmtree(data_to_delete)
                print('Directory was removed.')

            else:
                print()
                os.remove(data_to_delete)
                print('File was removed.')

            # Will ask to continue with another delete
            self.ask_to_continue('delete')

        except ValueError as e:
            print('Something went wrong trying to delete ' + data_to_delete)
            print(e)

    def ask_to_continue(self, process_type):
        print()
        print('Would you to like ' + process_type + ' another file or directory?')
        answer = input('Enter "y" for Yes, "q" for Quit or "e" for Something Else : ')
        if answer == 'y' or answer == 'Y':
            if process_type == 'delete':
                self.process_delete_data()
            elif process_type == 'move':
                self.process_move_data()
            elif process_type == 'rename':
                self.process_rename_data()
            else:
                assert process_type == 'rename' or process_type == 'move' or process_type == 'delete', 'process_type can only have a value of rename, move or delete'

        elif answer == 'e' or answer == 'E':
            self.main()
        else:
            print('Exiting program...')
            sys.exit()

    def delete_excluded_files(self, file_location):

        exclude_types = self.config.get('settings', 'exclude_types')

        exclude = exclude_types.split(',')

        for file_type in exclude:

            if str(file_location).endswith(file_type):
                print('Will delete file : ')
                print(file_location)
                try:
                    print()
                    os.remove(file_location)
                    print('File was removed.')
                except ValueError as e:
                    print('Something went wrong trying to delete the file')
                    print(file_location)
                    print(e)

    def rename_included_files(self, file_location, new_name):

        # Put in the data for dir well be using for the rename
        len_last_fwd_slash = file_location.rfind('/')

        old_data_name = file_location[len_last_fwd_slash:]
        dir_path = file_location[:len_last_fwd_slash]

        include_types = self.config.get('settings', 'include_types')

        include = include_types.split(',')

        for file_type in include:

            if str(file_location).endswith(file_type):

                # if os.path.isdir(file_location):
                print('Will rename : ')
                print(file_location)
                try:
                    print()
                    new_name_with_path = os.path.join(dir_path, new_name + '.' + file_type)
                    os.rename(file_location, new_name_with_path)
                    print('File was renamed to :')
                    print(new_name_with_path)

                except ValueError as e:
                    print('Something went wrong trying to rename the file')
                    print(file_location)
                    print(e)


if __name__ == '__main__':
    FileMaintenance().main()
