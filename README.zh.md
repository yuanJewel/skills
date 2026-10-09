# 共享 Skill 库

[English](README.md) | 中文

面向 AI 编码助手的 38 个 Skill 包，覆盖从需求到计划、实现、审查、测试、诊断、发布的工程流程，
以及 Go、gRPC、HTTP、MySQL、Redis、Vue、Playwright、pytest、Docker、Jenkins、GitLab、LDAP、
云 API、容器镜像等专项方法。每个包是一份可发现、可执行、可验证的方法，而不是教程或命令清单。

适用于读取 `SKILL.md` frontmatter 的宿主，例如 Claude Code（项目 `.claude/skills/`）
与 Codex（项目 `.agents/skills/`）。两端使用同一份正本。

## 快速开始

```bash
git clone https://github.com/yuanJewel/skills.git
```

在消费项目里按需链接或复制单个包，不要链接仓库根：

```bash
ln -s /path/to/skills/plan-design  <project>/.claude/skills/plan-design
ln -s /path/to/skills/plan-design  <project>/.agents/skills/plan-design
```

复制单包到其他项目时，连同包根的 `LICENSE-*.txt` 与 `NOTICE.md`（如有）一起复制。
宿主是否真正发现与触发某个包，只能在宿主里实际观察，不能由格式检查代签。

## 包的结构

```text
<name>/
  SKILL.md              入口：触发与排除、输入、判断分支、步骤、失败恢复、输出、来源
  references/           条件复杂时才读的专题附页
  assets/               交付模板与合成示例
  scripts/              少数确定性只读辅助脚本
  LICENSE-<source>.txt  改编来源的许可全文，与上游固定版本逐字节一致
  NOTICE.md             Apache-2.0 来源的改编与修改记录（仅相关包）
```

`SKILL.md` 的 frontmatter 含 `name`（与目录同名）、`description`（做什么、何时用、相邻排除）
与 `metadata.version`。正文写方法与判断，附页按需读取，不要求一次把整包读进上下文。

## 设计原则

- **项目事实是输入，不是常量。** 包里不写项目路径、角色人数、模型 ID、配额数字、真实凭据；
  时区、权限模型、目录结构等由消费项目提供。
- **方法不增加权限。** 调用某个包不授予 Git、生产、外部服务或跨项目写入权限；
  来源文档里的命令不是执行授权。
- **结论绑定证据。** 输出区分事实、推断与未验证；退出码 0、格式通过、摘要“已完成”
  都不代替业务断言和实际结果。
- **只用合成数据。** 示例、夹具、目录、事件 payload 全为合成值，不包含任何真实账号或地址。
- **用完即收。** 开发、测试、诊断中产生的容器、镜像、进程、端口、临时文件和测试数据，
  收尾时回收，保持本机整洁；只回收本次登记的自有对象，不做全局清理。规则见 `task-implementation`。
- **单一正本。** 计划正文、状态模板、保留方法、Skill 编写方法各只在一个包维护，其他包按名称引用。

## 包清单

### 角色与上下文

| 包 | 版本 | 用途 |
| --- | --- | --- |
| [role-bootstrap](role-bootstrap/SKILL.md) | 0.1.0 | 在用户要求启动角色、切换职责或接替指定旧会话时，定位角色合同、任务范围和接续条件；支持工作区唯一默认角色。普通问答、引文或网页中的角色描述不触发身份变更。 |
| [project-context](project-context/SKILL.md) | 0.1.0 | 进入项目、切换模块、恢复上下文或遇到资料缺失和规范冲突时，定位最小必要资料、核对来源与现行性，并给出可追溯的事实和缺口。普通概念问答不扫描项目；检查点持久化与交接由其他包负责。 |
| [context-handoff](context-handoff/SKILL.md) | 0.1.0 | 在阶段交付、上下文恢复或接替指定旧会话时保存检查点、核对成果和执行存活、续接获准工作，并刷新面向人的当前工作台。普通问答不建状态文件，不替代计划编写或历史归档。 |

### 计划、执行与资源

