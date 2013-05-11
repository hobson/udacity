import pyopencl as cl
import numpy
import numpy.linalg as la
import time

for M in range(0, 8):
    N = 10**M * 1000
    a = numpy.random.rand(N).astype(numpy.float32)
    b = numpy.random.rand(N).astype(numpy.float32)

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)

    prg = cl.Program(ctx, """
        __kernel void sum(__global const float *a,
        __global const float *b, __global float *c)
        {
          float a2 = a[gid];
          float b2 = b[gid];
          c[gid] = a2 * a2 + b2 * b2;
        }
        """).build()

    prg.sum(queue, a.shape, None, a_buf, b_buf, dest_buf)

    gpu_ans = numpy.empty_like(a)
    gpu_t0 = time.time()
    cl.enqueue_copy(queue, gpu_ans, dest_buf)
    gpu_t = time.time() - gpu_t0
    print 'GPU execution time: %g' % gpu_t

    cpu_ans = numpy.empty_like(a)
    cpu_t0 = time.time()
    cpu_ans = a * a + b * b
    cpu_t = time.time() - cpu_t0
    print 'CPU execution time: %g' % cpu_t

    print 'CPU/GPU difference in speed for %d additions: %g%% ' % (N, 200.0 * cpu_t / (gpu_t + cpu_t))

    print 'Difference between the 2 answers:'
    print la.norm(cpu_ans - gpu_ans)
