#!/usr/bin/python3

from vpython import *
from PIL import Image
import os.path
import sys
import argparse

_parser = argparse.ArgumentParser(prog='maze_generator',description='generates a 3D maze from a given 1 bit binary heightmap')
_parser.add_argument('--generate-maze',dest='maze_file',action='store',type=str,help='input image file used to generate maze')
_parser.add_argument('--template',dest='template_file',action='store',type=str,help='generate template for maze of given size and save to file')
_parser.add_argument('--size',dest='sizeOf',action='store',type=str,help='dimensions of template WIDTHxHEIGHT')

args = _parser.parse_args()


def save_image(image,filepath):
	image.save(filepath,format='PNG')
	print('image saved as {}'.format(filepath))

def load_image(filepath):
	_image = Image.open(filepath)
	_image.convert("1")
	return _image

def generate_template(filepath,dims):
	_template = Image.new(mode="1",size=dims,color=1)
	_template.save(filepath,format='PNG')
	print('template saves as {}'.format(filepath))

def get_value(image,x,y):
	coord = (x,y)
	return image.getpixel(coord)

#draw unit cube at xyz
def cube(x,y,z):
	_cube = box(pos=vector(x,y,z),length=1,width=1,height=1)

def generate_maze(filepath):
	maze_image = load_image(filepath)
	width,height = maze_image.size
	print('generating maze of size {0} x {1} ...'.format(width,height))

	for i in range(0,width-1):
		for j in range(0,height-1):
			cube(i,-j,0)
			if(get_value(maze_image,i,j)==0):
				cube(i,-j,0)

	print('done!')
	print('use ctrl+mouse to view the maze in 3D space')



if __name__ == '__main__':
	if(args.maze_file != None):
		_maze_file = args.maze_file
		if os.path.isfile(_maze_file):
			generate_maze(_maze_file)
			sys.exit(0)
		else:
			print('{} does not exist! exiting...'.format(_maze_file))
			sys.exit(1)
	elif(args.template_file != None):
		_template_file = args.template_file
		if not os.path.isfile(_template_file):
			if(args.sizeOf != None):
				_size = args.sizeOf.split('x')
				try:
					_dims = (int(_size[0]),int(_size[1]))
				except ValueError:
					print('enter dimensions in valid format!')
					sys.exit(1)
				generate_template(_template_file,_dims)
				sys.exit(0)
			else:
				print('enter valid dimensions in the form wxh')
				sys.exit(1)
		else:
			print('template of this name already exists!')
			sys.exit(1)
	else:
		print('exiting after doing nothing...')
		print(vars(args))
		sys.exit(0)
