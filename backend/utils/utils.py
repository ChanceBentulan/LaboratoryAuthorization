import logging

logging.basicConfig(level=logging.INFO)

def preprocess_days(days):
    # Define a mapping from single-letter to two-letter abbreviations
    day_mapping = {
        'm': 'mo',
        't': 'tu',
        'w': 'we',
        'th': 'th',  # Handle 'th' as is
        'f': 'fr',
        's': 'sa',
        'u': 'su'
    }
    
    # Convert input to lowercase to handle uppercase letters
    days = days.lower()
    
    # Use list comprehension to create the list of two-letter abbreviations
    two_letter_days = []
    i = 0
    while i < len(days):
        if days[i:i+2] in day_mapping:  # Check for two-letter days first
            two_letter_days.append(day_mapping[days[i:i+2]])
            i += 2
        else:
            if days[i] in day_mapping:  # Handle single-letter days
                two_letter_days.append(day_mapping[days[i]])
            i += 1
    
    # Join the two-letter abbreviations with '|' as the delimiter
    result = '|'.join(two_letter_days)
    
    # Optionally log the intermediate steps
    return result

def are_days_overlapping(days1, days2):
    set1 = set(days1.split('|'))
    set2 = set(days2.split('|'))
    return bool(set1 & set2)
