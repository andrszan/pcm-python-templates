# PCM Python 项目仓库

本仓库用于存放业务无关、完全自包含的 Python 后端基础架构项目起点。每个目录都应能够独立演进为真实项目。

## 仓库规则

- `main` 保存所有已经由维护者确认的最新项目内容，也是日常开发的默认分支。
- 日常直接在 `main` 修改对应项目目录；不要为每个项目维护长期开发分支。
- 需要独立评审、并行开发或隔离较大变更时，才创建短期分支；完成后合并回 `main`。
- 项目不得依赖仓库根目录文件、其他项目或共享工作区包。

## 项目目录

- [FastAPI + SQLAlchemy + MySQL API](templates/fastapi-sqlalchemy-mysql-api/README.md)：面向独立 MySQL API 服务起步的同步 FastAPI 项目。
- [FastAPI + SQLAlchemy + PostgreSQL API](templates/fastapi-sqlalchemy-postgresql-api/README.md)：面向独立 PostgreSQL API 服务起步的同步 FastAPI 项目。
- [FastAPI + SQLAlchemy + PostgreSQL Async API](templates/fastapi-sqlalchemy-postgresql-async-api/README.md)：面向异步 PostgreSQL API 服务起步的 FastAPI 项目。

项目目录位于 `templates/<project-id>/`，这是仓库的组织方式，不是项目内部的开发概念。
