"""
Vapor...
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile


@small_task
def vapor_task(read1: LatchFile, read2: LatchFile, read3: LatchFile) -> LatchFile:

    # A reference to our output.
    sam_file = Path("vapor_result.out").resolve()

    _vapor1_cmd = [
        "vapor",
        "bed", #How to specify the input format? bed or vcf?
        "--sv-input",
        read1.local_path,
        "--output-path",
        str(sam_file),     #str(Path(reads).resolve()), ... should I use the Path object?
        "--reference",
        read2.local_path,    
        "--pacbio-input",
        read3.local_path,
    ]

    subprocess.run(_vapor1_cmd)

    return LatchFile(str(sam_file), "latch:///vapor_result.sam")


# @small_task
# def sort_bam_task(sam: LatchFile) -> LatchFile:

#     bam_file = Path("covid_sorted.bam").resolve()

#     _samtools_sort_cmd = [
#         "samtools",
#         "sort",
#         "-o",
#         str(bam_file),
#         "-O",
#         "bam",
#         sam.local_path,
#     ]

#     subprocess.run(_samtools_sort_cmd)

#     return LatchFile(str(bam_file), "latch:///covid_sorted.bam")


@workflow
def vapor(read1: LatchFile, read2: LatchFile, read3) -> LatchFile:
    """Description...

    markdown header
    ----

    Write some documentation about your workflow in
    markdown here:

    > Regular markdown constructs work as expected.

    # Heading

    * content1
    * content2

    __metadata__:
        display_name: Assemble and Sort FastQ Files
        author:
            name:
            email:
            github:
        repository:
        license:
            id: MIT

    Args:

        read1:
          sv_input

          __metadata__:
            display_name: Read1

        read2:
          reference genome that pacbio files are aligned against

          __metadata__:
            display_name: Read2

        read3:
            PacBio read file to be assembled.
    """
    return vapor_task(read1=read1, read2=read2, read3=read3)
