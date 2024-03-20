import os
import pandas as pd
import yaml
from typing import Dict, Any, List
import json
from .trace_error import get_exception_info

allowed_image_extensions = ['.jpg', '.jpeg', '.png',".nii",".whl",".dcm",".zip"]
json_required_keys = ["Image ID", "Image Path"]
yaml_keys = ["Image", "Dataset"]
yaml_image_keys = ["path", "extension"]
yaml_dataset_keys = ["annotation","labels","download"]
yaml_allowed_annotations = ["coco","yolo"]

json_data = None
yaml_data = None



"""
*Check if we have Images folder and README file in the same directory
*Check if we have data.yaml and json file in the same directory

*Check if images in Image folder has valid extension 
*Check if required_columns_in_json are valid 

*Check Image Path in json is valid
*Check if required_columns_in_json are unique in json file


*Check if yaml file is valid
    Check if Image and Dataset exists
    Check if Image valid
    Check if Dataset extension is valid
"""



"""

Check if structure is valid

"""

# Check if selected file in folder path
def contains_selected_file_type( folder_path: str, file_type : str ) -> bool:
    """
    Check if a folder is contains selected extension

    Args:
        folder_path (str): The path to the folder to be checked.

    Returns:
        bool: True if the contains selected extension
    """

    try:
        extensions = list()
    
        for filename in os.listdir(os.path.join(os.getcwd(), folder_path)):
            if os.path.isfile(os.path.join(folder_path, filename)):
                file_extension = os.path.splitext(filename)[-1]
                extensions.append(file_extension)

        if file_type in extensions:
            return True
    
        return False
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Checks if we have Images folder and README file in the same directory
# Checks if we have data.yaml and .json file in the same directory
def is_structure_valid() -> bool:
    """
    Check if the folder structure contains mandatory files.

    Args:
        None

    Returns:
        bool: True if all mandatory files exist, False otherwise.
    """
    global json_data
    global yaml_data


    has_readme = False
    has_json = False

    try:
        files_list = os.listdir()

        for file in files_list:
            if "README" in file.upper():
                has_readme = True

        if not "Images" in files_list:
            print("Please Make Sure That You Have 'Images' Folder") 
        
        if not has_readme:
            print("Please Make Sure That You Have 'README' File") 


        # Read json file if exists  
        has_json = contains_selected_file_type("",".json")
        if has_json :
            with open( "data.json", "r") as json_file:
                json_data = json.load(json_file)

        else: 
            print("You may want to add json file")
        
        # Read yaml file if exists  
        has_yaml = contains_selected_file_type("",".yaml")
        if has_yaml:

            with open("data.yaml" , 'r') as file:
                yaml_data = yaml.safe_load(file)

        else:
            print("You may want to add yaml file")
            


        if "Images" in files_list and has_readme:
            return True
        return False
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check if images in Image folder are in valid file type 
def is_image_types_valid(allowed_extensions: list = allowed_image_extensions, images_folder : str = "Images") -> bool:
    """
    Check if images in the 'Images' folder have valid file types.

    Args:
        allowed_extensions (list): A list of allowed image file extensions (default is allowed_image_extensions).
        images_folder (str): The name of the folder containing the images (default is "Images").

    Returns:
        bool: True if all files are in valid type requirements are fulfilled, False otherwise.
    """

    try:
        images_path = os.path.join(os.getcwd(), images_folder)
    
        # List of files which has invalid extensions 
        invalid_files = []
        for filename in os.listdir(images_path):
            if os.path.isfile(os.path.join(images_path, filename)):
                file_extension = os.path.splitext(filename)[-1]
                if file_extension.lower() not in allowed_extensions:
                    invalid_files.append(filename)
        
        # Check if there is any file with invalid extension 
        if len(invalid_files) > 0:
            print(f"The following files in the '{images_folder}' folder have invalid file types:")
            for file in invalid_files:
                print("\t *",file)

            return False
        return True
    
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check if all mandatories are fulfilled
def check_mandatories_valid() -> bool:
    """
    Check if all mandatory requirements are fulfilled.

    Args:
        None

    Returns:
        bool: True if all mandatory requirements are fulfilled, False otherwise.
    """

    try:
            
        if is_structure_valid() and is_image_types_valid(allowed_image_extensions):
            print("Structure is valid")
            return True
        return False
    
    except :
        exception_information = get_exception_info()
        print(exception_information)


