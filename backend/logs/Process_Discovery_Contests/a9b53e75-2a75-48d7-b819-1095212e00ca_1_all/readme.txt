This folder contains the data set as was used for the Process
Discovery Contest of 2021 (PDC 2021). The data set contains 480
training logs, 96 corresponding test logs, 96 corresponding
ground truth logs, and 96 models. The logs are all stored using the
IEEE XES file format (see either https://www.xes-standard.org/ or
https://ieeexplore.ieee.org/document/7740858), while the models are
workflow nets (a subclass of Petri nets) stored in the PNML file
format (see
https://www.iso.org/obp/ui/#iso:std:iso-iec:15909:-2:ed-1:v1:en).

The data set is generated from a single base model that allows for
the following characteristics A-G to be configured:

A: Dependent tasks, also known as long-term dependencies. Possible
values are 0 for No and 1 for Yes. If Yes then all transitions that
bypass the dependent tasks are disabled.

B: Loops. Possible values are 0 for No, 1 for Simple, and 2
forComplex. If No, then all transitions that start a loop are
disabled. If Simple, then all transitions that are a shortcut
between the loop and the main flow are disabled.

C: OR constructs. Possible values are 0 for No and 1 for Yes. If
No, then all transitions that only take some inputs for an OR-join
and all transitions that generate only some outputs for an OR-split
are disabled.

D: Routing constructs, also known as invisible tasks. Possible
values are 0 for No and 1 for Yes. If Yes, then some transitions
are made invisible.

E: Optional tasks.Possible values are 0 for No and 1 for Yes. If
Yes, then some invisible transitions are added to allow skipping of
some (visible) transitions.

F: Duplicate tasks, also known as recurrent activities. Possible
values are 0 for No and 1 for Yes. If Yes, then some transitions
are relabeled to existing labels.

G: Noise. Possible values are:
   0: no noise,
   1: in every trace with probability 20% either one random event
      is removed (40%), moved (20%), or copied (40%),
   2: in every trace with probability 20% one random event is
      removed,
   3: in every trace with probability 20% one random event is
      moved to a random position, and
   4: in every trace with probability 20% one random event is
      copied to a random position.

The models and logs were generated in the following way from the
base model. For all 96 possible values for A-F, the corresponding
model pdc2021_ABCDEF.pnml is generated from the base model. From
every model pdc2021_ABCDEF.pnml, seven logs are generated:
 (1-5) five training logs pdc2021_ABCDEFG.xes each containing
       1000 traces,
 (6) a test log pdc2021_ABCDEF.xes containing 125 positive traces
     (fit the model perfectly) and 125 negative traces (do not fit
     the model), and
 (7) a ground truth log pdc2021_ABCDEF.xes that results from
     classifying the test log pdc2021_ABCDEF.xes using the model
     pdc2021_ABCDEF.pnml. In each ground truth log, the additional
     boolean “pdc:isPos” attribute denotes whether the trace is
     positive (fits the model, true) or negative (does not fit the
     model, false).

The negative traces in a test log are taken randomly from the non-
fitting traces contained in the other test logs in the data set.
