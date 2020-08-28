import os
import argparse
import pickle
import uuid


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-folder-name',
                        dest='source_folder_name', default='', required=False)
    parser.add_argument('--source-file-name',
                        dest='source_file_name', required=True)

    return parser.parse_args()


def clean_folder_name(folder_name):
    """
    Cleans folders name by removing duplicate '/' as well as leading and trailing '/' characters.
    """
    folder_name = folder_name.strip('/')
    if folder_name != '':
        folder_name = os.path.normpath(folder_name)
    return folder_name


def combine_folder_and_file_name(folder_name, file_name):
    """
    Combine together the provided folder_name and file_name into one path variable.
    """
    combined_name = os.path.normpath(
        f'{folder_name}{"/" if folder_name else ""}{file_name}')
    combined_name = os.path.normpath(combined_name)

    return combined_name


def main():
    args = get_args()
    source_file_name = args.source_file_name
    source_folder_name = clean_folder_name(args.source_folder_name)
    source_full_path = combine_folder_and_file_name(
        folder_name=source_folder_name, file_name=source_file_name)

    file_exists = os.path.exists(source_full_path)

    current_log_id = os.environ.get(
        'SHIPYARD_LOG_ID', 'local' + str(uuid.uuid4()))

    if os.path.exists('shipyard_shared_variables.pickle'):
        with open('shipyard_shared_variables.pickle', 'rb') as file:
            variables = pickle.load(file)
        variables[current_log_id] = file_exists
        with open('shipyard_shared_variables.pickle', 'wb') as file:
            pickle.dump(variables, file, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        variables = {}
        variables[current_log_id] = file_exists
        with open('shipyard_shared_variables.pickle', 'wb') as file:
            pickle.dump(variables, file, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