"""

Check if json is valid

"""

# Check if json includes valid keys
def is_json_keys_valid(json_file : Dict [Any , Any], checklist : List[str] =  json_required_keys)-> bool:
    """
    Check if the keys in a JSON file match a checklist of required keys.

    Args:
        json_file (Dict[Any, Any]): The JSON file contents as a dictionary.
        checklist (List[str]): Optional list of required keys (default is json_required_keys).

    Returns:
        bool: True if all required keys are present in the JSON file, False otherwise.
    """
    try:
        for key in checklist:
            if not key in json_file.keys():
                print(f"'{key}' Is Required. It Must Be In Json File")
                return False
        return True
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check if all keys has a corresponds
def json_keys_length(json_file : Dict [Any , Any])-> bool:
    """
    Check if all keys in a JSON file have corresponding values with the same length.

    Args:
        json_file (Dict[Any, Any]): The JSON file contents as a dictionary.

    Returns:
        bool: True if all keys have corresponding values with the same length, False otherwise.
    """

    try:
        length = len(list(json_file.values())[0])
        for value in json_file.values():
            if length != len(value):
                print("Length Of The Values Isn't The Same")
                return False        
        return True
    
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check if required_columns_in_json are unique in json file
def is_json_values_unique(json_file : Dict [Any , Any], checklist : List[str] = json_required_keys )-> bool:
    """
    Check if the values associated with keys in a JSON file are unique.

    Args:
        json_file (Dict[Any, Any]): The JSON file contents as a dictionary.
        checklist (List[str]): Optional list of keys to check for uniqueness (default is json_required_keys).

    Returns:
        bool: True if the values associated with all keys in the checklist are unique, False otherwise.
    """

    try:
        for key in checklist:
            if len(json_file[key]) != len(set(json_file[key])):
                print(f"{key} Includes Duplicate Values")
                return False
        return True
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check if paths are valid
def is_image_paths_valid(json_file : Dict [Any , Any])-> bool:
    """
    Check if the paths specified in a JSON file exist.

    Args:
        json_file (Dict[Any, Any]): The JSON file contents as a dictionary.

    Returns:
        bool: True if all paths specified in the JSON file exist, False otherwise.
    """
    try:
        for path in json_file["Image Path"]:
            if not os.path.exists(path):
                print(f"There Is No Such Path : {path}\nBut It Is Given Inside The Json Files")
                return False
        return True
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check all functions
def is_json_valid(json_file : Dict [Any , Any] = json_data) -> bool:
    """
    Check the validity of a JSON file.

    Args:
        json_file (Dict[Any, Any]): The JSON file contents as a dictionary (default is json_data).

    Returns:
        bool: True if the JSON file passes all validity checks, False otherwise.
    """
    # Check if json file exists
    try:

        if len(json_file.keys()) > 0: 
            if is_json_keys_valid(json_file) and is_json_values_unique(json_file) and is_image_paths_valid(json_file) and json_keys_length(json_file) :
                print("Json is valid")
                return True
            return False
        return True
    
    except :
        exception_information = get_exception_info()
        print(exception_information)



"""

Check if yaml is valid 

"""

