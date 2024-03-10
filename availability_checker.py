from validators import url, ValidationError
from requests import HTTPError, get, ConnectTimeout
from bs4 import BeautifulSoup
import logging
import asyncio, time

async def read_urls(path: str) -> list[str]:
    logging.debug(f"Reading URLs from: {path}")
    config_file = open(path, "r")
    data = config_file.read()
    
    # convert data into list
    url_list = data.split("\n")
    config_file.close
    
    return url_list

async def validate_url(url_string: str) -> bool:
    result = url(url_string)
    if isinstance(result, ValidationError):
        return False
    return True

# we can search for a specific tag content here
async def find_string_in_url(content: bytes, text_to_find: str) -> bool: 
    logging.debug(f"Searching for {text_to_find} within resposne content")
    soup = BeautifulSoup(content, "html.parser")
    found_text = soup.find(string=text_to_find)
    if found_text:
        extracted_text = found_text.text.strip()
        logging.debug(f"Found text {extracted_text} within the website response")
        return True
    logging.debug(f"I could not find {text_to_find}")
    return False

# we assume the string is a fixed thing not dependent on website or this could also be configured to search for a specific string
# later
async def is_url_available(url_string: url) -> tuple[bytes, bool]:
    try: 
        logging.debug(f"Checking availability for {url_string}")
        response = get(url_string, timeout=(20, None))
        logging.debug(f"Processed request in {response.elapsed}")
        if response.status_code in [200, 202, 301, 302, 400, 401, 403, 500, 503]:
            logging.debug(f"{url_string} responded with code {response.status_code}")
            return response.content, True
        else: 
            return response.content, False
    except HTTPError as http_error:
        logging.error(f"Http Error Occurred {http_error}")
        return None, False
    except ConnectTimeout as ce: 
        logging.error(f"Connection timeout occurred {ce}")
        return None, False
    except Exception as exp:
        logging.error(f"Exception occurred {exp}")
        return None, False
    
async def periodic(interval_sec, coroutine_name, *args, **kwargs):
    while True:
        await asyncio.sleep(interval_sec)
        await coroutine_name(*args, **kwargs)

async def read_url_task():
    url_strings = await read_urls("url-list.txt")
    
    for url_string in url_strings:
        if await validate_url(url_string):
            # now let's find some kind of string in the URL
            content, is_valid = await is_url_available(url_string)
            if content is not None and await find_string_in_url(content, "Google"):
                logging.debug(f"Found text in the returned content")
            else:
                logging.debug(f"Text was not found")
        else:
            logging.debug(f"{url_string} is not valid")
    
async def main():
    # create a task and schedule it every x seconds
    # TODO: Add logging
    logging.debug("Creating periodic task")
    await asyncio.create_task(periodic(5, read_url_task))
    await asyncio.sleep(1)

if __name__ == "__main__":
    # set up logging
    logging.basicConfig(filename="availability_checker.log", encoding="utf-8", level=logging.DEBUG, format='%(asctime)s %(message)s')
    asyncio.run(main())
    