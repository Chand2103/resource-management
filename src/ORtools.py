from ortools.sat.python import cp_model
def check_availabiliy(starts,ends,p_start,p_end):
    model = cp_model.CpModel()
    starting_times = starts
    ending_times = ends
    prefered_start = p_start
    prefered_end = p_end
    x = [model.NewIntVar(0, 22, f'x{i}') for i in range(len(starting_times))]
    y = [model.NewIntVar(0, 22, f'y{i}') for i in range(len(ending_times))]

    # Fix x[i] and y[i] to the given start/end times
    for i in range(len(starting_times)):
        model.Add(x[i] == starting_times[i])
        model.Add(y[i] == ending_times[i])

    p1 = model.NewIntVar(0,22,'p1')
    p2 = model.NewIntVar(0,22,'p2')

    model.add(p1 == prefered_start)
    model.add(p2 == prefered_end)

    size = len(starting_times) 

    for i in range(len(starting_times)):
        # Create a Boolean variable: is this task before preferred_start?
        before_pref = model.NewBoolVar(f'before_pref_{i}')

        # If before_pref is true → y[i] <= p1
        model.Add(y[i] <= p1).OnlyEnforceIf(before_pref)
        # Else → x[i] >= p2
        model.Add(x[i] >= p2).OnlyEnforceIf(before_pref.Not())

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        print("Solution exists")
        for i in range(len(starting_times)):
            print(f"Task {i+1}: starts at {solver.Value(x[i])}, ends at {solver.Value(y[i])}")

        print(solver.Value(p1),solver.Value(p2))
        return True    
    else:
        print("No solution")
        return False






