def mirror(sudo):
    res = [[x[i] for i in range(8, -1, -1)] for x in sudo]
    return res

def rotate(sudo):
    res = [[sudo[y][x] for y in range(9)] for x in range(8, -1, -1)]
    return res

def mutate_8(sudo):
    mir = mirror(sudo)
    res = [mir]
    last = rotate(sudo)
    res.append(last)
    last = rotate(last)
    res.append(last)
    last = rotate(last)
    res.append(last)

    res.append(sudo)
    last = rotate(mir)
    res.append(last)
    last = rotate(last)
    res.append(last)
    last = rotate(last)
    res.append(last)
    return res
    
def copy_sudo(sudo):
    return [[sudo[x][y] for y in range(9)] for x in range(9)]
    
def remove_x(sudo, first, second):
    res = copy_sudo(sudo)
    buffer = res[first]
    res[first] = res[second]
    res[second] = buffer
    return res

def remove_x_blocks(sudo, first, second):
    res = copy_sudo(sudo)
    buffer = res[first * 3:first * 3 + 3]
    res[first * 3:first * 3 + 3] = res[second * 3:second * 3 + 3]
    res[second * 3:second * 3 + 3] = buffer
    return res

def remove_y(sudo, first, second):
    res = copy_sudo(sudo)
    for x in range(9):
        
        buffer = res[x][first]
        res[x][first] = res[x][second]
        res[x][second] = buffer
    return res

def remove_y_inplace(sudo, first, second):
    res = sudo
    for x in range(9):
        buffer = res[x][first]
        res[x][first] = res[x][second]
        res[x][second] = buffer
    return res

def remove_y_blocks(sudo, first, second):
    res = copy_sudo(sudo)
    first *= 3
    second *= 3
    for i in range(3):
        remove_y_inplace(res, first+i, second+i)
    return res

def remove_schema(sudo, function):
    res = [sudo]
    last = function(sudo, 0, 1)
    res.append(last)
    last = function(last, 0, 2)
    res.append(last)
    
    last = function(sudo, 0, 2)
    res.append(last)
    last = function(last, 0, 1)
    res.append(last)
    last = function(last, 0, 2)
    res.append(last)
    return res

def remove_in_3(shift, sudo, function, first, second):
    return function(sudo, first + shift, second + shift)

def remove_in_3_in_3(sudo, function):
    res = remove_schema(sudo, lambda s, x, y: remove_in_3(0, s, remove_x,  x, y))
    res_ = []
    for sudo_1 in res:
        res_ += remove_schema(sudo_1, lambda s, x, y: remove_in_3(3, s, remove_x,  x, y))
        
    res_1 = []
    for sudo_1 in res_:
        res_1 += remove_schema(sudo_1, lambda s, x, y: remove_in_3(6, s, remove_x,  x, y))
        
    return res_1

def remove_3_3(sudo, function):
    return remove_schema(sudo, lambda s, x, y: function(s, x, y))

def check_sudo(sudo):
    """
    Return True if sudo solved
    """
    
    for x in range(9):
        checker = [False for _ in range(10)]
        for item in sudo[x]:
            if checker[item] == False:
                checker[item] = True
            else:
                return False
        if checker[0]:
            return False
    
    for y in range(9):
        checker = [False for _ in range(10)]
        for x in range(9):
            item = sudo[x][y]
            if checker[item] == False:
                checker[item] = True
            else:
                return False
        if checker[0]:
            return False
    
    for x in range(3):
        for y in range(3):
            checker = [False for _ in range(10)]
            for x_ in range(x*3, x*3+3):
                for y_ in range(y*3, y*3+3):
                    item = sudo[x_][y_]
                    if checker[item] == False:
                        checker[item] = True
                    else:
                        return False
            if checker[0]:
                return False
    return True

def check_list(sudos):
    
    for i in sudos:
        is_r = check_sudo(i)
        if is_r == False:
            return False
    return True

def mutate(sudo, check=True):
    #mutate y-axis
    result = remove_in_3_in_3(sudo, remove_y)
    
    result1 = result
    result = []
    for sudo1 in result1:
        result += remove_3_3(sudo, remove_y_blocks)
    
    #mutate x-axis
    result1 = result
    result = []
    for sudo1 in result1:
        result += remove_in_3_in_3(sudo, remove_x)

    result1 = result
    result = []
    for sudo1 in result1:
        result += remove_3_3(sudo, remove_x_blocks)    

    # mutate_8
    result1 = result
    result = []
    for sudo1 in result1:
        result += mutate_8(sudo1)
        
    # check list of mutation
    if check:
        is_right = check_list(result)
        if not is_right:
            raise Exception("Bad mutation: mutated sudoku is wrong")
            
    return result

