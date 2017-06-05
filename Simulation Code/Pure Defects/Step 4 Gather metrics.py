import csv
import os
import os.path


def find_files():
    # Read directory structure to find csv files for combination of defects for fractions a-e.
    metric_files = []
    root_path = './tau_p0_data/'
    counter = 0
    for root, dirs, files in os.walk(root_path):
        for file in files:
            ext = os.path.splitext(file)[1]
            filename = os.path.splitext(file)[0]
            if ext == '.txt' and filename.endswith('metrics'):
                full_path = os.path.join(root, file)
                metric_files.append({'full_path': full_path, 'filename': file})
                print "Found file: " + full_path
                counter = counter +1
    print "find_files counted " + str(counter) + " metric data files"
    return metric_files

def read_files(files):
    for fileinfo in files:
        metrics = {}
        with open(fileinfo['full_path'], 'r') as f:
            for line in f:
                words = line.split('\t')
                metrics[str(words[0]).rstrip('\n')] = words[1].rstrip('\n')
        split = fileinfo['filename'].split()
        metrics['first_defect'] = split[0]
        #metrics['combined_with_defect'] = split[3]
        result.append(metrics)

def write_result(result):
    print "Entering write result"
    for result_set in result:
        print result_set
    print "Writing result set to file..."
    with open('metrics.csv', 'wb') as csvfile:
        # these fieldnames must exist in the result dictionaries
        fieldnames = ['first_defect', 'combined_with_defect','max_Et', 'min_Et', 'max_k', 'min_k', 'min_residual_value_used_in_plot',
                       'min_residual_value_used_in_plot_Et', 'min_residual_value_used_in_plot_k']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result)


result = []
files = find_files()
read_files(files)
write_result(result)