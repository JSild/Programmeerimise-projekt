# Define file names
input_file = "naminami_links.txt"
output_file = "nami-nami_lingid.txt"

# Open the input file and output file
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        # Skip URLs containing /#comments
        if "/#comments" not in line:
            outfile.write(line)

print(f"Cleaned URLs have been written to {output_file}.")
