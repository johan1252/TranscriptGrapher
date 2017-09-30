#!/usr/bin/env python

##################################################
# Transcript Grapher
#
# Takes PDF formatted transcript and create output graph/
# Currently only tested with Queen's University Transcripts.
# 
# Concept proposal only so far.
# By Johan Cornelissen
#
##################################################

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import sys, re, getopt
import numpy as np
from matplotlib import pyplot as plt

numericalGrades = {
    "A+" : 100,
    "A"  : 89,
    "A-" : 84,
    "B+" : 79,
    "B"  : 76,
    "B-" : 72,
    "C+" : 69,
    "C"  : 66,
    "C-" : 62,
    "D+" : 59,
    "D"  : 56,
    "D-" : 52
}
    
def main():
    
    inputFile = ''
    outputFile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'transcript_grapher.py -i <inputfile,mandatory> -o <outputfile,optional>'
        print "Ex: transcript_grapher.py -i SSR_TSRPT_UN.pdf -o test.png"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'transcript_grapher.py -i <inputfile,mandatory> -o <outputfile,optional>'
            print "Ex: transcript_grapher.py -i SSR_TSRPT_UN.pdf -o test.png"
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg
    
    if inputFile == "":
        print "Please provide input file."
        print 'transcript_grapher.py -i <inputfile,mandatory> -o <outputfile,optional>'
        print "Ex: transcript_grapher.py -i SSR_TSRPT_UN.pdf -o test.png"
        sys.exit()        
    
    pdfText = convert(inputFile)
    printSection = False
    i = 1
    courses = []
    grades = []
    pattern = re.compile("^[A-D]?[\s(NG)+-]*$")
    namePattern = re.compile("Name:\s*(\w*,\w*)")
    for line in pdfText.splitlines():
        if "Name:" in line:
            transcriptName = namePattern.match(line).group(1)
        if printSection:
            if line == "":
                printSection = False
            else:    
                courses.append(line)    
        if line.find("Description") != -1:
            printSection = True
        gradeReg = pattern.match(line)
        if gradeReg:   
            if gradeReg.group() and gradeReg.group() != " ":
                grades.append(line)
    i = 0        
    for grade in grades:
        if grade == "TBD" or grade == "NG":
            del courses[i]
            del grades[i]
                        
    numGrades = len(grades)  
    newCourseList = []     
    for i in range(0,len(courses)):
        if i < numGrades: 
            newCourseList.append(courses[i])
        else:
            continue
            #print "TBD"  
              
    grades = convertGrades(grades)        
    graph(newCourseList,grades,outputFile,transcriptName)               

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    
    return text 

def convertGrades(grades): 
    percentageGrades = [] 
    for grade in grades:
        percentageGrades.append(numericalGrades[grade])                                 
    return percentageGrades


def graph(courses,grades,outputFile,transcriptName):
    courses = [elem[:6] for elem in courses]  
    plt.title("Grade Distribution : " + transcriptName)
    plt.xticks(range(0,len(courses)), courses, rotation=45, size='small', ha='right')
    plt.plot(np.arange(len(courses)), grades)
    if outputFile != "":
        plt.savefig(outputFile)
    plt.show()    
    
if __name__ == "__main__":
    sys.exit(main())