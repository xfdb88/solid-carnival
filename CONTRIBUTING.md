# Contributing to Instagram Scraper / 贡献指南

感谢您对本项目的关注！欢迎提交贡献。

Thank you for your interest in this project! Contributions are welcome.

## 贡献方式 / How to Contribute

### 报告问题 / Reporting Issues

如果您发现 bug 或有功能建议，请：

If you find a bug or have a feature suggestion:

1. 检查是否已有类似的 issue
2. 创建新的 issue，详细描述问题或建议
3. 如果是 bug，请提供：
   - 操作系统和 Python 版本
   - 错误信息和堆栈跟踪
   - 复现步骤

### 提交代码 / Submitting Code

1. Fork 本仓库
2. 创建功能分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. 进行更改并遵循代码风格

4. 添加或更新测试：
   ```bash
   pytest tests/
   ```

5. 更新文档（如果需要）

6. 提交更改：
   ```bash
   git commit -m "描述你的更改"
   ```

7. 推送到您的 fork：
   ```bash
   git push origin feature/your-feature-name
   ```

8. 创建 Pull Request

## 代码规范 / Code Standards

### Python 风格 / Python Style

- 遵循 PEP 8 规范
- 使用有意义的变量名
- 添加类型提示（Type hints）
- 为复杂逻辑添加注释

### 测试 / Testing

- 为新功能添加单元测试
- 确保所有测试通过
- 保持测试覆盖率

运行测试：
```bash
pytest tests/ -v --cov=instagram_scraper
```

### 文档 / Documentation

- 更新 README.md（如果添加新功能）
- 为函数和类添加 docstring
- 更新 QUICKSTART.md（如果改变使用方式）

## 开发环境设置 / Development Setup

1. 克隆仓库：
   ```bash
   git clone https://github.com/xfdb88/solid-carnival.git
   cd solid-carnival
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. 安装开发依赖：
   ```bash
   pip install -r requirements-dev.txt
   playwright install chromium
   ```

4. 配置 .env 文件：
   ```bash
   cp .env.example .env
   # 编辑 .env，填入测试账号
   ```

## Pull Request 指南 / Pull Request Guidelines

### 好的 PR 应该包含 / A good PR should include:

- 清晰的描述
- 相关的测试
- 文档更新
- 单一的关注点（不要混合多个不相关的更改）

### PR 标题格式 / PR Title Format:

- `feat: 添加新功能` / `feat: Add new feature`
- `fix: 修复bug` / `fix: Fix bug`
- `docs: 更新文档` / `docs: Update documentation`
- `test: 添加测试` / `test: Add tests`
- `refactor: 重构代码` / `refactor: Refactor code`
- `style: 代码格式` / `style: Code style`
- `chore: 其他更改` / `chore: Other changes`

## 注意事项 / Important Notes

### 合规性 / Compliance

⚠️ 所有贡献都必须遵守以下原则：

All contributions must comply with:

1. 不得添加绕过 Instagram 安全措施的代码
2. 不得添加恶意功能
3. 保持教育和研究目的
4. 尊重用户隐私
5. 遵守 Instagram 服务条款

1. Do not add code to bypass Instagram security measures
2. Do not add malicious features
3. Maintain educational and research purpose
4. Respect user privacy
5. Comply with Instagram Terms of Service

### 代码审查 / Code Review

- 维护者会审查所有 PR
- 可能会要求修改
- 请耐心等待反馈
- 保持讨论专业和友好

## 许可 / License

提交贡献即表示您同意您的代码将以 MIT 许可证发布。

By submitting a contribution, you agree that your code will be released under the MIT License.

## 问题？ / Questions?

如有疑问，请：

If you have questions:

- 查看现有的 issues 和 discussions
- 创建新的 issue 提问
- 在 PR 中讨论

---

再次感谢您的贡献！ / Thank you again for your contribution!
