# FastAPI + SQLAlchemy + PostgreSQL Async 模板协作规则

## 工作模式

- **模板维护模式**：当前目录仍属于 PCM 模板仓库时，保持模板业务中立，不加入用户、权限、订单、Todo 等业务模型、路由、数据或流程。
- **派生项目开发模式**：模板复制到独立项目后，可根据用户已确认的需求实现业务；仍不预建未确认的业务、依赖、基础设施或空架构层。

## 阅读与边界

- 修改前阅读 `README.md`、`pyproject.toml`、直接相关源码、`alembic/env.py` 和测试。
- 使用 `app/api.py` 聚合业务 router，并由 `API_PREFIX` 统一挂载；不得在业务路径中硬编码 `/api/v1`，也不创建 `api/v1`、service、repository、unit-of-work 或其他尚无真实职责的抽象。
- `core/` 只放配置、数据库、响应、错误、日志和 middleware；`main.py` 只创建应用、注册基础设施并挂载 router。没有真实业务职责时，不创建 models、schemas、services、repositories 或 routers 目录。
- 模板必须在目录被单独复制后仍可独立安装、运行、测试和构建。

## 数据库与配置

- 模板只支持 PostgreSQL，保持 SQLAlchemy 2.x AsyncIO、AsyncSession 和 asyncpg；不得加入同步 fallback、其他数据库或多驱动兼容分支。
- Schema 变更只通过 Alembic 管理，不使用 `Base.metadata.create_all()`，也不在应用启动时自动迁移。
- 生成 migration 后必须人工审查；新增模型时确保 Alembic 能导入对应 metadata。Alembic online 连接使用 async engine，但 revision 中的 `upgrade()` 和 `downgrade()` 保持同步函数。
- `/health` 是纯 liveness，不创建 Session、不执行 SQL，也不承担 readiness；`/ready` 只做最低限度的异步数据库连通性检查，不执行迁移、建表或业务查询。
- 业务接口显式使用 `ApiResponse[T]` 的 `code`、`message`、`data` 结构，`/health` 和 `/ready` 不使用该包装；分页只使用现有 `Page[T]` 与 `PageParams` 类型，不预建查询 helper。
- 业务接口通过 `get_db` 取得请求级 AsyncSession，并显式 `await commit()` 或 `await rollback()`；不得自动提交，也不得在并发 task 之间共享同一个 AsyncSession。
- `LOG_LEVEL`、`CORS_ORIGINS`、`APP_NAME`、`APP_VERSION`、`API_PREFIX`、`ENABLE_API_DOCS` 与数据库配置都通过 Settings 读取；docs、redoc、OpenAPI Schema 必须从 `API_PREFIX` 派生，关闭文档时三项一起关闭。CORS 只能使用 JSON allowlist，默认关闭且不得开启 credentials。
- 错误响应与日志不得回显原始输入、密码、数据库 URL、Authorization、Cookie、token 或内部异常细节；请求 ID 仅接受 `[A-Za-z0-9._-]{1,128}`。
- 不要随意调整 request-id/access、CORS、异常边界的中间件顺序。

## 模糊需求处理

- 能从项目文档、上下文和模板契约可靠推断时，采用满足目标的最简单业务中立方案；不要机械追问低影响工程细节。
- 新业务接口使用 `APIRouter`、tags、summary、Pydantic 请求/响应 schema 和 `ApiResponse[T]`；修改后验证 OpenAPI Schema 与 docs。
- 列表分页必须显式稳定排序，`total` 表示同一筛选条件后的总数；页码越界默认返回空列表，不预建 cursor、CRUD 基类或查询 DSL。
- 新增模型必须使用现有 `Base`，每次 Schema 变化都生成并人工审查 Alembic revision；依赖数据库生成值时显式 `await session.refresh()`。
- 若公开 API 契约、主键/审计/软删除、多租户、认证/权限、金额/时区、索引/级联、迁移策略或部署拓扑存在实质歧义，先提出定向问题；不得自行发明业务模型、示例数据或流程。

## 质量与验证

- 行为变化只增加覆盖该行为的最小 pytest，不为测试预建通用 fixture 或 mock 层。
- 使用 Ruff 处理格式、lint 和导入顺序，不额外引入重复工具。
- 完成修改前执行 README 中的 install、check、test 和 build 命令。
- PostgreSQL 集成测试未执行或被跳过时必须明确报告，不得表述为数据库验证已通过。
