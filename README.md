# solid-carnival

一个基于 Playwright 的 Instagram 数据采集工具

## 项目结构

```
solid-carnival/
├── LICENSE                    # Apache 2.0 许可证
├── README.md                  # 项目说明文档
├── .env.example              # 环境变量配置示例
├── pyproject.toml            # 项目配置和依赖
├── src/
│   └── igscraper/           # 主要代码包
│       ├── __init__.py      # 包初始化
│       ├── config.py        # 配置管理
│       ├── playwright_login.py  # Playwright 登录
│       ├── parser.py        # HTML 解析器
│       ├── rate_limiter.py  # 速率限制器
│       ├── scraper.py       # 主采集器
│       ├── cli.py           # 命令行接口
│       └── log.py           # 日志配置
├── data/
│   ├── input.csv            # 输入数据文件
│   └── output.csv           # 输出数据文件
└── tests/
    ├── test_parser.py       # 解析器测试
    └── test_rate_limiter.py # 速率限制器测试
```

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/xfdb88/solid-carnival.git
cd solid-carnival
```

2. 安装依赖：
```bash
pip install -e ".[dev]"
```

3. 安装 Playwright 浏览器：
```bash
playwright install chromium
```

## 配置

1. 复制 `.env.example` 为 `.env`：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 Instagram 凭证：
```
IG_USERNAME=your_username
IG_PASSWORD=your_password
```

## 使用

### 初始化项目
```bash
igscraper init
```

### 采集单个用户资料
```bash
igscraper profile <username>
```

### 批量采集用户资料
```bash
igscraper scrape -i data/input.csv -o data/output.csv
```

## 运行测试

```bash
pytest tests/ -v
```

## 功能特性

- ✅ 基于 Playwright 的浏览器自动化
- ✅ Instagram 登录管理
- ✅ 用户资料数据采集
- ✅ 速率限制功能
- ✅ HTML 解析器
- ✅ CSV 数据导入导出
- ✅ 命令行接口
- ✅ 完整的单元测试

## 许可证

Apache License 2.0
