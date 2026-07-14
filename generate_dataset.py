"""
generate_dataset.py
--------------------
Generates a realistic, synthetic civic-complaint dataset for the
Smart Complaint Management System (ai-service).

Output: complaints.csv
Columns: complaint_id, category, complaint_text, area, date_reported,
         priority, status

Run:
    python generate_dataset.py
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # reproducible output

# ---------------------------------------------------------------------
# 1. Areas / localities used to make complaints feel location-specific
# ---------------------------------------------------------------------
AREAS = [
    "Gandhi Nagar", "Anna Nagar", "Thillai Nagar", "Srirangam",
    "K.K. Nagar", "Cantonment", "Woraiyur", "Ariyamangalam",
    "Golden Rock", "Ponmalai", "Thiruverumbur", "Crawford",
    "Bharathi Nagar", "Vayalur Road", "Puthur", "Edamalaipatti Pudur",
    "Chinthamani", "Palpannai", "Melapudur", "Kattur",
]

STREET_TYPES = [
    "Main Road", "Cross Street", "2nd Street", "3rd Street",
    "Colony Road", "Bypass Road", "Market Street", "Lake Road"
]

# ---------------------------------------------------------------------
# 2. Category-specific complaint sentence templates
# ---------------------------------------------------------------------
TEMPLATES = {
    "Garbage": [
        "Garbage has not been collected in {area} {street} for over a week, causing bad smell.",
        "Overflowing garbage bin near {area} {street} is attracting stray dogs and flies.",
        "Household waste is being dumped on the roadside in {area} instead of the bin.",
        "The garbage truck has skipped our street ({area} {street}) for three days in a row.",
        "Uncollected garbage near the market in {area} is causing a hygiene issue.",
        "Plastic waste is piling up near the {area} {street} community bin.",
        "No garbage collection has happened in {area} since last Monday.",
        "Dead animal lying near the garbage dump in {area} {street}, needs urgent removal.",
        "Public dustbin at {area} junction is broken and waste is scattered on the road.",
        "Construction debris dumped illegally on {area} {street} is blocking the footpath.",
    ],

    "Water Supply": [
        "No water supply in {area} {street} for the past 2 days.",
        "Water pressure is extremely low in {area}, unable to fill overhead tank.",
        "Contaminated/muddy water is coming from the tap in {area} {street}.",
        "Water tanker has not arrived in {area} despite booking three days ago.",
        "Pipeline leakage near {area} {street} is wasting a large amount of water daily.",
        "Irregular water supply timing in {area}, water comes only for 10 minutes.",
        "No water supply since the pipeline repair work started in {area} {street}.",
        "Water supply valve in {area} is broken, entire street has no water.",
        "Salty/foul smelling water is being supplied in {area} {street}.",
        "New water connection request in {area} is pending for over a month.",
    ],

    "Drainage": [
        "Drainage water is overflowing onto the road in {area} {street}.",
        "Blocked drainage near {area} is causing mosquito breeding and bad odour.",
        "Sewage water has entered houses in {area} {street} after the rain.",
        "Open drain near {area} school is a safety hazard for children.",
        "Drainage cover is missing on {area} {street}, risk of accidents.",
        "Stagnant drainage water in {area} has been standing for over a week.",
        "Choked stormwater drain in {area} {street} floods during light rain.",
        "Foul smell from the drainage line near {area} market is unbearable.",
        "Broken underground drainage pipe in {area} is leaking onto the street.",
        "Drainage cleaning has not been done in {area} {street} for months.",
    ],
        "Street Light": [
        "Street light near {area} {street} has not been working for 10 days.",
        "Entire stretch of {area} {street} is dark at night due to non-functional lights.",
        "Street light pole in {area} is damaged and sparking, safety concern.",
        "Newly installed street light in {area} {street} is not switching on.",
        "Street light near {area} bus stop flickers constantly at night.",
        "No streetlight coverage on {area} {street}, unsafe for women at night.",
        "Street light timer in {area} is faulty; lights stay on during the day.",
        "Broken street light glass in {area} {street} is scattered on the footpath.",
        "Street light near {area} park has been off since last month.",
        "Multiple street lights along {area} {street} are non-functional after the storm.",
    ],

    "Road Damage": [
        "Large pothole on {area} {street} is causing accidents for two-wheelers.",
        "Road near {area} junction has completely eroded after recent rains.",
        "Uneven road surface on {area} {street} makes it difficult for vehicles to pass.",
        "Road repair work in {area} was left incomplete, causing traffic issues.",
        "Broken footpath tiles on {area} {street} are a tripping hazard for pedestrians.",
        "Deep crack across the road in {area} is widening every day.",
        "Speed breaker on {area} {street} is broken and unmarked, risky at night.",
        "Waterlogged potholes on {area} {street} are damaging vehicle tyres.",
        "Newly laid road in {area} is already cracking within a few months.",
        "Missing manhole cover on {area} {street} is extremely dangerous for commuters.",
    ],

    "Electricity": [
        "Frequent power cuts in {area} {street} for the past week without prior notice.",
        "Electric pole near {area} is leaning dangerously and needs urgent repair.",
        "Transformer near {area} {street} is making loud noise and sparking.",
        "Low voltage supply in {area} is damaging household appliances.",
        "Exposed electrical wires near {area} {street} are a serious safety hazard.",
        "Power has not been restored in {area} since yesterday's outage.",
        "Street junction box in {area} is open with live wires exposed.",
        "Electricity meter in {area} {street} is malfunctioning, incorrect readings.",
        "Overhead electric line is sagging dangerously low on {area} {street}.",
        "Repeated tripping of power supply in {area} disrupts daily work.",
    ],
}

PRIORITIES = ["Low", "Medium", "High"]
STATUSES = ["Pending", "In Progress", "Resolved"]

CATEGORIES = list(TEMPLATES.keys())
COMPLAINTS_PER_CATEGORY = 110

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 7, 1)


def random_date():
    delta_days = (END_DATE - START_DATE).days
    return START_DATE + timedelta(days=random.randint(0, delta_days))


def generate_rows():
    rows = []
    complaint_id = 1

    for category in CATEGORIES:
        templates = TEMPLATES[category]

        for _ in range(COMPLAINTS_PER_CATEGORY):

            template = random.choice(templates)
            area = random.choice(AREAS)
            street = random.choice(STREET_TYPES)

            text = template.format(
                area=area,
                street=street
            )

            row = {
                "complaint_id": complaint_id,
                "category": category,
                "complaint_text": text,
                "area": area,
                "date_reported": random_date().strftime("%Y-%m-%d"),
                "priority": random.choice(PRIORITIES),
                "status": random.choice(STATUSES),
            }

            rows.append(row)
            complaint_id += 1

    random.shuffle(rows)

    for i, row in enumerate(rows, start=1):
        row["complaint_id"] = i

    return rows
def save_csv(rows, filename="complaints.csv"):
    fieldnames = [
        "complaint_id",
        "category",
        "complaint_text",
        "area",
        "date_reported",
        "priority",
        "status",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    rows = generate_rows()
    save_csv(rows)

    print(f"Generated {len(rows)} complaints -> complaints.csv")

    for cat in CATEGORIES:
        count = sum(1 for r in rows if r["category"] == cat)
        print(f"  {cat}: {count} complaints")