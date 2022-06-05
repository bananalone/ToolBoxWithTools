from colorama import init, Fore, Back


MOD = 'm'
ADD = '+'
DEL = '-'
UNCHANGED = 'unchanged'

def listOps(former: str, latter: str) -> list:
    if former == latter:
        return []
    
    len_former = len(former)
    len_latter = len(latter)
    # 操作矩阵 op_mat[i][j] 表示该位置的操作
    op_mat = [[UNCHANGED for j in range(len_latter + 1)] for i in range(len_former + 1)]
    # 索引矩阵 ind_mat[i][j] 表示上一个操作的位置(i, j)
    ind_mat = [[[-1, -1] for j in range(len_latter + 1)] for i in range(len_former + 1)]
    # 距离矩阵 dist_mat[i][j] 表示从i到j的最短编辑距离
    dist_mat = [[0 for j in range(len_latter + 1)] for i in range(len_former + 1)]
    for i in range(len_former + 1):
        dist_mat[i][0] = i
        if i > 0:
            op_mat[i][0] = DEL
            ind_mat[i][0] = [i-1,0]
    for j in range(len_latter + 1):
        dist_mat[0][j] = j
        if j > 0:
            op_mat[0][j] = ADD
            ind_mat[0][j] = [0, j-1]
    for i in range(1, len_former + 1):
        for j in range(1, len_latter + 1):
            if former[i-1] == latter[j-1]:
                cost = 0
            else:
                cost = 1
            # DEL
            if dist_mat[i-1][j]+1 <= dist_mat[i][j-1]+1 and dist_mat[i-1][j]+1 <= dist_mat[i-1][j-1]+cost:
                dist_mat[i][j] = dist_mat[i-1][j]+1
                op_mat[i][j] = DEL
                ind_mat[i][j] = [i-1, j]
            # ADD
            elif dist_mat[i][j-1]+1 <= dist_mat[i-1][j]+1 and dist_mat[i][j-1]+1 <= dist_mat[i-1][j-1]+cost:
                dist_mat[i][j] = dist_mat[i][j-1]+1
                op_mat[i][j] = ADD
                ind_mat[i][j] = [i, j-1]
            # MOD or unchanged
            elif dist_mat[i-1][j-1]+cost <= dist_mat[i-1][j]+1 and dist_mat[i-1][j-1]+cost <= dist_mat[i][j-1]+1:
                dist_mat[i][j] = dist_mat[i-1][j-1]+cost
                if cost == 0: # unchanged
                    op_mat[i][j] = UNCHANGED
                else: # MOD
                    op_mat[i][j] = MOD
                ind_mat[i][j] = [i-1, j-1]
    
    # 获得修改former为latter的字符操作，_ops[operation, former_index, argument]
    _ops = []
    i, j = len_former, len_latter
    while i != -1 and j != -1:
        if op_mat[i][j] == ADD:
            _ops.insert(0, [
                ADD,
                i,
                latter[j-1], # 添加的字符
            ])
        elif op_mat[i][j] == DEL:
            _ops.insert(0, [
                DEL,
                i-1,
                1, # 删除字符个数
            ])
        elif op_mat[i][j] == MOD:
            _ops.insert(0, [
                MOD,
                i-1,
                latter[j-1], # 替换字符
            ])
        i, j = ind_mat[i][j]

    # 获得修改former为latter的字符串操作，合并_ops的相邻同类操作
    ops = [_ops[0]]
    for i in range(1, len(_ops)):
        if _ops[i][0] == ops[-1][0]: # 操作一致
            if _ops[i][0] == ADD and _ops[i][1] == ops[-1][1]:
                ops[-1][2] += _ops[i][2]
            elif _ops[i][0] == DEL and _ops[i][1] == ops[-1][1] + ops[-1][2]:
                ops[-1][2] += 1
            elif _ops[i][0] == MOD and _ops[i][1] == ops[-1][1] + 1:
                ops[-1][2] += _ops[i][2]
        else: # 操作不一致
            ops.append(_ops[i])
    return ops

def fmtText(text: str) -> str:
    init()
    return Back.BLACK + Fore.WHITE + text + Fore.RESET + Back.RESET

def fmtTextWithOps(text: str, ops: list) -> str:
    init()
    latter = Back.BLACK
    start = 0 # former index
    for op in ops:
        latter += Fore.WHITE + text[start : op[1]] + Fore.RESET
        if op[0] == ADD:
            latter += Fore.GREEN + op[2] + Fore.RESET
            start = op[1]
        elif op[0] == DEL:
            latter += Fore.RED + text[op[1] : op[1] + op[2]] + Fore.RESET
            start = op[1] + op[2]
        elif op[0] == MOD:
            len_mod = len(op[2])
            latter += Fore.RED + text[op[1] : op[1] + len_mod] + Fore.RESET + Fore.GREEN + op[2] + Fore.RESET
            start = op[1] + len_mod
    latter += Fore.WHITE + text[start:] + Fore.RESET + Back.RESET
    return latter

