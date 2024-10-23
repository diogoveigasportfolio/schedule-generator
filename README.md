# schedule-generator

Use python and an yaml file to generate a weekly school schedule.

There are 2 yaml files, with for the colors that will be used for each class, and there the one used for the schedule.

Use the present yaml files for reference to put your schedule data. Each "class" should have the following properties.

```
- Day: Monday
  Start: "08:30"
  End: "10:30"
  ClassName: ACM
  ClassNumber: (TP2)
  Room: E363
```

To run the script and generate the png file, execute the file as you normally would:

`python table-schedule-maker.py`

If it doesn't work, make sure your python version is `3.13.0rc1`.
