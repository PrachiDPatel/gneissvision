"""
GneissVision — VLM-based mineral classifier
Phase 1: zero-labeled-data start using Claude claude-sonnet-4-6 vision + mineral knowledge base
"""

import base64
import json
import os
from pathlib import Path
from dataclasses import dataclass, field

import anthropic

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
KB_PATH = ROOT / "knowledge_base" / "minerals.json"
LABELED_PATH = ROOT / "data" / "labeled_corrections.jsonl"

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class ImagePair:
    """One sample: a PPL and XPL image of the same region."""
    ppl_path: Path
    xpl_path: Path
    sample_id: str = ""

    def __post_init__(self):
        if not self.sample_id:
            self.sample_id = self.ppl_path.stem

@dataclass
class Prediction:
    mineral: str
    confidence: str          # "high" | "moderate" | "low"
    reasoning: str           # the model's step-by-step optical reasoning
    alternatives: list[str]  # other minerals to consider
    flags: list[str]         # e.g. "EDS_needed", "stage_rotation_needed"
    raw_response: str = ""

@dataclass
class LabeledExample:
    sample_id: str
    ppl_path: str
    xpl_path: str
    predicted: str
    correct: str
    user_notes: str = ""

# ---------------------------------------------------------------------------
# Knowledge base
# ---------------------------------------------------------------------------

def load_knowledge_base() -> dict:
    with open(KB_PATH) as f:
        return json.load(f)

def format_kb_for_prompt(kb: dict) -> str:
    """Condense the knowledge base into a readable reference string for the prompt."""
    lines = []
    lines.append("=== MINERAL OPTICAL PROPERTIES REFERENCE ===\n")

    def format_mineral(name, data):
        lines.append(f"## {name.upper().replace('_', ' ')}")
        ppl = data.get("PPL", {})
        xpl = data.get("XPL", {})
        lines.append(f"  PPL: color={ppl.get('color','?')}, pleochroism={ppl.get('pleochroism','?')}, "
                     f"relief={ppl.get('relief','?')}, cleavage={ppl.get('cleavage','?')}")
        lines.append(f"  XPL: birefringence={xpl.get('birefringence','?')}, "
                     f"color={xpl.get('interference_color','?')}, twinning={xpl.get('twinning','?')}")
        distinguishing = data.get("distinguishing_features", [])
        if distinguishing:
            lines.append(f"  KEY: {distinguishing[0]}")
        lines.append("")

    for name, data in kb.get("major_minerals", {}).items():
        format_mineral(name, data)
    lines.append("--- REE ACCESSORIES ---")
    for name, data in kb.get("ree_accessories", {}).items():
        format_mineral(name, data)

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Image encoding
# ---------------------------------------------------------------------------

def encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

def image_media_type(path: Path) -> str:
    ext = path.suffix.lower()
    return {"jpg": "image/jpeg", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".tif": "image/tiff", ".tiff": "image/tiff"}.get(ext, "image/jpeg")

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are GneissVision, an expert petrographic mineral identification assistant.
You reason like an experienced petrographer analyzing thin sections from igneous and metamorphic rocks.

Your identification process:
1. Examine the PPL (plane polarized light) image: note color, pleochroism potential, relief, cleavage, habit, alteration
2. Examine the XPL (crossed polarized light) image: note interference color (birefringence order), twinning, extinction character, any anomalous colors
3. Apply the systematic decision workflow (colored? → isotropic? → birefringence level? → twinning/cleavage split)
4. Name the most likely mineral with reasoning
5. Flag when EDS/TIMA-X chemical data or stage rotation is needed to confirm

Always explain your reasoning step by step — do not just name a mineral. The user is learning petrography.

When uncertain, say so honestly and explain what additional observation would resolve the ambiguity.

