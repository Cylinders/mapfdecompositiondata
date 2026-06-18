import os
import csv
import re

def parse_directory_to_csv(input_dir, output_csv):
    """
    Parses all text files in the given input directory and writes the extracted metrics to the output CSV.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Directory '{input_dir}' not found.")
        return

    fieldnames = [
        'filename', 'pathtomap', 'pathtoscen', 
        'CBSoutput', 'CBSHoutput', 'BCPoutput', 'MDDSAToutput', 
        'CBStime', 'CBSHtime', 'BCPtime'
    ]
    
    num_pattern = r'([-+]?[0-9]*\.?[0-9]+)'

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, _, files in os.walk(input_dir):
            for file in files:
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Could not read {filepath}: {e}")
                    continue

                # Extract data using regex
                map_match = re.search(r'map:\s*"([^"]+)"', content)
                scen_match = re.search(r'scenario:\s*"([^"]+)"', content)
                
                cbs_out_match = re.search(r'^CBS:\s*' + num_pattern, content, re.MULTILINE)
                cbsh_out_match = re.search(r'^CBSH:\s*' + num_pattern, content, re.MULTILINE)
                bcp_out_match = re.search(r'^BCP:\s*' + num_pattern, content, re.MULTILINE)
                mddsat_out_match = re.search(r'^MDDSAT:\s*' + num_pattern, content, re.MULTILINE)
                
                cbs_time_match = re.search(r'CBS took\s*' + num_pattern + r'\s*ms', content)
                cbsh_time_match = re.search(r'CBSH took\s*' + num_pattern + r'\s*ms', content)
                bcp_time_match = re.search(r'BCP took\s*' + num_pattern + r'\s*ms', content)

                writer.writerow({
                    'filename': file,
                    'pathtomap': map_match.group(1) if map_match else '',
                    'pathtoscen': scen_match.group(1) if scen_match else '',
                    'CBSoutput': cbs_out_match.group(1) if cbs_out_match else '',
                    'CBSHoutput': cbsh_out_match.group(1) if cbsh_out_match else '',
                    'BCPoutput': bcp_out_match.group(1) if bcp_out_match else '',
                    'MDDSAToutput': mddsat_out_match.group(1) if mddsat_out_match else '',
                    'CBStime': cbs_time_match.group(1) if cbs_time_match else '',
                    'CBSHtime': cbsh_time_match.group(1) if cbsh_time_match else '',
                    'BCPtime': bcp_time_match.group(1) if bcp_time_match else ''
                })

    print(f"Success! Data parsed from '{input_dir}' and saved to '{output_csv}'.")

if __name__ == '__main__':
    my_input_directory = './my_text_files'
    my_output_file = 'final_results.csv'
    
    parse_directory_to_csv(my_input_directory, my_output_file)