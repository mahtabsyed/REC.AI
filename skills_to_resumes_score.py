# This python file takes 1 jd skills in docx format and searches against
# multiple resume in the specified folder and scores each resume 10 points for each skill found
#
# Usage: python3 skills_to_resumes_score.py jobdesc/jd_skills.csv resumes/
# As of now jd and resume should be in .docx format
import pandas as pd
import docx2txt
import sys
import glob, os

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
if len(sys.argv) < 3:
    print("Error : less arguments than expected...exiting...")
    print("Usage: python3 skills_to_resumes_score.py jobdesc/jd_skills.csv resumes/")
    sys.exit(1)

try:
    # Skills as words/phrases separated by new line
    #skills = docx2txt.process(sys.argv[1])
    # Keep an eye on this separator, .docx to txt causes double \n\n
    # so we use separator as "\n\n". If word doc format is different this may change
    # we can use a csv instead
    # jd_skills = skills.split(sep="\n\n")
    # print(f"No of skills: {len(jd_skills)} --  Max score: {len(jd_skills)*10}")
    # print(jd_skills)

    # If the jd_skills are in CSV format use this code
    skills = pd.read_csv(sys.argv[1], delimiter=',')
    jd_skills = skills["Skills"].values.tolist()
    print(f"No of skills: {len(jd_skills)} --  Max score: {len(jd_skills) * 10}")
    print(jd_skills)

    # Take the jd_skills and loop all resumes to match and score
    os.chdir(sys.argv[2])
    for file in glob.glob("*.docx"):
        print("--------------------")
        print(f"Processing : {file}")
        resume = docx2txt.process(file)
        resume_text = str(resume)

        skills_found = []
        resume_score = 0
        for skill in jd_skills:
            if resume_text.find(skill) > 0:
                skills_found.append(skill)
                resume_score = resume_score + 10
        print(f"Resume score: {resume_score}")
        print(f"Skills found: {skills_found}")

        # Create a JSON with
        # Resume name, resume_score and skills_found
        # Call API to update the appropriate db

except:
  print("An exception occurred. Please check the arguments and if the folder and files exist...")
  sys.exit(1)
