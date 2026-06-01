import os
import requests
import json
import datetime
from collections import defaultdict
import xml.etree.ElementTree as ET

def fetch_contribution_calendar(token, username):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Fetch last 30 days
    to_date = datetime.datetime.utcnow()
    from_date = to_date - datetime.timedelta(days=30)
    
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "login": username,
        "from": from_date.isoformat() + "Z",
        "to": to_date.isoformat() + "Z"
    }
    
    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": query, "variables": variables}
    )
    
    if response.status_code != 200:
        print(f"Error fetching data for {username}: {response.text}")
        return []
        
    data = response.json()
    if "errors" in data:
        print(f"GraphQL Errors for {username}: {data['errors']}")
        return []
        
    weeks = data.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionCalendar", {}).get("weeks", [])
    
    days = []
    for week in weeks:
        for day in week.get("contributionDays", []):
            days.append(day)
            
    # Filter to exactly the last 30 days as GraphQL might return slightly more
    days_dict = {d["date"]: d["contributionCount"] for d in days}
    return days_dict

def main():
    token1 = os.environ.get("GH_TOKEN_1") or os.environ.get("GITHUB_TOKEN")
    token2 = os.environ.get("GH_TOKEN_2") or token1
    
    usernames = [
        {"name": "parpsyche", "token": token1},
        {"name": "parths-infiswift", "token": token2}
    ]
    
    combined_contributions = defaultdict(int)
    
    for u in usernames:
        if not u["token"]:
            print(f"No token provided for {u['name']}. Skipping.")
            continue
            
        print(f"Fetching data for {u['name']}...")
        days_dict = fetch_contribution_calendar(u["token"], u["name"])
        for date_str, count in days_dict.items():
            combined_contributions[date_str] += count

    # Generate dates for the last 30 days
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)).isoformat() for i in range(29, -1, -1)]
    
    counts = [combined_contributions.get(d, 0) for d in dates]
    
    generate_line_graph(dates, counts)
    generate_line_graph(dates, counts, dark_mode=True)

def generate_line_graph(dates, counts, dark_mode=False):
    width = 600
    height = 200
    padding_left = 40
    padding_bottom = 30
    padding_top = 40
    padding_right = 20
    
    bg_color = "#0d1117" if dark_mode else "#ffffff"
    text_color = "#c9d1d9" if dark_mode else "#24292f"
    border_color = "#30363d" if dark_mode else "#e1e4e8"
    line_color = "#2ea043" if dark_mode else "#2da44e"
    fill_color = "rgba(46, 160, 67, 0.2)" if dark_mode else "rgba(45, 164, 78, 0.2)"
    grid_color = "#21262d" if dark_mode else "#ebedf0"
    
    svg = ET.Element("svg", width=str(width), height=str(height), viewBox=f"0 0 {width} {height}", fill="none", xmlns="http://www.w3.org/2000/svg")
    ET.SubElement(svg, "style").text = f"""
        .title {{ font: 600 16px 'Segoe UI', Ubuntu, Sans-Serif; fill: {text_color}; }}
        .label {{ font: 400 10px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8b949e; }}
    """
    
    ET.SubElement(svg, "rect", x="0", y="0", width=str(width), height=str(height), rx="4.5", fill=bg_color, stroke=border_color)
    
    total_commits = sum(counts)
    ET.SubElement(svg, "text", x="20", y="25", **{"class": "title"}).text = f"30-Day Contributions: {total_commits} (Combined)"
    
    if not counts:
        ET.SubElement(svg, "text", x="20", y="100", **{"class": "label"}).text = "No data"
        suffix = "-dark" if dark_mode else ""
        filename = f"dist/combined-tech-stats{suffix}.svg"
        os.makedirs("dist", exist_ok=True)
        tree = ET.ElementTree(svg)
        ET.indent(tree, space="  ", level=0)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        return
        
    max_count = max(counts)
    if max_count == 0:
        max_count = 5 # default scale

    # Drawing grid and y-labels
    graph_width = width - padding_left - padding_right
    graph_height = height - padding_top - padding_bottom
    
    y_steps = 4
    for i in range(y_steps + 1):
        y = padding_top + graph_height - (i * graph_height / y_steps)
        val = int(i * max_count / y_steps)
        ET.SubElement(svg, "line", x1=str(padding_left), y1=str(y), x2=str(width-padding_right), y2=str(y), stroke=grid_color, stroke_width="1")
        ET.SubElement(svg, "text", x=str(padding_left-10), y=str(y+3), text_anchor="end", **{"class": "label"}).text = str(val)

    # Calculate points
    points = []
    x_step = graph_width / (len(counts) - 1)
    for i, count in enumerate(counts):
        x = padding_left + (i * x_step)
        y = padding_top + graph_height - (count / max_count * graph_height)
        points.append((x, y))
        
    # Draw area fill
    path_data = f"M {points[0][0]} {padding_top + graph_height} "
    for x, y in points:
        path_data += f"L {x} {y} "
    path_data += f"L {points[-1][0]} {padding_top + graph_height} Z"
    
    ET.SubElement(svg, "path", d=path_data, fill=fill_color)
    
    # Draw line
    line_data = f"M {points[0][0]} {points[0][1]} "
    for x, y in points[1:]:
        line_data += f"L {x} {y} "
        
    ET.SubElement(svg, "path", d=line_data, fill="none", stroke=line_color, stroke_width="2", stroke_linejoin="round", stroke_linecap="round")
    
    # Draw points (optional, maybe too cluttered for 30 points, just do line)
    
    # X-axis labels (first and last date)
    first_date = datetime.datetime.strptime(dates[0], "%Y-%m-%d").strftime("%b %d")
    last_date = datetime.datetime.strptime(dates[-1], "%Y-%m-%d").strftime("%b %d")
    ET.SubElement(svg, "text", x=str(padding_left), y=str(height-10), text_anchor="start", **{"class": "label"}).text = first_date
    ET.SubElement(svg, "text", x=str(width-padding_right), y=str(height-10), text_anchor="end", **{"class": "label"}).text = last_date

    suffix = "-dark" if dark_mode else ""
    filename = f"dist/combined-tech-stats{suffix}.svg"
    
    os.makedirs("dist", exist_ok=True)
    tree = ET.ElementTree(svg)
    ET.indent(tree, space="  ", level=0)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Generated {filename}")

if __name__ == "__main__":
    main()
