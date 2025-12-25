# AI Tool Comparison — 3D Text Helix

![Three.js](https://img.shields.io/badge/Three.js-black?logo=three.js&logoColor=white)
![ChatGPT](https://img.shields.io/badge/ChatGPT-74aa9c?logo=openai&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-d97706)
![Deepseek](https://img.shields.io/badge/Deepseek-4D6BFE)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?logo=google&logoColor=white)

Comparing AI code generation tools on a visual, interactive task: generating a 3D text helix visualizer from a single prompt.

## The Task

User inputs text → characters spiral around a rotating double-helix (DNA-style) structure → interactive controls for rotation, zoom, colors, speed.

## Models Tested

- ChatGPT (GPT-4o, free tier)
- Claude (3.5 Sonnet, free tier)
- Deepseek (V3, free tier)
- Gemini (1.5, free tier)

## Quick Results

| Model | Basic Prompt | Engineered Prompt |
|-------|--------------|-------------------|
| ChatGPT | ❌ Broken | ❌ Broken |
| Claude | ⚠️ Misinterpreted | ✅ Full |
| Deepseek | ⚠️ UI bug | ✅ Best |
| Gemini | ⚠️ Imprecise | ✅ Full |

## Contents


## Key Takeaways

1. **Prompt specificity ** — 3/4 models went from broken/wrong to fully functional with detailed requirements
2. **ChatGPT failed entirely** on Three.js despite syntactically valid code
3. **Deepseek surprised** — best code structure (OOP), best UI polish
4. **Test immediately** — code that looks correct may not run

See [ANALYSIS.md](ANALYSIS.md) for full technical breakdown.
