Process Mining Book: CHAPTER 5
--------------------------------


The twelve logs named L1-L12 used in Chapter 5 are included. Per event log there are three files:
- a .txt file describing the event log
- a .xes file that can be loaded into ProM 6
- a .mxml file that can be loaded into ProM 6 and earlier versions of ProM (e.g., ProM 5.2)

A short description of these events logs:

- L1 is the log used to discover the WF-net N1 in Figure 5.1.

- L2 is the log used to discover the WF-net N2 in Figure 5.2.

- L3 is the log used to discover the WF-net N3 in Figure 5.5.

- L4 is the log used to discover the WF-net N4 in Figure 5.6.

- L5 is the log used to discover the WF-net N5 in Figure 5.8.

- L6 is the log used to discover the WF-net N6 in Figure 5.9.

- L7 is the log used to discover the incorrect WF-net N7 in Figure 5.10. The correct WF-net is shown in Figure 5.11.

- L8 is the log used to discover the WF-net N8 in Figure 5.12. The correct WF-net is shown in Figure 5.13.

- L9 is a log used to illustrate the limitations of the alpha algorithm (see Figure 5.14).

- L10 is a log used to illustrate the limitations of the alpha algorithm (see Figure 5.20).

- L11 is a log used to illustrate the limitations of the alpha algorithm (see Figure 5.21).

- L12 is a log used to illustrate the dilemma related to infrequent sequences (relates to the choice between N4 and N9).


Note that the log files do not contain meaningful information related to time, resources, etc. They are intended to illustrate the alpha algorithm (and its limitations).

Also several Petri net models have been included N1-N11 (see .pmnl files). In some cases both the correct and incorrect model are included.

The files bigger-example.xes and bigger-example.mxml contain the larger event log shown in Figure 5.24. This event log contains information about 1391 cases. The model discovered by the alpha algorithm is stored in N-bigger-example.pmnl. This corresponds to WF-net N1 in Figure 5.24.

Note that event log bigger-example.xes is also used in Chapter 7.



