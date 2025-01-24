from datetime import datetime, timedelta

# UCT time zones with offsets relative to UTC
TIMEZONES = {
    "UTC": 0,
    "EST": -5,
    "CST": -6,
    "PST": -8,
    "IST": 5.5,
    # Add more timezones if needed
}

# UCT calendar setup
UCT_START_DATE = datetime(2022, 6, 2)  # UCT starts on June 2, 2022
UCT_DAYS_PER_YEAR = 500
UCT_MONTHS = [
    ("Norya", 42), ("Solstara", 42), ("Yrennis", 42), ("Veldra", 42),
    ("Zirath", 42), ("Gorrath", 42), ("Lathorim", 42), ("Meldrith", 42),
    ("Fensira", 42), ("Ardenis", 42), ("Phelora", 42), ("Thandris", 38),
]

# Convert IRL to UCT
def convert_irl_to_uct(timezone, year, month, day, hour, period):
    if timezone not in TIMEZONES:
        raise ValueError("Unsupported timezone.")
    
    # Adjust hour for AM/PM
    if period.lower() == "pm" and hour != 12:
        hour += 12
    elif period.lower() == "am" and hour == 12:
        hour = 0

    # Create datetime object for IRL time
    irl_datetime = datetime(year, month, day, hour)
    irl_utc = irl_datetime - timedelta(hours=TIMEZONES[timezone])

    # Calculate days since UCT start
    days_since_uct_start = (irl_utc - UCT_START_DATE).days
    uct_year = days_since_uct_start // UCT_DAYS_PER_YEAR + 1
    day_of_year = days_since_uct_start % UCT_DAYS_PER_YEAR + 1

    # Find the UCT month and day
    cumulative_days = 0
    for month_name, days_in_month in UCT_MONTHS:
        if day_of_year <= cumulative_days + days_in_month:
            uct_month = month_name
            uct_day = day_of_year - cumulative_days
            break
        cumulative_days += days_in_month

    uct_hour = irl_utc.hour
    return uct_year, uct_month, uct_day, uct_hour

def main():
    print("Welcome to the Universal Civ Time (UCT) Converter!")
    print("This tool helps you convert your real-world (IRL) time into UCT time and vice versa.")
    print("Follow the instructions step by step, and I'll guide you through the process.")
    print("-" * 60)

    # Ask the user what they want to do
    mode = input("Do you want to convert:\n1) Your IRL time to UCT\n2) A UCT time to IRL\nEnter 1 or 2: ").strip()

    if mode == "1":
        print("\nGreat! Let's convert your IRL time to UCT.")
        print("I'll need a few details about your time. Don't worry, it's simple!")
        
        # Gather IRL time inputs
        try:
            timezone = input(f"\nFirst, what is your timezone? (Supported: {', '.join(TIMEZONES.keys())}): ").strip()
            year = int(input("Enter the current year (e.g., 2025): ").strip())
            month = int(input("Enter the current month (1-12): ").strip())
            day = int(input("Enter the current day of the month (1-31): ").strip())
            hour = int(input("Enter the current hour (1-12): ").strip())
            period = input("Is it AM or PM? (type 'AM' or 'PM'): ").strip()

            # Perform the conversion
            uct_year, uct_month, uct_day, uct_hour = convert_irl_to_uct(timezone, year, month, day, hour, period)

            # Display the result
            print("\nYour IRL time has been successfully converted to UCT!")
            print(f"UCT Time: Year {uct_year}, Month {uct_month}, Day {uct_day}, Hour {uct_hour}:00 UCT")
            print("Thanks for using the UCT Converter!")
        except Exception as e:
            print(f"Oops! Something went wrong: {e}")

    elif mode == "2":
        print("\nOkay, let's convert a UCT time to IRL time.")
        print("You'll need to tell me the UCT year, month (if you know it), and time.")

        # Gather UCT time inputs
        try:
            uct_year = int(input("\nEnter the UCT year: ").strip())
            know_month = input("Do you know the UCT month? (yes/no): ").strip().lower()

            if know_month == "yes":
                uct_month = input("Enter the UCT month (e.g., Norya, Solstara): ").strip()
                uct_day = int(input(f"Enter the day of the month in {uct_month}: ").strip())
            else:
                uct_month = None
                uct_day = int(input("Enter the day of the UCT year (1-500): ").strip())

            uct_hour = int(input("Enter the hour (0-23): ").strip())

            # Calculate IRL time for all timezones
            irl_times = convert_uct_to_irl(uct_year, uct_month, uct_day, uct_hour)

            # Display the result
            print("\nYour UCT time has been successfully converted to IRL time!")
            print("Here are the IRL times in all supported timezones:")
            for tz, time in irl_times.items():
                print(f"{tz}: {time}")
            print("Thanks for using the UCT Converter!")
        except Exception as e:
            print(f"Oops! Something went wrong: {e}")

    else:
        print("Invalid choice. Please restart the program and enter 1 or 2.")

if __name__ == "__main__":
    main()
