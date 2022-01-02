""" This is an interface for testing """
import argparse
import os
import subprocess

WORKING_DIR = os.getcwd()
MODULE_DIR = __file__

def get_parser():
    parser = argparse.ArgumentParser(description='instant coding answers via the command line')
    parser.add_argument('simfilename', metavar='SIMFILENAME', type=str, nargs=1, help='the sim file to execute')
    parser.add_argument('-j', '--jobname', help='job name for slurm (<6 char)', default='job',  action='store')
    parser.add_argument('-N', '--nodes', help='number of nodes', default='2', action='store')
    parser.add_argument('-n', '--cpus', help='number of cpus', default='12', action='store')
    parser.add_argument('-p', '--partition', help='partition name; acqua default - nodes24gb' , default='nodes24gb', action='store')
    return parser

def check_args(args, host):
    assert '.sim' not in args['simfilename'][0] , "Don't include .sim in simfilename"
    assert len(args['jobname'])<7, "The jobname is too long (char<7)"

    # Check host computing configuration
    if host == 'acqua' or 'YW_Desktop':
        args['star_path'] = "/opt/Siemens/15.06.007-R8/STAR-CCM+15.06.007-R8"
        # todo: impment more star version. But no need right now

        assert int(args['nodes'] )<= 5, "Max node: 5"
        if args['partition'] in ['nodes24gb', 'nodes32gb']:
            assert int(args['cpus']) ==12, "nodes24gb/32gb: use 12 cpus"
        elif args['partition'] =='nodes64gb':
            assert int(args['cpus'] )== 16, "nodes64gb: use 16 cpus"
        else:
            raise ValueError("partition for Acqua not in: nodes24gb, nodes32gb, nodes64gb ")
    elif host == 'eofe7':
        raise NotImplementedError("Engaging: to do")
    else:
        raise ValueError("Unknown hostname:%s"%host)

    return args

def read_file(template_file_name):
    filepath = os.path.join(os.path.dirname(__file__), 'file_templates', template_file_name)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def write_file(file_name, content):
    write_to = os.path.join(WORKING_DIR, file_name)
    with open(write_to, 'w', encoding='utf-8') as f:
        f.write(content)
    return

def prepare_java_file(jobname):
    content = read_file('simple_run.java')
    content_m = content.replace('JOBNAME', jobname)
    write_file(file_name='%s.java'%jobname, content=content_m)
    return

def prepare_slurm_file(simfilename, jobname, star_path):
    content = read_file('slurm.slurm')
    content_m = content.replace("SIM_FILE_NAME", simfilename)
    content_m = content_m.replace("JOB_NAME", jobname)
    content_m = content_m.replace("STAR_VERSION", star_path)
    write_file(file_name='%s.slurm' % jobname, content=content_m)
    return

def prepare_shell_file(jobname, n_nodes, n_cpus, partition):
    content = "sbatch --nodes=%s --cpus-per-task=%s -p %s %s.slurm"%(n_nodes, n_cpus, partition, jobname)
    write_file('%s.sh'%jobname, content)
    return

def prepare_files(args):
    simfilename = args['simfilename'][0]
    jobname = args['jobname']
    n_nodes = args['nodes']
    n_cpus = args['cpus']
    partition = args['partition']
    star_path = args['star_path']
    # Prepare files
    prepare_java_file(jobname)
    prepare_slurm_file(simfilename, jobname, star_path)
    prepare_shell_file(jobname, n_nodes, n_cpus, partition)
    return

def check_machine():
    hostname = subprocess.check_output("hostname", encoding='utf-8', shell=True)
    host = hostname.split('.')[0]
    return host

def submit_job(args):
    bash_file = "%s.sh"%args['jobname']
    os.system('chmod 754 "%s"'%bash_file)
    os.system('./%s' % bash_file)


def command_line_runner():  # pylint: disable=too-many-return-statements,too-many-branches
    # Check machine

    # Get Parser
    parser = get_parser()
    args = vars(parser.parse_args()) # get dictionary pairs
    print(args)
    host = check_machine()
    check_args(args, host)
    prepare_files(args)
    submit_job(args)

