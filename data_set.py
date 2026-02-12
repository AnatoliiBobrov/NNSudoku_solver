import multiprocessing
import random
from pickle import dump, load
from mutations import copy_sudo, check_sudo

def try_rand_sudo():
    squares = [[[True for _ in range(9)] for y in range(9)] for x in range(9)]
    field = []
    for x in range(9):
        row = []
        for y in range(9):
            
            new_list = [i for i, val in enumerate(squares[x][y]) if val]
            #print(new_list)
            
            if new_list != []:
                cur_digit = random.choice(new_list)
                #print(cur_digit)
                row.append(cur_digit + 1)

                #flush in 3*3
                for x_ in range(x, (x // 3 + 1) * 3):
                    for y_ in range((y // 3) * 3, (y // 3 + 1) * 3):
                        squares[x_][y_][cur_digit] = False

                #flush in line
                for x_ in range(x+1, 9):
                    squares[x_][y][cur_digit] = False

                #flush in row
                for y_ in range(y+1, 9):
                    squares[x][y_][cur_digit] = False
            else:
                return None
        field.append(row)
    return field


def get_random_sudo(attempts=1000000):
    res = try_rand_sudo()
    attempt = 1
    while res == None and attempt < attempts:
        res = try_rand_sudo()
        attempt += 1
    return res, attempt
    
def get_dset_mean_attempts(arguments):
    count, random_state = arguments
    if random_state != None:
        random.seed(random_state)
    dset = []
    att = 0
    for i in range(count):
        d_, a_ = get_random_sudo(1000000)
        att += a_
        dset.append(d_)
    return dset, (att / count)

def get_dset_multiprocessing(count, processes=11, random_state=42):
    result = []
    with multiprocessing.Pool(processes=11) as pool:
        arguments = list(map(lambda i: (count - (count // processes) * (processes - 1) if i == processes - 1 else count // processes, random_state + i), range(processes)))
        print (arguments)
        result = pool.map(get_dset_mean_attempts, arguments)
    r1 = result
    result = []
    for r_ in r1:
        result += r_[0]
    return result



def calc_mean_attempts():
    print (get_dset_mean_attempts(1000)[1])

def get_categorized(sudo=None):
    if sudo == None:
        sudo = get_random_sudo()[0]
    res = []
    for x in sudo:
        line = []
        for y in x:
            line_ = [0 for _ in range(10)]
            line_[y] = 1
            line += line_
        res.append(line)
    return res

def from_categorized(sudo, threshold=0.5):
    res = []
    for x in sudo:
        line = []
        for y in range(0, 90, 10):
            item = 0
            max_val = 0.
            for y_ in range(10):
                val = x[y + y_]
                if val > max_val:
                    item = y_
                    max_val = val
            line.append(item)
            
        res.append(line)
    return res

def generate_zero(sudo, count=-1):
    if count == -1:
        count = 16
    r_choicer = [i for i in range(81)]
    random.shuffle(r_choicer)
    res = copy_sudo(sudo)
    for i in range(count):
        item = r_choicer.pop()
        x = item // 9
        y = item % 9
        res[x][y] = 0
    return res

def smash(sudo):
    res = []
    for line in sudo:
        res += line
    return res

def unsmash(sudo):
    res = []
    for i in range(9):
        res.append(sudo[i*90: i*90 + 90])
    return res

def load_dset(f_name="d_set.pkl"):
    result = None
    with open(f_name, "rb") as file:
        result = load(file)
    return result

def save_dset(d_set, f_name="d_set.pkl"):
    with open(f_name, "wb") as file:
        dump(d_set, file)

def compare_sudos(test_val, solved):
    for x in range(9):
        for y in range(9):
            val_1 = test_val[x][y]
            val_2 = solved[x][y]
            if val_1 != 0:
                if val_1 != val_2:
                    return False
    return check_sudo(solved)

def set_digit(task, solution):
    """
    Return False, if still not solved (else True) and new task without one 0
    Solution is unsmashed categorized matrix
    """
    res = []
    coord_x, coord_y = 0, 0
    digit = -1
    probability = 0.
    zeros = 0.
    solution_cat = []
    for x in range(9):
        line = []
        for y in range(9):
            item = 0
            max_val = 0.
            for y_ in range(10):
                val = solution[x][y * 10 + y_]
                if val > max_val:
                    item = y_
                    max_val = val
            line.append(item)
            if task[x][y] == 0:
                zeros += 1.
                if probability < max_val and item != 0:
                    probability = max_val
                    coord_x = x
                    coord_y = y
                    digit = item
        res.append(line)
    #print(zeros)
    f_c_res = res
    if zeros < 0.5:
        if compare_sudos(task, f_c_res):
            return True, None
        else:
            return False, None
    if digit == -1:
        return False, None
    if compare_sudos(task, f_c_res):
        return True, None
    else:
        new_task = copy_sudo(task)
        new_task[coord_x][coord_y] = digit
        return False, new_task

def to_10_dim(sudo):
    dims = [[[0. for _ in range(9)] for _ in range(9)] for _ in range(10)]
    for x in range(9):
        for y in range(9):
            item = sudo[x][y]
            dims[item][x][y] = 1.
    return dims