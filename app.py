
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Analyzer")
st.write("A data analytics dashboard for understanding student performance.")

st.sidebar.header("Settings")
pass_mark = st.sidebar.slider(
    "Passing marks",
    min_value=0,
    max_value=100,
    value=35
)

def sample_data():
    return pd.DataFrame({
        "Student": [
            "Aarav", "Diya", "Rahul", "Priya", "Arjun",
            "Sneha", "Kiran", "Ananya", "Vikram", "Meera"
        ],
        "Maths": [85, 92, 45, 78, 30, 88, 67, 95, 40, 73],
        "Science": [90, 89, 50, 82, 25, 91, 72, 94, 42, 76],
        "English": [78, 95, 60, 75, 40, 85, 70, 90, 55, 80]
    })

uploaded_file = st.file_uploader(
    "Upload student marks CSV",
    type=["csv"]
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as error:
        st.error(f"Unable to read CSV: {error}")
        st.stop()
else:
    st.info("Sample data is displayed. Upload a CSV to analyze your own data.")
    df = sample_data()

required = ["Student", "Maths", "Science", "English"]

if not all(column in df.columns for column in required):
    st.error("CSV must contain: Student, Maths, Science, English.")
    st.stop()

df = df[required].copy()
df["Student"] = df["Student"].astype("string").str.strip()

subjects = ["Maths", "Science", "English"]

for subject in subjects:
    df[subject] = pd.to_numeric(df[subject], errors="coerce")

if df.empty:
    st.warning("No student records found.")
    st.stop()

if df["Student"].isna().any() or df["Student"].eq("").any():
    st.error("Every student must have a name.")
    st.stop()

if df[subjects].isna().any().any():
    st.error("Please correct missing or invalid marks in the CSV.")
    st.stop()

if not df[subjects].ge(0).all().all() or not df[subjects].le(100).all().all():
    st.error("All marks must be between 0 and 100.")
    st.stop()

df["Average"] = df[subjects].mean(axis=1).round(2)

df["Result"] = df[subjects].ge(pass_mark).all(axis=1).map({
    True: "Pass",
    False: "Fail"
})

df["Grade"] = pd.cut(
    df["Average"],
    bins=[-0.01, 34.99, 49.99, 59.99, 74.99, 100],
    labels=["F", "D", "C", "B", "A"]
)

total = len(df)
average = df["Average"].mean()
passed = int(df["Result"].eq("Pass").sum())
failed = total - passed

st.subheader("📈 Class Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", total)
c2.metric("Class Average", f"{average:.2f}%")
c3.metric("Passed", passed)
c4.metric("Pass Rate", f"{passed / total * 100:.1f}%")

st.subheader("📋 Student Results")
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("📊 Average Marks by Subject")

fig, ax = plt.subplots()
df[subjects].mean().plot(kind="bar", ax=ax)
ax.set_ylabel("Average Marks")
ax.set_ylim(0, 100)
ax.set_xlabel("Subject")
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
plt.close(fig)

st.subheader("🎯 Pass and Fail Analysis")

result_counts = df["Result"].value_counts()

fig, ax = plt.subplots()
result_counts.plot(kind="bar", ax=ax)
ax.set_ylabel("Number of Students")
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
plt.close(fig)

st.subheader("🏆 Top 5 Students")

top_students = df.nlargest(5, "Average")
st.dataframe(top_students, use_container_width=True, hide_index=True)

st.download_button(
    "⬇️ Download Results as CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="student_performance_results.csv",
    mime="text/csv"
)

st.caption("Built with Python, Pandas, Matplotlib and Streamlit.")
