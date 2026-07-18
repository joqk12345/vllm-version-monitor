# TECHNOLOGY BRIEF / {{ report_month }}

# {{ project_name }} 版本演进简报

> {{ subtitle }}

**一句话结论**：{{ one_sentence_conclusion }}

**最新正式版本**：{{ latest_stable_version }}（{{ latest_stable_date }}）；**最新稳定补丁**：{{ latest_patch_version_or_none }}（{{ latest_patch_date_or_none }}）。

> 版本口径：{{ versioning_note }}

---

## 01 版本演进时间线

| 阶段 | 时间 | 代表版本 | 核心主题 | 关键证据 |
|---|---|---|---|---|
| 阶段 1：{{ phase_1_name }} | {{ phase_1_period }} | {{ phase_1_versions }} | {{ phase_1_theme }} | {{ phase_1_evidence }} |
| 阶段 2：{{ phase_2_name }} | {{ phase_2_period }} | {{ phase_2_versions }} | {{ phase_2_theme }} | {{ phase_2_evidence }} |
| 阶段 3：{{ phase_3_name }} | {{ phase_3_period }} | {{ phase_3_versions }} | {{ phase_3_theme }} | {{ phase_3_evidence }} |
| 阶段 4：{{ phase_4_name }} | {{ phase_4_period }} | {{ phase_4_versions }} | {{ phase_4_theme }} | {{ phase_4_evidence }} |
| 阶段 5：{{ phase_5_name }} | {{ phase_5_period }} | {{ phase_5_versions }} | {{ phase_5_theme }} | {{ phase_5_evidence }} |

```text
{{ phase_1_short }} → {{ phase_2_short }} → {{ phase_3_short }} → {{ phase_4_short }} → {{ phase_5_short }}
```

## 02 核心判断

| 技术主线 | 演进路径 | 当前判断 |
|---|---|---|
| 性能与缓存 | {{ performance_path }} | {{ performance_assessment }} |
| 调度、并行与集群 | {{ distributed_path }} | {{ distributed_assessment }} |
| 模型、架构与服务接口 | {{ architecture_path }} | {{ architecture_assessment }} |

**总体判断**：{{ overall_assessment }}

## 03 关键版本里程碑

| 时间 | 版本 | 版本意义 / 关键 Feature | 证据 |
|---:|---|---|---|
| {{ milestone_1_date }} | {{ milestone_1_version }} | {{ milestone_1_impact }} | {{ milestone_1_source }} |
| {{ milestone_2_date }} | {{ milestone_2_version }} | {{ milestone_2_impact }} | {{ milestone_2_source }} |
| {{ milestone_3_date }} | {{ milestone_3_version }} | {{ milestone_3_impact }} | {{ milestone_3_source }} |
| {{ milestone_4_date }} | {{ milestone_4_version }} | {{ milestone_4_impact }} | {{ milestone_4_source }} |
| {{ milestone_5_date }} | {{ milestone_5_version }} | {{ milestone_5_impact }} | {{ milestone_5_source }} |
| {{ milestone_6_date }} | {{ milestone_6_version }} | {{ milestone_6_impact }} | {{ milestone_6_source }} |

> 选择 8–15 个真正改变架构、性能边界或部署方式的版本；不要把普通 bugfix 逐条列为里程碑。

## 04 技术选型启示

### 适合重点关注 {{ project_name }} 的场景

- {{ fit_case_1 }}
- {{ fit_case_2 }}
- {{ fit_case_3 }}

### 生产部署需要特别管理

- {{ risk_1 }}
- {{ risk_2 }}
- {{ risk_3 }}

## 05 版本与证据说明

- **资料来源**：{{ official_sources }}
- **截止日期**：{{ as_of_date }}；GitHub 发布日期按 {{ timezone }} 统计。
- **版本筛选**：{{ release_filter }}
- **证据边界**：仅把官方 Release、文档或已合并 PR 明确写出的内容作为“已支持”；未收集到证据时写“待确认”，不写“不支持”。
- **独立版本线**：{{ independent_version_lines_or_none }}

---

*{{ project_name }} 版本演进简报 · 自动采集 + 人工/LLM 证据复核 · {{ report_month }}*
