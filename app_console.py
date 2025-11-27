from logic import (
    load_courses, load_prereqs, load_sections,
    get_eligible_courses, check_conflicts, bfs_unlock_path
)


def main():
    print("=== ACADEMIC PLANNER ===\n")
    
    courses = load_courses()
    prereqs = load_prereqs()
    sections = load_sections()
    
    # Get completed courses
    print("Enter your completed courses (comma-separated codes):")
    print("Example: DECSC 31, ITMGT 45")
    completed = [c.strip() for c in input("> ").split(',') if c.strip()]
    
    # Show eligible courses
    print("\n--- ELIGIBLE COURSES ---")
    eligibility = get_eligible_courses(completed, prereqs, courses)
    
    for code, (is_eligible, missing) in eligibility.items():
        status = "OK" if is_eligible else f"NOT OK - Missing: {', '.join(missing)}"
        print(f"{code}: {status}")
    
    # Select sections
    print("\n--- SELECT SECTIONS ---")
    print("Available sections:")
    for i, sec in enumerate(sections):
        print(f"{i}. {sec['Code']} - {sec['Section']} ({sec['Time']})")
    
    print("\nEnter section numbers to add (comma-separated):")
    selected_indices = [int(x.strip()) for x in input("> ").split(',') if x.strip().isdigit()]
    selected_sections = [sections[i] for i in selected_indices if i < len(sections)]
    
    # Check eligibility for selected sections
    print("\n--- ELIGIBILITY RE-CHECK FOR SELECTED SECTIONS ---")
    ineligible = [(sec['Code'], eligibility.get(sec['Code'], (True, []))[1]) 
                  for sec in selected_sections 
                  if not eligibility.get(sec['Code'], (True, []))[0]]
    
    if ineligible:
        for code, missing in ineligible:
            print(f"WARNING: {code} is NOT eligible - Missing: {', '.join(missing)}")
    else:
        print("All selected courses are eligible.")
    
    # Check for conflicts
    print("\n--- CONFLICT CHECK ---")
    conflicts = check_conflicts(selected_sections)
    if conflicts:
        for c1, c2, day in conflicts:
            print(f"CONFLICT: {c1} and {c2} on {day}")
    else:
        print("No conflicts detected.")
    
    # Show course unlocks
    print("\n--- COURSE PATH (BFS) ---")
    print("Enter a course code to see what it unlocks:")
    unlock_input = input("> ").strip()
    
    if unlock_input in prereqs:
        unlocked = bfs_unlock_path(unlock_input, prereqs)
        print(f"{unlock_input} unlocks: {', '.join(unlocked)}" if unlocked 
              else f"{unlock_input} does not unlock any other courses.")
    else:
        print("Course not found.")

if __name__ == "__main__":
    main()
