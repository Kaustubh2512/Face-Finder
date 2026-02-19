import streamlit as st
import pandas as pd
from pathlib import Path
import os
import cv2
import numpy as np
from face_finder1 import load_face_app, build_known_embeddings, process_event_photos

# Page Configuration
st.set_page_config(
    page_title="Face Finder AI",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.title("👤 Face Finder AI")
st.markdown("Automate face identification in event photos with high-accuracy AI.")

# Initialize Session State
if 'face_app' not in st.session_state:
    st.session_state.face_app = None
if 'processed_df' not in st.session_state:
    st.session_state.processed_df = None

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    known_path = st.text_input("Known Faces Directory", value="Known", help="Directory containing folders of people's faces")
    photos_path = st.text_input("Event Photos Directory", value="Event Photos", help="Directory containing images to scan")
    output_path = st.text_input("Output Directory", value="output", help="Where matched images will be saved")
    
    st.divider()
    
    st.subheader("Performance Settings")
    fast_mode = st.toggle("Fast Mode", value=False, help="Uses lower resolution detection for 2-3x speedup. Good for clear photos.")
    use_gpu = st.toggle("Use GPU Acceleration", value=True, help="Use graphics card for 10x speedup (requires compatible hardware).")
    
    det_size_val = 320 if fast_mode else 640
    
    st.divider()
    
    st.subheader("Fine-tuning")
    threshold = st.slider("Match Threshold", 0.0, 1.0, 0.35, 0.05, help="Lower = more matches, Higher = more accurate")
    min_face = st.number_input("Min Face Size (px)", value=60, step=10)

    st.divider()
    
    if st.button("🚀 Start Processing"):
        st.session_state.start_processing = True
    else:
        st.session_state.start_processing = False

# Main Area
tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Processing", "🖼️ Results"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("How it works")
        st.write("""
        1. **Known Faces**: Create a folder for each person inside your 'Known' directory. Put clear photos of them inside.
        2. **Event Photos**: Put all your event or group photos in another directory.
        3. **Processing**: The AI will build a visual profile for each known person and scan all event photos.
        4. **Export**: Found faces are saved in organized folders and detailed reports are generated.
        """)
    with col2:
        st.info("💡 **Tip:** Clear front-facing photos in the 'Known' folder yield the best results.")

with tab2:
    if st.session_state.get('start_processing', False):
        kp = Path(known_path)
        pp = Path(photos_path)
        op = Path(output_path)
        
        if not kp.exists() or not pp.exists():
            st.error("Error: Please make sure both 'Known' and 'Event Photos' directories exist.")
        else:
            with st.status("🔍 Processing faces...", expanded=True) as status:
                # 1. Load Model
                if st.session_state.face_app is None:
                    st.write("Loading AI models (InsightFace)...")
                    st.session_state.face_app = load_face_app(det_size=det_size_val, use_gpu=use_gpu)
                
                # 2. Build Embeddings
                st.write("Building reference database for known people...")
                people_embs = build_known_embeddings(st.session_state.face_app, kp, min_size=min_face)
                
                if not people_embs:
                    st.error("No valid faces found in 'Known' directory!")
                    status.update(label="Scanning Failed", state="error")
                else:
                    st.write(f"Loaded {len(people_embs)} individuals.")
                    
                    # Progress Bar Placeholder
                    pb = st.progress(0)
                    st_text = st.empty()

                    def update_progress(current, total, filename):
                        percent = current / total
                        pb.progress(percent)
                        st_text.text(f"Scanning ({current}/{total}): {filename}")

                    # 3. Process Photos
                    df = process_event_photos(
                        st.session_state.face_app,
                        people_embs,
                        pp,
                        op,
                        threshold,
                        min_face,
                        progress_callback=update_progress
                    )
                    st.session_state.processed_df = df
                    status.update(label="Processing Complete!", state="complete", expanded=False)
                    
                    # Detailed Summary after processing
                    st.success("Matching finished successfully!")
                    
                    # Show quick stats
                    matches = df[df['matches'] != ""]
                    unique_people_found = set()
                    for m in matches['matches']:
                        unique_people_found.update(m.split(","))
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Photos Scanned", len(df))
                    c2.metric("Photos with Matches", len(matches))
                    c3.metric("People Identified", len(unique_people_found))

                    if not matches.empty:
                        st.subheader("Detected Individuals")
                        # Count matches per person
                        all_matches = []
                        for m in matches['matches']:
                            all_matches.extend(m.split(","))
                        
                        counts = pd.Series(all_matches).value_counts().reset_index()
                        counts.columns = ['Person', 'Appearances']
                        st.bar_chart(counts.set_index('Person'))

    elif st.session_state.processed_df is None:
        st.write("Configure settings in the sidebar and click **Start Processing**.")
    else:
        st.write("Processing previously completed. Check the Results tab.")

with tab3:
    if st.session_state.processed_df is not None:
        df = st.session_state.processed_df
        
        # Summary Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Photos", len(df))
        m2.metric("Matches Found", len(df[df['matches'] != ""]))
        m3.metric("Unique People", len(set(",".join(df['matches'].tolist()).split(",")) - {""}))
        
        st.divider()
        
        # View Results
        st.subheader("Match Breakdown")
        st.dataframe(df, width='stretch')
        
        # Preview Annotated Images
        if len(df) > 0:
            st.subheader("Preview Annotated Images")
            # Filter to only photos with matches
            matched_df = df[df['matches'] != ""]
            if not matched_df.empty:
                selected_photo = st.selectbox("Select a photo to preview:", matched_df['photo'].tolist())
                ann_path = matched_df[matched_df['photo'] == selected_photo]['annotated'].values[0]
                if Path(ann_path).exists():
                    st.image(str(ann_path), caption=f"Identified: {matched_df[matched_df['photo'] == selected_photo]['matches'].values[0]}")
                else:
                    st.warning("Annotated image file not found.")
    else:
        st.info("Start processing to see results here.")

# Footer
st.divider()
st.caption("Built with ❤️ using Streamlit and InsightFace.")
