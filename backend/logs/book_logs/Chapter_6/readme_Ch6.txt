Process Mining Book: CHAPTER 6
--------------------------------

The files L-heur-1.xes and L-heur-1.mxml contain event log L used in Section 6.2.2. This event log contains 40 cases and 139 events and is used to explain the heuristic mining algorithm.

The files L-heur-2.xes and L-heur-2.mxml contain the same event log but now the first sequence <a,e> is more frequent (50 times rather than 5 times).

One can use these event logs to apply the various process discovery algorithms (not just the heuristics miner but also the genetic miner, alpha miner, fuzzy miner, etc.). 

Event log L1 (see files L1.xes and L1.mxml) is used to build the transition systems in figures 6.12, 6.13, 6.14, and 6.15. One can use ProM’s transition miner to reproduce these results. 

The same log (L1.xes/L1.mxml) is used to illustrate state-based regions (see Figure 6.17).

Event log L9 (see files L9.xes and L9.mxml) is used to show that language-based regions can be used to discover the WF-net shown in Figure 6.19. (Use the proper settings to reproduce this using the ILP miner in ProM.) 

Note that again these event logs contain no timestamps, resources, etc.

