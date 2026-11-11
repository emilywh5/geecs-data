import pandas as pd
import re
from pathlib import Path

def extract_event_date(filename):
    semester_match = re.search(r"\b([FW])(\d{2})\b", filename)
    date_match = re.search(r"\((\d{2})_(\d{2})\)", filename)
    if not semester_match or not date_match:
        return pd.NaT

    semester, year = semester_match.groups()
    month, day = date_match.groups()
    year = 2000 + int(year)

def calculate_attendance(folder):

    attendance_data = []

    for file in folder.glob("*csv"):
        df = pd.read_csv(file)

        event_name = file.stem
        attendance = len(df)
        event_date = extract_event_date(file.stem)

        attendance_data.append({
            "event_date": event_date,
            "event_name": event_name,
            "attendance": attendance
        })

    attendance_df = pd.DataFrame(attendance_data)
    attendance_df["event_date"] = pd.to_datetime(attendance_df["event_date"])

    attendance_df = attendance_df.sort_values("event_data")

    return attendance_df

folder_name = Path(r"C:\Users\ecw31\Desktop\GEECS_F26_Data")

dfs = []

for file in folder_name.glob("*.csv"):
    df = pd.read_csv(file)

    df["source_file"] = file.stem

    dfs.append(df)

all_events = pd.concat(dfs, ignore_index=True)

output_folder = folder_name / "processed"
output_folder.mkdir(exist_ok=True)

all_events.to_csv(
    output_folder / "attendance_over_time.csv",
    index=False
)

print("Attendance data exported successfully!")