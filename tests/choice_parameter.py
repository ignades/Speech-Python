import sys
import argparse
from typing import List, Optional

class ParameterPassingDemo:
    def __init__(self):
        """Initialize the demo class with various parameter passing methods"""
        pass

    def basic_argv_method(self):
        """
        Basic method using sys.argv for parameter passing
        Usage: python script.py param1 param2
        """
        # Check if sufficient arguments are provided
        if len(sys.argv) < 3:
            print("Usage: python script.py param1 param2")
            sys.exit(1)

        # Access parameters
        param1 = sys.argv[1]
        param2 = sys.argv[2]

        print(f"Basic argv Method:")
        print(f"Parameter 1: {param1}")
        print(f"Parameter 2: {param2}")
        return param1, param2

    def argparse_method(self):
        """
        Advanced method using argparse for flexible parameter passing
        Usage: python script.py --name John --age 30 --city "New York"
        """
        # Create argument parser
        parser = argparse.ArgumentParser(description="Demonstrate parameter passing")

        # Add arguments with different types and optionality
        parser.add_argument('--name', type=str, help='Name of the person', required=True)
        parser.add_argument('--age', type=int, help='Age of the person', default=None)
        parser.add_argument('--city', type=str, help='City of residence', default='Unknown')
        parser.add_argument('--skills', nargs='+', help='List of skills', default=[])

        # Parse arguments
        args = parser.parse_args()

        print(f"\nArgparse Method:")
        print(f"Name: {args.name}")
        print(f"Age: {args.age}")
        print(f"City: {args.city}")
        print(f"Skills: {args.skills}")

        return vars(args)

    def interactive_input_method(self):
        """
        Interactive method for parameter input
        Usage: python script.py
        """
        print("\nInteractive Input Method:")

        # Collect parameters interactively
        name = input("Enter your name: ")

        # Input validation for age
        while True:
            try:
                age = int(input("Enter your age: "))
                break
            except ValueError:
                print("Please enter a valid number for age.")

        # Multiple input for skills
        skills = []
        while True:
            skill = input("Enter a skill (or press Enter to finish): ")
            if not skill:
                break
            skills.append(skill)

        print(f"\nCollected Information:")
        print(f"Name: {name}")
        print(f"Age: {age}")
        print(f"Skills: {skills}")

        return {
            'name': name,
            'age': age,
            'skills': skills
        }

    def custom_decorator_method(self, required_params: List[str] = None):
        """
        Custom method with decorator for parameter validation
        Usage: Demonstrates runtime parameter checking
        """
        def parameter_validator(func):
            def wrapper(*args, **kwargs):
                # Check if all required parameters are present
                if required_params:
                    missing_params = [
                        param for param in required_params
                        if param not in kwargs
                    ]

                    if missing_params:
                        raise ValueError(f"Missing required parameters: {missing_params}")

                return func(*args, **kwargs)
            return wrapper

        @parameter_validator
        def process_data(name: Optional[str] = None,
                         age: Optional[int] = None,
                         city: Optional[str] = None):
            """Internal method to process validated parameters"""
            print("\nCustom Decorator Method:")
            print(f"Name: {name}")
            print(f"Age: {age}")
            print(f"City: {city}")
            return {'name': name, 'age': age, 'city': city}

        return process_data

def main():
    # Create an instance of the demo class
    demo = ParameterPassingDemo()

    # Print available methods
    print("\nAvailable Parameter Passing Methods:")
    print("1. Basic sys.argv Method")
    print("2. Argparse Method")
    print("3. Interactive Input Method")
    print("4. Custom Decorator Method")

    # Method selection
    method_choice = input("\nSelect a method (1-4): ")

    try:
        if method_choice == '1':
            # Basic argv method requires command-line arguments
            demo.basic_argv_method()

        elif method_choice == '2':
            # Argparse method (run with additional arguments)
            demo.argparse_method()

        elif method_choice == '3':
            # Interactive input method
            demo.interactive_input_method()

        elif method_choice == '4':
            # Custom decorator method
            validator = demo.custom_decorator_method(['name', 'age'])
            validator(name="Alice", age=30, city="London")

        else:
            print("Invalid method selection!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
