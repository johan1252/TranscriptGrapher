# Transcript Grapher

Python tool to graph university course grade history by using a singular pdf transcript input.
Can be used for trend analysis based on a user's university course grades.
Prototype only, so far can only be used on Queen's University transcripts (Queen's transcripts have been tested, use others at own risk).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The following python libraries are used by the program:

```
cStringIO
pdfminer
numpy
matplotlib
sys
re
getopt
numpy
```

## How to run

Using command line
```
transcript_grapher.py -i <inputfile,mandatory> -o <outputfile,optional>
Ex: transcript_grapher.py -i SSR_TSRPT_UN.pdf -o test.png
```
Where SSR_TSRPT_UN.pdf is any Queen's University provided transcript.
"-o" allows the output graph to be saved to a file in addition to being shown on screen.

Example Graph Output:
![alt text](https://github.com/johan1252/TranscriptGrapher/blob/master/ExampleOuput.png?raw=true)

## Authors

Johan Cornelissen
