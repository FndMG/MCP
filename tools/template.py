from core.call_api import call_api
from common.decorator import log_function_call
from tools.toolbase import ToolsBase, tool
from config.endpoint import ApiEndpoints

class TemplateTools(ToolsBase):
    @log_function_call
    @tool
    async def get_template_list(self) -> dict:
        """
        Get a list of templates.

        Returns:
            TemplateList
        """
        result = await call_api(http_method="GET", api_url=ApiEndpoints.TEMPLATE_LIST_URL)
        return result

    @log_function_call
    @tool
    async def get_template_detail(self, template_id: str) -> dict:
        """
        Get template details.

        Args:
            template_id: Template ID

        Returns:
            TemplateDetail
        """
        url = f"{ApiEndpoints.TEMPLATE_DETAIL_URL}/{template_id}"
        result = await call_api(http_method="GET", api_url=url)
        return result
