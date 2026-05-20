# GneissVision

Petrographic thin section image pair → Claude Vision → mineral identification + optical reasoning.

Built for my research at UGA's Center for Applied Isotope Studies. Feed it a PPL/XPL image pair and it tells you what mineral you're looking at, why, and what to check if it's unsure.

## How it works

1. Load a plane-polarized light (PPL) + cross-polarized light (XPL) image pair of a thin section
2. Claude Vision analyzes optical properties — color, pleochroism, cleavage, extinction angle, birefringence
3. Returns a prediction with confidence level, step-by-step optical reasoning, and flags for ambiguous cases (e.g. `EDS_needed`, `stage_rotation_needed`)
4. Corrections feed back into a labeled dataset — the model gets better as you use it

Starts from zero labeled data. The knowledge base (`minerals.json`) encodes optical mineralogy rules and carries most of the weight until enough corrections accumulate.

## Stack

- Python
- Anthropic Claude Vision API
- Active learning via JSONL correction log
