import json
import uuid
import sys


def make_id():
    return str(uuid.uuid4())


def main():
    # Read your Hugo-friendly resume
    with open("data/resume.json", "r") as f:
        src = json.load(f)

    basics = src.get("basics", {})

    # Initialize the base Reactive Resume v5 structure
    rx = {
        "picture": {
            "hidden": False,
            "url": "https://smileyniloc.github.io/my-bio/images/me.jpg",
            "size": 64,
            "rotation": 0,
            "aspectRatio": 1,
            "borderRadius": 0,
            "borderColor": "rgba(0,0,0,0)",
            "borderWidth": 0,
            "shadowColor": "rgba(0,0,0,0)",
            "shadowWidth": 0,
        },
        "basics": {
            "name": basics.get("name", ""),
            "headline": basics.get("label", ""),
            "email": basics.get("email", ""),
            "phone": basics.get("phone", ""),
            "location": "",
            "website": {"url": basics.get("url", ""), "label": "Portfolio"},
            "customFields": [],
        },
        "summary": {
            "title": "Summary",
            "columns": 1,
            "hidden": False,
            "content": f"<p>{basics.get('summary', '')}</p><br><p>{basics.get('aboutme', '')}</p>",
        },
        "sections": {
            "profiles": {
                "title": "Profiles",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "experience": {
                "title": "Experience",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "education": {
                "title": "Education",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "projects": {
                "title": "Projects",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "skills": {"title": "Skills", "columns": 1, "hidden": False, "items": []},
            "languages": {
                "title": "Languages",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "interests": {
                "title": "Interests",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "awards": {"title": "Awards", "columns": 1, "hidden": False, "items": []},
            "certifications": {
                "title": "Certifications",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "publications": {
                "title": "Publications",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "volunteer": {
                "title": "Volunteer",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
            "references": {
                "title": "References",
                "columns": 1,
                "hidden": False,
                "items": [],
            },
        },
        "customSections": [],
        "metadata": {
            "template": "rhyhorn",
            "layout": {
                "sidebarWidth": 25,
                "pages": [
                    {
                        "fullWidth": False,
                        "main": [
                            "summary",
                            "experience",
                            "education",
                            "projects",
                            "volunteer",
                        ],
                        "sidebar": ["profiles", "skills", "awards"],
                    }
                ],
            },
            "css": {"enabled": False, "value": ""},
            "page": {
                "gapX": 20,
                "gapY": 20,
                "marginX": 24,
                "marginY": 24,
                "format": "letter",
                "locale": "en-US",
                "hideIcons": False,
            },
            "design": {
                "level": {"icon": "", "type": "hidden"},
                "colors": {
                    "primary": "rgba(0,0,0,1)",
                    "text": "rgba(0,0,0,1)",
                    "background": "rgba(255,255,255,1)",
                },
            },
            "typography": {
                "body": {
                    "fontFamily": "Inter",
                    "fontWeights": ["400"],
                    "fontSize": 10,
                    "lineHeight": 1.5,
                },
                "heading": {
                    "fontFamily": "Inter",
                    "fontWeights": ["700"],
                    "fontSize": 14,
                    "lineHeight": 1.5,
                },
            },
            "notes": "",
        },
    }

    # Map Profiles
    for p in basics.get("profiles", []):
        rx["sections"]["profiles"]["items"].append(
            {
                "id": make_id(),
                "hidden": False,
                "options": {"showLinkInTitle": False},
                "icon": p.get("network", "").lower() + "-logo",
                "network": p.get("network", ""),
                "username": p.get("username", ""),
                "website": {"url": p.get("url", ""), "label": p.get("network", "")},
            }
        )

    # Map Work -> Experience
    for w in src.get("work", []):
        desc = (
            "<ul>"
            + "".join([f"<li>{h}</li>" for h in w.get("highlights", [])])
            + "</ul>"
        )
        period = f"{w.get('startDate', '')} - {w.get('endDate', '')}"
        rx["sections"]["experience"]["items"].append(
            {
                "id": make_id(),
                "hidden": False,
                "options": {"showLinkInTitle": False},
                "company": w.get("name", ""),
                "position": w.get("position", ""),
                "location": "",
                "period": period.strip(" - "),
                "website": {"url": "", "label": ""},
                "description": desc,
            }
        )

    # Map Education
    for e in src.get("education", []):
        courses = e.get("courses", [])
        highlights = e.get("highlights", [])
        desc = f"<p><strong>Highlights:</strong> {', '.join(highlights)}</p><p><strong>Courses:</strong> {', '.join(courses)}</p>"
        period = f"{e.get('startDate', '')} - {e.get('endDate', '')}"
        rx["sections"]["education"]["items"].append(
            {
                "id": make_id(),
                "hidden": False,
                "options": {"showLinkInTitle": False},
                "school": e.get("institution", ""),
                "degree": e.get("studyType", ""),
                "area": e.get("area", ""),
                "grade": e.get("score", ""),
                "location": "",
                "period": period.strip(" - "),
                "website": {"url": e.get("url", ""), "label": "Website"},
                "description": desc,
            }
        )

    # Map Projects
    for proj in src.get("projects", []):
        desc_html = (
            f"<p>{proj.get('description', '')}</p><ul>"
            + "".join([f"<li>{h}</li>" for h in proj.get("highlights", [])])
            + "</ul>"
        )
        if proj.get("keywords"):
            desc_html += (
                f"<p><em>Keywords: {', '.join(proj.get('keywords', []))}</em></p>"
            )
        rx["sections"]["projects"]["items"].append(
            {
                "id": make_id(),
                "hidden": False,
                "options": {"showLinkInTitle": False},
                "name": proj.get("name", ""),
                "period": "",
                "website": {
                    "url": proj.get("url", ""),
                    "label": "Link" if proj.get("url") else "",
                },
                "description": desc_html,
            }
        )

    # Map Skills
    for s in src.get("skills", []):
        rx["sections"]["skills"]["items"].append(
            {
                "id": make_id(),
                "hidden": False,
                "options": {"showLinkInTitle": False},
                "icon": "",
                "name": s.get("name", ""),
                "proficiency": "",
                "level": 0,
                "keywords": s.get("keywords", []),
            }
        )

    # Map Volunteer
    for v in src.get("volunteer", []):
        desc = (
            f"<p>{v.get('summary', '')}</p><ul>"
            + "".join([f"<li>{h}</li>" for h in v.get("highlights", [])])
            + "</ul>"
        )
        period = f"{v.get('startDate', '')} - {v.get('endDate', 'Present')}"
        rx["sections"]["volunteer"]["items"].append(
            {
                "id": make_id(),
                "hidden": False,
                "options": {"showLinkInTitle": False},
                "organization": v.get("organization", ""),
                "location": "",
                "period": period.strip(" - "),
                "website": {"url": "", "label": ""},
                "description": desc,
            }
        )

    # Map Awards
    for a in src.get("awards", []):
        rx["sections"]["awards"]["items"].append(
            {
                "id": make_id(),
                "hidden": False,
                "options": {"showLinkInTitle": False},
                "title": a.get("title", ""),
                "awarder": a.get("awarder", ""),
                "date": a.get("date", ""),
                "website": {"url": "", "label": ""},
                "description": f"<p>{a.get('summary', '')}</p>",
            }
        )

    # Write out the final payload specifically for the curl command
    final_payload = {"data": rx}
    with open("data/rx-payload.json", "w") as out:
        json.dump(final_payload, out)


if __name__ == "__main__":
    main()
