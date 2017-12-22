CC=g++
LN=g++
OPT=-std=gnu++17 -Wextra -Werror -fPIC $(shell pkg-config --cflags Qt5OpenGL) -g -pg
LIB=-lm -lstdc++ $(shell pkg-config --libs Qt5OpenGL) -lGL -lGLU
OBJ= src/window.o src/moc_window.o src/main.o
OBJ+=src/render.o src/moc_render.o

all: OPT += -Os -O3
all: executable
  
debug: OPT += -g -pg -D__DEBUG
debug: executable

executable: $(OBJ)
	$(LN) $(LIB) $(OBJ) -o calc

%.o: %.cpp
	$(CC) $(OPT) -c $< -o $@

clean:
	rm -f $(OBJ) calc

update:
	moc-qt5 src/window.h -o src/moc_window.cpp
	moc-qt5 src/render.h -o src/moc_render.cpp