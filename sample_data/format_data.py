import json
import random
import decimal

year_list = ["Freshman", "Sophomore", "Junior", "Senior"]

skills_list = []
bios_list = []
major_list =[]

with open("linkedin_skills.txt") as f1:
    skills_list = [line.rstrip() for line in f1]

with open("majors_list.txt") as f2:
    major_list = [line.rstrip() for line in f2]

#research_interests = [line.rstrip('\n') for line in open("Research_Interests.txt")]
#technical_skills = [line.rstrip('\n') for line in open("Technical_Skills.txt")]

with open("bios.txt") as f3:
    lines_file = f3.readlines()
    current_bio = ""
    for i in range(len(lines_file)):
        if(i == len(lines_file) - 1):
            current_bio = current_bio + lines_file[i]
            bios_list.append(current_bio)
        elif(len(lines_file[i + 1]) == 1):
            current_bio = current_bio + lines_file[i]
            current_bio = current_bio[1:]
            current_bio = current_bio[:-1]
            bios_list.append(current_bio)
            current_bio = ""
        else:
            current_bio = current_bio + lines_file[i]
del bios_list[0]



research_interests = [line.rstrip('\n') for line in open("research_interests.txt")]
technical_skills = [line.rstrip('\n') for line in open("technical_skills.txt")]
year = ["Freshman", "Sophomore", "Junior", "Senior"]
majors_list = [line.rstrip('\n') for line in open("majors_list.txt")]
current_profile = {
    "Year": random.choice(year),
    "Major": random.choice(majors_list),
    "GPA": float(decimal.Decimal(random.randrange(230, 400))/100),
    "About Me": random.choice(bios_list),
    "Research Interests": random.choice(research_interests),
    "Technical Skills": random.choice(technical_skills),
}
#print(type(json.dumps(current_profile)))
list_of_profiles = []

json_list = []
for i in range(100):
    current_profile = {
        "Year": random.choice(year),
        "Major": random.choice(majors_list),
        "GPA": float(decimal.Decimal(random.randrange(230, 400))/100),
        "About Me": random.choice(bios_list),
        "Research Interests": random.choice(research_interests),
        "Technical Skills": random.choice(technical_skills),
    }
    list_of_profiles.append(current_profile)

final_json = json.dumps(list_of_profiles, indent=4)
with open("sample_formatted_data.json", "r+") as j:
    j.write(final_json)
