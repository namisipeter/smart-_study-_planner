import os

# File name for data persistence
DATA_FILE = "study_log.txt"


def classify_session(duration: int) -> str:
    """Classifies a study session based on duration in minutes.

    Args:
        duration (int): Duration of the session in minutes.

    Returns:
        str: "Short" (< 30 min), "Medium" (30-90 min), or "Long" (> 90 min).
    """
    if duration < 30:
        return "Short"
    elif 30 <= duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session(sessions: list) -> None:
    """Prompts user for session details, validates input, and appends to the master list.

    Args:
        sessions (list): The list containing all logged session dictionaries.
    """
    print("\n--- Add New Study Session ---")
    
    subject = input("Enter Subject (e.g., Computer Science): ").strip()
    while not subject:
        print("Subject cannot be empty. Please enter a valid subject.")
        subject = input("Enter Subject: ").strip()

    topic = input("Enter Topic (e.g., Data Structures): ").strip()
    while not topic:
        print("Topic cannot be empty. Please enter a valid topic.")
        topic = input("Enter Topic: ").strip()

    date_str = input("Enter Date/Day (e.g., 2026-10-15 or Monday): ").strip()
    while not date_str:
        print("Date/Day cannot be empty.")
        date_str = input("Enter Date/Day: ").strip()

    # Input validation loop for duration
    while True:
        try:
            duration = int(input("Enter Duration in minutes: ").strip())
            if duration > 0:
                break
            else:
                print("Duration must be a positive integer greater than zero.")
        except ValueError:
            print("Invalid input! Please enter a valid numerical integer.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date_str,
        "duration": duration
    }
    
    sessions.append(session)
    print(f"✓ Session successfully added for '{subject}'!")


def view_sessions(sessions: list) -> None:
    """Displays all logged study sessions in a formatted tabular layout.

    Args:
        sessions (list): The master list of session dictionaries.
    """
    print("\n--- All Logged Study Sessions ---")
    if not sessions:
        print("No study sessions logged yet.")
        return

    # Table Header
    header = f"{'Date/Day':<15} | {'Subject':<20} | {'Topic':<25} | {'Min':<6} | {'Category':<8}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    # Table Rows
    for s in sessions:
        category = classify_session(s['duration'])
        print(f"{s['date']:<15} | {s['subject']:<20} | {s['topic']:<25} | {s['duration']:<6} | {category:<8}")
    
    print("-" * len(header))


def search_by_subject(sessions: list) -> None:
    """Searches and displays sessions for a specific subject (case-insensitive).

    Args:
        sessions (list): The master list of session dictionaries.
    """
    print("\n--- Search Sessions by Subject ---")
    if not sessions:
        print("No study sessions logged yet.")
        return

    query = input("Enter subject to search for: ").strip().lower()
    matches = [s for s in sessions if s['subject'].lower() == query]

    if not matches:
        print(f"No sessions found matching subject: '{query}'")
        return

    print(f"\nFound {len(matches)} matching session(s):")
    header = f"{'Date/Day':<15} | {'Subject':<20} | {'Topic':<25} | {'Min':<6} | {'Category':<8}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    total_minutes = 0
    for s in matches:
        category = classify_session(s['duration'])
        total_minutes += s['duration']
        print(f"{s['date']:<15} | {s['subject']:<20} | {s['topic']:<25} | {s['duration']:<6} | {category:<8}")

    print("-" * len(header))
    total_hours = total_minutes / 60.0
    print(f"Total time spent on '{query.capitalize()}': {total_minutes} mins ({total_hours:.2f} hrs)")


def study_statistics(sessions: list) -> None:
    """Calculates and outputs analytical metrics for all logged sessions.

    Args:
        sessions (list): The master list of session dictionaries.
    """
    print("\n--- Study Analytics & Statistics ---")
    if not sessions:
        print("No data available to calculate statistics.")
        return

    # 1. Total hours across all sessions
    total_minutes = sum(s['duration'] for s in sessions)
    total_hours = total_minutes / 60.0

    # 2. Breakdown per subject
    subject_totals = {}
    for s in sessions:
        subj = s['subject'].title()
        subject_totals[subj] = subject_totals.get(subj, 0) + s['duration']

    # 3. Subject with minimum total time spent
    min_subject = min(subject_totals, key=subject_totals.get)
    min_subject_hours = subject_totals[min_subject] / 60.0

    # 4. Single session with maximum duration
    max_session = max(sessions, key=lambda x: x['duration'])

    # Display Metrics
    print(f"• Total Time Studied (All Subjects) : {total_hours:.2f} hours ({total_minutes} mins)")
    
    print("\n• Breakdown by Subject:")
    for subj, mins in subject_totals.items():
        print(f"  - {subj:<20}: {mins / 60.0:.2f} hrs ({mins} mins)")

    print(f"\n• Subject with Least Time Spent    : {min_subject} ({min_subject_hours:.2f} hrs)")
    print(f"• Longest Single Study Session      : {max_session['subject']} - {max_session['topic']} "
          f"({max_session['duration']} mins on {max_session['date']})")


def load_sessions(file_path: str = DATA_FILE) -> list:
    """Parses saved session data from a delimiter-separated text file.

    Args:
        file_path (str): Path to the persistence file.

    Returns:
        list: A list of session dictionaries.
    """
    sessions = []
    if not os.path.exists(file_path):
        return sessions

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("||")
                if len(parts) == 4:
                    subject, topic, date_str, duration_str = parts
                    sessions.append({
                        "subject": subject,
                        "topic": topic,
                        "date": date_str,
                        "duration": int(duration_str)
                    })
    except (FileNotFoundError, ValueError) as e:
        print(f"Warning: Could not fully read log file standardly ({e}). Starting fresh/partial data.")

    return sessions


def save_sessions(sessions: list, file_path: str = DATA_FILE) -> None:
    """Saves session dictionaries to a file using '||' delimiter.

    Args:
        sessions (list): The list of session dictionaries.
        file_path (str): Path to the persistence file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for s in sessions:
                record = f"{s['subject']}||{s['topic']}||{s['date']}||{s['duration']}\n"
                f.write(record)
        print(f"✓ Data successfully saved to '{file_path}'.")
    except IOError as e:
        print(f"Error saving data to file: {e}")


def main() -> None:
    """Main execution loop for the CLI interface."""
    sessions = load_sessions()

    while True:
        print("\n==================================")
        print("      SMART STUDY PLANNER         ")
        print("==================================")
        print("1. Add Session")
        print("2. View All Sessions")
        print("3. Search Sessions by Subject")
        print("4. View Statistics")
        print("5. Save & Exit")
        print("==================================")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            add_session(sessions)
        elif choice == '2':
            view_sessions(sessions)
        elif choice == '3':
            search_by_subject(sessions)
        elif choice == '4':
            study_statistics(sessions)
        elif choice == '5':
            save_sessions(sessions)
            print("Thank you for using Smart Study Planner. Happy studying!")
            break
        else:
            print("Invalid selection! Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()