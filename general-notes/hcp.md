# High Performance Computing
Navigating and working on PNNL's High Performance Computing (HPC) clusters can be tricky for beginners, and the How-To articles on confluence make me sad, so here are some of the common HPC tasks I find myself scouring confluence in reference to.

Note: This document is specific to `pic`, but *should* be applicable to PNNL's other HPC clusters as well.

## Tracking and Using Your Allocation
Tracking your allocation usage can be accomplished via the `sbank` module:
```
$ module load sbank
$ sbank balance statement

User             Usage |          Account       Usage | Account Limit   Available (CPU hrs)
---------- ----------- + ---------------- ----------- + ------------- -----------
tim                  0 |            CSSEF     388,946 |     1,250,000     861,054
tim                  0 |              CZT     432,209 |       534,351     102,142
tim                  0 |             HERO   5,904,628 |     5,910,000       5,372
tim          1,409,805 |              OPS   2,644,523 |     2,864,000     219,477
```

To see your default project:
```
$ module load sbank
$ sbank user account
```
For further information, see [Tracking and Using Your Allocation](https://confluence.pnnl.gov/confluence/display/RC/Tracking+and+Using+Your+Allocation)

## Modules
On PNNL's HPC clusters, Modules are software packages and libraries that can be used to develop and execute your software. Some commonly used modules include [git](https://git-scm.com/), [R](https://www.r-project.org/about.html), and [gcc](https://gcc.gnu.org/).

### Useful Module Commands
* **List available modules**: `module avail`
* **Loading Modules**: `module load <module_name>`
* **List currently-loaded modules**: `module list`
* **Remove all loaded modules**: `module purge`


## The SBATCH job script
PNNL HPC clusters use [SLURM](https://slurm.schedmd.com/) `SBATCH` commands to schedule and run jobs. As such, job scripts **must** contain additional lines of `SBATCH` comments that gives SLURM details about the job you wish to execute.

### Required SBATCH Lines
```
#SBATCH -A project_name
#SBATCH -t time_limit
#SBATCH -N number_of_nodes
```
where:
* `project_name` is the name of a valid project (Ex: `"ceds"`)
* `time_limit` is the amount of time to allow the job to run before killing it. It can take one of the following formats:
  * `minutes`
  * `minutes:seconds`
  * `hours:minutes:seconds`
  * `days-hours`
  * `days-hours:minutes`
  
### Recommended SBATCH Lines
```
#SBATCH -n number_of_cores
#SBATCH -J job_name
#SBATCH -o job_output_filename(stdout)
#SBATCH -e job_errors_filename(stderr)
```
where:
* `number_of_cores` specifies the number of cores per node to use. The default is to use all of the cores on each node
* `job_name` is the name of your `sbatch` script file
* `job_output_filename` is the file where output from your job is written. Default is `slurm-%j.out`, where `%j` is the slurm job ID
* `job_error_filename` is the file where errors raised by your job are written. It follows the same naming convention as `job_output_filename`

### Submitting a Job
A job can be submitted to the node queue on the cluster by using the `sbatch` command:
```
sbatch submission_script
```
where `submission_script` is the name of the `SBATCH` job script you wish to run.

### Checking Job Progress
Since the HPC cluster is a shared resource, you'll want to check the progress of your job on the cluster. This can be accomplished via the `squeue` command:
```
$ squeue
JOBID PARTITION     NAME     USER  ST       TIME  NODES NODELIST(REASON)
  237     slurm sbatch.t      tim   R       0:06      8 node[0439-0443,0445-0447]
  236     slurm sbatch.t      tim   R       0:17      1 node0205
  235     slurm sbatch.t      tim   R       0:29     10 node[0233-0242]
```

The use of the `-l` flag yields more information:
```
$ squeue -l
Sun Oct  9 18:51:26 2011
  JOBID PARTITION     NAME     USER    STATE       TIME TIMELIMIT  NODES NODELIST(REASON)
    237     slurm sbatch.t      tim  RUNNING       0:34   2:00:00      8 node[0439-0443,0445-0447]
    236     slurm sbatch.t      tim  RUNNING       0:45   2:00:00      1 node0205
    235     slurm sbatch.t      tim  RUNNING       0:57   2:00:00     10 node[0233-0242]
```

Other useful `squeue` flags include:
* `-u <username>` restricts output to my jobs (replace `<username>` with your username)
* `-p <node>` restricts output to jobs located on `<node>`
* `sprio` shows how your priority compares to others if your job is on hold
* `–A <allocation_name>` shows how many jobs are running under the allocation specified by `<allocation_name>`

**Example**: If I'm only running one job and want to check its progess, I'll use the following command:
```
squeue -u <my_username> 
```
or 
```
squeue -u <my_username> -p shared
```
if I know that my job is running on the `shared` node

### Cancelling a job
Your job can be cancelled and its execution stopped with the following command:
```
scancel job_id
```

## Running Interactive Jobs
Interactive jobs open a new command prompt via [X11 forwarding](https://www.ssh.com/manuals/client-user/61/client-tunnel-x11.html). Unlike simply running a job through a PuTTY, launching an interactive job moves execution off the login node. 

The first step is to download and install [PuTTY](https://www.putty.org/) and [Xming](https://sourceforge.net/projects/xming/)

### Configuring PuTTY
In order to successfully launch an interavtive job, you must configure PuTTY to launch an interactive session via Xming.
See [Launching Interavtive Jobs](https://confluence.pnnl.gov/confluence/display/RC/Launching+Interactive+Jobs) for instructions bc I'm lazy.

### Launching Interactive Jobs
Interactive jobs are launched via the `isub` command:
```
isub -A <your_account> -W <minutes> -N <num_nodes> -s <shell>
```
where:
* `<your_account>` is the project account relevant to the job (same as the `#SBATCH -A` line in a batch job)
* `<minutes>` is the length of time to allow the interavtive job to run, in minutes
* `<num_nodes>` is the number of nodes to use (= processor core count / 24). Default is 2
* `<shell>` is the shell to use. Default is your current shell

**Example**: To run a 30 minute interactive job in csh on 2 nodes under the project `constancetest`:
```
isub -A constancetest -W 30 -N 2 -s csh
```
