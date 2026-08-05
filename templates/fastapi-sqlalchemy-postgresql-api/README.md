# FastAPI + SQLAlchemy + PostgreSQL API 项目

业务无关的同步 PostgreSQL API 基础项目，提供 FastAPI、SQLAlchemy 2.x、Alembic、Pydantic v2、pytest 和 Ruff 的最小可运行配置，以及响应、错误、探针与请求日志约定。

项目只支持 PostgreSQL，只包含基础设施，不包含业务模型、认证、任务队列、缓存、WebSocket、Docker 或 CI。

## 环境要求

- Python 3.12
- uv
- 执行迁移或数据库集成测试时，需要可访问的 PostgreSQL

## 快速开始

先安装依赖并创建本地配置：

```bash
uv sync --locked
cp .env.example .env
```

编辑 `.env`，填写一个**已经存在**的 PostgreSQL database 及其可登录用户。首次配置项目、且 `DB_NAME` 指向的新 database 尚不存在时，需要先创建这个数据库：

```bash
# 命令创建数据库示例
createdb -U postgres app
```

将命令中的 `app` 换成 `.env` 的 `DB_NAME`。数据库已存在时跳过此步骤；不要把迁移指向已有业务数据库。

然后运行迁移并启动服务：

```bash
uv run --locked alembic upgrade head
uv run --locked uvicorn app.main:app --reload
```

访问健康检查：

```bash
curl http://127.0.0.1:8000/health
```

预期响应：

```json
{"status":"ok"}
```

访问基础设施与 API 文档：

```text
/health                 # 进程存活
/ready                  # PostgreSQL 就绪
/api/v1/docs            # Swagger UI
/api/v1/redoc           # ReDoc
/api/v1/openapi.json    # OpenAPI Schema
```

`/health` 仅表示应用进程能够响应请求，不访问数据库，也不表示数据库已经就绪。`/ready` 会执行最小的 `SELECT 1`：数据库可用时返回 `{"status":"ok"}`，不可用时返回 `503 {"status":"unavailable"}`；它不执行迁移、建表或业务查询。

业务接口显式使用 `ApiResponse[T]` 返回以下结构，`code` 与 HTTP 状态码一致：

```json
{"code":200,"message":"OK","data":{}}
```

HTTPException、请求校验错误（422）和未处理异常（500）也使用同一外层结构；422 只返回字段位置、消息和类型，500 不暴露内部细节。`HTTPException.detail` 只能是经过审查、可公开的字符串；字典、列表、异常对象或原始输入不会回显。`/health` 与 `/ready` 是运维探针，不使用该业务响应结构。分页仅提供 `Page[T]` 与 `PageParams`（`page`/`size`）类型，业务查询自行实现且必须显式指定稳定排序。

业务 router 在 `src/app/api.py` 聚合，并由 `API_PREFIX` 统一挂载。新增业务端点须使用 APIRouter、tags、summary、Pydantic 请求/响应模型与 `ApiResponse[T]`，修改后验证 OpenAPI Schema。

```text
src/app/
├── core/       # 配置、数据库、响应、错误、日志与 middleware
├── api.py      # 业务 API 聚合
├── health.py   # 根级探针
└── main.py     # 应用装配
```

HTTPException 的 `detail` 仅能填写已经审查、可公开的字符串；dict、list、异常对象或原始第三方响应不会被回显。项目文档未明确时，agent 应直接采用当前业务中立工程默认；涉及公开 API、数据模型、认证/权限、迁移或部署边界的实质歧义，必须先确认，不能以示例业务或空架构层代替决策。开始业务开发或需要增强基础能力时，参见[项目按需扩展指南](docs/项目按需扩展指南.md)。

