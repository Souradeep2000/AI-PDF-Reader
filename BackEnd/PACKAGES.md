### 🛠️ Under the Hood: The 4-Stage OCR Engine

When a PDF is uploaded, the backend processes it through a highly optimized document intelligence pipeline to transform raw pixels into context-aware, structured text chunks.

---

#### 📊 Pipeline Dataflow

> **[01. Pre-Processing]**
> ↳ _Adaptive Thresholding • Bilateral Filtering • Radon Deskewing_
> 👇 _(Output: Clean Binarized Canvas)_
>
> **[02. Layout Analysis]**
> ↳ _Morphological Dilation • RLSA • Contours Classification_
> 👇 _(Output: Segmented Reading Order Blocks)_
>
> **[03. OCR Core Extraction]**
> ↳ _CNN Feature Mapping • RNN/LSTM Networks • Beam Search_
> 👇 _(Output: Raw Text Character Matrix)_
>
> **[04. Post-Processing & Regularization]**
> ↳ _Regex De-hyphenation • Tabular Reconstruction • Unicode Normalization_
> 👇 _(Output: Final Output)_
>
> 🎉 **[🚀 Clean Structured Markdown / JSON Text]**

---

#### 📐 The Processing Pipeline Breakdown

| Stage                  | Focus                | Key Techniques                                                      | Engineering Objective                                                                                                                                   |
| :--------------------- | :------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **01. Normalization**  | Image Pre-processing | Adaptive Thresholding, Bilateral Filtering, Radon Deskewing         | Converts raw scans to binary text matrices, strips out noise, and straightens crooked uploads to a perfect $0^\circ$ baseline.                          |
| **02. Segmentation**   | Layout Analysis      | Morphological Dilation, RLSA, Contours Classification               | Isolates structural blocks (`Headers`, `Columns`, `Tables`). Ensures multi-column articles are read in human logical order rather than straight across. |
| **03. Extraction**     | The OCR Core         | CNN Feature Mapping, RNN/LSTM Networks, Beam Search Decoding        | Translates character blocks into token strings, ranking text probability against an inline language model for high accuracy.                            |
| **04. Regularization** | Post-processing      | Regex De-hyphenation, Tabular Reconstruction, Unicode Normalization | Stitches broken line wraps back together, rebuilds table matrices, and cleans up digital artifacts before sending text to the vector store.             |

---
