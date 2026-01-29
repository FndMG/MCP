from os import getenv
from dotenv import load_dotenv

load_dotenv()


class UserEndpoints:
    PROTOCOL = getenv("PROTOCOL", "http")
    API_HOST_NAME = getenv("API_HOST_NAME")

    if API_HOST_NAME and not API_HOST_NAME.startswith("http"):
        API_BASE_URL = f"{PROTOCOL}://{API_HOST_NAME}"
    else:
        API_BASE_URL = API_HOST_NAME

    USER_LIST_URL = f"{API_BASE_URL}/users"
    USER_DETAIL_URL = f"{API_BASE_URL}/users"
    USER_CREATE_URL = f"{API_BASE_URL}/users"
    USER_UPDATE_URL = f"{API_BASE_URL}/users"
    USER_DELETE_URL = f"{API_BASE_URL}/users"