# Checks if yaml keys are adequate 
def is_yaml_keys_valid(yaml_file : Dict [Any,Any] = yaml_data, check_list : List [str] = yaml_keys) -> bool:
    """
    Check if the keys in a YAML file match a checklist of required keys.

    Args:
        yaml_file (Dict[Any, Any]): The YAML file contents as a dictionary (default is yaml_data).
        check_list (List[str]): Optional list of required keys (default is yaml_keys).

    Returns:
        bool: True if all required keys are present in the YAML file, False otherwise.
    """

    try:
        for key in check_list:
            if not key in yaml_file.keys():
                print(f"'{key}' Is Required. It Must Be In Yaml File")
                return False
        return True
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check if yaml Image is valid 
def is_yaml_image_valid(yaml_file : Dict [Any,Any] = yaml_data, check_list : List [str] = yaml_image_keys) -> bool:
    """
    Check if the image settings in a YAML file are valid.

    Args:
        yaml_file (Dict[Any, Any]): The YAML file contents as a dictionary (default is yaml_data).
        check_list (List[str]): Optional list of keys to check for image settings (default is yaml_image_keys).

    Returns:
        bool: True if the image settings in the YAML file are valid, False otherwise.
    """

    try: 
        for key in check_list:
            if not key in yaml_file["Image"].keys():
                print(f"Your Yaml File Image Key Must Include {key} ")
                return False
            
        if not (os.path.exists(yaml_file["Image"]["path"])) :
            print("Image Path Isn't Exists. Check Your Yaml File")
            return False
        
        if not yaml_file["Image"]["extension"] in allowed_image_extensions:
            print("Your Image Extension Isn't Valid. Check Your Yaml File")
            
        return True
    
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check if yaml Dataset is valid 
def is_yaml_dataset_valid(yaml_file : Dict [Any,Any] = yaml_data, check_list : List [str] = yaml_dataset_keys) -> bool:
    """
    Check if the dataset settings in a YAML file are valid.

    Args:
        yaml_file (Dict[Any, Any]): The YAML file contents as a dictionary (default is yaml_data).
        check_list (List[str]): Optional list of keys to check for dataset settings (default is yaml_dataset_keys).

    Returns:
        bool: True if the dataset settings in the YAML file are valid, False otherwise.
    """

    try:
    # Must include yaml_dataset_keys 
        for key in check_list:
            if not key in yaml_file["Dataset"].keys():
                print(f"Your Yaml File Dataset Key Must Include {key} ")

                return False
            
        # Must be dictionary and have at least one element in it
        if not isinstance(yaml_file["Dataset"]["labels"], dict):
            print("Dataset Must Include Label. Check Your Yaml File")
            return False
        
        # Check if annotation is allowed
        if not yaml_file["Dataset"]["annotation"].lower() in yaml_allowed_annotations:
            print("Your Annotation Isn't Valid. Check Your Yaml File")
            return False
        return True
    
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check if yaml mandatories are fulfilled
def is_yaml_valid() -> bool:
    """
    Check the validity of a YAML file.

    Args:
        None

    Returns:
        bool: True if the YAML file passes all validity checks, False otherwise.
    """

    try:
        # If there is any yaml file 
        if len(yaml_data) > 0 :
            if is_yaml_keys_valid(yaml_data,yaml_keys) and is_yaml_image_valid(yaml_data,yaml_image_keys) and is_yaml_dataset_valid(yaml_data,yaml_dataset_keys):
                print("Yaml file is valid")
                return True
            return False
        return True
    except :
        exception_information = get_exception_info()
        print(exception_information)


# Check the validity of a folder structure and its contents.
def is_folder_valid(given_path : str) -> bool:
    """
    Check the validity of a folder structure and its contents.

    Args:
        given_path (str): The path to the folder to be checked.

    Returns:
        bool: True if the folder structure and its contents pass all validity checks, False otherwise.
    """

    try: 
        print("Given Path : ", given_path)
        os.chdir(given_path)
        print("Path Changed : ",os.getcwd())
        print("List of files: ",os.listdir())
        if  check_mandatories_valid() and is_json_valid(json_data) and is_yaml_valid():
            print("Structure and files are valid")
            return True
        return False
    
    except :
        exception_information = get_exception_info()
        print(exception_information)




if __name__ == "__main__":
    is_folder_valid(os.getcwd())