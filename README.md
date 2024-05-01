# Punch

CLI work clocking system.

## Getting Started

[How to use]

<br>

## TODO

- Add ability to start and stop (a) break(s) in between punch-in and -out.

  > #### For example:
  >
  > ```
  > PS C:Users\natha> punch in
  > PS C:Users\natha> punch break start
  > PS C:Users\natha> punch break end
  > PS C:Users\natha> punch out
  > ```

- `punch state` should show how much time has elapsed since punch-in.
- Refactor `TimeLog` and `LogEntry` classes.
- `punch state` should show when to clock out to achieve 8 hours.