import os

def clear_imported_files(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Ask user for confirmation
        user_input = input(f"Chces vycistit subor{file_path}? (ano/nie): ").strip().lower()
        
        if user_input == 'ano':
            # Open the file in write mode to clear its contents
            with open(file_path, 'w') as file:
                file.write("")  # Write empty string to clear the file content
            print(f"Súbor {file_path} bol vycisteny.")
        else:
            print("nevycistil si subor")
    else:
        print(f"Subor {file_path} neexistuje.")

def main():
    imported_files_file = 'imported_files.txt'
    clear_imported_files(imported_files_file)

if __name__ == '__main__':
    main()
