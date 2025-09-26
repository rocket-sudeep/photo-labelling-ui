import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Image Labeling App", layout="centered")
st.title("🔖 Image Labeling Tool (Yes/No)")

st.markdown("""
### How to Use  
1. Upload a CSV file with two columns:  
   - `image_link` → URL of the image  
   - `is_register` → existing label (`Yes` or `No`)  

2. Use the **Yes/No selector** to confirm or change the label. Select "Yes" if the image is an Anganwadi register, otherwise "No".
3. Click **Next** to go to the next image, or **Back** to correct the previous one.  
4. You can **jump to any image** also using the + / - buttons on top of the image box.
5. At any time, click **Download CSV** to export your work (with a `new_label` column).  
""")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Validate CSV
    if not {"image_link", "is_register"}.issubset(df.columns):
        st.error("CSV must contain 'image_link' and 'is_register' columns.")
    else:
        # Initialize session state
        if "index" not in st.session_state:
            st.session_state.index = 0
        if "new_labels" not in st.session_state:
            st.session_state.new_labels = [None] * len(df)
        if "loading" not in st.session_state:
            st.session_state.loading = False

        # Jump to image
        jump_index = st.number_input(
            "Jump to image number:",
            min_value=1,
            max_value=len(df),
            value=st.session_state.index + 1,
            step=1
        )
        if jump_index - 1 != st.session_state.index:
            st.session_state.loading = True
            st.session_state.index = jump_index - 1
            st.experimental_rerun()

        idx = st.session_state.index
        row = df.iloc[idx]

        # Image placeholder
        image_placeholder = st.empty()

        # Show loading message if navigating
        if st.session_state.loading:
            image_placeholder.text("⏳ Loading image...")
            time.sleep(0.5)  # simulate small loading delay
            st.session_state.loading = False

        # Show image
        image_placeholder.image(row["image_link"], caption=f"Image {idx+1} of {len(df)}", use_container_width=True)

        # Default selection based on is_register or saved new_label
        default_label = (
            st.session_state.new_labels[idx]
            if st.session_state.new_labels[idx] is not None
            else row["is_register"]
        )

        new_label = st.radio(
            "Select label:", ["Yes", "No"],
            index=0 if str(default_label).strip().lower() == "yes" else 1,
            key=f"radio_{idx}"
        )

        # Save label
        st.session_state.new_labels[idx] = new_label

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back", disabled=(idx == 0)):
                st.session_state.loading = True
                st.session_state.index = max(0, idx - 1)
                st.rerun()

        with col2:
            if st.button("Next ➡️", disabled=(idx == len(df)-1)):
                st.session_state.loading = True
                st.session_state.index = min(len(df)-1, idx + 1)
                st.rerun()

        st.markdown("---")

        # Temporary CSV export at any time
        df["new_label"] = st.session_state.new_labels  # update current labels
        st.download_button(
            "💾 Download CSV Now",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="labeled_data.csv",
            mime="text/csv"
        )

        # Optional: show success when all labeled
        if all(label is not None for label in st.session_state.new_labels):
            st.success("✅ All images labeled!")