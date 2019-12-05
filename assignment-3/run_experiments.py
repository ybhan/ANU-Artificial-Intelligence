""" Student Details

    Student Name: Jeff Yuanbo Han
    Student ID: u6617017
    Email: u6617017@anu.edu.au
    Date: 2018-05-25
"""
import subprocess


def run_command(format_dict):
    command = "python3 planner.py benchmarks/{domain}/domain.pddl benchmarks/{domain}/problem{problem}.pddl"\
                      " {domain}_tmp 1:30:1 -q ramp {pgconfig} -r true".format(**format_dict)
    format_dict['command'] = command
    outer_command = "python3 benchmark.py {time} {memory} '{command}' logs/{domain}{problem}_{log}"\
                    .format(**format_dict)

    result = subprocess.run(outer_command, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode('utf-8').split('\n')[-2]
    return output


def main():
    # Arguments for benchmark.py
    domains = {'miconic', 'pipesworld', 'rovers'}
    problems = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    pgconfigs = ['-p false', '-p true -l fmutex', '-p true -l reachable', '-p true -l both']

    for domain in domains:
        for pgconfig in pgconfigs:
            if pgconfig == pgconfigs[0]:
                log = 'n'
            elif pgconfig == pgconfigs[1]:
                log = 'f'
            elif pgconfig == pgconfigs[2]:
                log = 'r'
            elif pgconfig == pgconfigs[3]:
                log = 'b'

            for problem in problems:
                format_dict = {'domain': domain, 'problem': problem, 'pgconfig': pgconfig,
                               'time': 100, 'memory': 1024, 'log': log}
                output = run_command(format_dict)
                print(output)

                # CPU time out
                #if float(output.split()[-2]) > 95:
                #    break


if __name__ == '__main__':
    main()
