import csv

def read_csv_to_matrix(filename):
    matrix = []
    header = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            matrix.append([int(cell.strip()) if cell.strip() else 0 for cell in row])
    return header, matrix

def mirror_diagonal(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i+1, n):
            matrix[j][i] = matrix[i][j]
            matrix[i][j] = matrix[j][i]
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def write_matrix_to_csv(header, matrix, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(matrix)

if __name__ == "__main__":
    filename = 'Board.csv'
    header, matrix = read_csv_to_matrix(filename)
    mirrored_matrix = mirror_diagonal(matrix)
    print_matrix(mirrored_matrix)
    write_matrix_to_csv(header, mirrored_matrix, 'FullBoard.csv')