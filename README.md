# PCM Python 模板仓库

本仓库用于存放业务无关、完全自包含的 Python 后端基础架构模板。

## 仓库规则

- `main` 保存所有已经由维护者确认的最新模板内容。
- 不得直接在 `main` 开发模板。
- 每个具体模板使用长期开发分支 `template/<template-id>`。
- 开始开发前，先将最新 `main` 合入对应模板分支。
- 模板不得依赖仓库根目录文件、其他模板或共享工作区包。

## 模板目录

- [FastAPI + SQLAlchemy + MySQL API](templates/fastapi-sqlalchemy-mysql-api/README.md)：面向独立 MySQL API 服务起步的业务无关同步 FastAPI 模板。

具体模板存放在：

```text
templates/<template-id>/
```
