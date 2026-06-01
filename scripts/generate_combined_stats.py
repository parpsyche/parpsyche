import os
import requests
import json
import datetime
from collections import defaultdict
import xml.etree.ElementTree as ET

def fetch_weekly_contributions(token, username):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Calculate timestamp for 7 days ago
    from_date = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat() + "Z"
    
    query = """
    query($login: String!, $from: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from) {
          commitContributionsByRepository(maxRepositories: 100) {
            repository {
              name
              owner { login }
              languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                edges {
                  size
                  node {
                    name
                    color
                  }
                }
              }
            }
            contributions {
              totalCount
            }
          }
        }
      }
    }
    """
    
    variables = {
        "login": username,
        "from": from_date
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
        
    return data.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("commitContributionsByRepository", [])

def main():
    # Use standard GITHUB_TOKEN if available, else require a PAT
    token1 = os.environ.get("GH_TOKEN_1") or os.environ.get("GITHUB_TOKEN")
    token2 = os.environ.get("GH_TOKEN_2") or token1
    
    usernames = [
        {"name": "parpsyche", "token": token1},
        {"name": "parths-infiswift", "token": token2}
    ]
    
    language_stats = defaultdict(lambda: {"size": 0, "color": "#858585", "commits": 0})
    total_size = 0
    
    for u in usernames:
        if not u["token"]:
            print(f"No token provided for {u['name']}. Skipping.")
            continue
            
        print(f"Fetching data for {u['name']}...")
        repos = fetch_weekly_contributions(u["token"], u["name"])
        
        for repo_contrib in repos:
            repo = repo_contrib["repository"]
            commits = repo_contrib["contributions"]["totalCount"]
            languages = repo.get("languages", {}).get("edges", [])
            
            # Distribute commit weight by language size in repo
            # This is an approximation since GitHub doesn't give languages per commit
            repo_total_size = sum(edge["size"] for edge in languages)
            
            for edge in languages:
                lang_name = edge["node"]["name"]
                lang_color = edge["node"]["color"] or "#858585"
                lang_size = edge["size"]
                
                # Approximate size added by this user this week (just using raw size or we can use commits)
                # Let's use a blended metric: repo_lang_ratio * user_commits
                if repo_total_size > 0:
                    ratio = lang_size / repo_total_size
                    weight = commits * ratio
                    language_stats[lang_name]["size"] += weight
                    language_stats[lang_name]["color"] = lang_color
                    language_stats[lang_name]["commits"] += commits * ratio
                    total_size += weight

    if total_size == 0:
        print("No language data found for the past week.")
        # Fallback to empty state
        generate_svg({}, 0)
        return
        
    # Sort languages by size
    sorted_langs = sorted(language_stats.items(), key=lambda x: x[1]["size"], reverse=True)
    
    # Take top 5, group rest into "Other"
    top_langs = sorted_langs[:5]
    other_size = sum(lang[1]["size"] for lang in sorted_langs[5:])
    if other_size > 0:
         top_langs.append(("Other", {"size": other_size, "color": "#ededed", "commits": 0}))
         
    generate_svg(top_langs, total_size)
    generate_svg(top_langs, total_size, dark_mode=True)

def generate_svg(top_langs, total_size, dark_mode=False):
    width = 400
    height = 200
    
    bg_color = "#0d1117" if dark_mode else "#ffffff"
    text_color = "#c9d1d9" if dark_mode else "#24292f"
    border_color = "#30363d" if dark_mode else "#e1e4e8"
    
    svg = ET.Element("svg", width=str(width), height=str(height), viewBox=f"0 0 {width} {height}", fill="none", xmlns="http://www.w3.org/2000/svg")
    ET.SubElement(svg, "style").text = f"""
        .title {{ font: 600 16px 'Segoe UI', Ubuntu, Sans-Serif; fill: {text_color}; }}
        .lang-name {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: {text_color}; }}
        .lang-stat {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8b949e; }}
    """
    
    ET.SubElement(svg, "rect", x="0", y="0", width=str(width), height=str(height), rx="4.5", fill=bg_color, stroke=border_color)
    ET.SubElement(svg, "text", x="25", y="35", **{"class": "title"}).text = "Weekly Tech Stack (Both Profiles)"
    
    if not top_langs or total_size == 0:
         ET.SubElement(svg, "text", x="25", y="70", **{"class": "lang-name"}).text = "No contributions this week."
    else:
        # Draw bar
        bar_x = 25
        bar_y = 55
        bar_w = 350
        bar_h = 10
        ET.SubElement(svg, "rect", x=str(bar_x), y=str(bar_y), width=str(bar_w), height=str(bar_h), rx="5", fill="#ebedf0")
        
        current_x = bar_x
        for lang_name, lang_data in top_langs:
            ratio = lang_data["size"] / total_size
            w = bar_w * ratio
            if w > 0:
                ET.SubElement(svg, "rect", x=str(current_x), y=str(bar_y), width=str(w), height=str(bar_h), rx="5" if current_x==bar_x or (current_x+w)>=(bar_x+bar_w) else "0", fill=lang_data["color"])
                current_x += w
                
        # Draw legend
        leg_y = 85
        col1_x = 25
        col2_x = 200
        
        for i, (lang_name, lang_data) in enumerate(top_langs):
            ratio = lang_data["size"] / total_size
            pct = f"{ratio * 100:.1f}%"
            
            x = col1_x if i % 2 == 0 else col2_x
            y = leg_y + (i // 2) * 25
            
            ET.SubElement(svg, "circle", cx=str(x+5), cy=str(y-4), r="5", fill=lang_data["color"])
            ET.SubElement(svg, "text", x=str(x+15), y=str(y), **{"class": "lang-name"}).text = lang_name
            ET.SubElement(svg, "text", x=str(x+100), y=str(y), **{"class": "lang-stat"}).text = pct

    suffix = "-dark" if dark_mode else ""
    filename = f"dist/combined-tech-stats{suffix}.svg"
    
    os.makedirs("dist", exist_ok=True)
    tree = ET.ElementTree(svg)
    ET.indent(tree, space="  ", level=0)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Generated {filename}")

if __name__ == "__main__":
    main()
