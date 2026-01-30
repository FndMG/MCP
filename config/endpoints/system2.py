from os import getenv
from dotenv import load_dotenv

load_dotenv()


class System2Endpoints:
    PROTOCOL = getenv("SYSTEM2_PROTOCOL", "http")
    API_HOST_NAME = getenv("SYSTEM2_HOST_NAME")

    if API_HOST_NAME and not API_HOST_NAME.startswith("http"):
        API_BASE_URL = f"{PROTOCOL}://{API_HOST_NAME}"
    else:
        API_BASE_URL = API_HOST_NAME

    USER_LIST_URL = f"{API_BASE_URL}/users"
    USER_DETAIL_URL = f"{API_BASE_URL}/users"
