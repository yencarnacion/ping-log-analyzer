import re
import pandas as pd
import numpy as np
import gnuplotlib as gp

def get_aprox_time(seconds):
    
    # Convert the seconds to hours, minutes and seconds                           
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return hours, minutes, seconds
    
def process_ping_log(file_path):
    with open(file_path, 'r') as f:
        next(f)  # skip the first line
        log_data = f.readlines()

    ping_times = []
    fail_times = []
    sequence = 0

    # Loop through each line
    for line in log_data:
        search_result = re.search(r'time=(\d+(\.\d+)?) ms', line)
        if search_result:
            ping_times.append(float(search_result.group(1)))
        else:
            fail_times.append(line)

        # Use re.search to find the the value for icmp_seq
        match = re.search(r'icmp_seq=(\d+)', line)
    
        # If a match was found
        if match:
            # Store the integer value
            sequence = int(match.group(1))

    if ping_times:
        # Convert the list to a Pandas Series
        float_series = pd.Series(ping_times)

        # Convert the list of ping times to a numpy array
        float_array = np.array(ping_times)

        # Plot the boxplot
        gp.plot(float_array, terminal='dumb 80,30',
        cmds='set style fill solid 0.25 noborder; set style boxplot outliers pointtype 7; set style data boxplot')
        
        # Use the describe function
        desc = float_series.describe()

        # Define the format
        pd.set_option('display.float_format', lambda x: '%.1f' % x)

        print(desc)

        # Get the 'count' value in seconds
        hours, minutes, seconds = get_aprox_time(desc['count'])

        # Print the result
        print(f"\nCount converted to hours:minutes:seconds: {int(hours)}:{int(minutes):02}:{int(seconds):02}")

        # Get the 'sequence' value in seconds
        hours, minutes, seconds = get_aprox_time(sequence)

        # Print the result
        print(f"\nSequence converted to hours:minutes:seconds: {int(hours)}:{int(minutes):02}:{int(seconds):02}")

        # Count the values greater than 3000 (3 seconds)
        count = np.sum(float_array > 3000)

        print(f"Count of values above 3000 ms (3 seconds): {count}")

    else:
        print('No ping times found in log.')

    if fail_times:
        print(f'Number of failed pings: {len(fail_times)}')
        for fail in fail_times:
            print(f'Failed connection at: {fail}')
    else:
        print('No failed pings found in log.')


# specify your log file path here
log_file = 'ping_output.txt'
process_ping_log(log_file)