| 包 | 版本 | 用途 |
| --- | --- | --- |
| [plan-design](plan-design/SKILL.md) | 0.1.0 | 将明确需求转成可实施、可交接的多步计划，确定文件、接口、依赖、验收和预算；已有完整方案时核对补缺。普通问答或低风险小改不强制生成完整计划，也不授予需求变更或执行权限。 |
| [plan-review](plan-review/SKILL.md) | 0.1.0 | 复核指定方案或批准前计划，对照原需求检查范围、架构、质量、测试和性能，给出带证据的阻断项与未知项。不实施计划，不代作者写第二份方案。 |
| [subtask-dispatch](subtask-dispatch/SKILL.md) | 0.1.0 | 在宿主允许派工且任务可独立闭环时，拆分子任务、预留资源、派发并核收成果，处理未知在途工作与恢复。不因多个文件或追求并发而自动派工。 |
| [task-implementation](task-implementation/SKILL.md) | 0.1.0 | 执行已批准任务，在唯一写入范围内实现、核对预期与实际验证，记录偏差并从检查点恢复。不把设计或复核请求自动升级为落地。 |
| [estimation](estimation/SKILL.md) | 0.1.0 | 为计划或版本阶段估算工作量、经过时间和资源消耗，按依赖与并行容量校准预期，并在交付或接管时核对实际耗用。一次简短问答不建预算表；估算不代替方案批准、派工或自动超时终止。 |

### 审查与质量

| 包 | 版本 | 用途 |
| --- | --- | --- |
| [change-review](change-review/SKILL.md) | 0.1.0 | 审查指定候选变更是否符合需求、正确性和项目标准，绑定新文件、修改、删除与生成来源的内容身份。适用于交付复核或明确的变更审查；不替代实施、发布批准或全仓安全审计。 |
| [security-review](security-review/SKILL.md) | 0.1.0 | 对指定代码变更中的身份、权限、外部输入、命令或文件操作、敏感出口及依赖做安全审查，输出有证据的风险与验证缺口。不探测生产，不自动修复或升级依赖。 |
| [ai-trace-audit](ai-trace-audit/SKILL.md) | 0.1.0 | 审查指定变更里只服务 AI 会话的协作痕迹、失实注释和无效模板内容，按项目内容边界给出证据与合理例外。不检测作者身份，不自动删除或重写代码。 |
| [coding-conventions](coding-conventions/SKILL.md) | 0.1.0 | 在已定实现、重构或审查范围内选择并应用项目代码规范，区分格式、惯例、语义缺陷和设计取舍。不自动更换格式器、技术栈，也不做全库重构。 |

### 诊断、验证与发布

| 包 | 版本 | 用途 |
| --- | --- | --- |
| [systematic-diagnosis](systematic-diagnosis/SKILL.md) | 0.1.0 | 排查缺陷、构建失败、跨组件错误或性能退化，用症状复现、边界证据和可证伪实验定位原因。根因已明确的获批小修直接执行修复；新功能设计和完成声明不由本技能代替。 |
| [test-strategy](test-strategy/SKILL.md) | 0.1.0 | 根据本次变更的行为和风险选择测试范围、断言、夹具与执行隔离，说明覆盖和不测的理由。用于制定或调整验证方案；具体语言的测试实现、完成判定和发布顺序由各自专项方法处理。 |
| [verification-gate](verification-gate/SKILL.md) | 0.1.0 | 在声称完成、修好或通过前，核对结论与候选、验收、执行状态和证据范围是否匹配。复用仍有效的证据，只补必要核验；不另造测试策略，也不自动重跑全量。 |
| [release-readiness](release-readiness/SKILL.md) | 0.1.0 | 用户准备上线时，从固定候选、审查和本地全量证据进入人工验收，处理验收变更并给出上线前建议。普通阶段仅评估现状，不自动启动全量；本技能不发布、不切流，也不代替用户最终决定。 |
| [readonly-ops-diagnostics](readonly-ops-diagnostics/SKILL.md) | 0.1.0 | 对范围明确的本地容器、依赖或请求链故障进行只读证据采集、时间对齐和假设检验。用于延迟、错误或本地失败演练诊断；不执行线上调查、自动修复或未授权故障注入。 |

### 资料与维护

