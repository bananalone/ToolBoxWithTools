from enum import Enum, auto
from typing import Any, List, Union

from colorama import Fore, Back, init


class DiffType(Enum):
    ADD = auto()
    DEL = auto()
    
class Color:
    FORE_REd = Fore.RED
    FORE_GREEN = Fore.GREEN
    FORE_BLUE = Fore.BLUE
    FORE_BLACK = Fore.BLACK
    FORE_WHITE = Fore.WHITE
    BACK_RED = Back.RED
    BACK_GREEN = Back.GREEN
    BACK_BLUE = Back.BLUE
    BACK_BLACK = Back.BLACK
    BACK_WHITE = Back.WHITE

class DiffFinder:
    _DIFF_TYPE = 'Type'
    _DIFF_POS = 'Position'
    _DIFF_ARGS = 'Args'
    
    def __init__(self) -> None:
        self._former = None
        self._latter = None
        # status
        self._dist_mat = None # 距离矩阵 dist_mat[i][j] 表示从i到j的最短编辑距离 操作包括增减(ADD)和删除(DEL)
        self._diff_mat = None # 差异矩阵 diff_mat[i][j] 表示该位置的操作
        self._parent_mat = None  # 索引矩阵 parent_mat[i][j] 表示上一个操作的位置(i, j)
        self._diffs = None # 差异列表 保存每处差异
        init()
        
    def analyse(self, former: str, latter: str):
        self._former = former
        self._latter = latter
        if self._same():
            return
        self._analyse_mat()
        self._analyse_diffs()
        
    def getDistance(self) -> int:
        if self._same():
            return 0
        return self._dist_mat[len(self._dist_mat)-1][len(self._diff_mat[0])-1]
    
    def listDiffs(self) -> Union[List, None]:
        if self._same():
            return None
        return self._diffs
    
    def format(self, unchanged_color=Color.FORE_WHITE, add_color=Color.FORE_GREEN, del_color=Color.FORE_REd, background_color=Color.BACK_BLACK) -> str:
        if self._same():
            return background_color + unchanged_color + self._former + Fore.RESET + Back.RESET
        text = background_color
        start = 0 # former index
        for diff in self._diffs:
            text += unchanged_color + self._former[start: diff[DiffFinder._DIFF_POS]] + Fore.RESET
            if diff[DiffFinder._DIFF_TYPE] == DiffType.ADD:
                text += add_color + diff[DiffFinder._DIFF_ARGS] + Fore.RESET
                start = diff[DiffFinder._DIFF_POS]
            elif diff[DiffFinder._DIFF_TYPE] == DiffType.DEL:
                _start =  diff[DiffFinder._DIFF_POS]
                _end = _start + diff[DiffFinder._DIFF_ARGS]
                text += del_color + self._former[_start: _end] + Fore.RESET
                start = _end
        text += unchanged_color + self._former[start:] + Fore.RESET + Back.RESET
        return text
    
    def _same(self) -> bool:
        if self._former == self._latter:
            return True
        return False
    
    def _analyse_mat(self):
        len_former = len(self._former)
        len_latter = len(self._latter)
        self._dist_mat = self._new_mat(len_former+1, len_latter+1, 0)
        self._diff_mat = self._new_mat(len_former+1, len_latter+1, None)
        self._parent_mat = self._new_mat(len_former+1, len_latter+1, None)
        for i in range(len_former + 1):
            self._dist_mat[i][0] = i
            if i > 0:
                self._diff_mat[i][0] = DiffType.DEL
                self._parent_mat[i][0] = (i-1, 0)
        for j in range(len_latter+1):
            self._dist_mat[0][j] = j
            if j > 0:
                self._diff_mat[0][j] = DiffType.ADD
                self._parent_mat[0][j] = (0, j-1)
        for i in range(1, len_former+1):
            for j in range(1, len_latter+1):
                cadd = self._dist_mat[i][j-1]
                cdel = self._dist_mat[i-1][j]
                clast = self._dist_mat[i-1][j-1]
                if self._former[i-1] == self._latter[j-1]: # 字符相等
                    if cadd < cdel and cadd < clast:
                        self._dist_mat[i][j] = cadd + 1
                        self._diff_mat[i][j] = DiffType.ADD
                        self._parent_mat[i][j] = (i, j-1)
                    elif cdel < cadd and cdel < clast:
                        self._dist_mat[i][j] = cdel + 1
                        self._diff_mat[i][j] = DiffType.DEL
                        self._parent_mat[i][j] = (i-1, j)
                    else:
                        self._dist_mat[i][j] = clast
                        self._diff_mat[i][j] = None
                        self._parent_mat[i][j] = (i-1, j-1)
                else: # 字符不相等
                    if cadd <= cdel:
                        self._dist_mat[i][j] = cadd + 1
                        self._diff_mat[i][j] = DiffType.ADD
                        self._parent_mat[i][j] = (i, j-1)
                    else:
                        self._dist_mat[i][j] = cdel + 1
                        self._diff_mat[i][j] = DiffType.DEL
                        self._parent_mat[i][j] = (i-1, j)

    def _analyse_diffs(self):
        diffs = []
        pos = (len(self._former), len(self._latter))
        while pos:
            i, j = pos
            diff = self._create_diff(i, j)
            if diff:
                diffs.insert(0, diff) # 倒插
            pos = self._parent_mat[i][j]
        self._diffs = [diffs[0]]
        for k in range(1, len(diffs)):
            pop_diff = self._diffs.pop()
            merged_diff = self._merge_diffs(pop_diff, diffs[k])
            if merged_diff:
                self._diffs.append(merged_diff)
            else:
                self._diffs.append(pop_diff)
                self._diffs.append(diffs[k])

    def _new_mat(self, h: int, w: int, init_value: Any) -> List[List]:
        return [[init_value for j in range(w)] for i in range(h)]
        
    def _create_diff(self, i, j) -> dict:
        if self._diff_mat[i][j] == DiffType.ADD:
            return {
                DiffFinder._DIFF_TYPE: DiffType.ADD,
                DiffFinder._DIFF_POS: i,
                DiffFinder._DIFF_ARGS: self._latter[j-1], # 增加的字符
            }
        elif self._diff_mat[i][j] == DiffType.DEL:
            return {
                DiffFinder._DIFF_TYPE: DiffType.DEL,
                DiffFinder._DIFF_POS: i-1,
                DiffFinder._DIFF_ARGS: 1, # 删除字符个数
            }
        else:
            return None
    
    def _merge_diffs(self, a: dict, b: dict) -> dict:
        merge = False
        if a[DiffFinder._DIFF_TYPE] == b[DiffFinder._DIFF_TYPE]:
            if a[DiffFinder._DIFF_TYPE] == DiffType.ADD and a[DiffFinder._DIFF_POS] == b[DiffFinder._DIFF_POS]:
                merge = True
            elif a[DiffFinder._DIFF_TYPE] == DiffType.DEL and a[DiffFinder._DIFF_POS] + a[DiffFinder._DIFF_ARGS] == b[DiffFinder._DIFF_POS]:
                merge = True
        if merge:
            return {
                DiffFinder._DIFF_TYPE: a[DiffFinder._DIFF_TYPE],
                DiffFinder._DIFF_POS: a[DiffFinder._DIFF_POS],
                DiffFinder._DIFF_ARGS: a[DiffFinder._DIFF_ARGS] + b[DiffFinder._DIFF_ARGS],
            }
        else:
            return None
    

if __name__ == '__main__':
    finder = DiffFinder()
    finder.analyse('13', '133')
    diffs = finder.listDiffs()
    print(diffs)
    text = finder.format()
    print(text)