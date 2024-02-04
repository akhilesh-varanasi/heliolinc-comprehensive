import pandas as pd

##
## ADES reading/writing
##

def read_psv_ades(fn):
    """Read PSV ADES file
    
    Args:
        fn (str): Filename
        
    Returns:
        tuple: loaded dataframe, header
    """
    header = []
    with open(fn) as fp:
        # consume and store the header
        while True:
            line = fp.readline()
            if line[0] in ['#', '!']:
                header.append(line.rstrip())
                continue
            # the line is the header
            names = [ s.strip() for s in line.split('|') ]
            break
        df = pd.read_csv(fp, sep='|', header=0, names=names)
    return df, header