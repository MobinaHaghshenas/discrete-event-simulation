# Simulation Results

This folder contains the main results of the discrete-event simulation and resource analysis for the repair system.

The simulation evaluates machine failures, lost machine time, repairman utilization, repair-system congestion, transition time, and the effect of changing the number of repairmen and spare machines.

## System Performance

The simulation was conducted over a **40-hour period**. The main reported performance measures include machine failures, lost time caused by the lack of spare machines, repairman utilization, transition time, and maximum queue length.

### Number of Failures

The simulation produced an estimated average of **708.5 machine failures**.

The reported interval estimate is:

```text
Point estimate: 708.50
Interval estimate: [706.31, 710.69]
```

### Total Lost Time

Total lost time represents the time associated with machine unavailability when a failed machine cannot immediately be replaced by a spare machine.

The reported point estimate is:
```text
Point estimate: 550.84 hours
Interval estimate: [542.12, 559.57] hours
```

### Total Transition Time

The total transition time associated with moving machines through the repair process was estimated as:
```text
Point estimate: 290.99 hours
Interval estimate: [290.07, 291.91] hours```

### Maximum Queue Length

The maximum queue length at the repair station was estimated as:
```text
Point estimate: 27.50 machines
Interval estimate: [26.10, 28.90] machines```

## Repairman Performance
### Repairman Employment

The average employment percentage of the repairmen was estimated as:
```text
Point estimate: 94.42%
Interval estimate: [94.24%, 94.60%]```

The individual repairman results reported in the study show employment percentages generally around the mid-90% range.

### Resource and Cost Analysis

The simulation was also used to investigate the effect of changing the number of repairmen and spare machines.

The cost analysis considers the opportunity cost of machine unavailability together with repairman cost. The report states that the opportunity cost of a lost milling machine is 10 times the repairman's wage cost.

### Resource Scenarios

The report evaluates several resource ranges.

For a maximum of **10 repairmen and 10 spare machines**, the reported minimum-cost configuration was:
```text
Repairmen: 10
Spare machines: 10
Total cost: 650,290```

For a maximum of **20 repairmen and 20 spare machines**, the reported minimum-cost configuration was:
```text
Repairmen: 18
Spare machines: 20
Total cost: 139,850```

For a maximum of **50 repairmen and 50 spare machines**, the reported minimum-cost configuration was:
```text
Repairmen: 19
Spare machines: 50
Total cost: 58,870```

The report also shows that, at higher resource limits, the optimal number of repairmen changes relatively little while the number of spare machines increases. This reflects the higher cost associated with machine shortages compared with the additional repairman cost.


## Key Results

|Performance Measure	|Point Estimate	|Interval Estimate|
Number of failures	708.50	[706.31, 710.69]
Total lost time (hours)	550.84	[542.12, 559.57]
Total transition time (hours)	290.99	[290.07, 291.91]
Maximum queue length	27.50	[26.10, 28.90]
Repairman employment	94.42%	[94.24%, 94.60%]
Resource Optimization Summary
Maximum Resource Range	Repairmen	Spare Machines	Reported Minimum Cost
10	10	10	650,290
20	18	20	139,850
50	19	50	58,870

These results illustrate how discrete-event simulation can be used to evaluate operational performance and compare alternative resource-allocation policies before making changes to the repair system.
