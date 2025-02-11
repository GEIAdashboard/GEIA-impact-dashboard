import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from fpdf import FPDF

# Streamlit Dashboard
st.title("GEIA Social Impact Dashboard")
st.subheader("Community Impact Metrics")

# Data Upload Option
st.info("📂 Please upload a CSV file containing the community impact data.")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data uploaded successfully!")
else:
    st.warning("⚠️ No file uploaded. Please upload a CSV to proceed.")
    df = pd.DataFrame()

# Display Data Table
if not df.empty:
    st.dataframe(df)

    # Interactive Filtering
    selected_community = st.selectbox("Select a Community", df["Community"].unique())
    df_filtered = df[df["Community"] == selected_community]

    # Visualizing Metrics
    st.subheader("Community Sentiment Analysis")
    fig, ax = plt.subplots()
    ax.bar(df_filtered["Community"], df_filtered["Community Sentiment (1-10)"], color='skyblue')
    ax.set_ylabel("Sentiment Score")
    ax.set_title("Community Well-Being Sentiment Scores")
    st.pyplot(fig)

    st.subheader("Income Growth vs. Employment Rate")
    fig, ax = plt.subplots()
    ax.scatter(df_filtered["Income Growth (%)"], df_filtered["Employment Rate (%)"], c='green', label="Communities")
    ax.set_xlabel("Income Growth (%)")
    ax.set_ylabel("Employment Rate (%)")
    ax.set_title("Correlation Between Income Growth & Employment")
    st.pyplot(fig)

    st.subheader("Food Security Index Across Communities")
    fig, ax = plt.subplots()
    ax.bar(df_filtered["Community"], df_filtered["Food Security Index"], color='orange')
    ax.set_ylabel("Food Security Score")
    ax.set_title("Food Security Levels by Community")
    st.pyplot(fig)

    st.subheader("Education Access Comparison")
    fig, ax = plt.subplots()
    ax.plot(df_filtered["Community"], df_filtered["Education Access (%)"], marker='o', linestyle='-', color='blue')
    ax.set_ylabel("Education Access (%)")
    ax.set_title("Percentage of Population with Education Access")
    st.pyplot(fig)

    # Generate Custom CSR/ESG Report (PDF)
    def generate_pdf(selected_community):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"GEIA Social Impact Report - {selected_community}", ln=True, align='C')
        pdf.ln(10)
        df_filtered = df[df["Community"] == selected_community]
        
        for index, row in df_filtered.iterrows():
            pdf.cell(0, 10, f"Community: {row['Community']}", ln=True)
            pdf.cell(0, 10, f"Income Growth: {row['Income Growth (%)']:.2f}%,", ln=True)
            pdf.cell(0, 10, f"Employment Rate: {row['Employment Rate (%)']:.2f}%,", ln=True)
            pdf.cell(0, 10, f"Food Security Index: {row['Food Security Index']:.2f},", ln=True)
            pdf.cell(0, 10, f"Education Access: {row['Education Access (%)']:.2f}%,", ln=True)
            pdf.cell(0, 10, f"Community Sentiment: {row['Community Sentiment (1-10)']:.2f},", ln=True)
            pdf.ln(5)
        
        pdf.output("GEIA_Social_Impact_Report.pdf")
        return "GEIA_Social_Impact_Report.pdf"

    selected_report_community = st.selectbox("Generate Report for Community", df["Community"].unique())
    if st.button("Download CSR/ESG Report (PDF)"):
        pdf_path = generate_pdf(selected_report_community)
        st.success("Report generated successfully!")
        st.download_button("Download Report", data=open(pdf_path, "rb"), file_name="GEIA_Social_Impact_Report.pdf")

st.markdown("### Deployment Plan:")
st.markdown("- Deploying on Streamlit Cloud for beta testing.")
st.markdown("- Optimizing UI for sponsors and mobile users.")
