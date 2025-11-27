import json
import csv
from collections import deque

# ============ DATA LOADING ============

def load_courses(filepath="data/courses.json"):
    with open(filepath, 'r') as f:
        return json.load(f)

def load_prereqs(filepath="data/prereqs.json"):
    with open(filepath, 'r') as f:
        return json.load(f)

def load_sections(filepath="data/sections.csv"):
    sections = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sections.append(row)
    return sections

# ============ ALGORITHM 1: BINARY SEARCH ============

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

# ============ ALGORITHM 2: PREREQUISITE ELIGIBILITY ============

def check_eligibility(course_code, completed_courses, prereq_graph):
    required = prereq_graph.get(course_code, [])
    missing = []
    completed_sorted = sorted(completed_courses)
    for req in required:
        if not binary_search(completed_sorted, req):
            missing.append(req)
    is_eligible = len(missing) == 0
    return is_eligible, missing

def get_eligible_courses(completed_courses, prereq_graph, courses):
    eligibility = {}
    for code in courses.keys():
        is_eligible, missing = check_eligibility(code, completed_courses, prereq_graph)
        eligibility[code] = (is_eligible, missing)
    return eligibility

# ============ ALGORITHM 3: SCHEDULE CONFLICT DETECTION ============

def parse_time(time_str):
    parts = time_str.strip().split()
    if len(parts) == 2:
        day_part, time_part = parts
    else:
        day_part = parts[0]
        time_part = parts[1] if len(parts) > 1 else ""
    times = time_part.split('-')
    if len(times) != 2:
        return []
    start = int(times[0])
    end = int(times[1])

    day_map = {
        'M': 'MON', 'T': 'TUE', 'W': 'WED',
        'TH': 'THU', 'F': 'FRI', 'SAT': 'SAT'
    }

    days = []
    if '-' in day_part:
        day_range = day_part.split('-')
        if day_range[0] == 'M' and day_range[1] == 'TH':
            days = ['MON', 'TUE', 'WED', 'THU']
        elif day_range[0] == 'T' and day_range[1] == 'F':
            days = ['TUE', 'WED', 'THU', 'FRI']
    else:
    # Single or multiple (e.g., "TF", "SAT")
        i = 0
    while i < len(day_part):
        # Check for 3-letter days first
        if i + 2 < len(day_part) and day_part[i:i+3] == 'SAT':
            days.append('SAT')
            i += 3
        # Check for 2-letter days
        elif i + 1 < len(day_part) and day_part[i:i+2] == 'TH':
            days.append('THU')
            i += 2
        # Single letter
        else:
            days.append(day_map.get(day_part[i], day_part[i]))
            i += 1

    return [(day, start, end) for day in days]

def check_conflicts(selected_sections):
    schedule_by_day = {}
    for sec in selected_sections:
        time_slots = parse_time(sec['Time'])
        for day, start, end in time_slots:
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
            prev = slots[i-1]
            curr = slots[i]
            if curr['start'] < prev['end']:
                conflicts.append((prev['course'], curr['course'], day))
    return conflicts

# ============ ALGORITHM 4: BFS FOR COURSE PATH ============

def bfs_unlock_path(course_code, prereq_graph):
    reverse_graph = {}
    for course, prereqs in prereq_graph.items():
        for p in prereqs:
            if p not in reverse_graph:
                reverse_graph[p] = []
            reverse_graph[p].append(course)

    unlocked = []
    visited = set()
    queue = deque([course_code])
    visited.add(course_code)

    while queue:
        current = queue.popleft()
        if current in reverse_graph:
            for next_course in reverse_graph[current]:
                if next_course not in visited:
                    visited.add(next_course)
                    unlocked.append(next_course)
                    queue.append(next_course)

    return unlocked
