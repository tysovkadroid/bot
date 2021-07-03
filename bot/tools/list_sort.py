def list_sort(dsr_lst, exe_lst):
    exe_lst_indices = [i[0] for i in sorted(
        enumerate(exe_lst), key=lambda x:x[1])]
    exe_lst_indices_indices = [i[0] for i in sorted(
        enumerate(exe_lst_indices), key=lambda x:x[1])]
    sorted_lst = [x for _, x in sorted(
        zip(exe_lst_indices_indices, dsr_lst))]
    return sorted_lst
