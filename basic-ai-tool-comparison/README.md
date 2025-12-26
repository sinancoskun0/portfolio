# AI Tool Comparison — 3D Text Helix

![Three.js](https://img.shields.io/badge/Three.js-black?logo=three.js&logoColor=white)
![ChatGPT](https://img.shields.io/badge/ChatGPT-74aa9c?logo=openai&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-d97706)
![Deepseek](https://img.shields.io/badge/Deepseek-4D6BFE)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?logo=google&logoColor=white)

Comparing AI code generation tools with a task where success is immediately visible - a 3D text helix visualizer with interactive elements. 
All four tested models are given the same prompts (as visible in the prompts.txt file), then compared and contrasted according to the requirements defined in the prompt.

## The Task

When the user inputs text (specifically; a character), that character is supposed to spiral around a rotating helix-like structure. The structure is meant to have interactive controls to define the way it rotates, a zoom function, a way to set the colors of the structure, and its rotation speed.

## Models Tested

- ChatGPT (GPT-4o)
- Claude (3.5 Sonnet)
- Deepseek (V3)
- Gemini (1.5)

## Quick Results

| Model | Basic Prompt | Engineered Prompt |
|-------|--------------|-------------------|
| ChatGPT | ❌ Broken | ❌ Broken |
| Claude | ⚠️ Misinterpreted | ✅ Full |
| Deepseek | ⚠️ UI bug | ✅ Best |
| Gemini | ⚠️ Imprecise | ✅ Full |

## Contents


## Key Takeaways

1. **Prompt specificity matters** — 3/4 models went from broken/wrong to fully functional with detailed requirements
2. **ChatGPT failed** on Three.js despite syntactically valid code
3. **Deepseek overperforemd** with the best code structure (OOP) and most polished UI

See [ANALYSIS.md](ANALYSIS.md) for full technical breakdown.
