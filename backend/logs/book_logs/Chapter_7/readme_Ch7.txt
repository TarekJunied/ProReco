Process Mining Book: CHAPTER 7
--------------------------------


The files Lfull.xes and Lfull.mxml contain the event log described in Table 7.1. The log contains 1391 cases following 21 different traces (7539 events in total).

The following mapping is used:
a = register request, 
b = examine thoroughly, 
c = examine casually, 
d = check ticket, 
e = decide, 
f = reinitiate request, 
g = pay compensation, and 
h = reject request.


The four WF-nets shown in Figure 7.2 are included in the files N1.pnml, N2.pnml, N3.pnml, and N4.pnml (tpn files for ProM 5.2 are also included). 

One can use the conformance checking in ProM 5.2 to compute the fitness values given in Chapter 7 (use tpn files and mxml logs). Note that the conformance checker also provides other conformance-related metrics (not just fitness).

One can also use a range of conformance checking plug-ins in ProM 6. Use for example the "Replay log on Petri net" plug-in in ProM 6. This plug-in is using a cost-based approach with penalties for the various discrepancies between event log and model.
