---
paths:
  - "src/app/core/database.py"
  - "src/app/**/models/**/*.py"
  - "src/app/**/models.py"
  - "src/app/**/model.py"
  - "alembic/**"
  - "alembic.ini"
---

# 数据库与迁移规范

- 保持 PostgreSQL-only、同步 SQLAlchemy 2.x、同步 `Session` 与 Psycopg 3；连接 URL 使用 `postgresql+psycopg`。不增加其他数据库兼容分支，也不把现有 engine、Session 或迁移栈改为异步实现。
- 新模型继承 `app.core.database.Base`。主键、审计、软删除、多租户、金额精度、时区、枚举、索引、外键和级联属于数据语义，存在实质歧义时先确认，不按惯例自行补齐。
- 每次 Schema 变更都确保模型可被 `alembic/env.py` 导入 metadata，生成 revision 并人工审查 nullable、默认值、索引、约束、外键、数据回填与锁表影响；不直接交付未经审查的 autogenerate 输出。
- 禁止用 `Base.metadata.create_all()` 代替迁移，也不在启动、lifespan、测试 fixture 或业务路由中偷偷建表或迁移。迁移是独立发布步骤，涉及部署兼容性时明确迁移与应用版本的先后关系。
- 业务通过 `get_db` 获取请求级同步 Session；依赖只管理创建和关闭，不自动提交。写操作显式 `commit()`，预期数据库异常后，在继续使用 Session 前先 `rollback()`；事务边界围绕明确的业务操作设计。
- 简单端点直接使用 Session，不为分层完整预建 service/repository；只在真实的业务或数据访问复用需求出现时提取。
- PostgreSQL database 必须预先存在；Alembic upgrade 不负责创建 database。使用专用、可丢弃的 PostgreSQL database 验证 migration upgrade，必要时验证 downgrade 或回滚方案，不指向已有业务数据库。连接配置、迁移命令及集成测试方式以 README 为准。
- 当前项目没有业务模型和 revision；此时 `alembic upgrade head` 只验证 Alembic 配置与 PostgreSQL 连接，并可能创建 `alembic_version` 表。
- 未运行真实 PostgreSQL 集成测试或迁移验证时明确报告对应部分未验证；默认 pytest 通过不能代替数据库验证。
