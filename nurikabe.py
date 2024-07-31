class Grid:
    
    def __init__(self, file_name):
        
        if file_name == None:
            self.matrix = []
            self.dims = (0, 0)
            self.wall_count = 0
            self.contains_2x2wall = False
            self.numbers_sum = 0
            self.wall_size = 0
        else:
            self.matrix = text_to_matrix(file_name)
            self.dims = dimensions(self.matrix)
            self.wall_count = walls_in_matrix(self.matrix)
            self.contains_2x2wall = contains_2x2wall(self.matrix)
            self.numbers_sum = numbers_sum(self.matrix)
            self.wall_size = self.dims[0]*self.dims[1] - self.numbers_sum
            

    def is_valid_position(self, pos):
        return is_valid_position(pos, self.dims)
    
    def is_number(self, pos):
        
        symbol = self.matrix[pos[0]][pos[1]]
        is_number = True
        
        if symbol == '#' or symbol == '.':
            is_number = False
            
        return is_number

    
    def is_wall(self, pos):
        
        symbol = self.matrix[pos[0]][pos[1]]
        is_wall = False
        
        if symbol == '#':
            is_wall = True
            
        return is_wall

    
    def value(self, pos):
        return int(self.matrix[pos[0]][pos[1]])

    
    def height(self):
        return self.dims[0]

    
    def width(self):
        return self.dims[1]

    
    def no_wall_count(self):
        return self.height()*self.width() - self.wall_count
    
    def contains_square(self):
        return self.contains_2x2wall

    
    def numbers_list(self):
        
        list, current_row = [], 0
        while current_row < self.dims[0]:
            
            current_column = 0
            while current_column < self.dims[1]:
                
                if self.is_number((current_row, current_column)):
                    list.append((current_row, current_column))
                
                current_column += 1
            current_row += 1
            
        return list

    
    def valid_islands(self):
        
        clone = clone_matrix(self.matrix)
        numbers = self.numbers_list()
        
        valid, current = True, 0
        while current < len(numbers) and valid:
            
            island = []
            island.append(numbers[current])
            
            valid = is_valid_island(clone, island)
            current += 1
            
        return valid

    
    def connected_wall(self):
        clone = clone_matrix(self.matrix)
        
        if self.wall_count == 0:
            is_connected = True
        else:
            is_connected = connected_wall_size(clone) == self.wall_count
        
        return is_connected

    
    def empty_cells_list(self):
        
        list, curent_row = [], 0
        
        while current_row < self.dims[0]:
            
            current_column = 0
            while current_column < self.dims[1]:
                
                if not self.is_wall((current_row, current_column)) and not self.is_number((current_row, current_column)):
                    list.append((current_row, current_column))
                    
                current_column += 1
            current_row += 1
            
        return list

    
    def clone(self):
        clone = Grid(None)
        clone.matrix = clone_matrix(self.matrix)
        clone.dims = self.dims
        clone.wall_count = self.wall_count
        clone.contains_2x2wall = self.contains_2x2wall
        clone.numbers_sum = self.numbers_sum
        clone.wall_size = self.wall_size
        return clone

    
    def add_wall(self, position):
        
        if not self.is_wall(position):
            
            self.matrix[position[0]][position[1]] = '#'
            self.wall_count += 1
            
            if self.is_valid_position((position[0]-1, position[1]-1)):
                square = square2x2((position[0]-1, position[1]-1))
                self.contains_2x2wall = walls(square, self.matrix)

    
    def remove_wall(self, position):
        
        if self.is_wall(position):
            self.matrix[position[0]][position[1]] = '.'
            self.wall_count -= 1
            self.contains_2x2wall = False

    
    def is_valid_solution(self):
        return self.valid_islands() and self.connected_wall() and not self.contains_2x2wall and self.wall_count == self.wall_size

    
    def backtracking_nurikabe(self, empty_cells, count):
        
        if count == len(empty_cells):
            rv = False
            
        else:
            self.add_wall(empty_cells[count])
            
            if self.contains_2x2wall:
                rv = False
                
            elif self.wall_count == self.wall_size:
                rv = self.is_valid_solution()
                
            else:
                rv = self.backtracking_nurikabe(empty_cells, count + 1)
                
            if not rv:
                self.remove_wall(empty_cells[count])
                rv = self.backtracking_nurikabe(empty_cells, count + 1)
                
        return rv

    
    def solve_nurikabe(self, output_file_name):
        
        clone = self.clone()
        output_file = open(output_file_name, 'w')
        empty_cells = clone.empty_cells_list()
        
        if clone.backtracking_nurikabe(empty_cells, 0):
            
            output_grid = clone
            current_row = 0
            
            while current_row < clone.dims[0]:
                
                current_column = 0
                while current_column < clone.dims[1]:
                    
                    output_file.write(clone.matrix[current_row][current_column])
                    
                    current_column += 1
                
                if current_row < clone.dims[0] - 1:
                    output_file.write('\n')
                
                current_row += 1
                
        else:
            
            output_grid = Grilla(None)
            print('The given grid admits no solution. \n')
            
        return output_grid
