# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
# Productivity Index (darcy law)
def j_darcy(ko, h, bo, uo, re, rw, s, flow_regime="seudocontinuo"):
    if flow_regime == "seudocontinuo":
        J_darcy = ko * h / (141.2 * bo * uo * (np.log(re / rw) - 0.75 + s))
    elif flow_regime == "continuo":
        J_darcy = ko * h / (141.2 * bo * uo * (np.log(re / rw) + s))
    return J_darcy

#%%
# Productivity Index
def j(q_test, pwf_test, pr, pb, ef=1, ef2=None):
    if ef == 1:
        if pwf_test >= pb:
            J = q_test / (pr - pwf_test)
        else:
            J = q_test / (
                (pr - pb)
                + (pb / 1.8) * (1 - 0.2 * (pwf_test / pb) - 0.8 * (pwf_test / pb) ** 2)
            )
    elif ef != 1 and ef2 is None:
        if pwf_test >= pb:
            J = q_test / (pr - pwf_test)
        else:
            J = q_test / (
                (pr - pb)
                + (pb / 1.8)
                * (1.8 * (1 - pwf_test / pb) - 0.8 * ef * (1 - pwf_test / pb) ** 2)
            )
    elif ef != 1 and ef2 is not None:
        if pwf_test >= pb:
            J = ((q_test / (pr - pwf_test)) / ef) * ef2
        else:
            J = (
                (
                    q_test
                    / (
                        (pr - pb)
                        + (pb / 1.8)
                        * (
                            1.8 * (1 - pwf_test / pb)
                            - 0.8 * ef * (1 - pwf_test / pb) ** 2
                        )
                    )
                )
                / ef
            ) * ef2
    return J

#%%
# Q(bpd) @ Pb
def Qb(q_test, pwf_test, pr, pb, ef=1, ef2=None):
    qb = j(q_test, pwf_test, pr, pb, ef, ef2) * (pr - pb)
    return qb

#%%
# AOF(bpd)
def aof(q_test, pwf_test, pr, pb, ef=1, ef2=None):
    if ef == 1 and ef2 is None:
        if pr > pb:  # Yac. subsaturado
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef=1) + (
                    (j(q_test, pwf_test, pr, pb) * pb) / 1.8
                )
        else:  # Yac. Saturado
            AOF = q_test / (1 - 0.2 * (pwf_test / pr) - 0.8 * (pwf_test / pr) ** 2)

    elif ef < 1 and ef2 is None:
        if pr > pb:
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb, ef) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef) + (
                    (j(q_test, pwf_test, pr, pb, ef) * pb) / 1.8
                ) * (1.8 - 0.8 * ef)
        else:
            AOF = (
                q_test
                / (
                    1.8 * ef * (1 - pwf_test / pr)
                    - 0.8 * ef**2 * (1 - pwf_test / pr) ** 2
                )
            ) * (1.8 * ef - 0.8 * ef**2)

    elif ef > 1 and ef2 is None:
        if pr > pb:
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb, ef) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef) + (
                    (j(q_test, pwf_test, pr, pb, ef) * pb) / 1.8
                ) * (0.624 + 0.376 * ef)
        else:
            AOF = (
                q_test
                / (
                    1.8 * ef * (1 - pwf_test / pr)
                    - 0.8 * ef**2 * (1 - pwf_test / pr) ** 2
                )
            ) * (0.624 + 0.376 * ef)

    elif ef < 1 and ef2 >= 1:
        if pr > pb:
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb, ef, ef2) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef, ef2) + (
                    j(q_test, pwf_test, pr, pb, ef, ef2) * pb / 1.8
                ) * (0.624 + 0.376 * ef2)
        else:
            AOF = (
                q_test
                / (
                    1.8 * ef * (1 - pwf_test / pr)
                    - 0.8 * ef**2 * (1 - pwf_test / pr) ** 2
                )
            ) * (0.624 + 0.376 * ef2)

    elif ef > 1 and ef2 <= 1:
        if pr > pb:
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb, ef, ef2) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef, ef2) + (
                    j(q_test, pwf_test, pr, pb, ef, ef2) * pb / 1.8
                ) * (1.8 - 0.8 * ef2)
        else:
            AOF = (
                q_test
                / (
                    1.8 * ef * (1 - pwf_test / pr)
                    - 0.8 * ef**2 * (1 - pwf_test / pr) ** 2
                )
            ) * (1.8 * ef - 0.8 * ef2**2)
    return AOF

