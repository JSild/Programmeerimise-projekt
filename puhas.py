# Define file names
input_file = "nami-nami_lingid.txt"
output_file = "korras_nami-nami_lingid.txt"

# Open the input file and output file
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        # Replace duplicate instances of 'https://nami-nami.ee'
        corrected_line = line.replace("https://nami-nami.eehttps://nami-nami.ee", "https://nami-nami.ee")
        outfile.write(corrected_line)

print(f"Deduplicated URLs have been written to {output_file}.")