Respond in this JSON format:
{
  "mineral": "mineral_name",
  "confidence": "high|moderate|low",
  "reasoning": "step-by-step optical reasoning referencing specific PPL and XPL observations",
  "alternatives": ["other_mineral_1", "other_mineral_2"],
  "flags": ["EDS_needed|stage_rotation_needed|confirm_with_assemblage|..."]
}"""

# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

class GneissVisionClassifier:

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.kb = load_knowledge_base()
        self.kb_text = format_kb_for_prompt(self.kb)

    def classify(self, pair: ImagePair) -> Prediction:
        """Run VLM inference on a PPL+XPL image pair."""

        ppl_b64 = encode_image(pair.ppl_path)
        xpl_b64 = encode_image(pair.xpl_path)
        ppl_type = image_media_type(pair.ppl_path)
        xpl_type = image_media_type(pair.xpl_path)

        user_content = [
            {
                "type": "text",
                "text": f"Here is a petrographic thin section image pair (sample: {pair.sample_id}).\n"
                        f"Image 1 is PPL (plane polarized light). Image 2 is XPL (crossed polars).\n\n"
                        f"Reference:\n{self.kb_text}\n\n"
                        f"Identify the mineral in the center of the image. Reason step by step."
            },
            {
                "type": "image",
                "source": {"type": "base64", "media_type": ppl_type, "data": ppl_b64}
            },
            {
                "type": "text",
                "text": "Above: PPL. Below: XPL of the same region."
            },
            {
                "type": "image",
                "source": {"type": "base64", "media_type": xpl_type, "data": xpl_b64}
            }
        ]

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}]
        )

        raw = response.content[0].text
        try:
            # Strip markdown code fences if present
            clean = raw.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            data = json.loads(clean)
            return Prediction(
                mineral=data.get("mineral", "unknown"),
                confidence=data.get("confidence", "low"),
                reasoning=data.get("reasoning", ""),
                alternatives=data.get("alternatives", []),
                flags=data.get("flags", []),
                raw_response=raw
            )
        except json.JSONDecodeError:
            return Prediction(
                mineral="parse_error",
                confidence="low",
                reasoning=raw,
                alternatives=[],
                flags=["parse_error"],
                raw_response=raw
            )

# ---------------------------------------------------------------------------
# Active learning: save user corrections
# ---------------------------------------------------------------------------

def save_correction(pair: ImagePair, predicted: str, correct: str, notes: str = "") -> None:
    """Log a user correction. These become training examples for the fine-tuned model later."""
    LABELED_PATH.parent.mkdir(parents=True, exist_ok=True)
    example = LabeledExample(
        sample_id=pair.sample_id,
        ppl_path=str(pair.ppl_path),
        xpl_path=str(pair.xpl_path),
        predicted=predicted,
        correct=correct,
        user_notes=notes
    )
    with open(LABELED_PATH, "a") as f:
        f.write(json.dumps(example.__dict__) + "\n")
    print(f"Saved correction: {predicted} → {correct} ({pair.sample_id})")

def load_corrections() -> list[LabeledExample]:
    if not LABELED_PATH.exists():
        return []
    examples = []
    with open(LABELED_PATH) as f:
        for line in f:
            data = json.loads(line.strip())
            examples.append(LabeledExample(**data))
    return examples

def correction_summary() -> dict:
    """Show how many labeled examples exist per class."""
    examples = load_corrections()
    counts: dict[str, int] = {}
    for ex in examples:
        counts[ex.correct] = counts.get(ex.correct, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))

# ---------------------------------------------------------------------------
# Interactive session (CLI)
# ---------------------------------------------------------------------------

def interactive_session():
    """Simple REPL for classifying image pairs and recording corrections."""
    clf = GneissVisionClassifier()
    print("\nGneissVision — petrographic mineral classifier")
    print("Commands: classify <ppl_path> <xpl_path> | correct <correct_mineral> | summary | quit\n")

    last_pair: ImagePair | None = None
    last_prediction: Prediction | None = None

    while True:
        try:
            cmd = input(">>> ").strip().split()
        except (EOFError, KeyboardInterrupt):
            break

        if not cmd:
            continue

        if cmd[0] == "quit":
            break

        elif cmd[0] == "classify" and len(cmd) >= 3:
            ppl = Path(cmd[1])
            xpl = Path(cmd[2])
            if not ppl.exists() or not xpl.exists():
                print("File not found.")
                continue
            last_pair = ImagePair(ppl_path=ppl, xpl_path=xpl)
            print(f"Classifying {last_pair.sample_id}...")
            last_prediction = clf.classify(last_pair)
            print(f"\nPrediction: {last_prediction.mineral} [{last_prediction.confidence} confidence]")
            print(f"Reasoning:\n{last_prediction.reasoning}")
            if last_prediction.alternatives:
                print(f"Alternatives: {', '.join(last_prediction.alternatives)}")
            if last_prediction.flags:
                print(f"Flags: {', '.join(last_prediction.flags)}")
            print()

        elif cmd[0] == "correct" and len(cmd) >= 2:
            if last_pair is None or last_prediction is None:
                print("No recent prediction to correct.")
                continue
            correct_mineral = cmd[1]
            notes = " ".join(cmd[2:]) if len(cmd) > 2 else ""
            save_correction(last_pair, last_prediction.mineral, correct_mineral, notes)

        elif cmd[0] == "summary":
            counts = correction_summary()
            print("Labeled examples per mineral:")
            for mineral, count in counts.items():
                bar = "█" * count
                print(f"  {mineral:20s} {count:3d}  {bar}")
            print()

        else:
            print("Unknown command.")

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    interactive_session()
