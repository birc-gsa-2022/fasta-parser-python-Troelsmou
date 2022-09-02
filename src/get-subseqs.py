import argparse
import sys

#coordinate_default = sys.stdin

parser = argparse.ArgumentParser(prog = "fasta_recs")
parser.add_argument("--fasta-path", nargs = 1, type = str, help = "Path to input fasta file")
parser.add_argument("--coordinate-path", nargs = "?", type = str, help = "Path to input fasta file",
	default = False)


def fasta_scanner(file_object):
	name_indices = list()
	sequence_indices = list()

	loop_count = 0
	for i in file_object:
		if i[0] == ">":
			name_indices.append(loop_count)
		loop_count +=1
	for i in range(len(name_indices)):
		start = name_indices[i] + 1
		sequence_indices.append(start)
		if i == len(name_indices)-1:
			end = loop_count - 1
		else:
			end = name_indices[i + 1] - 1
		sequence_indices.append(end)
	out = {"names": name_indices,
	"sequences": sequence_indices}
	return(out)

def extract_names(file_object, name_indices):
	names = list()
	loop_count = 0
	for i in file_object:
		if loop_count in name_indices:
			if i[1] == " ":
				names.append(i[2:len(i)])
			else:
				names.append(i[1:len(i)])
		loop_count+=1
	return(names)

def extract_sequences(file_object, indice_dict):
	out = list()
	loop_count = 0
	seq_count = 0
	for i in file_object:
		if loop_count in indice_dict["names"]:
			seq = ""
			loop_count +=1
			continue
		seq = seq + i
		if loop_count == indice_dict["sequences"][seq_count*2 + 1]:
			out.append(seq)
			seq_count +=1
		loop_count +=1
	return(out)


def fasta_reader(file_path):
	file_object = open(r"{path}".format(path=file_path), "r")
	indice_dict = fasta_scanner(file_object)
	file_object = open(r"{path}".format(path=file_path), "r")
	names = extract_names(file_object, indice_dict["names"])
	file_object = open(r"{path}".format(path=file_path), "r")
	sequences = extract_sequences(file_object, indice_dict)
	for i in range(len(names)):
		names[i] = names[i].replace("\n", "")
		sequences[i] = sequences[i].replace("\n", "")
	out_dict = {
	"names": names,
	"sequences": sequences
	}
	return(out_dict)

args = parser.parse_args()

fasta_dict = fasta_reader(args.fasta_path[0])

real_dict = dict()

for i in range(len(fasta_dict["names"])):
	real_dict[fasta_dict["names"][i]] = fasta_dict["sequences"][i]

if not args.coordinate_path or args.coordinate_path == "-":
	args.coordinate_path = list()
	for i in range(len(real_dict)):
		args.coordinate_path.append(input())
else:
	coordinate_file = open(r"{path}".format(path=args.coordinate_path), "r")
	args.coordinate_path = list()
	for i in coordinate_file:
		args.coordinate_path.append(i)

for i in args.coordinate_path:
	coords = i.split()
	if coords[1] == coords[2]:
		sys.stdout.write(real_dict[coords[0]][int(coords[1])-1] + "\n")
	else:
		sys.stdout.write(real_dict[coords[0]][int(coords[1])-1:int(coords[2])-1] + "\n")

