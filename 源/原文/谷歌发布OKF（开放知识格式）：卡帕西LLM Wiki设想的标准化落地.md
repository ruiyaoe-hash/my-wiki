# 谷歌发布OKF（开放知识格式）：卡帕西LLM Wiki设想的标准化落地

> 来源: 得到大脑 · 创建: 2026-06-21

### **📰 核心事件概述**

**发布背景与意义**
- **时间**：2026年6月13日（文档日期），相关报道于2026年6月19日发布。
- **发布方**：**谷歌**（Google Cloud）。
- **核心产品**：**OKF（Open Knowledge Format，开放知识格式）**。
- **愿景实现**：将**卡帕西**提出的“**LLM Wiki**”设想转化为可执行的标准，解决大语言模型（LLM）在构建复杂系统时缺乏相关上下文的问题。

### **🔍 OKF核心定义与目标**

#### **(一) 定义**
- **本质**：一种**开放规范**（open specification），用于表示元数据、上下文和整理后的知识（curated knowledge）。
- **技术实现**：采用**YAML格式**的元文件目录（directory of metadata files），配合少量**统一约定**（agreed-upon conventions）。

#### **(二) 目标**
- **跨平台兼容**：使不同供应商编写的知识能够被不同主体（agents）直接消费，无需转换（no translation required）。
- **标准化**：建立**供应商中立**（vendor-neutral）、**人类友好**（human-friendly）的知识表示标准。

### **👥 关键人物与机构**

| 角色 | 姓名/机构 | 具体信息 |
| :--- | :--- | :--- |
| **提出者** | **卡帕西** | LLM Wiki设想的原创者 |
| **发布机构** | **谷歌** | 负责将设想转化为OKF标准 |
| **技术负责人** | Sam McCreery | 谷歌Data Analytics Engineering Data Tech Lead |
| **技术负责人** | Amit Hormati | 谷歌BigQuery Engineering, Data Cloud Tech Lead |

### **📝 补充细节**
- **痛点解决**：尽管基础模型（foundation models）不断进步，但**缺乏相关上下文**常限制其能力，尤其在构建诊断系统、分析灾难等场景中，模型需要正确信息才能产生准确结果。
- **发布渠道**：相关内容由“**量子位**”在视频号平台报道，附带OKF标识图片（黑色背景白色圆环配青绿色斜条）。
