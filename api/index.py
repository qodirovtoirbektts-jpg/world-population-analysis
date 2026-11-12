"""
Vercel Serverless Python API
World Population Analytics (2026)
"""

import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "world_population_2026.json"

def get_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = get_data()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        path = self.path
        if "uzbekistan" in path.lower():
            uzb = [d for d in data if d.get("Country/Territory") == "Uzbekistan"]
            res = uzb[0] if uzb else {}
        elif "top10" in path.lower():
            res = data[:10]
        else:
            res = {
                "total_countries": len(data),
                "year": 2026,
                "world_population_2026": sum(int(d.get("2026 Population", 0)) for d in data),
                "countries": data
            }
            
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
        return
