import globals

if __name__ == "__main__":
    try:
        with open(globals.cache_file, 'w') as file:
            file.truncate(0)
        print(f"Cache {globals.cache_file} has been cleared.")
    except Exception as e:
        print(f"Could not clear cache")