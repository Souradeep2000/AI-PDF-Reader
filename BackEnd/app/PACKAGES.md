# Behind the Scenes: How OCR Works

Optical Character Recognition (OCR) looks like magic, but it is actually a highly coordinated pipeline that transforms raw pixels into editable text strings.

### The OCR Pipeline Workflow

| Step 1: Input                            | Step 2: Clean                                 | Step 3: Locate                                     | Step 4: Transcribe                                  | Step 5: Verify                                          |
| :--------------------------------------- | :-------------------------------------------- | :------------------------------------------------- | :-------------------------------------------------- | :------------------------------------------------------ |
| **Raw Image** <br> 📷 _(Messy / Tilted)_ | **Pre-Processing** <br> 🧼 _(Clean B&W Text)_ | **Layout Analysis** <br> 📐 _(Find Lines & Words)_ | **Character Recognition** <br> 🧠 _(AI Reads Text)_ | **Post-Processing** <br> 📝 _(Dictionary & Spellcheck)_ |

👉 **Output:** Clean, searchable, and editable text!

---

### Packages Used: Image Pre-Processing (Cleaning the Canvas)

Before reading any text, the engine has to clean up the image. Raw photos have shadows, tilts, and background noise that confuse AI models.

- **Binarization (Thresholding):** Converts the image to strict black and white. Background noise and shadows are stripped away, leaving only sharp text silhouettes.
- **Deskewing:** Detects if the page or camera was tilted and rotates the image back to a perfect horizontal alignment.
- **Denoising:** Erases stray pixels, smudges, or artifacts that might look like accidental periods or commas.

---

### Packages Used: Layout Analysis (Finding the Coordinates)

The engine cannot read everything at once; it needs to know _where_ to look and in what order.

- **Text Detection:** The algorithm scans the image to identify blocks of text, separating them from images, geometric shapes, or blank margins.
- **Segmentation:** It breaks down those large text blocks into individual paragraphs, lines, and eventually crops out single words or characters.

---

### Packages Used: Character Recognition (The Reading AI)

This is the core brain of the system, where shapes are translated into digital letters. Modern engines use two main approaches:

- **Feature Extraction (Older Method):** The engine matches the lines, loops, and intersections of a character against a database of known fonts (e.g., if it has two diagonal lines meeting at a top point with a crossbar, it's an `A`).
- **Neural Networks / Deep Learning (Modern Method):** Uses **CNNs** (Convolutional Networks) to extract visual features and **LSTMs** (Long Short-Term Memory) to read characters sequentially. The AI looks at context—knowing that after the letters `a-p-p-l-e`, the next blurry shape is highly likely to be an `s`.

---

### Packages Used: Post-Processing (The Spellcheck)

The vision model isn't perfect and frequently confuses lookalike characters (like the number `0` and the letter `O`, or `l` and `1`).

- **Lexicon Matching:** The output string is run through a built-in dictionary and language model.
- **Contextual Correction:** If the engine spits out the word `Fr0g`, the language processor automatically corrects the `0` to an `o` because "Frog" is a valid dictionary word and "Fr0g" is not.

---

### 🛠️ Inshort the Hood: The 4-Stage OCR Engine

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

# Behind the scope: How Next Works To be added

---
