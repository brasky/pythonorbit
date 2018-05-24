
def getMaxTriangle(profitResult):
    profitResultSorted = sorted(profitResult, key=lambda k: k['profit'])
    return profitResultSorted[-1]
