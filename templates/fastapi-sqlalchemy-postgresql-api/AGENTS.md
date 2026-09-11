# 项目开发规则

## 底线

- 保持 PostgreSQL-only、同步 SQLAlchemy 2.x 与 Psycopg 3；连接 URL 使用 `postgresql+psycopg`，不因偏好改为异步或增加数据库兼容分支。
- 只按已确认需求增加业务、依赖、基础设施和有真实职责的架构层，不预建空目录或通用抽象。项目须能独立安装、运行、测试和构建。
- 业务 router 经 `src/app/api.py` 与 `API_PREFIX` 挂载，不硬编码 `/api/v1`；`main.py` 只做装配，`core/` 只放基础设施。业务响应使用 `ApiResponse[T]`，探针不包装。
- `/health` 不访问数据库；`/ready` 只检查 PostgreSQL 连通性，不迁移、建表或执行业务查询。
- Schema 只通过 Alembic 变更并人工审查 revision；禁止 `create_all()` 和启动自动迁移。`get_db` 提供请求级同步 Session 且不自动提交，业务显式决定事务提交与回滚。
- 配置统一由 Settings 读取；CORS 默认关闭且禁用 credentials；不随意调整 middleware 顺序。日志与错误不得泄露原始输入、凭据、数据库 URL、Authorization、Cookie、token 或内部异常细节。
- 可可靠推断的低影响工程细节采用最简单方案；公开 API、数据模型、权限、迁移或部署有实质歧义时先定向确认，不自行发明业务或示例数据。

## 按任务阅读与验证

修改前阅读直接相关源码、调用方与测试。下列 Markdown 正文供所有 Agent 按任务读取；Claude 的 `paths` 只是自动加载入口，不限制规则的适用范围，已加载的内容无需重复读取：

- API、响应、分页、探针：`.claude/rules/api.md`。
- 模型、Schema、Session、事务或迁移：`.claude/rules/database.md`；涉及模型或迁移时另读 `alembic/env.py` 与相关 revision。
- 应用装配、配置、日志、middleware、错误处理或依赖：`.claude/rules/infrastructure.md`。
- 行为变化增加最小 pytest，不预建通用 fixture/mock 层；使用现有 Ruff，不引入重复工具。同步受影响的 README、OpenAPI、配置示例与迁移说明。
- 完成前执行 README 的安装、静态检查、测试和构建命令，按实际变更追加迁移、OpenAPI 或外部依赖验证；PostgreSQL 集成测试未执行或跳过时明确报告数据库行为未验证。
