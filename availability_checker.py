from validators import url, ValidationError

def read_urls(path: str) -> list[str]:
    config_file = open(path, "r")
    data = config_file.read()
    
    # convert data into list
    url_list = data.split("\n")
    config_file.close
    
    return url_list

def validate_url(url_string: str) -> bool:
    result = url(url_string)
    if isinstance(result, ValidationError):
        return False
    return True
    
    
if __name__ == "__main__":
    url_strings = read_urls("url-list.txt")
    
    for url_string in url_strings:
        if validate_url(url_string):
            print(f"Valid url {url_string} found")
        else:
            print(f"{url_string} is not valid")