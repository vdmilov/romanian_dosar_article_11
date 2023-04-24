from download import *
from transform import *


def execute_pipeline():
	download_dosar_pdfs()
	move_dosar_pdfs()
	read_and_transform_dosar_pdfs()
	delete_dosar_pdfs()


if __name__ == '__main__':
	execute_pipeline()