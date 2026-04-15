import pandas as pd
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse

PORT = 8000

colleges = pd.read_csv("india_colleges.csv")
schools = pd.read_csv("india_schools.csv")


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = """
            <html>
            <head>
            <title>Education Finder</title>
            <style>
            body { font-family: Arial; background:#f4f6f8; padding:40px; }
            form { background:white; padding:20px; width:400px; margin:auto; border-radius:10px; }
            input, select { width:100%; padding:10px; margin-top:10px; }
            button { margin-top:15px; padding:10px; width:100%; background:#4CAF50; color:white; border:none; }
            </style>
            </head>
            <body>

            <h2 style="text-align:center;"> Education Finder</h2>

            <form action="/search" method="get">
                <label>Category:</label>
                <select name="category">
                    <option value="college">College</option>
                    <option value="school">School</option>
                </select>

                <label>City:</label>
                <input type="text" name="location" required>

                <label>Max Fees:</label>
                <input type="text" name="fees">

                <button type="submit">Search</button>
            </form>

            </body>
            </html>
            """

            self.wfile.write(html.encode())

        elif self.path.startswith("/search"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)

            category = params.get("category", [""])[0].lower()
            location = params.get("location", [""])[0].lower()
            fees = params.get("fees", [""])[0]

            try:
                fees = int(fees) if fees else None
            except:
                fees = None

            if category == "college":
                df = colleges.copy()
                df = df[df["city"].str.lower().str.contains(location, na=False)]

                if fees:
                    df = df[df["fees_ug_inr"].fillna(0) <= fees]

            elif category == "school":
                df = schools.copy()
                df = df[df["city"].str.lower().str.contains(location, na=False)]

            else:
                df = pd.DataFrame()

            if df.empty:
                table = "<h3>No results found</h3>"
            else:
                table = df.head(50).to_html(index=False)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = f"""
            <html>
            <head>
            <style>
            body {{ font-family: Arial; padding:20px; background:#f4f6f8; }}
            table {{ border-collapse: collapse; width:100%; background:white; }}
            th, td {{ padding:10px; border:1px solid #ddd; }}
            th {{ background:#4CAF50; color:white; }}
            </style>
            </head>
            <body>

            <h2> Results</h2>
            <a href="/"> Back</a>
            <br><br>

            {table}

            </body>
            </html>
            """

            self.wfile.write(html.encode())


# Run server
print(f"✅ Open in browser: http://localhost:{PORT}")
import webbrowser
webbrowser.open(f"http://localhost:{PORT}")

server = HTTPServer(("localhost", PORT), MyHandler)
server.serve_forever()   