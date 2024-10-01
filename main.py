import argparse
import sys

from src.validator import YAMLResumeValidator


def main():
    parser = argparse.ArgumentParser(description='Validate a YAML resume file.')
    parser.add_argument('-p', '--path_to_yaml_file', type=str, help='Path to the YAML file to validate.')

    args = parser.parse_args()
    file_path = args.path_to_yaml_file

    if not file_path.endswith('.resume'):
        print("Error: File must have a .resume extension.")
        sys.exit(1)

    try:
        with open(file_path, 'r') as file:
            yaml_string = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except IOError:
        print(f"Error: Unable to read file '{file_path}'.")
        sys.exit(1)

    is_valid, errors = YAMLResumeValidator.check(yaml_string)

    if is_valid:
        print("YAML is valid!")
    else:
        print("YAML is invalid. Errors:")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    main()
