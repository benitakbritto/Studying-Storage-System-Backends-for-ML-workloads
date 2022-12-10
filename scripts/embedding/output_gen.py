import csv
import os

def write_output(output_file, fields, rows):
    with open(output_file, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(rows) 

def gen_output(source_path, output_file):
    fields = ['ds', 'dsize', 'esize', 'bsize', 'time']
    rows = []

    file_names = os.listdir(source_path)

    for fname in file_names:
        # print(fname)
        tokens = fname.split("_")
        dsize = tokens[0].strip("d")
        esize = tokens[1].strip("e")
        bsize = tokens[2].strip("b")

        # read a file
        with open(source_path + "/" + fname, "r") as f:

            for line in f:
                # skip first line as it says "dataset prepared"
                if line.strip() == "dataset prepared":
                    continue
                
                # each line is of format: 
                # Datastore: [ds], Total time: [time] s
                line_tokens = line.split(",")
                ds = line_tokens[0].strip().strip("Datastore:").strip()
                time = line_tokens[1].strip().strip("Total time:").strip("s").strip()

                rows.append([ds, dsize, esize, bsize, time])

    write_output(output_file=output_file, fields=fields, rows=rows)

if __name__ == "__main__":
    gen_output(source_path="./output/graph/", output_file="./graph_data.csv")