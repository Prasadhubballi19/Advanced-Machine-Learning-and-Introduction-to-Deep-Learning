import pandas as pd
import webbrowser

# =========================
# LOAD DATA
# =========================
colleges = pd.read_csv("india_colleges.csv")
schools = pd.read_csv("india_schools.csv")

# =========================
# USER INPUT
# =========================
print("\n===== EDUCATION FINDER =====\n")

category = input("Enter category (college/school): ").strip().lower()
location = input("Enter city: ").strip().lower()
max_fees = input("Enter max fees (press Enter to skip): ").strip()

if max_fees != "":
    try:
        max_fees = int(max_fees)
    except:
        print("❌ Invalid fees input")
        exit()
else:
    max_fees = None

# =========================
# FILTER LOGIC
# =========================
if category == "college":
    df = colleges.copy()

    # city filter (contains for better search)
    df = df[df["city"].str.lower().str.contains(location, na=False)]

    # fees filter
    if max_fees:
        df = df[df["fees_ug_inr"].fillna(0) <= max_fees]

    # sort by rating (optional)
    if "rating" in df.columns:
        df = df.sort_values(by="rating", ascending=False)

elif category == "school":
    df = schools.copy()

    df = df[df["city"].str.lower().str.contains(location, na=False)]

    if "rating" in df.columns:
        df = df.sort_values(by="rating", ascending=False)

else:
    print("❌ Invalid category! Choose 'college' or 'school'")
    exit()

# =========================
# CHECK RESULTS
# =========================
if df.empty:
    print("❌ No results found!")
    exit()

# =========================
# CREATE BEAUTIFUL HTML
# =========================
html_content = f"""
<html>
<head>
<title>Search Results</title>
<style>
body {{
    font-family: Arial;
    background: #f4f6f8;
    padding: 20px;
}}
h1 {{
    color: #333;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    background: white;
}}
th, td {{
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
}}
th {{
    background-color: #4CAF50;
    color: white;
}}
tr:hover {{
    background-color: #f1f1f1;
}}
</style>
</head>
<body>

<h1>🔍 Search Results</h1>
<p><b>Category:</b> {category.title()} | <b>City:</b> {location.title()}</p>

{df.head(50).to_html(index=False)}

</body>
</html>
"""

# =========================
# SAVE & OPEN IN CHROME
# =========================
file_path = "results.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("\n✅ Opening results in browser...")

webbrowser.open(file_path)