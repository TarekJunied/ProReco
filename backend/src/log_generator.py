import pm4py


def init_training_logs(no_logs):
    for i in range(no_logs):
        cur_tree = pm4py.generate_process_tree()
        cur_log = pm4py.play_out(cur_tree)
        rel_path = "../logs/training_logs/log_" + str(i) + ".xes"
        pm4py.write_xes(cur_log, rel_path)
        print(f"generated {i}-th log")
