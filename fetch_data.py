import os
import logging
import json
import xml.etree.ElementTree as ET


# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

def read_files_from_folder(folder_path):
    """
    Reads the files from the specified folder path.

    Args:
        folder_path (str): The path of the folder containing the files.

    Returns:
        list: A list of file names in the folder.

    Raises:
        OSError: If there is an error reading the files from the folder.
    """
    try:
        files = os.listdir(folder_path)
        return files
    except OSError as e:
        logging.error(f"Error reading files from folder: {e}")
        return []

def parse_orphanet_xml(file_path):
    """
    Parses an XML file containing Orphanet data.

    Args:
        file_path (str): The path of the XML file.

    Returns:
        list: A list of dictionaries containing the name and OrphaCode of each disorder.

    Raises:
        ET.ParseError: If there is an error parsing the XML file.
        FileNotFoundError: If the specified file is not found.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        diseases = []
        for disorder in root.findall('.//Disorder'):
            name = disorder.find('.//Name[@lang="en"]')
            orpha_code = disorder.find('.//OrphaCode')
            if name is not None and orpha_code is not None:
                diseases.append({'name': name.text, 'orpha_code': orpha_code.text})
        return diseases
    except ET.ParseError as e:
        logging.error(f"Error parsing XML file: {e}")
        return []
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return []

def main():
    """
    Main function that reads XML files from a folder, parses them, and saves the results as JSON.

    Returns:
        None
    """
    diseases_dict = {}
    for file in read_files_from_folder('Rare_Diseases'):
        if file.endswith('.xml'):
            diseases = parse_orphanet_xml('Rare_Diseases/' + file)
            file_name = file.split('.')[0]
            diseases_dict[file_name] = diseases

    # Dump diseases_dict as JSON
    with open('Diseases_list.json', 'w') as f:
        json.dump(diseases_dict, f)

if __name__ == "__main__":
    main()



        