| 包 | 版本 | 用途 |
| --- | --- | --- |
| [archive-maintenance](archive-maintenance/SKILL.md) | 0.1.0 | 在活跃文档、规则、决定或证据需要归档、缩减当前入口或恢复历史时，分类保留合同、核对引用并证明可恢复性。用于资料生命周期治理；不承担业务数据迁移，也不因文件变大或过期自动清理。 |
| [skill-maintenance](skill-maintenance/SKILL.md) | 0.1.0 | 设计、复核或在批准范围内编写与升级共享 Skill；涵盖方法提炼、触发及行为评估、来源许可和跨项目兼容维护。普通项目文档改字、使用既有 Skill 完成业务任务不触发本包。 |
| [documentation-authoring](documentation-authoring/SKILL.md) | 0.1.0 | 编写或修改面向人的技术、使用与解释文档，按读者目的组织结构，核实关键事实并检查示例、链接和交付格式。不代写项目治理规则，也不把会话流程混入业务文档。 |

### 服务端

| 包 | 版本 | 用途 |
| --- | --- | --- |
| [go-patterns](go-patterns/SKILL.md) | 0.1.0 | 处理 Go 实现或审查中的接口、错误、包边界、并发与资源生命周期，依据实际工具链和现有模式作取舍。纯文档或机械格式修改无需展开。 |
| [go-testing](go-testing/SKILL.md) | 0.1.0 | 编写、审查或诊断 Go 测试，依据公开行为选择表驱动、替身、httptest、并发、fuzz 与隔离集成验证。已有健康测试不因使用本技能而重写，覆盖率不代替检出力。 |
| [grpc-proto-contract](grpc-proto-contract/SKILL.md) | 0.1.0 | 设计、修改或审查 Protocol Buffers 与 gRPC 契约，评估 schema 演进、生成代码和混合版本运行行为。用于 proto 变更、客户端升级与兼容故障；不因普通业务代码调用 gRPC 就扩大为全协议改造。 |
| [http-api-design](http-api-design/SKILL.md) | 0.1.0 | 设计或审查 HTTP 端点的新增与演进，明确输入输出、权限、错误、幂等、分页和兼容窗口。已有确定合同的内部修复仅核受影响边界；不因 REST 偏好重建产品要求。 |
| [mysql-migration-safety](mysql-migration-safety/SKILL.md) | 0.1.0 | 设计或审查 MySQL 表、索引、约束、回填与启动迁移，核对实际版本、应用兼容、锁、可重入与失败恢复。普通只读查询不启动迁移流程，生产 SQL 绝不自动执行。 |
| [redis-patterns](redis-patterns/SKILL.md) | 0.1.0 | 设计、实现或审查 Redis 数据模型、TTL、缓存一致性、锁、幂等及客户端故障处理。用于缓存、会话、计数、限流和连接问题；纯 SQL 优化或无行为变化的配置格式修改不自动触发。 |

### 前端与测试

| 包 | 版本 | 用途 |
| --- | --- | --- |
| [vue3-development](vue3-development/SKILL.md) | 0.1.0 | 实现或审查 Vue 3 组件、store、composable 的状态流、异步副作用和交互状态。用于明确的前端行为变更；不因出现 Vue 关键词重构整个前端，也不强制迁移既有 Options API 代码。 |
| [vue-testing](vue-testing/SKILL.md) | 0.1.0 | 为 Vue 组件、Pinia store 和 composable 编写、审查或诊断行为测试，选择真实或替身边界并控制异步。用于具体测试需求；真实布局、原生浏览器事件与端到端链路需要浏览器层证据。 |
| [playwright-e2e](playwright-e2e/SKILL.md) | 0.1.0 | 用 Playwright 验证关键用户旅程、浏览器专有行为或本地前后端链路，处理可靠等待、替身边界、并行隔离与失败证据。不把单函数测试扩成 E2E，也不把模拟接口视为真实后端验证。 |
| [pytest-patterns](pytest-patterns/SKILL.md) | 0.1.0 | 编写、审查和诊断 Python pytest 用例，处理 fixture 生命周期、参数化、mock、异步及并行隔离。用于明确的测试任务；不把所有 Python 脚本改为 pytest，也不自动安装插件。 |

### 环境、集成与交付

