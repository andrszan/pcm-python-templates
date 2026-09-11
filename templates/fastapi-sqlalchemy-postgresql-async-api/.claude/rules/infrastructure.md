---
paths:
  - "src/app/main.py"
  - "src/app/core/config.py"
  - "src/app/core/errors.py"
  - "src/app/core/logging.py"
  - "src/app/core/middleware.py"
  - "src/app/**/dependencies.py"
  - "src/app/**/security.py"
  - "src/app/**/clients/**/*.py"
  - "src/app/**/middleware.py"
  - ".env.example"
  - "pyproject.toml"
  - "uv.lock"
---

# 基础设施规范

- `main.py` 只创建应用、注册基础设施并挂载 router；`core/` 只承担配置、数据库、响应、错误、日志和 middleware，不加入业务专属工具。只有出现真实职责时才增加目录、依赖或架构层。
- 新运行配置统一加入 Settings，不在业务模块读取 `os.environ`；同步 `.env.example`、README 和测试。密钥来自运行环境或秘密管理服务，不写入源码、迁移、测试输出或文档。
- 业务 API、docs、redoc 和 OpenAPI Schema 路径从 `API_PREFIX` 派生；关闭文档时同时关闭后三项。`APP_VERSION` 是 OpenAPI 展示版本，不等同于构建产物版本。
- CORS 仅使用 JSON allowlist，默认关闭且始终禁用 credentials；配置格式和已有环境变量以 README 为准。
- 外部请求 ID 只接受 `[A-Za-z0-9._-]{1,128}`，否则生成新 ID。保持 request-id/access 位于 CORS 和异常边界外层，调整顺序前验证错误响应与跨域行为。
- 访问日志只记录请求 ID、方法、路径、状态和耗时，不记录 query string、body、Authorization、Cookie、token、密码或数据库 URL。错误响应不回显原始输入、异常对象或内部细节；`HTTPException.detail` 只使用经过审查的公开字符串。
- 新依赖必须有真实消费者、明确版本范围、同步锁文件、许可证/安全影响评估及最小测试；不因已安装或文档提及就宣称已接入。缓存、队列、任务、外部服务、Docker、CI 与部署能力只按已确认需求增加。
- 外部服务接入先定义超时、重试、幂等、失败响应、日志与 readiness 影响；多副本部署不依赖进程内共享状态。migration 保持独立发布步骤，应用启动不自动迁移。
- 修改后覆盖配置校验、文档开关、探针或 middleware 中受影响的行为；涉及外部依赖与部署时按实际变更追加专项验证，并明确报告未验证部分。标准检查命令见 README。
