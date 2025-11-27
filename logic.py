import json
import csv
from collections import deque


def load_courses(filepath="data/courses.json"):
    with open(filepath, 'r') as f:
        return json.load(f)

def load_prereqs(filepath="data/prereqs.json"):
    with open(filepath, 'r') as f:
        return json.load(f)

def load_sections(filepath="data/sections.csv"):

    with open(filepath, 'r') as f:
        return list(csv.DictReader(f))

# ALGORITHM 1: BINARY SEARCH 

def binary_search(sorted_list, target):
    low, high = 0, len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == target:
            return True
        elif sorted_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False

# ALGORITHM 2: PREREQUISITE ELIGIBILITY

def check_eligibility(course_code, completed_courses, prereq_graph):
    required = prereq_graph.get(course_code, [])

    completed_sorted = sorted(completed_courses)
    missing = [req for req in required if not binary_search(completed_sorted, req)]
    return len(missing) == 0, missing

def get_eligible_courses(completed_courses, prereq_graph, courses):
    return {code: check_eligibility(code, completed_courses, prereq_graph) 
            for code in courses.keys()}

# ALGORITHM 3: SCHEDULE CONFLICT DETECTION

def parse_time(time_str):
    parts = time_str.strip().split()
    day_part = parts[0]
    time_part = parts[1] if len(parts) > 1 else ""
    
    times = time_part.split('-')
    if len(times) != 2:
        return []
    
    start, end = int(times[0]), int(times[1])

    # Handle day ranges
    if '-' in day_part:
        day_range = day_part.split('-')
        if day_range == ['M', 'TH']:
            days = ['MON', 'TUE', 'WED', 'THU']
        elif day_range == ['T', 'F']:
            days = ['TUE', 'WED', 'THU', 'FRI']
        else:
            days = []
    else:
        # Parse individual days
        day_map = {'M': 'MON', 'T': 'TUE', 'W': 'WED', 'TH': 'THU', 'F': 'FRI', 'SAT': 'SAT'}
        days = []
        i = 0
        while i < len(day_part):
            if day_part[i:i+3] == 'SAT':
                days.append('SAT')
                i += 3
            elif day_part[i:i+2] == 'TH':
                days.append('THU')
                i += 2
            else:
                days.append(day_map.get(day_part[i], day_part[i]))
                i += 1

    return [(day, start, end) for day in days]

def check_conflicts(selected_sections):
    schedule_by_day = {}
    
    for sec in selected_sections:
        for day, start, end in parse_time(sec['Time']):
            if day not in schedule_by_day:
                schedule_by_day[day] = []
            schedule_by_day[day].append({
                'course': sec['Code'],
                'section': sec['Section'],
                'start': start,
                'end': end
            })

    conflicts = []
    for day, slots in schedule_by_day.items():
        slots.sort(key=lambda x: x['start'])
        for i in range(1, len(slots)):
            if slots[i]['start'] < slots[i-1]['end']:
                conflicts.append((slots[i-1]['course'], slots[i]['course'], day))
    
    return conflicts

# ALGORITHM 4: BFS FOR COURSE PATH

def bfs_unlock_path(course_code, prereq_graph):
    # Build reverse graph
    reverse_graph = {}
    for course, prereqs in prereq_graph.items():
        for p in prereqs:
            reverse_graph.setdefault(p, []).append(course)

    unlocked = []
    visited = {course_code}
    queue = deque([course_code])


    while queue:
        current = queue.popleft()
        for next_course in reverse_graph.get(current, []):
            if next_course not in visited:
                visited.add(next_course)
                unlocked.append(next_course)
                queue.append(next_course)

    return unlocked