#%%
# Qo (bpd) @ Darcy Conditions
def qo_darcy(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None):
    qo = j(q_test, pwf_test, pr, pb) * (pr - pwf)
    return qo

#%%
# Qo(bpd) @ vogel conditions
def qo_vogel(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None):
    qo = aof(q_test, pwf_test, pr, pb) * (1 - 0.2 * (pwf / pr) - 0.8 * (pwf / pr) ** 2)
    return qo

#%%
# Qo(bpd) @ vogel conditions
def qo_ipr_compuesto(q_test, pwf_test, pr, pwf, pb):
    if pr > pb:  # Yac. subsaturado
        if pwf >= pb:
            qo = qo_darcy(q_test, pwf_test, pr, pwf, pb)
        elif pwf < pb:
            qo = Qb(q_test, pwf_test, pr, pb) + (
                (j(q_test, pwf_test, pr, pb) * pb) / 1.8
            ) * (1 - 0.2 * (pwf / pb) - 0.8 * (pwf / pb) ** 2)

    elif pr <= pb:  # Yac. Saturado
        qo = aof(q_test, pwf_test, pr, pb) * (
            1 - 0.2 * (pwf / pr) - 0.8 * (pwf / pr) ** 2
        )
    return qo

#%%
# Qo(bpd) @Standing Conditions
def qo_standing(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None):
    qo = aof(q_test, pwf_test, pr, pb, ef=1) * (
        1.8 * ef * (1 - pwf / pr) - 0.8 * ef**2 * (1 - pwf / pr) ** 2
    )
    return qo

#%%
# Qo(bpd) @ all conditions
def qo(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None):
    if ef == 1 and ef2 is None:
        if pr > pb:  # Yac. subsaturado
            if pwf >= pb:
                qo = qo_darcy(q_test, pwf_test, pr, pwf, pb)
            elif pwf < pb:
                qo = Qb(q_test, pwf_test, pr, pb) + (
                    (j(q_test, pwf_test, pr, pb) * pb) / 1.8
                ) * (1 - 0.2 * (pwf / pb) - 0.8 * (pwf / pb) ** 2)
        else:  # Yac. Saturado
            qo = qo_vogel(q_test, pwf_test, pr, pwf, pb)

    elif ef != 1 and ef2 is None:
        if pr > pb:  # Yac. subsaturado
            if pwf >= pb:
                qo = qo_darcy(q_test, pwf_test, pr, pwf, pb, ef, ef2)
            elif pwf < pb:
                qo = Qb(q_test, pwf_test, pr, pb, ef) + (
                    (j(q_test, pwf_test, pr, pb, ef) * pb) / 1.8
                ) * (1.8 * (1 - pwf / pb) - 0.8 * ef * (1 - pwf / pb) ** 2)
        else:  # Yac.saturado
            qo = qo_standing(q_test, pwf_test, pr, pwf, pb, ef)

    elif ef != 1 and ef2 is not None:
        if pr > pb:  # Yac. subsaturado
            if pwf >= pb:
                qo = qo_darcy(q_test, pwf_test, pr, pwf, pb, ef, ef2)
            elif pwf < pb:
                qo = Qb(q_test, pwf_test, pr, pb, ef, ef2) + (
                    (j(q_test, pwf_test, pr, pb, ef, ef2) * pb) / 1.8
                ) * (1.8 * (1 - pwf / pb) - 0.8 * ef * (1 - pwf / pb) ** 2)
            else:  # Yac. saturado
                qo = qo_standing(q_test, pwf_test, pr, pwf, pb, ef, ef2)
    return qo
