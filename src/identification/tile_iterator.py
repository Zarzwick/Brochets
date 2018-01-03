from numpy import ndarray, shape

class TiledIterator(object):
    '''Provide tiles over the two first dimensions of a ndarray.'''

    def __init__(self, arr, subdiv):
        '''Subdivides an array in subdiv[DIMENSION] regions in each DIMENSION.'''
        self.arr = arr
        self.subdiv = subdiv
        self.subshape = (shape(arr)[0]//subdiv[0], shape(arr)[1]//subdiv[1])
        self.iteration = 0

    def __iter__(self):
        '''Return itself...'''
        return self

    def __next__(self):
        '''Provide a couple of slices for accessing the array.'''
        if self.iteration < self.subdiv[0] * self.subdiv[1]:
            width  = self.subdiv[1]
            line   = (self.iteration // width) * self.subshape[0]
            column = (self.iteration %  width) * self.subshape[1]
            self.iteration += 1
            return (slice(line, line+self.subshape[0]),
                    slice(column, column+self.subshape[1]))
        else:
            raise StopIteration

