# GneissVision — CS & ML Concepts Guide

> The "why does the code work" companion to `petrography_guide.md`.
> Concepts are explained in terms of what GneissVision is actually doing.

---

## 1. What a neural network actually is

A neural network is a function that takes numbers in and produces numbers out — trained to approximate some pattern by adjusting millions of internal parameters (called **weights**) until its output matches a known correct answer.

For images, the "numbers in" are pixel values (each pixel becomes 3 numbers: R, G, B). The "numbers out" are confidence scores, one per possible class:

```
[0.72, 0.03, 0.18, 0.07]
 quartz  biotite  plagioclase  garnet
```

The network guesses quartz (72% confident). If the correct answer was plagioclase, the training process adjusts the weights slightly to make the network more likely to output a higher plagioclase score next time. Repeat this millions of times across thousands of examples — that's training.

**The weights ARE the model.** When you save or load a model file, you're saving/loading the weights. The architecture (the structure of the network) is fixed; the weights are what get learned.

---

## 2. CNNs vs Vision Transformers — what GneissVision uses

### CNNs (Convolutional Neural Networks) — the older approach
CNNs were the dominant architecture for images from ~2012 to ~2020. They work by sliding small filters across the image to detect local patterns (edges, textures, color patches) and combining them into higher-level features. They're fast, well-understood, and good at texture recognition.

**Why they were the standard for mineral ID:** Minerals have distinctive textures (cleavage crack patterns, twinning stripes, birefringence color patterns) that CNN filters could learn.

**The problem:** CNNs need a lot of labeled examples per class to work well. They don't generalize well from descriptions — you can't tell a CNN "this mineral is yellow-brown with high relief" and have it understand. You have to *show* it thousands of labeled examples.

### Vision Transformers (ViT) — newer, what Phase 3 will use
Instead of local filters, ViTs divide the image into a grid of patches (e.g., 16×16 pixel squares) and process them using the same "attention" mechanism as language models. This lets the model look at relationships between distant parts of the image — useful when a cleavage angle on one side of a grain matters relative to the twinning pattern on the other side.

ViTs also transfer better from large pretrained models, meaning you need fewer examples to fine-tune them.

**GneissVision Phase 3 plan:** Fine-tune a pretrained ViT (like `google/vit-base-patch16-224`) on the labeled examples you accumulate through Phase 1+2. At ~50-100 examples per mineral class, a ViT can achieve reasonable accuracy while a CNN from scratch would need thousands.

### Why GneissVision doesn't start with either
Both CNNs and ViTs require labeled training data to learn from. We have none. So Phase 1 uses a completely different approach — see Section 4.

---

## 3. Transfer learning and fine-tuning

Training a model from random weights on millions of images takes weeks on specialized hardware and costs thousands of dollars. Nobody does this from scratch for a new task.

Instead: **transfer learning**. Take a model already trained on a huge dataset (like ImageNet — 14 million labeled photos), and use its weights as a starting point. This model already understands edges, textures, shapes, color gradients. You then **fine-tune** it on your specific task — continuing training on your small dataset, adjusting the weights slightly toward your domain.

```
Pretrained ViT                  Fine-tuned GneissVision ViT
(knows: dog, cat, chair...)  →  (knows: quartz, biotite, monazite...)
         ↑
14M ImageNet images               ~500 labeled thin section patches
(someone else paid for this)       (you labeled these via active learning)
```

**The analogy:** A geologist trained on general earth science (pretrained model) learns mineral optics much faster than a non-scientist because they already understand crystallography, chemistry, light behavior. The pretrained weights are that background knowledge.

**What gets fine-tuned:** Usually just the last few layers of the network (the "head") that produce the final classification, while the earlier layers that detect basic features are frozen. This prevents "catastrophic forgetting" — destroying the general knowledge while learning the specific task.

---

## 4. Vision-Language Models (VLMs) — what Phase 1 actually uses

This is the most important concept for GneissVision's current approach.

A VLM is a model that understands both images and text together. Claude claude-sonnet-4-6 (the model used in `classifier.py`) is one. GPT-4o is another. They're trained on vast quantities of image-text pairs from the internet, academic papers, books — including geological literature.

**What makes them different from a plain image classifier:**
- They can reason in language about what they see
- They can take text context as input and use it to inform image interpretation
- They can explain their reasoning, not just output a label
- They generalize to new tasks without any domain-specific training data