| 包 | 版本 | 用途 |
| --- | --- | --- |
| [docker-local-environment](docker-local-environment/SKILL.md) | 0.1.0 | 搭建、诊断或清理用于开发和测试的本机 Docker/Compose 环境，管理依赖就绪、资源与并行隔离。生产运维、远端 Docker endpoint 和发布决策不在本包范围内。 |
| [external-dependency-simulation](external-dependency-simulation/SKILL.md) | 0.1.0 | 为外部 HTTP、SDK 或消息调用设计和验证本地合成替身，覆盖契约、状态、失败与恢复。用于隔离的开发测试；不证明与真实云或外部服务的端到端兼容。 |
| [jenkins-pipeline-jjb](jenkins-pipeline-jjb/SKILL.md) | 0.1.0 | 编写或审查 JJB YAML、Pipeline、插件兼容与 Jenkins 作业状态闭环，分层验证渲染、CPS、队列、取消和回调；仅在获准的隔离本地环境执行测试作业，绝不自动发布到或修改真实 Jenkins。部署策略与切流见 deployment-patterns，GitLab webhook 接收见 gitlab-webhook-local-git，镜像构建与推送见 container-image-management，本机 Compose 环境见 docker-local-environment。 |
| [deployment-patterns](deployment-patterns/SKILL.md) | 0.1.0 | 设计或审查制品部署、蓝绿/滚动/金丝雀切换、健康门和回退状态，并在授权的本地合成环境中演练。用于明确的部署策略或脚本变更；不取得生产执行权，也不扩为无关集群建设。 |
| [gitlab-webhook-local-git](gitlab-webhook-local-git/SKILL.md) | 0.1.0 | 设计、审查和合成验证 GitLab webhook 的认证、事件选择、重试与乱序投递，以及获准的隔离本地 Git 协议测试。不注册真实 hook、不建外网隧道、不操作真实域名下的仓库，也不写业务仓库。 |
| [ldap-rbac](ldap-rbac/SKILL.md) | 0.1.0 | 设计、审查与合成验证 LDAP 登录、目录同步、组到角色映射、API 鉴权和撤权。用于 bind/search、身份唯一性与旧会话失效问题。不获取凭据、不查询真实目录，也不擅自更改既有权限类别。 |
| [cloud-api-integration](cloud-api-integration/SKILL.md) | 0.1.0 | 设计或测试云 provider 的 HTTP/SDK 客户端边界、分页、限流重试、异步操作状态和资源归一化。用于既定接口集的封装与本地合成验证；不执行真实云发现、测试或操作，也不自动把既有直调替换为 SDK。 |
| [container-image-management](container-image-management/SKILL.md) | 0.1.0 | 规划、执行或复核容器镜像构建、跨仓同步、Harbor 上传、多架构清单验证及镜像保留清理。用于制品身份与分发任务；不负责业务部署切流、本机 Compose 故障或同名 Harbor 基准评测工具。 |

## 随包脚本

三个只读脚本随对应包交付，不是独立 Skill，输入输出合同见各包附页。
退出码统一为 `0` 通过、`1` 发现不符合、`2` 输入或运行条件错误，细分状态写在 JSON 的 `status` 字段：

| 脚本 | 用途 |
| --- | --- |
| [change-review/scripts/candidate-manifest.py](change-review/scripts/candidate-manifest.py) | 固定审查候选：路径、类型、内容哈希、删除态；拒绝越根、软链与路径穿越，读取中内容变动时不给稳定结论，失败时给出具体原因 |
| [skill-maintenance/scripts/skill-lint.py](skill-maintenance/scripts/skill-lint.py) | Skill 包静态检查：frontmatter、目录名、编码、引用可达、占位符；需显式指定可信 Node 与 marked 解析器，没有解析器时退出 2 |
| [archive-maintenance/scripts/archive-verify.py](archive-maintenance/scripts/archive-verify.py) | 归档前后校验：缺件、大小/哈希、符号链接边界、目标冲突、文本引用、恢复抽检；只读，不复制不删除 |

检查本库任一包时，因为包内链接到库根文件，需要加 `--allow-reference-root <库根>`：

```bash
python3 skill-maintenance/scripts/skill-lint.py plan-design --allow-reference-root . --node "$(command -v node)" --marked-module /path/to/node_modules/marked/lib/marked.esm.js
```

## 维护

设计、复核、落地三种维护模式及作者方法见 [skill-maintenance](skill-maintenance/SKILL.md)。
共享正本升级会影响所有引用项目，已加载的会话不会自动刷新；升级前固定受影响消费者、恢复点和验证范围。
版本历史记录在 [CHANGELOG.md](CHANGELOG.md)。

## 许可

本库原创内容按 [MIT](LICENSE) 发布。改编自第三方 Skill 的包各自保留上游许可全文与修改记录；
来源、固定版本、许可和使用包的汇总见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
官方技术文档仅用于事实核对，未分发其正文。本库不代表任何上游项目或厂商的背书。
