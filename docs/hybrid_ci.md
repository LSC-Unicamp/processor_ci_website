# Hybrid CI

Hardware verification checks the processor in isolation, while software CI projects such as [KernelCI](https://kernelci.org) assume the hardware underneath is already stable. Between the two there is an intermediate zone: defects that only appear when a complete operating system runs on the core, such as subtle MMU faults, interrupt controller problems, or cache coherence bugs. A core can pass every compliance test and still fail to boot Linux.

Hybrid CI is our answer to that gap. It extends the Processor CI into a single continuous integration loop in which an evolving soft-core and an evolving software stack are exercised against one another on real hardware at every commit. We call this approach *hybrid HW/SW CI*.

![The hybrid HW/SW CI loop](assets/ci_loop.svg)

## Two principles

The loop is built on two ideas that set it apart from the usual FPGA prototyping flow.

The first one is **bidirectional co-evolution**. Software is usually treated as a fixed regression suite run against evolving hardware, so only the hardware is under development. Here both sides are first-class: test results inform the hardware flow, and changes to the hardware trigger a new validation of the software that targets it.

The second one is **real hardware as a persistent CI runner**. Instead of placing a design on a board, checking it, and removing it, the FPGA-hosted soft-core stays online between builds and behaves like any other runner in a software CI system, always available to receive deployments and return results.

## From commit to Linux boot

A commit to a core starts the hardware flow. The [LiteX](https://github.com/enjoy-digital/litex) SoC generator builds the complete system from a YAML description, covering the core, memory, interconnect, and peripherals. Vivado then synthesizes the design on a dedicated build node, which takes between 5 and 25 minutes and also yields the physical metrics of the design: LUT and flip-flop usage, power estimate, and maximum frequency.

The handoff between the two flows is the most delicate step. Every build shifts the memory map, so the software has to follow it. The pipeline automates this: LiteX exports the map of the Control and Status Registers as JSON and CSV, a script reconstructs the hardware topology into a Device Tree source, and the compiled `.dtb` is injected into the OpenSBI build to produce a custom `fw_jump.bin`. The kernel never boots against a stale description, which removes the traditional kernel panics caused by outdated static descriptions.

With the bitstream programmed over JTAG, the board becomes an active runner. The LiteX BIOS loads OpenSBI, the Linux kernel, and the root filesystem over TFTP and NFS, so no SD card is ever flashed by hand. Once the kernel reaches userspace, the KernelCI tooling takes control, monitors the serial console to validate the boot smoke test, and starts the regression suites.

## What we run on the core

The software side uses an unmodified mainline Linux kernel, without board-specific patches, and a minimal userspace generated with Buildroot. Validation runs 117 KUnit test suites, covering core data structures, cryptographic algorithms, file systems, and low-level kernel APIs, alongside targeted `kselftest` modules for CPU hotplugging, FPU state, and memory footprint. Serial logs are parsed into JSON and published to the same KernelCI dashboards that upstream kernel maintainers already use.

## Current results

We evaluated six RISC-V cores on three boards from the farm: the Digilent Arty A7-100T, the Digilent Nexys 4 DDR, and the OpenSource SDR Lab Kintex-7. VexIIRiscv, CVA6, NaxRiscv, and Rocket booted mainline Linux and passed the full suite, with Rocket also evaluated in dual-core and quad-core configurations. BlackParrot and OpenC906 did not reach the OS-level phase, the first one because of a synthesis and integration error in LiteX and the second one because of an exception during the OpenSBI handoff.

The clearest demonstration of the methodology came from the quad-core Rocket. It passed every suite in the single-core and dual-core configurations, but consistently crashed during the `printk-ringbuffer` KUnit test, which stresses concurrent memory access across threads. We verified that the bitstream met all timing constraints and that the interconnect wrappers were identical to the stable dual-core baseline, which points to an edge case in the cache coherence protocol or the memory consistency model. This is a defect that neither single-core RTL simulation nor standard compliance tests can see, and it only surfaces under a multicore OS-level workload.

## Next steps

Processor CI already supports the synthesis and RTL simulation of more than 100 RISC-V cores, and the next goal is to bring that scale to OS-level validation. We also plan to pair the expanded matrix with larger FPGA platforms, such as the Xilinx VC709, to reach more complex multicore topologies, and to integrate formal RISC-V architectural compliance suites into the loop.

## Paper

The methodology, the infrastructure, and the full evaluation are described in detail in:

- [Automated OS-Level Verification for RISC-V Softcores: Bridging FPGA and Linux KernelCI](assets/RSP2026_CI.pdf) — Julio N. Avelar, Marcio Godoi, Ana L. P. Costa, Rodolfo Azevedo, and Sandro Rigo. To appear in the [37th International Workshop on Rapid System Prototyping (RSP 2026)](https://conferences.imt-atlantique.fr/rsp-symposium/), part of Embedded Systems Week, Barcelona, Spain, October 2026.
