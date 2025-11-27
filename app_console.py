from logic import (
    load_courses, load_prereqs, load_sections,
    get_eligible_courses, check_conflicts, bfs_unlock_path
)


def main():
    print("=== ACADEMIC PLANNER ===\n")
    
    # Load data
    courses = load_courses()
    prereqs = load_prereqs()
    sections = load_sections()
    
    # Step 1: Get completed courses
    print("Enter your completed courses (comma-separated codes):")
    print("Example: DECSC 31, ITMGT 45")
    completed_input = input("> ")
    completed = [c.strip() for c in completed_input.split(',') if c.strip()]
    
    # Step 2: Check eligibility
    print("\n--- ELIGIBLE COURSES ---")
    eligibility = get_eligible_courses(completed, prereqs, courses)
    
    for code, (is_eligible, missing) in eligibility.items():
        status = "OK" if is_eligible else f"NOT OK - Missing: {', '.join(missing)}"
        print(f"{code}: {status}")
    
    # Step 3: Select sections
    print("\n--- SELECT SECTIONS ---")
    print("Available sections:")
    for i, sec in enumerate(sections):
        print(f"{i}. {sec['Code']} - {sec['Section']} ({sec['Time']})")
    
    print("\nEnter section numbers to add (comma-separated):")
    selected_input = input("> ")
    selected_indices = [int(x.strip()) for x in selected_input.split(',') if x.strip().isdigit()]
    selected_sections = [sections[i] for i in selected_indices if i < len(sections)]
    
    # Step 4a: Re-check eligibility of selected sections
    print("\n--- ELIGIBILITY RE-CHECK FOR SELECTED SECTIONS ---")
    ineligible_selected = []
    for sec in selected_sections:
        code = sec['Code']
        is_eligible, missing = eligibility.get(code, (True, []))
        if not is_eligible:
            ineligible_selected.append((code, missing))
            print(f"WARNING: {code} is NOT eligible - Missing: {', '.join(missing)}")
    if not ineligible_selected:
        print("All selected courses are eligible.")
    
    # Step 4b: Check time conflicts
    print("\n--- CONFLICT CHECK ---")
    conflicts = check_conflicts(selected_sections)
    if conflicts:
        for c1, c2, day in conflicts:
            print(f"CONFLICT: {c1} and {c2} on {day}")
    else:
        print("No conflicts detected.")
    
    # Step 5: BFS unlock path
    print("\n--- COURSE PATH (BFS) ---")
    print("Enter a course code to see what it unlocks:")
    unlock_input = input("> ").strip()
    if unlock_input in prereqs:
        unlocked = bfs_unlock_path(unlock_input, prereqs)
        if unlocked:
            print(f"{unlock_input} unlocks: {', '.join(unlocked)}")
        else:
            print(f"{unlock_input} does not unlock any other courses.")
    else:
        print("Course not found.")


if __name__ == "__main__":
    main()
