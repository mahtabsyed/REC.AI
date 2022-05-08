# This python file takes 1 job description in docx format and searches against
# multiple resume in the specified folder and scores each resume as percentage match
#
# Usage: python3 jd_to_resumes_score.py jobdesc/jd_spm.docx resumes/

# As of now jd and resume should be in .docx format


import docx2txt
from mvp_utils import extract_text_pdf_pdfminer3
import sys
import glob, os

# Import summarize from gensim
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords# Import the library
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
if len(sys.argv) < 3:
    print("Error : less arguments than expected...exiting...")
    print("Usage: python3 jd_to_resumes_score.py jobdesc/jd_spm.docx resumes/")
    sys.exit(1)

try:
    jd_text = docx2txt.process(sys.argv[1])
    # Summarize the text with ratio 0.1 (10% of the total words.)
    #jd_text_summary = summarize(jd_text, ratio=0.1)
    #print(jd_text_summary)

    # Take the jd_text and loop all resumes to match
    os.chdir(sys.argv[2])
    for file in glob.glob("*.docx"):
        print("--------------------")
        print(f"Processing : {file}")
        resume = docx2txt.process(file)
        resume_text = str(resume)
        # Summarize the text with ratio 0.1 (10% of the total words.)
        #resume_text_summary = summarize(resume_text, ratio=0.2)
        #print(resume_text_summary)

        # Recycle the text variable from summarizing
        # creating A list of text
        text_list = [resume_text, jd_text]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text_list)

        # get the match percentage
        matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
        matchPercentage = round(matchPercentage, 2)
        print("Your resume matches about " + str(matchPercentage) + "% of the job description.")

        # Create a JSON with
        # Job description, Resume name and Score per Resume
        # Call API to update the appropriate db

except:
  print("An exception occurred")
  sys.exit(1)

