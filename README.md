# Image Labeling Tool (Yes/No)

A **Streamlit-based tool** for labeling images with "Yes" or "No" options, one-by-one, with easy navigation, skipping, and CSV export functionality.

---

## Features

- Upload a CSV file containing image URLs and existing labels.
- Navigate images one-by-one with **Back** and **Next** buttons.
- **Jump to any image** by specifying its number.
- **Preselects existing labels** from the CSV (`is_register` column).
- Update labels and save them in a new column `new_label`.
- Show a **loading message** while switching images.
- Export labeled CSV **anytime**, even if not all images are labeled.
- Supports **partial labeling**.

---

## CSV Format

The input CSV must contain the following columns:

| Column       | Description                        |
|-------------|------------------------------------|
| `image_link` | URL of the image to label           |
| `is_register` | Original label (`Yes` or `No`)     |

The output CSV will include an additional column:

| Column       | Description                        |
|-------------|------------------------------------|
| `new_label`  | Label selected by the user          |

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

```

3. Install the required packages:
```bash
pip install streamlit pandas
```

---

## Usage
1. Run the Streamlit app:
```bash
streamlit run app.py
```

1. Upload your CSV file with image_link and is_register columns. 
2. Navigate through images and select Yes/No for each. 
3. Use the Jump to Image input to quickly move to any image. 
4. Click Download CSV Now at any time to save your progress.

---

Notes

1. Uploaded files are stored in memory; they are not automatically saved to disk.
2. new_label values will persist in the session as long as the app is running.
3. Works best with URLs accessible by the machine running the app.