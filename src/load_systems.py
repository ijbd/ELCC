import os
import sys
import numpy as np

LAUNCH_FILE = 'elcc_job_0.txt'

def init():

    # Save time and money 
    print("Job Checklist: Have you...")
    user_check("Activated conda environment? (y/n): ",'y')
    user_check("Checked batch resources? (y/n): ",'y')
    user_check("Completed 10 iteration test job? (y/n): ",'y')

    # New launcher file
    new_job()

def user_check(message, test_response):

    status = input(message) == test_response
    if not status:
        sys.exit(1)

def new_job():

    global LAUNCH_FILE

    i = 0
    while os.path.exists('elcc_job_'+str(i)+'.txt'):
        i += 1
    
    LAUNCH_FILE = 'elcc_job_'+str(i)+'.txt'

def add_job(parameters):

    global root_directory
    global LAUNCH_FILE

    # start string with
    parameter_string = ''

    parameters = fix_region_string(parameters)

    for key in parameters:
        parameter_string = parameter_string + ' ' + str(key.replace(' ','_')) + ' ' + str(parameters[key])
    
    with open(LAUNCH_FILE,'a') as f:
        f.write('python -u elcc_driver.py ' + parameter_string + '\n')

def run_job():
# call batch script on current job

    global LAUNCH_FILE

    # launch job
    os.system('sbatch elcc_single_job.sbat '+LAUNCH_FILE)

    # start new file for running
    new_job()

def fix_region_string(parameters):
#list to formatted string

    if 'region' in parameters:
        
        regions = parameters['region']

        if isinstance(regions,str):
            return parameters

        #otherwise fix string
        region_str = '\"' + ' '.join(np.sort(regions)) + '\"'

        region_str = region_str[:-1] + '\"'

        parameters['region'] = region_str
    
    return parameters
    

def main():

    global root_directory

    parameters = dict()

    ########### DO NOT WRITE ABOVE THIS LINE (please?) #############



    # test
    parameters['iterations'] = 5000

    # clean up 2019
    year = 2019
    for region in ['basin','california','mountains','northwest','southwest']:
        parameters['region'] = region.capitalize()
        
        parameters['year'] = year
        parameters['root directory'] = '/home/ijbd/output/'+region+'/'+str(year)+'/'
        
        parameters['temperature dependent FOR'] = True

        add_job(parameters)
        run_job()

        parameters['temperature dependent FOR'] = False

        add_job(parameters)
        run_job()

    
    

if __name__ == "__main__":
    init()
    main()