**This is why GneissVision can work with zero labeled examples on day one:** you give Claude the optical property reference (the knowledge base) as text, show it the PPL+XPL images, and ask it to reason through the identification the way a petrographer would. It already has enough understanding of optics, mineralogy, and systematic reasoning to do a reasonable job.

**The tradeoff:** VLMs are slow (1-5 seconds per image), expensive (API cost per call), and require internet access. Phase 3's fine-tuned ViT will run locally in milliseconds for free — but needs the labeled data that Phase 1+2 build up.

---

## 5. RAG — Retrieval Augmented Generation

RAG is the technique used to feed the mineral knowledge base to the VLM.

The problem: a VLM has general knowledge from training but might not have detailed, up-to-date, or domain-specific information. You can't retrain it every time you add new mineral descriptions.

The solution: at inference time (when you're asking it a question), retrieve relevant information and include it in the prompt as context. The model reads it like a reference sheet before answering.

```
Without RAG:                     With RAG (GneissVision):
"What mineral is this?"    →     "Here is the optical property reference
                                  for 20 minerals. Now: what mineral is this?"
   ↓                                      ↓
Relies on training memory       Reads the reference, then reasons from it
(may be vague or wrong)         (grounded in your specific knowledge base)
```

In `classifier.py`, `format_kb_for_prompt()` converts `minerals.json` into a readable reference string that gets prepended to every classification request. When you update `minerals.json` with a new mineral, every future classification immediately benefits — no retraining needed.

**The name:** "Retrieval" because you retrieve relevant documents; "Augmented" because you augment the prompt with them; "Generation" because the model generates a response. In GneissVision the retrieval is simple (always inject the whole knowledge base) but in larger systems you'd retrieve only the most relevant entries.

---

## 6. Active learning

Standard machine learning: collect all your labeled data, then train. **Active learning** flips this: train iteratively, and at each step ask a human to label only the examples the model is most uncertain about.

**Why this matters for GneissVision:**

If the model is 99% sure something is quartz, your label confirms what it already knows — low value. If it's 51% quartz / 49% plagioclase, your label on that example teaches it the exact decision boundary it's struggling with — high value. Active learning prioritizes high-value labels.

```
Standard approach:
Label 1000 random examples → train → get 70% accuracy

Active learning:
Label 100 uncertain examples → train → get 70% accuracy
                 ↑
         same result, 10x less labeling work
```

In `classifier.py` Phase 1, the "active learning" is informal — you classify an image, see the prediction and confidence level, and correct it if wrong. In Phase 3, the system will explicitly rank its uncertain predictions and surface those first.

The corrections saved to `data/labeled_corrections.jsonl` are your growing training dataset. Every line is a labeled example. When you have enough, that file becomes the fine-tuning dataset.

---

## 7. Semantic segmentation vs. patch classification

Two different ways to approach the mineral ID problem:

### Patch classification (GneissVision Phase 1)
Crop a small region (~100-200px) around one mineral grain → classify what mineral it is. Simple, works with VLMs, but requires manual cropping or a separate grain detection step.

```
Whole thin section image
        ↓
[manually crop or auto-detect grain]
        ↓
Patch: 150×150px of one grain
        ↓
Classify → "plagioclase (high confidence)"
```

### Semantic segmentation (GneissVision Phase 3+ goal)
Classify every pixel in the whole image simultaneously — producing a colored map where each region is labeled with its mineral. This is what TIMA-X does automatically with EDS.

```
Whole thin section image
        ↓
U-Net or Mask R-CNN
        ↓
Pixel-level map:
  [quartz=blue] [plagioclase=green] [biotite=brown] [monazite=red]
```

Segmentation requires much more labeled data (you're labeling individual pixels, not just image patches) and is a harder problem. It's the Phase 3+ goal once you have a real dataset.

**SAM (Segment Anything Model)** — a Meta AI model that detects object boundaries in any image without training. It can propose grain boundaries automatically, solving the "how do we find individual grains" step before classification. GneissVision's planned pipeline:

```
SAM → grain boundary proposals → crop each grain → VLM/ViT classifies each crop → reassemble into labeled map
```

---

## 8. Embeddings — how models "understand" similarity

When a neural network processes an image, the second-to-last layer produces a vector of numbers (e.g., 768 numbers) called an **embedding**. This vector encodes "what this image looks like" in a high-dimensional space where similar images are close together.

```
quartz grain A  → [0.2, 0.8, 0.1, ...]  ← these two are close in 768D space
quartz grain B  → [0.2, 0.7, 0.1, ...]

biotite grain   → [0.9, 0.1, 0.7, ...]  ← far from quartz embeddings
```

**Why this matters for GneissVision:**
- You can find similar training examples by comparing embeddings
- You can detect when a new image is "different from everything seen so far" (anomaly detection — useful for spotting REE accessories you haven't seen before)
- Few-shot learning works by comparing embeddings: "this unknown grain is closest to monazite examples in embedding space"

In Phase 2-3, storing embeddings of your labeled examples enables fast similarity search without rerunning the whole model.

---

## 9. The GneissVision pipeline — all together

Here's how all the pieces connect in the final vision (pun intended):

```
INPUT: PPL image + XPL image of thin section
         │
         ▼
┌─────────────────────┐
│  SAM2               │  ← finds grain boundaries automatically
│  (grain detection)  │
└─────────────────────┘
         │  → list of grain region crops
         ▼
┌─────────────────────────────────────────┐
│  Phase 1 (now): VLM + RAG              │
│  - Claude claude-sonnet-4-6 vision             │
│  - minerals.json injected as context   │
│  - reasons step-by-step, explains why  │
└─────────────────────────────────────────┘
         │  → predictions + confidence + reasoning
         ▼
┌─────────────────────────────────────────┐
│  Active learning loop                  │
│  - user corrects wrong predictions     │
│  - corrections saved to .jsonl         │
│  - uncertain predictions surfaced first │
└─────────────────────────────────────────┘
         │  → grows labeled dataset
         ▼
┌─────────────────────────────────────────┐
│  Phase 3: Fine-tuned ViT               │
│  - trained on accumulated corrections  │
│  - runs locally, fast, free            │
│  - VLM still used for uncertain cases  │
└─────────────────────────────────────────┘
         │  → mineral labels per grain
         ▼
OUTPUT: Labeled mineral map + modal analysis
        (% quartz, % plagioclase, % REE accessories, etc.)
```

---

## 10. Vocabulary reference

| Term | Definition |
|---|---|
| **Weight** | A single learnable number inside a neural network. A model has millions. |
| **Training** | The process of adjusting weights to minimize prediction error on labeled examples. |
| **Inference** | Running a trained model on new data to get predictions (not training — weights don't change). |
| **Loss function** | A number measuring how wrong the model's predictions are. Training minimizes this. |
| **Gradient descent** | The algorithm that adjusts weights to reduce the loss. Takes small steps downhill on the loss landscape. |
| **Epoch** | One full pass through the training dataset. Training usually runs for many epochs. |
| **Batch** | A small group of examples processed together in one training step (e.g., 32 images at once). |
| **Overfitting** | Model memorizes training examples instead of learning general patterns — fails on new images. Prevented by having enough data and using regularization. |
| **Transfer learning** | Starting from a pretrained model's weights rather than random initialization. |
| **Fine-tuning** | Continuing training of a pretrained model on a new task/dataset. |
| **VLM** | Vision-Language Model — understands both images and text. Claude, GPT-4o are examples. |
| **RAG** | Retrieval-Augmented Generation — injecting reference text into the prompt at inference time. |
| **Embedding** | A vector of numbers that encodes the "meaning" of an image or text in high-dimensional space. |
| **Active learning** | Training loop where the model requests labels for the examples it's most uncertain about. |
| **Semantic segmentation** | Classifying every pixel in an image (vs. classifying the whole image as one class). |
| **SAM** | Segment Anything Model — Meta's model for detecting object boundaries in arbitrary images. |
| **ViT** | Vision Transformer — image model using the attention mechanism from language models. |
| **CNN** | Convolutional Neural Network — image model using sliding local filters. |
| **Hyperparameter** | A setting you choose before training (learning rate, batch size) as opposed to weights the model learns. |
| **Confidence score** | The model's own estimate of how likely its prediction is correct. Not always reliable. |
| **Prompt** | The full text (and images) sent to a VLM as input. Prompt engineering = crafting this carefully. |
| **Context window** | The maximum amount of text+images a VLM can process at once. |
