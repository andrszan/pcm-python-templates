---
paths:
  - "src/app/api.py"
  - "src/app/health.py"
  - "src/app/core/responses.py"
  - "src/app/**/routers/**/*.py"
  - "src/app/**/schemas/**/*.py"
  - "src/app/**/router.py"
  - "src/app/**/schemas.py"
---

# API 开发规范

- 新端点使用 `APIRouter`、tags、summary、Pydantic 请求/响应 schema 与明确的 `response_model`；通过 `src/app/api.py` 聚合，资源路径不硬编码版本前缀。
- 业务成功响应显式使用 `ApiResponse[T]`，保留 `code`、`message`、`data` 结构，`code` 与 HTTP 状态码一致；不增加全局自动包装器。错误信息只包含经过审查的公开内容，不将原始输入、SQL、异常对象或第三方错误放入 `HTTPException.detail`。
- 分页复用 `Page[T]` 和 `PageParams`，查询显式稳定排序；`total` 为同一筛选条件下的总数，页码越界默认返回空列表。排序字段由业务语义决定，不预建查询 helper、cursor、CRUD 基类或查询 DSL。
- `/health` 是纯 liveness，不创建 Session、不执行 SQL；`/ready` 仅执行最低限度数据库连通性检查。两者不使用业务响应包装，也不执行迁移、建表或业务查询。
- `main.py` 只做应用装配；业务规则放在资源附近，不放入 `core/`。只有真实且稳定的复用需求出现时，才提取 service/use-case 或 repository。
- 新能力改变公开 HTTP 契约时，先明确路径、字段、状态码、错误语义与权限要求；不要把普通 JSON 响应约定直接套用于文件、流式响应或 Webhook。
- 修改后补充成功路径和明确失败分支的最小测试，验证 OpenAPI Schema 与 docs，同步受影响的 README 契约。路径及开关配置见 README“数据库配置”。
