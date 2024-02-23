
import subprocess
import matplotlib.pyplot as plt
from random import randint
from decimal import Decimal as D

# to create set file section
def dat_file_sets(path: str, n: int):
    f_dat = open(path, "w")
    f_dat.write("\n")
    f_dat.write("### INSIEMI ###\n")
    set_str = "set P := "
    range_str = ""
    for i in range(1,n+1):
        range_str += str(i) + " "
    set_str += range_str
    set_str = set_str[:-1] + ';'
    f_dat.write(set_str)
    f_dat.write("\n\n")
    f_dat.close()

# to create param file section
def dat_file_params(path: str, points: list[str], n_k: int):
    n = len(points)
    f = open(path, "a")
    f.write("### PARAMETRI ###\n")
    f.write("param d:\n")
    m_d = []
    first_row = [""]
    for i in range(1,n+1):
        first_row.append(str(i))
    first_row.append(":=")
    m_d.append(first_row)
    for i in range(0,n):
        row = [str(i+1)]
        for _ in range(0, i+1):
            row.append(".")
        for j in range(i+1, n):
            coordinates_1 = points[i].split(";")
            coordinates_2 = points[j].split(";")
            sum = D('0')
            for k in range(len(coordinates_1)):
                sum += (D(coordinates_1[k])-D(coordinates_2[k])) ** 2
            d = sum.sqrt()
            row.append(str(d))
        row.append("" if i<n-1 else ";")
        m_d.append(row)  
    max_lengths = [max(map(len, col)) for col in zip(*m_d)]
    str_mat = ""
    for row in m_d:
        formatted_row = "\t".join("{:<{}}".format(value, max_len) for value, max_len in zip(row, max_lengths))
        str_mat += "\t" + formatted_row + "\n"
    f.write(str_mat)
    f.write("param K := " + str(n_k) + ";")
    f.close()

# to create points.dat
def creating_dat():
    f = open("./points.txt", "r")
    points_str = f.readlines()
    f.close()
    k = int(points_str.pop(0))
    if len(points_str) == 0:
        print("Incorrect File!")
        return
    points_str.pop(0)
    if len(points_str) == 0:
        print("Incorrect File!")
    else:
        dat_file_sets("./points.dat", len(points_str))
        dat_file_params("./points.dat", points_str, k)

# problem solve with ampl subprocess
def solve():
    subprocess.run("cd .. & ampl.exe raggruppamento_di_punti\points.run > raggruppamento_di_punti\sol.txt", shell=True, check=True)

def reading_points(path: str) -> tuple[int, list[tuple[float,float]]]:
    f = open(path, 'r')
    points = []
    if (K:=int(f.readline())) < 2:
        print('K >= 2.')
        K = 2
    elif int(f.readline()) <= 0:
        print('n must be positive.')
    else:
        while str_pt := f.readline():
            str_coo = str_pt.split(';')
            points.append(tuple([float(coo) for coo in str_coo]))
    return K, points

def random_color() -> str:
    return '#%02x%02x%02x' % (randint(0, 255), randint(0, 255), randint(0, 255))

def plotting_points(K: int, points: list[tuple[float,float]], rel_subsets: list[int]):
    plt.figure(num='©2024 FB & AM')

    # different plotting due to n
    if (n := len(points[0])) not in [2,3]:
        print('Graph is only for 2 or 3 coordinates.')
        return
    if n == 3: # 3D plotting graph
        plt.axes(projection='3d')

    # K different colors
    rel_colors = ["blue", "red", "green", "yellow"] + ([random_color() for _ in range(K-4)] if K > 4 else [])

    for pt in points:
        plt.plot(*pt, marker='o', color=rel_colors[rel_subsets[points.index(pt)]-1])
    plt.show()

def reading_results(path: str) -> list[int]:
    with open(path, 'r') as file_sol:
        str_tot = file_sol.read()
    a_str_sol = str_tot.split('x :=\n')[1].split(';')[0].split('\n')[:-1]
    a_sol = [r.split(' ')[0:2] + r.split(' ')[4:5] for r in a_str_sol]
    return [int(a[1]) for a in a_sol if a[2]=='1']

def plotting():
    # reading file
    K, points = reading_points('points.txt')

    # plot font settings
    plt.rcParams['font.sans-serif'] = "Latin Modern Math" # according to LatEX style
    plt.rcParams['font.family'] = "sans-serif"

    # plotting points
    plotting_points(K, points, reading_results('sol.txt'))

def main():
    creating_dat()
    solve()
    plotting()

# entry point
if __name__ == '__main__':
    main()
    