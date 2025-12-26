# 3D Text Helix — AI Tool Comparison Analysis

## Overview

Tested four AI models on generating a 3D text helix visualizer from a single prompt. Each model received the same basic prompt, then the same detailed engineered prompt. Goal: evaluate how well each handles ambiguous vs. specific instructions for visual and interactive code generation.

## Models Tested

| Model | Access | Version |
|-------|--------|---------|
| ChatGPT | chatgpt.com | GPT-4o |
| Claude | claude.ai  | Claude 3.5 Sonnet |
| Deepseek | chat.deepseek.com | Deepseek V3 |
| Gemini | gemini.google.com | Gemini 1.5 |

---

## Results Summary

| Model | Basic Prompt | Engineered Prompt |
|-------|--------------|-------------------|
| ChatGPT | ❌ Non-functional | ❌ Non-functional |
| Claude | ⚠️ Wrong interpretation | ✅ Fully functional |
| Deepseek | ⚠️ Viewport broken | ✅ Best overall |
| Gemini | ⚠️ Works, imprecise | ✅ Fully functional |

---

## Detailed Findings

### ChatGPT

**Basic Prompt:**
- Black background renders, small text field with preset text appears
- Non-functional: no helix appears, nor do any of the inputs
- Console shows errors (THREE.FontLoader undefined)
- **Root cause**: Uses legacy Three.js script tag pattern (trends have outgrown training data)

**Engineered Prompt:**
- Uses ES6 modules (correct approach this time)
- All UI elements present: text input, sliders, color pickers
- Code structure looks reasonable
- **Still non-functional** — same black screen result despite cleaner architecture

**Code Quality:**
- Basic: 127 lines, legacy patterns, architectural failure
- Advanced: 185 lines, modern ES6, runtime failure

**Verdict:** Failed entirely. The model produced syntactically valid code that doesn't execute. Unable to produce a working Three.js application on either attempt.

---

### Claude

**Basic Prompt:**
- Visually polished UI with gradient background, rounded controls, instructions panel
- Uses older Three.js r128 via script tag (works, but not modern)
- **Critical flaw**: Creates a predefined(!) helix structure using `TubeGeometry,` meaning the DNA shape exists independently of the text
- Text characters are placed onto(!) the existing helix, not used to build the helix
- All sliders functional, mouse controls work
- Has extra features not requested: text size slider, helix height slider

**Engineered Prompt:**
- Switches to ES6 modules with import maps (modern approach)
- Clean code with section comment headers
- Helix is now correctly built from the text — characters define the shape
- Odd characters -> Strand A, even characters -> Strand B (correct)
- All UI controls work: text input (real-time), speed slider, radius slider, color pickers
- Proper sprite cleanup with dispose()-method calls
- Connecting lines between characters on each strand

**Code Quality:**
- Basic: 452 lines, verbose, extra features, wrong interpretation
- Advanced: 312 lines, well-structured sections, correct implementation

**Verdict:** Basic prompt produces a polished but fundamentally incorrect interpretation. Engineered prompt achieves full compliance with clean, readable code.

---

### Deepseek

**Basic Prompt:**
- **Unique approach**: Uses vanilla Canvas 2D with manual 3D projection mathematics, no Three.js used at all
- Implements own `rotatePoint()` and `project()` functions for 3D→2D transformation
- Very polished UI with gradient header, explanatory subtitle, FPS counter, character count
- Includes "Apply Text" button (not real-time) and "Reset View" button
- **But**: CSS layout breaks the page; the helix canvas is only 1/4 visible, cannot scroll to see it
- What's visible looks correct: both strands, connecting lines, text glow effect
- Has features like dropdown color select instead of color picker

**Engineered Prompt:**
- Switches to Three.js (correct for the complexity)
- **OOP class-based architecture**: `HelixVisualizer` class encapsulates everything
- Most sophisticated code structure of all outputs
- Clean separation: constructor, init methods, update methods, event handlers
- Real-time text updates, all sliders work
- Proper color update method that redraws canvas textures
- Best UI design: subtle glassmorphism, cyan accent color, clear instructions panel

**Code Quality:**
- Basic: 532 lines, manual 3D math, but layout bug
- Advanced: 617 lines, OOP pattern, very maintainable code

**Verdict:** Basic prompt showed creativity (building 3D from scratch) but had a blocking bug. Engineered prompt produced the most polished and professionally structured output.

---

### Gemini

**Basic Prompt:**
- Uses ES6 modules with import maps (modern)
- Uses `FontLoader` and `TextGeometry` for actual 3D extruded text (not sprites)
- Minimal, functional UI: just a text input and brief instructions
- **Flaw**: Both strands display the same text repeated, not split between strands
- Shape is more of a loose spiral than a true double helix
- Works and updates in real-time, but interpretation is imprecise

**Engineered Prompt:**
- Maintains ES6 modules approach
- Uses state management object pattern (clean and maintainable):
  ```javascript
  const state = {
      text: "HELLO WORLD",
      radius: 100,
      rotationSpeed: 0.5,
      // ...
  };
  ```
- Sprites with glow/shadow effect (`ctx.shadowBlur`)
- Adds fog effect for depth perception (`scene.fog = new THREE.FogExp2(...)`)
- All features work correctly
- Proper cleanup with geometry/material disposal
- Characters correctly split: odd -> Strand A, even -> Strand B

