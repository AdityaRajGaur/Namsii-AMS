import nltk
import re

# Initialize the NLTK library
nltk.download('punkt')
def extract_ticket_details(message):
    print('in extract details')
    # Extract ticket details using regular expressions
    summary_pattern = r"summary ['\"]([^'\"]+)['\"]"  # Pattern to match the summary
    description_pattern = r"description ['\"]([^'\"]+)['\"]"  # Pattern to match the description
    project_pattern = r"project ['\"]([^'\"]+)['\"]"  # Pattern to match the project

    summary_matches = re.findall(summary_pattern, message)
    description_matches = re.findall(description_pattern, message)
    project_matches = re.findall(project_pattern, message)

    # Extracted ticket details
    summary = summary_matches[0] if summary_matches else None
    description = description_matches[0] if description_matches else None
    project = project_matches[0] if project_matches else None

    # Print the extracted ticket details
    print("Summary:", summary)
    print("Description:", description)
    print("Project:", project)



    return [project,summary,description]