Objective
---------

Over time I'd like to convert many of the [Udacity Parallel Programming class](https://www.udacity.com/course/cs344) exercises and examples from Nvidia's Cuda library implementation to opencl. Even better than that, I may try out pyopencl, if the performance penalty isn't to big for using python to orchestrate the process.

pyopencl_example.py
-------------------

While taking the Udacity parallel computing class I decided to compare performance between CPU (serial) and GPU (parallel) implementation. So I ran a simple kernel, `a * a + b * b`, for an array of 32-bit random floats between 0 and 1 using pyopencl and numpy. I wanted to see if it was worthwhile to take my GPU BTC mining rig offline periodically to do scientific computing. But even my a bottom-of-the-barrel 64-bit AMD Sempron 145 (2.8 GHz, 5600 bogo-MIPS) processor with 8GB DRAM can beat a Radeon 7750 GPU for all but the largest arrays. And the best-possible throughput gain on the GPU is about 4x.

So numpy must be well-optimized and the pyopencl_example must be pretty poorly optimized. I tried optimizing my GPU kernel by minimizing array index lookups, etc, but nothing I came up with made a significant difference for this simple kernel. Both the CPU and GPU gave exactly the same answer, so that's nice.

Here's the output with crude measurements of execution time. The "Difference between the 2 answers" is any discrepancy in the mathematical operations performed on the GPU relative to the CPU. Surprisingly I never saw even the slightest rounding error difference. Either the CPU and GPU use the exact same machine code to perform the multiplications and additions or my comparision is not precise enough itself to catch small errors.


```
GPU execution time: 0.0115399
CPU execution time: 2.7895e-05
CPU/GPU speed ratio for 10^0 kernel executions: 0.241726% 
Difference between the 2 answers:
0.0
GPU execution time: 0.0115771
CPU execution time: 2.19345e-05
CPU/GPU speed ratio for 10^1 kernel executions: 0.189464% 
Difference between the 2 answers:
0.0
GPU execution time: 0.0116088
CPU execution time: 2.19345e-05
CPU/GPU speed ratio for 10^2 kernel executions: 0.188947% 
Difference between the 2 answers:
0.0
GPU execution time: 0.0115681
CPU execution time: 2.59876e-05
CPU/GPU speed ratio for 10^3 kernel executions: 0.22465% 
Difference between the 2 answers:
0.0
GPU execution time: 0.011663
CPU execution time: 7.70092e-05
CPU/GPU speed ratio for 10^4 kernel executions: 0.660289% 
Difference between the 2 answers:
0.0
GPU execution time: 0.023535
CPU execution time: 0.000612974
CPU/GPU speed ratio for 10^5 kernel executions: 2.60452% 
Difference between the 2 answers:
0.0
GPU execution time: 0.0234549
CPU execution time: 0.0182121
CPU/GPU speed ratio for 10^6 kernel executions: 77.6472% 
Difference between the 2 answers:
0.0
GPU execution time: 0.0668991
CPU execution time: 0.240016
CPU/GPU speed ratio for 10^7 kernel executions: 358.773% 
Difference between the 2 answers:
0.0
GPU execution time: 0.567215
CPU execution time: 2.24371
CPU/GPU speed ratio for 10^8 kernel executions: 395.566% 
Difference between the 2 answers:
0.0
```


With cgminer running at -I 9 on all the GPUs, the speed advantage for a GPU doesn't budge significantly.  So pyopencl is effective at interrupting cgminer and prioritizing its threads.



```
GPU execution time: 0.179582
CPU execution time: 2.7895e-05
CPU/GPU speed ratio for 10^0 kernel executions: 0.0155333% 
Difference between the 2 answers:
0.0
GPU execution time: 0.263615
CPU execution time: 2.31266e-05
CPU/GPU speed ratio for 10^1 kernel executions: 0.00877287% 
Difference between the 2 answers:
0.0
GPU execution time: 0.263666
CPU execution time: 2.40803e-05
CPU/GPU speed ratio for 10^2 kernel executions: 0.00913287% 
Difference between the 2 answers:
0.0
GPU execution time: 0.011616
CPU execution time: 2.81334e-05
CPU/GPU speed ratio for 10^3 kernel executions: 0.242195% 
Difference between the 2 answers:
0.0
GPU execution time: 0.0116951
CPU execution time: 7.60555e-05
CPU/GPU speed ratio for 10^4 kernel executions: 0.650317% 
Difference between the 2 answers:
0.0
GPU execution time: 0.023536
CPU execution time: 0.000617981
CPU/GPU speed ratio for 10^5 kernel executions: 2.62569% 
Difference between the 2 answers:
0.0
GPU execution time: 0.0236619
CPU execution time: 0.0189419
CPU/GPU speed ratio for 10^6 kernel executions: 80.0524% 
Difference between the 2 answers:
0.0
GPU execution time: 0.0630081
CPU execution time: 0.230431
CPU/GPU speed ratio for 10^7 kernel executions: 365.717% 
Difference between the 2 answers:
0.0
GPU execution time: 0.82972
CPU execution time: 2.4491
CPU/GPU speed ratio for 10^8 kernel executions: 295.172% 
Difference between the 2 answers:
0.0
```

Installation was a bit tricky. You have to make sure setuptools is overriden by distribute. But Ubuntu 12.04 makes this easy. Thanks to kermit666 on SO for this simple approach to getting virtualenv wrapper and numpy up and running quickly on a fresh Ubuntu install.


#!/usr/bin/env sh
sudo apt-get install python-pip python-dev
sudo pip install virtualenv virtualenvwrapper

echo 'export PROJECT_HOME="$HOME/src"' &gt;&gt; $HOME/.bashrc
echo 'export WORKON_HOME="$HOME/.virtualenvs"' &gt;&gt; $HOME/.bashrc
echo 'source /usr/local/bin/virtualenvwrapper.sh' &gt;&gt; $HOME/.bashrc

sudo apt-get install -y gfortran g++
# sudo apt-get remove -y --purge python-setuptools

# start a new virtalenv project
mkproject parallel
pip install --upgrade distribute
pip install mako numpy pyopencl




