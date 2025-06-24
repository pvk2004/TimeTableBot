import pandas as pd
import re


def clean_time_slot(slot):
    # Extracts time ranges like "9:00 AM to 10:00 AM" or "9:00 AM - 10:00 AM"
    match = re.findall(r'(\d{1,2}:\d{2}\s*[APMapm\.]*)', slot)
    if len(match) == 2:
        return f"{match[0]} – {match[1]}"
    return slot.strip()


def parse_excel_timetable(file_path):
    """
    Parses an Excel timetable file and returns a dict:
    { 'Monday': [('9:00 AM', 'DBMS'), ...], ... }
    """
    df = pd.read_excel(file_path, header=0)
    df = df.fillna("")  # Replace NaN with empty string
    days = df.iloc[:, 0].astype(str).str.strip()
    # Clean up time slot headers
    time_slots = [clean_time_slot(str(col)) for col in df.columns[1:]]
    timetable = {}
    for idx, day in enumerate(days):
        if not day or day.lower() == "nan":
            continue
        subjects = df.iloc[idx, 1:]
        slot_list = []
        prev_subject = None
        start_time = None
        prev_time = None
        for i, (time, subject) in enumerate(zip(time_slots, subjects)):
            subject_str = str(subject).replace('\n', ' ').strip()
            if not subject_str or subject_str.lower() == "nan":
                continue
            if prev_subject is None:
                # Start new subject block
                prev_subject = subject_str
                start_time = time
            elif subject_str != prev_subject:
                # End previous block, start new
                slot_list.append((start_time, prev_time, prev_subject))
                prev_subject = subject_str
                start_time = time
            prev_time = time
        # Add last subject block
        if prev_subject is not None:
            slot_list.append((start_time, prev_time, prev_subject))
        timetable[day] = slot_list
    return timetable


def parse_pdf_timetable(file_path):
    """
    Placeholder for PDF timetable parsing.
    """
    raise NotImplementedError("PDF parsing not implemented yet.")
