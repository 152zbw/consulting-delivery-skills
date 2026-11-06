# 外部 Skill 研究与取舍

研究日期：2026-11-06。记录实际查看的作者仓库及具体文件，不以星数或市场宣传证明产出质量。下列是流程思想的对照和自主实现说明，未复制第三方代码、提示词正文、样式包或私有数据，也未安装运行第三方项目。上游可能更新，链接指向当时查看的分支内容；未锁定提交，不声称已完成版本级复现。

|来源|查看位置与许可情况|参考的流程思想|本仓库中的处理|
|---|---|---|---|
|Anthropic Proposal Builder|[SKILL.md](https://github.com/anthropics/knowledge-work-plugins/blob/main/small-business/skills/proposal-builder/SKILL.md)；仓库[Apache-2.0](https://github.com/anthropics/knowledge-work-plugins/blob/main/LICENSE)|从发现资料组织提案，使用自有模板，另报内部风险|自主写交付起点卡；不引入自动签署、收款或按历史价格自动推算报价|
|Meaningfy proposal-writing|[SKILL.md](https://github.com/meaningfy-ws/skillery/blob/develop/skills/proposal-writing/SKILL.md)中标Apache 2.0，但根[LICENSE](https://github.com/meaningfy-ws/skillery/blob/develop/LICENSE)为GPL-3.0|关注范围与估算边界的一致|只作研究比较；许可标识不一致，未复制或移植文本/代码，不将其Proof of Value商业模式强加给公司|
|Peter Bamuhigire Proposal Skills|[methodology](https://github.com/peterbamuhigire/proposal-skills/blob/main/skills/pipeline/06-methodology/SKILL.md)、[review](https://github.com/peterbamuhigire/proposal-skills/blob/main/skills/meta/bid-red-team-dual-review/SKILL.md)；[MIT](https://github.com/peterbamuhigire/proposal-skills/blob/main/LICENSE)|让方法产出证据，区分审查与文风检查|自主增加方法可执行性、未评估状态和评委视角；不搬地区采购规则，不复制其多代理调度要求|
|Joel Kohlman Instructional Design|[SKILL.md](https://github.com/joelrkohlman/instructional-design/blob/main/SKILL.md)；[MIT](https://github.com/joelrkohlman/instructional-design/blob/main/LICENSE)|培训适用性诊断、可观察目标和情景原型|自主增加非培训措施、练习原型和迁移验证；不引入LMS/SCORM开发作为默认范围|
|Anthropic Skill Creator|[SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)；技能目录[Apache-2.0](https://github.com/anthropics/skills/blob/main/skills/skill-creator/LICENSE.txt)|真实请求测试、迭代、定量与定性评价分开|自建触发与行为验收用例；不将结构检查冒称模型对照实验，不自动触发付费测试|
|Ningzimu Codex PPT|[SKILL.md](https://github.com/ningzimu/codex-ppt-skill/blob/main/skills/codex-ppt/SKILL.md)、[仓库](https://github.com/ningzimu/codex-ppt-skill)|分阶段产物及最终文件检查|借鉴流程组织方式；图片式PPT不适合本技能默认的原生可编辑要求，未移植脚本或视觉资产|

这是本项目独立编写的规则与实现；来源并不构成机构背书或公司知识产权授权。未来若复制或改编第三方文本/代码，应另查对应文件实际许可证、NOTICE及保留义务，不能仅依此表认定。

## 本次实现位置

每个skill的 references/field-practice.md 保存对应专项细则；review-protocol.md新增专业检查状态；evals/cases.json保存可复用请求及验收依据。现有文件生成、模板适配和安全边界保留，未引入外部依赖。
