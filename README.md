# Instagram Profile Scraper

一个用于抓取 Instagram 公开用户资料的 Python 爬虫工具。

## ⚠️ 重要声明 / Important Notice

**本项目仅用于教育和研究目的。使用本工具时，您必须遵守以下规定：**

### 合规要求 / Compliance Requirements

1. **仅限公开数据**: 本工具仅用于抓取公开可见的 Instagram 用户资料信息
2. **遵守服务条款**: 使用前请确保您已阅读并同意 [Instagram 服务条款](https://help.instagram.com/581066165581870)
3. **尊重隐私**: 不得用于侵犯用户隐私或用于任何非法目的
4. **遵守速率限制**: 工具内置速率限制以避免对 Instagram 服务造成负担
5. **个人使用**: 本工具仅供个人学习研究使用，不得用于商业目的

**This project is for educational and research purposes only. By using this tool, you must comply with:**

1. **Public Data Only**: This tool only scrapes publicly visible Instagram profile information
2. **Terms of Service**: Ensure you have read and agree to [Instagram Terms of Service](https://help.instagram.com/581066165581870)
3. **Privacy Respect**: Do not use for privacy violation or illegal purposes
4. **Rate Limiting**: Built-in rate limiting to avoid burdening Instagram services
5. **Personal Use**: For personal learning and research only, not for commercial use

### 免责声明 / Disclaimer

使用本工具的风险由使用者自行承担。作者不对因使用本工具而导致的任何账号封禁、数据丢失或其他问题承担责任。

The user assumes all risks associated with using this tool. The author is not responsible for any account bans, data loss, or other issues resulting from the use of this tool.

---

## 功能特性 / Features

- ✅ 使用 Playwright 进行浏览器自动化和 JavaScript 渲染
- ✅ 使用 httpx + BeautifulSoup4 进行 HTML 解析
- ✅ 从 CSV 文件批量读取用户名
- ✅ 输出结构化的 CSV 数据
- ✅ 内置速率限制和重试机制
- ✅ 支持代理配置
- ✅ 完整的日志记录
- ✅ 命令行界面
- ✅ 单元测试

## 安装 / Installation

### 前置要求 / Prerequisites

- Python 3.9+
- pip

### 步骤 / Steps

1. 克隆仓库:
```bash
git clone https://github.com/xfdb88/solid-carnival.git
cd solid-carnival
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 安装 Playwright 浏览器:
```bash
playwright install chromium
```

4. 配置环境变量:
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 Instagram 凭证
```

## 配置 / Configuration

在 `.env` 文件中配置以下参数：

```env
# Instagram 登录凭证
INSTAGRAM_USERNAME=your_username_here
INSTAGRAM_PASSWORD=your_password_here

# 代理设置（可选）
PROXY_URL=

# 速率限制（秒）
RATE_LIMIT_DELAY=2
MAX_RETRIES=3
RETRY_DELAY=5

# 日志级别
LOG_LEVEL=INFO
```

## 使用方法 / Usage

### 基本用法

1. 在 `data/input.csv` 中添加要抓取的用户名：
```csv
username
instagram
natgeo
```

2. 运行爬虫：
```bash
python -m instagram_scraper.cli
```

### 自定义输入输出文件

```bash
python -m instagram_scraper.cli -i path/to/input.csv -o path/to/output.csv
```

### 命令行选项

```bash
python -m instagram_scraper.cli --help
```

选项说明：
- `-i, --input`: 指定输入 CSV 文件路径（默认：data/input.csv）
- `-o, --output`: 指定输出 CSV 文件路径（默认：data/output.csv）
- `--version`: 显示版本信息

## 输出格式 / Output Format

输出的 CSV 文件包含以下字段：

| 字段名 | 说明 |
|--------|------|
| username | Instagram 用户名 |
| display_name | 显示名称 |
| bio | 个人简介 |
| email | 邮箱（如果公开） |
| phone | 电话（如果公开） |
| links | 外部链接 |
| gender | 性别（如果可推断） |
| age | 年龄（如果可推断） |
| region | 地区（如果可推断） |
| warning_code | 警告代码 |
| error | 错误信息 |

## 项目结构 / Project Structure

```
solid-carnival/
├── instagram_scraper/      # 主要代码
│   ├── __init__.py
│   ├── __main__.py        # 模块入口
│   ├── cli.py             # 命令行接口
│   ├── config.py          # 配置管理
│   ├── logger.py          # 日志配置
│   └── scraper.py         # 爬虫核心逻辑
├── tests/                  # 测试文件
│   ├── __init__.py
│   └── test_scraper.py
├── data/                   # 数据目录
│   ├── input.csv          # 输入文件
│   └── output.csv         # 输出文件（生成）
├── logs/                   # 日志目录
├── .env                    # 环境变量（需创建）
├── .env.example           # 环境变量示例
├── .gitignore
├── LICENSE                # MIT 许可证
├── README.md
└── requirements.txt       # Python 依赖
```

## 测试 / Testing

运行测试：

```bash
pip install pytest pytest-asyncio
pytest tests/
```

## 技术栈 / Tech Stack

- **Playwright**: 浏览器自动化和 JavaScript 渲染
- **httpx**: HTTP 客户端
- **BeautifulSoup4**: HTML 解析
- **python-dotenv**: 环境变量管理
- **tenacity**: 重试机制

## 速率限制 / Rate Limiting

为了遵守 Instagram 的使用政策并避免账号被封，本工具实现了以下机制：

- 每次请求之间有可配置的延迟（默认 2 秒）
- 自动重试机制，使用指数退避策略
- 最大重试次数限制
- 错误记录和处理

## 故障排除 / Troubleshooting

### 登录失败

如果遇到登录问题：
1. 检查 `.env` 文件中的凭证是否正确
2. Instagram 可能启用了双因素认证，需要手动处理
3. 尝试使用代理

### 抓取失败

如果抓取失败：
1. 检查网络连接
2. 确认用户名是否正确
3. 查看日志文件获取详细错误信息

## 许可证 / License

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献 / Contributing

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 联系方式 / Contact

如有问题或建议，请通过 GitHub Issues 联系。

---

**再次提醒**: 请负责任地使用本工具，遵守所有相关法律法规和服务条款。
