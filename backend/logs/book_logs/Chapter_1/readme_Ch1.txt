Process Mining Book: CHAPTER 1
--------------------------------

The files
- running-example.csv
- running-example.xls
- running-example.xes
- running-example.mxml
contain the event log shown in Table 1.1 (and Table 1.2). The xes and mxml files can be loaded into ProM and used to discover the process model shown in Figure 1.5 (e.g., using the alpha algorithm). 

Sometimes (e.g., in Tables 1.2 and 1.3) short names are used:
a = register request, 
b = examine thoroughly, 
c = examine casually, 
d = check ticket, 
e = decide, 
f = reinitiate request, 
g = pay compensation, and 
h = reject request.

The files
- running-example.pnml
- running-example-v52.pnml
- running-example-v52.tpn
contain the process model shown in Figure 1.5. The model can be imported into ProM and used for different types of analysis (e.g., verification and conformance checking).

The files
- running-example-just-two-cases.csv
- running-example-just-two-cases.xls
- running-example-just-two-cases.xes
- running-example-just-two-cases.mxml
contain the event log used to construct the process model in Figure 1.6 (cases 1 and 4).

The files
- running-example-just-two-cases.pnml
- running-example-just-two-cases-v52.pnml
- running-example-just-two-cases-v52.tpn
contain the process model shown in Figure 1.6. The model can be imported into ProM and used for different types of analysis (e.g., verification and conformance checking).


The files
- running-example-non-conforming.csv
- running-example-non-conforming.xls
- running-example-non-conforming.xes
- running-example-non-conforming.mxml
contain the event log shown in Table 1.3. This log is used to illustrate the notion of conformance checking. For example, a conformance check of this event log and running-example.pnml will show that cases 7, 8 and 10 deviate.

Note that the above files are not representative for real-life event logs and models in terms of size and complexity. However, because of their simplicity, they serve as a nice illustration of the basic concepts.