- `uv sync --locked`：严格按 `uv.lock` 创建或同步项目 `.venv`；依赖声明与锁文件不一致时失败。
- `cp .env.example .env`：创建只属于当前机器的配置文件，随后填写已有 PostgreSQL database 的连接参数。
- `uv run --locked alembic upgrade head`：将**已有** database 升级到最新 migration；它不会创建 PostgreSQL database，可能创建 `alembic_version` 表。
- `uv run --locked uvicorn app.main:app --reload`：在项目虚拟环境启动开发服务，并在源码修改时自动重载。
- `curl http://127.0.0.1:8000/health`：只验证 HTTP health 响应。

当前项目不包含业务模型和 migration revision，因此 `alembic upgrade head` 只验证 Alembic 配置与数据库连接。

## 数据库配置

数据库连接由 `.env` 中的十一项配置提供：

```dotenv
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=app
DB_USER=postgres
DB_PASSWORD=change-me
APP_NAME=FastAPI SQLAlchemy PostgreSQL API
APP_VERSION=1.0.0
API_PREFIX=/api/v1
ENABLE_API_DOCS=true
LOG_LEVEL=INFO
CORS_ORIGINS=[]
```

`API_PREFIX` 统一决定业务 API、Swagger、ReDoc 和 OpenAPI Schema 路径；业务端点只定义资源段，由 `app/api.py` 聚合并在应用入口附加此前缀。`/health` 与 `/ready` 始终是根级运维端点。将 `ENABLE_API_DOCS=false` 会同时关闭 Swagger、ReDoc 与 OpenAPI Schema。`APP_VERSION` 是 OpenAPI 展示版本，不等同于 `pyproject.toml` 的构建产物版本。

`CORS_ORIGINS` 必须是 JSON 字符串数组，例如 `CORS_ORIGINS=["http://localhost:3000","https://example.com"]`。默认空列表不开放跨域，且始终关闭 credentials。

项目通过 SQLAlchemy `URL.create()` 构造 `postgresql+psycopg` URL。不要把真实凭据提交到仓库。

业务端点通过 `get_db` 获得请求级同步 Session；它只在请求结束后关闭 Session，不会自动提交。端点或用例必须显式决定 `commit()` 与 `rollback()`。

增加真实 SQLAlchemy 模型后，确保模型模块已被 `alembic/env.py` 导入，再生成并人工审查迁移：

```bash
uv run --locked alembic revision --autogenerate -m "描述变更"
uv run --locked alembic upgrade head
```

Schema 变更统一通过 Alembic 管理，不在应用启动时调用 `create_all()` 或自动执行迁移。

## 标准命令

安装：

```bash
uv sync --locked
```

开发：

```bash
uv run --locked uvicorn app.main:app --reload
```

静态检查：

```bash
uv run --locked ruff check . && uv run --locked ruff format --check .
```

测试：

```bash
uv run --locked pytest
```

构建：

```bash
uv build
```

默认测试会验证配置、响应/错误契约、探针、请求 ID、`get_db` 生命周期和 `/health`；如果没有显式提供全部 `DB_*`，真实 PostgreSQL 集成测试会明确跳过。使用专用、可丢弃的测试数据库执行完整测试：

```bash
DB_HOST=127.0.0.1 \
DB_PORT=5432 \
DB_NAME=app_test \
DB_USER=postgres \
DB_PASSWORD=change-me \
uv run --locked pytest
```

使用同一组 `DB_*` 单独执行 `uv run --locked alembic upgrade head`，可验证 Alembic 与 PostgreSQL 的连接。迁移可能创建 `alembic_version` 表，不要指向已有业务数据库。

## 运行边界

`uv build` 会在 `dist/` 生成 wheel 和 sdist。非开发模式可直接运行：

```bash
uv run --locked uvicorn app.main:app --host 0.0.0.0 --port 8000
```

进程编排、反向代理、容器和多环境部署应按实际运行平台补充，不属于本项目默认能力。应用使用或生成 `X-Request-ID` 并在响应中回传；访问日志只记录请求 ID、方法、路径、状态与耗时，不记录 query string、body、Authorization、Cookie、数据库 URL 或凭据。
