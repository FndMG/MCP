from core.call_api import call_api
from common.decorator import log_function_call
from tools.toolbase import ToolsBase, tool
from config.endpoints.system2 import System2Endpoints


class UserTools(ToolsBase):
    @log_function_call
    @tool
    async def get_user_list(self) -> dict:
        """
        Get a list of users.

        Returns:
            UserList
        """
        result = await call_api(http_method="GET", api_url=System2Endpoints.USER_LIST_URL)
        return result

    @log_function_call
    @tool
    async def get_user_detail(self, user_id: str) -> dict:
        """
        Get user details.

        Args:
            user_id: User ID

        Returns:
            UserDetail
        """
        url = f"{System2Endpoints.USER_DETAIL_URL}/{user_id}"
        result = await call_api(http_method="GET", api_url=url)
        return result