**Code Quality:**
- Basic: 108 lines, minimal, works but imprecise
- Advanced: 246 lines, state pattern, good visual polish

**Verdict:** Basic prompt produced working but imprecise output. Engineered prompt matched Deepseek quality with cleaner, more concise code.

---

## Technical Comparison

### Architecture Approaches

| Model | Basic Prompt | Engineered Prompt |
|-------|--------------|-------------------|
| ChatGPT | Legacy script tags | ES6 modules |
| Claude | Legacy script tags | ES6 modules |
| Deepseek | Vanilla Canvas 2D | OOP class pattern |
| Gemini | ES6 modules | ES6 modules + state object |

### Lines of Code

| Model | Basic | Engineered | Delta |
|-------|-------|------------|-------|
| ChatGPT | 127 | 185 | +58 |
| Claude | 452 | 312 | -140 |
| Deepseek | 532 | 617 | +85 |
| Gemini | 108 | 246 | +138 |

Note: More lines ≠ better. Claude's basic was bloated with wrong features; the advanced version is leaner and correct.

### Feature Implementation (Engineered Prompt)

| Feature | ChatGPT | Claude | Deepseek | Gemini |
|---------|---------|--------|----------|--------|
| Runs without errors | ❌ | ✅ | ✅ | ✅ |
| Double helix shape | ❌ | ✅ | ✅ | ✅ |
| Text splits odd/even | ❌ | ✅ | ✅ | ✅ |
| 3 rotations | ❌ | ✅ | ✅ | ✅ |
| Auto-rotation | ❌ | ✅ | ✅ | ✅ |
| OrbitControls | ❌ | ✅ | ✅ | ✅ |
| Real-time text update | ❌ | ✅ | ✅ | ✅ |
| Speed slider | ❌ | ✅ | ✅ | ✅ |
| Radius slider | ❌ | ✅ | ✅ | ✅ |
| Color pickers (2) | ❌ | ✅ | ✅ | ✅ |
| Strand lines | ❌ | ✅ | ✅ | ✅ |
| Dark background | ❌ | ✅ | ✅ | ✅ |
| Responsive resize | ❌ | ✅ | ✅ | ✅ |
| **Score** | **0/13** | **13/13** | **13/13** | **13/13** |

---

## Key Observations

### 1. Prompt specificity is decisive

Three of four models improved dramatically with the engineered prompt:
- Claude: Wrong concept → correct implementation
- Deepseek: Broken layout → polished product
- Gemini: Imprecise interpretation → full compliance

The basic prompt's ambiguity ("characters spiral around a rotating double helix") led to divergent interpretations. The engineered prompt's explicit requirements (odd/even split, 3 rotations, specific controls) left no room for misinterpretation. But: creativity (Deepseek's impressive UI, Claude's additional features) are lost with that clarifying specificity also.

### 2. ChatGPT's Three.js handling is broken

Both attempts failed at runtime. The basic version used outdated patterns; the advanced version looked correct but still didn't work. This suggests either:
- A systematic issue with ChatGPT's Three.js training data
- Version mismatch assumptions
- Testing/validation gap in code generation

### 3. Deepseek's creativity is notable

The basic prompt response used vanilla Canvas 2D with manual 3D projection — no Three.js dependency at all. While this caused problems (harder to implement all features), it shows the model understood the GOAL (3D visualization) and chose an alternative PATH. This kind of creative problem-solving is valuable, even when the result has bugs.

### 4. Code structure quality varies significantly

- **Best structure**: Deepseek (OOP class)
- **Cleanest code**: Gemini (state object + minimal)
- **Most readable**: Claude (section headers)
- **Most problematic**: ChatGPT (doesn't run)

### 5. UI/UX polish differs even among working outputs

All three working models (Claude, Deepseek, Gemini) produced functional UIs, but:
- **Deepseek**: Most polished (glassmorphism, accent colors, instructions)
- **Gemini**: Clean and minimal
- **Claude**: Professional but slightly more generic

---

## Recommendations

### For using AI code generation:

1. **Always use detailed, specifically engineered prompts** for complex visual/interactive work. Ambiguity leads to divergent (often wrong) interpretations.

2. **Specify the tech stack explicitly** (e.g., "using Three.js from CDN with ES6 modules"). This prevents models from choosing incompatible approaches.

3. **Test immediately**. ChatGPT's output looked valid but didn't run. Syntax validity ≠ runtime correctness.

4. **Try multiple models** for important tasks. Performance varies significantly by domain — Deepseek excelled here but might not elsewhere. Settling for one model and sticking to it may lead to productivity/time loss (i.e. sticking with ChatGPTs result and trying to fix it manually/prompting further to get it functional might lead to loss of valuable time, whereas an immedate switch to a different model would have led to a working solution much faster)

---

## Conclusion

Prompt engineering transformed three out of four models from "partially working" to "fully compliant." The one exception (ChatGPT) failed regardless of prompt quality.

For visual/interactive code generation, **prompt specificity matters more than model choice** — but given equal prompts, Deepseek and Gemini outperformed expectations while ChatGPT underperformed significantly.
