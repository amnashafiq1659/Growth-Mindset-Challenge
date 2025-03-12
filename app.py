import streamlit as st
import pandas as pd   
import os 
from io import BytesIO

st.set_page_config(page_title="Data Wizard: Convert & Clean", layout="wide")

# Custom Styling
st.markdown(
    """
   <style>
    body {
        background: linear-gradient(135deg, #1A1A2E, #16213E);
        color: #E6E6E6 ;
        font-family: 'Poppins', sans-serif;
    }
    .title {
        color: #00FFFF;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        text-shadow: 0px 0px 15px #00FFFF;
    }
    .subtitle {
        color: #FF00FF;
        font-size: 20px;
        font-style: italic;
        text-shadow: 0px 0px 15px #FF00FF;
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF00FF, #00FFFF);
        color: white;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0px 0px 15px #00FFFF;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #00FFFF, #FF00FF);
        box-shadow: 0px 0px 20px #FF00FF;
        transform: scale(1.05);
    }
    .data-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 0px 15px rgba(0, 255, 255, 0.5);
    }
    .upload-box {
        border: 2px dashed #00FFFF;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        transition: 0.3s;
    }
    .upload-box:hover {
        background: rgba(0, 255, 255, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation with Dark Mode Toggle
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload", "Cleaning", "Visualization", "Export"])

st.sidebar.markdown("---")

st.markdown("<div class='title'>🔄 Data Wizard: Convert & Clean</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Magically transform, visualize, AI-powered, fast, and intelligent data cleaning at your fingertips!</div>", unsafe_allow_html=True)

if page == "Upload":
    st.subheader("📂 Drag & Drop Your Files (CSV or Excel)")
uploaded_files = st.file_uploader("Drop or select files to clean and analyze", type=["csv","xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue 

        st.markdown(f"<div class='data-card'><b>📄 File Name:</b> {file.name} | <b>📦 Size:</b> {file.size / 1024:.2f} KB</div>", unsafe_allow_html=True)


        st.write("### 🔍 Data Preview")
        st.dataframe(df.head())

st.sidebar.subheader("⚡ Quick Actions")

if st.sidebar.button("🧹 Remove Duplicates"):
    if "df" in locals():
        df.drop_duplicates(inplace=True)
        st.success("✅ Duplicates removed successfully!")
    else:
        st.error("❌ Please upload a file first!")

if st.sidebar.button("🛠 Auto-Fill Missing Values"):
    if "df" in locals():
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        st.success("✅ Missing values filled successfully!")
    else:
        st.error("❌ Please upload a file first!")

st.sidebar.markdown("---")       

if page == "Cleaning":
        st.subheader("🛠 Smart Data Cleaning!")
        if st.checkbox(f"✅ AI-Suggested Cleaning"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🧹 Remove Duplicates", key="remove_duplicates"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"🛠 Auto-Fill Missing Values", key="auto_fill_missing" ):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values auto-filled!")       

if page == "Visualization":
            st.subheader("📊 Interactive Data Visualization")
            if st.checkbox(f"📈 Show Trends"):
                st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

if page == "Export":
            st.subheader("🔄 Export Clean Data!")
            conversion_type = st.radio(f"Convert to:", ["CSV","Excel"])
            if st.button(f"📥 Download Clean Data"):
                buffer = BytesIO()
                file_name = f"cleaned_data.{conversion_type.lower()}"
                if conversion_type == "CSV":
                    df.to_csv(buffer,index=False) 
                    mime_type = "type/csv"

                elif conversion_type == "Excel":
                       df.to_excel(buffer,index=False)
                       mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label = "📥 Download Clean Data",
                    data=buffer,
                    file_name = file_name,
                    mime = mime_type,
                )       

st.success("✅ All files processed successfully! Your clean data is ready.")                
