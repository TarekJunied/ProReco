import os

def print_newest_output():
    folder_path = "./outputs"
    try:
        # Check if the folder path exists
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return

        # Get a list of all .txt files in the folder
        txt_files = [filename for filename in os.listdir(folder_path) if filename.endswith(".txt")]

        # Check if there are any .txt files
        if not txt_files:
            print("No .txt files found in the folder.")
            return

        # Find the newest .txt file based on creation time
        newest_file = max(txt_files, key=lambda filename: os.path.getctime(os.path.join(folder_path, filename)))

        # Construct the full path to the newest file
        file_path = os.path.join(folder_path, newest_file)

        # Read and print the content of the newest file
        with open(file_path, 'r') as file:
            file_contents = file.read()
            print(f"Contents of the newest file '{newest_file}':")
            print(file_contents)
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to print the newest file in the folder
def start_job():
    #TODO: add some monitoring functions to this
    command = "sbatch jobscript.sh"


print_newest_output()