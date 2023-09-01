SM (StructuredMiner) version 1.1 - January 2017

Copyright © 2016 - Adriano Augusto, Raffaele Conforti, Marcello La Rosa, Marlon Dumas.

OVERVIEW:

SM is a standalone tool for mining BPMN maximally structured process models in two phase.
The first phase discovers the BPMN process model from an input log using Heuristic Miner or Fodina Miner (choice up to the user). 
The second phase structures the discovered model combining BPStruct and Extended Oulsnam Structurer (both used with default settings).

SM takes as input a log as "mxml" or "xes" file. The BPMN maximally structured process model is dumped as a "bpmn" file, 
that can be opened and visualized using Apromore (http://apromore.qut.edu.au/).

Questions and comments may be addressed to Adriano Augusto (a.augusto [at] qut.edu.au) or 
Raffaele Conforti (raffaele.conforti [at] qut.edu.au).

CONTENTS OF THIS DISTRIBUTION

This distribution contains the following files and folders:
* StructuredMiner.jar - Java console application (see usage below) 
* LICENSE.txt - licensing terms for SM
* logs/ - sample artificial logs
* outputs/ - outputs of the sample logs

USAGE:

COMMAND: java -jar StructuredMiner.jar [hm|fo] [p] [f] [minutes] logFileName.[mxml|xes] bpmnFileName

PARAM1 (mandatory) - mining algorithn: hm|fo
        - HM stands for Heuristics Miner ProM 6.5
        - FO stands for Fodina Micdner

PARAM2 (optional) - pull-up rule flag: p
        - when present enable the pull-up rule and the output model may not be weakly bisimilar

PARAM3 (optional) - force structuring flag: f
        - when present it forces the structuring, meaning the structured model may lose or gain behaviour

PARAM4 (optional) - minutes for time-out of the TBA*: integer > 0
        - if not set, the time-out is by default 2 minutes

PARAM5 (mandatory) - input log file name: logFileName.[mxml|xes]
        - accepted log files are in .mxml or .xes format

PARAM6 (mandatory) - output model file name: bpmnFileName
        - this will be the name of the output .bpmn file containing the structured model

EXAMPLES:	
	java -jar StructuredMiner.jar hm .\logs\artificial1.mxml .\outputs\artificial1
	java -jar StructuredMiner.jar hm p 10 .\logs\artificial2.mxml .\outputs\artificial2
	java -jar StructuredMiner.jar fo p f 5 .\logs\artificial3.mxml .\outputs\artificial3


LICENSING:

The SM tool is distributed under the terms of the Lesser GNU General Public License (LGPL) version 3. 
The text of the LGPL license is available at http://www.gnu.org/licenses/lgpl.txt
The LGPL license is an extension of the GPL license available : http://www.gnu.org/licenses/gpl.html

A copy of the license is included in file LICENSE.txt
