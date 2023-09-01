# import libraries

def j(q_test, pwf_test, pr, pb, ef=1, ef2=None):
    if ef == 1:
        if pwf_test >= pb:
            J = q_test / (pr - pwf_test)
        else:
            J = q_test / ((pr - pb) + (pb / 1.8) *
                          (1 - 0.2 * (pwf_test / pb) - 0.8 * (pwf_test / pb)**2))
    elif ef != 1 and ef2 is None:
        if pwf_test >= pb:
            J = q_test / (pr - pwf_test)
        else:
            J = q_test / ((pr - pb) + (pb / 1.8) *
                          (1.8 * (1 - pwf_test / pb) - 0.8 * ef * (1 - pwf_test / pb)**2))
    elif ef !=1 and ef2 is not None:
        if pwf_test >= pb:
            J = ((q_test / (pr - pwf_test)) / ef) * ef2
        else:
            J = ((q_test / ((pr - pb) + (pb / 1.8) *
                            (1.8 * (1 - pwf_test / pb) - 0.8 *
                             ef * (1 - pwf_test / pb)**2))) / ef) * ef2
    return J