import torch
import torch.optim as optim
import numpy as np
import random
from data_set import *
from mutations import *
from model import *
import kagglehub

def load_dataset():
    path = kagglehub.dataset_download("bryanpark/sudoku").replace("\\", "/") + "/sudoku.csv"
    print("Path to dataset files:", path)
    quizzes = np.zeros((1000000, 81), np.int32)
    solutions = np.zeros((1000000, 81), np.int32)
    for i, line in enumerate(open(path, 'r').read().splitlines()[1:]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    return [i.tolist() for i in quizzes], [i.tolist() for i in solutions]

def train(task, solution):
    print()
    print("Start training of model")
    dtype=torch.float32
    net = Sudoku_solver(dtype)
    device = "cuda"
    net = net.to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.0001)
    epochs = 10
    count_in_epoch = 990000
    order = list(range(count_in_epoch))
    batch_size = 5
    shift = 10000
    
    for epoch in range(epochs):
        epoch_loss = 0.
        pointer = 0
        random.shuffle(order)
        
        for i in range(count_in_epoch // batch_size):
            
            y = []
            x = []
            for _ in range(batch_size):
                current_index = order[pointer] + shift
                y_ = solution[current_index]
                y.append(smash(get_categorized(y_)))
                x.append(to_10_dim(task[current_index]))
                pointer += 1
            x, y = map(lambda x: torch.tensor(x, dtype=dtype).to(device), [x, y])
            out = net(x)
            optimizer.zero_grad()
            loss = criterion(y, out)
            epoch_loss += loss.item()
            loss.backward()
            optimizer.step()

        epoch_loss = (epoch_loss / count_in_epoch) * batch_size
        print(f"Epoch: {epoch}, loss: {epoch_loss:.5f}")
        
    return net

def test(net, task, solution):
    print()
    print("Start testing of model")
    dtype=torch.float32
    device = "cuda"
    net = net.to(device)
    accuracy = 0.
    count = len(task)
    y = solution
    x = task
    for y_y in range(count):
        task__ = x[y_y]
        while True:
            x_ = torch.tensor([to_10_dim(task__)], dtype=dtype).to(device)
            out = unsmash(net(x_).tolist()[0])
            is_ready, task__ = set_digit(task__, out)
            if task__ == None:
                if is_ready:
                    accuracy += 1.
                break
                
    accuracy = accuracy / count * 100.
    print(f"Accuracy: {accuracy:.2f}%")

def main():
    task, solution = load_dataset()
    net = train(task, solution)
    count = 10000
    test(net, task[:count], solution[:count])

if __name__ == "__main__":
    main()