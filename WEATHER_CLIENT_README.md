# Weather MCP Client

这是一个专门用于与天气查询MCP服务器通信的Python客户端，使用stdio协议进行通信。

## 功能特性

- 🌤️ 连接到基于uvx的天气查询MCP服务器
- 📊 查询任意地点的天气信息
- 🔧 列出服务器上可用的工具
- 💬 交互式聊天模式
- 🛠️ 完整的错误处理和资源清理

## 安装依赖

确保你已经安装了所需的依赖：

```bash
# 安装项目依赖
pip install -e .

# 或者直接安装所需包
pip install mcp anthropic python-dotenv
```

## 使用方法

### 1. 基本使用

```python
from mcp_stdio_client import WeatherMCPClient
import asyncio

async def main():
    client = WeatherMCPClient()
    
    try:
        # 连接到天气服务器
        await client.connect_to_weather_server()
        
        # 查询天气
        result = await client.query_weather("Beijing")
        print(result)
        
    finally:
        await client.cleanup()

asyncio.run(main())
```

### 2. 运行示例脚本

```bash
# 运行基本示例
python weather_client_example.py

# 运行交互式模式
python weather_client_example.py --interactive
```

### 3. 直接运行客户端

```bash
# 启动交互式天气客户端
python mcp_stdio_client.py
```

## 交互式命令

在交互式模式下，你可以使用以下命令：

- **输入地点名称**: 查询该地点的天气（例如：`Beijing`, `New York`, `London`）
- **`tools`**: 列出服务器上所有可用的工具
- **`quit`**: 退出客户端

## 服务器要求

此客户端设计用于与以下命令启动的MCP服务器通信：

```bash
uvx --from git+https://github.com/Zero-Hero-ing/Zero-Hero-ing.git query_weather
```

确保你的系统上已安装：
- `uvx` (通常通过 `pip install uv` 安装)
- 网络连接以访问GitHub仓库

## 示例输出

```
🚀 Starting Weather MCP Client Example

1. Connecting to weather server...
Connecting to weather MCP server...
✅ Connected successfully! Available tools: ['query_weather']

🔧 Tool: query_weather
   Description: Query weather information for a location

2. Listing available tools...

📋 Available Tools:
1. query_weather
   Description: Query weather information for a location

3. Querying weather for example locations...

--- Weather for Beijing ---
🌤️  Querying weather for 'Beijing' using tool 'query_weather'...
Weather data for Beijing: Temperature 15°C, Condition: Partly Cloudy

--- Weather for New York ---
🌤️  Querying weather for 'New York' using tool 'query_weather'...
Weather data for New York: Temperature 8°C, Condition: Rainy
```

## 错误处理

客户端包含完整的错误处理：

- 连接失败时的详细错误信息
- 工具调用失败的错误处理
- 优雅的资源清理
- 用户中断处理（Ctrl+C）

## API参考

### WeatherMCPClient

主要的客户端类，提供以下方法：

#### `connect_to_weather_server()`
连接到天气MCP服务器

#### `query_weather(location: str) -> str`
查询指定地点的天气信息

#### `list_available_tools()`
列出服务器上所有可用的工具

#### `interactive_chat()`
启动交互式聊天会话

#### `cleanup()`
清理资源和关闭连接

## 故障排除

如果遇到连接问题，请检查：

1. **uvx是否已安装**: `uvx --version`
2. **网络连接**: 确保可以访问GitHub
3. **仓库URL**: 确认 `https://github.com/Zero-Hero-ing/Zero-Hero-ing.git` 可访问
4. **权限**: 确保有执行uvx命令的权限

## 许可证

此项目遵循与主项目相同的许可证。
