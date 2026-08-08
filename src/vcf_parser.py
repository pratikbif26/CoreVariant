import pandas as pd
import io

def parse_uploaded_vcf(uploaded_file):
    """
    Parses a VCF BytesIO object from Streamlit and returns a Pandas DataFrame.
    Filters out header lines and extracts standard variant columns.
    """
    # Read the uploaded file and decode the bytes to strings
    vcf_text = uploaded_file.getvalue().decode("utf-8")
    
    # Extract only the data lines, ignoring the ## meta-information headers
    data_lines = [line for line in vcf_text.split('\n') if line and not line.startswith('##')]
    
    if not data_lines:
        return pd.DataFrame() # Return empty if file is invalid
        
    # The first valid line should be the column headers (starting with #CHROM)
    header = data_lines[0].replace('#', '').split('\t')
    
    # Parse the remaining variant lines
    variants = []
    for line in data_lines[1:]:
        columns = line.split('\t')
        if len(columns) >= 5:
            variants.append({
                "CHROM": columns[0],
                "POS": columns[1],
                "ID": columns[2] if columns[2] != '.' else f"{columns[0]}:{columns[1]}",
                "REF": columns[3],
                "ALT": columns[4]
            })
            
    return pd.DataFrame(variants)