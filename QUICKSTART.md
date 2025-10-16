# Quick Start Guide / 快速开始指南

## 中文版

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/xfdb88/solid-carnival.git
cd solid-carnival

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 2. 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 Instagram 账号和密码
# 使用任何文本编辑器，例如：
nano .env
# 或
vim .env
```

在 `.env` 文件中设置：
```
INSTAGRAM_USERNAME=你的用户名
INSTAGRAM_PASSWORD=你的密码
```

### 3. 准备数据

在 `data/input.csv` 文件中添加要抓取的用户名：
```csv
username
instagram
natgeo
cristiano
```

### 4. 运行

```bash
# 使用默认配置运行
python -m instagram_scraper.cli

# 或指定自定义输入输出文件
python -m instagram_scraper.cli -i data/my_users.csv -o data/my_results.csv
```

### 5. 查看结果

结果将保存在 `data/output.csv` 文件中。

---

## English Version

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/xfdb88/solid-carnival.git
cd solid-carnival

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your Instagram credentials
# Use any text editor, for example:
nano .env
# or
vim .env
```

Set in `.env` file:
```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### 3. Prepare Data

Add usernames to scrape in `data/input.csv`:
```csv
username
instagram
natgeo
cristiano
```

### 4. Run

```bash
# Run with default configuration
python -m instagram_scraper.cli

# Or specify custom input/output files
python -m instagram_scraper.cli -i data/my_users.csv -o data/my_results.csv
```

### 5. View Results

Results will be saved in `data/output.csv`.

---

## Advanced Usage / 高级使用

### Install as Package / 作为包安装

```bash
pip install .
# 或
python setup.py install

# 然后可以直接运行
instagram-scraper
```

### Run Tests / 运行测试

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Using Proxy / 使用代理

在 `.env` 文件中设置代理：
```
PROXY_URL=http://proxy.example.com:8080
```

### Adjust Rate Limiting / 调整速率限制

在 `.env` 文件中：
```
RATE_LIMIT_DELAY=3  # 每次请求间隔（秒）
MAX_RETRIES=5       # 最大重试次数
RETRY_DELAY=10      # 重试延迟（秒）
```

### Logging / 日志

日志文件保存在 `logs/` 目录，文件名格式：`scraper_YYYYMMDD_HHMMSS.log`

查看日志级别选项：
- DEBUG: 详细调试信息
- INFO: 常规信息（默认）
- WARNING: 警告信息
- ERROR: 错误信息

在 `.env` 中设置：
```
LOG_LEVEL=DEBUG
```

## Troubleshooting / 故障排除

### 问题1：登录失败
- 检查用户名和密码是否正确
- 如果启用了双因素认证，需要手动处理
- 尝试使用代理

### 问题2：抓取失败
- 检查网络连接
- 确认用户名拼写正确
- 查看日志文件获取详细错误信息

### 问题3：速率限制
- 增加 `RATE_LIMIT_DELAY` 的值
- 减少并发请求数量

### 问题4：浏览器安装失败
```bash
# 手动安装 Playwright 浏览器
python -m playwright install chromium

# 如果需要系统依赖
python -m playwright install-deps chromium
```

## Support / 支持

如遇到问题，请在 GitHub Issues 中提问。
