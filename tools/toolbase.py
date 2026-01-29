def tool(func):
    func._is_tool = True
    return func

class ToolsBase:
    def get_tools_list(self):
        tools = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and getattr(attr, "_is_tool", False):
                tools.append(attr)
        return tools
