'''
TACO: Transcriptome meta-assembly from RNA-Seq
Copyright (C) 2012-2015 Matthew Iyer

@author: mkiyer
@author: yniknafs
'''
import collections
import logging
import os

__author__ = "Matthew Iyer and Yashar Niknafs"
__copyright__ = "Copyright 2015"
__credits__ = ["Matthew Iyer", "Yashar Niknafs"]
__license__ = "GPL"
__version__ = "0.4.0"
__maintainer__ = "Yashar Niknafs"
__email__ = "yniknafs@umich.edu"
__status__ = "Development"


class TacoError(Exception):
    pass

Exon = collections.namedtuple('Exon', ['start', 'end'])


class Strand:
    POS = 0
    NEG = 1
    NA = 2

    STRANDS = [POS, NEG, NA]
    NAMES = ['pos', 'neg', 'none']
    FROM_GTF = {'+': POS, '-': NEG, '.': NA}
    TO_GTF = {POS: '+', NEG: '-', NA: '.'}

    @staticmethod
    def to_str(s):
        return Strand.NAMES[s]

    @staticmethod
    def from_gtf(s):
        return Strand.FROM_GTF[s]

    @staticmethod
    def to_gtf(s):
        return Strand.TO_GTF[s]



class Sample(object):
    REF_ID = 'R'

    def __init__(self, gtf_file, _id):
        self.gtf_file = gtf_file
        self._id = _id

    @staticmethod
    def parse_tsv(filename, header=False, sep='\t'):
        cur_sample_id = 1
        gtf_files = set()
        ids = set()
        samples = []
        with open(filename) as f:
            if header:
                f.next()
            # table rows
            for line in f:
                fields = line.strip().split(sep)
                gtf_file = fields[0]
                if gtf_file in gtf_files:
                    m = "GTF file '%s' is not unique" % gtf_file
                    raise TacoError(m)
                if not Sample.gtf_valid(gtf_file):
                    m = "GTF file '%s' is not valid" % gtf_file
                    raise TacoError(m)
                if len(fields) > 1:
                    _id = fields[1]
                    if _id in ids:
                        m = "sample_id '%s' is not unique" % _id
                        raise TacoError(m)
                else:
                    _id = cur_sample_id
                    cur_sample_id += 1
                samples.append(Sample(gtf_file, _id))
        return samples

    @staticmethod
    def write_tsv(samples, filename, header=True, sep='\t'):
        with open(filename, 'w') as f:
            if header:
                print >>f, sep.join(['gtf', 'sample_id'])
            for s in samples:
                print >>f, sep.join([s.gtf_file, str(s._id)])

    @staticmethod
    def gtf_valid(gtf_file):
        if gtf_file is None:
            logging.error('GTF file %s is None' % (gtf_file))
            return False
        if not os.path.exists(gtf_file):
            logging.error('GTF file %s not found' % (gtf_file))
            return False
        return True


class Results(object):
    TMP_DIR = 'tmp'
    STATUS_FILE = 'status.json'
    ARGS_FILE = 'args.pickle'
    SAMPLE_FILE = 'samples.txt'
    TRANSFRAGS_GTF_FILE = 'transfrags.gtf'
    TRANSFRAGS_FILTERED_GTF_FILE = 'transfrags.filtered.gtf'
    AGGREGATE_STATS_FILE = 'aggregate_stats.txt'
    LOCUS_INDEX_FILE = 'loci.txt'
    SPLICE_GRAPH_GTF_FILE = 'splice_graph.gtf'
    BEDGRAPH_FILES = ['expr.pos.bedgraph', 'expr.neg.bedgraph',
                      'expr.none.bedgraph']
    SPLICE_BED_FILE = 'splice_junctions.bed'
    PATH_GRAPH_STATS_FILE = 'path_graph_stats.txt'
    ASSEMBLY_GTF_FILE = 'assembly.gtf'
    ASSEMBLY_BED_FILE = 'assembly.bed'

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.tmp_dir = os.path.join(output_dir, Results.TMP_DIR)
        self.args_file = os.path.join(output_dir, Results.ARGS_FILE)
        self.status_file = os.path.join(output_dir, Results.STATUS_FILE)
        self.sample_file = os.path.join(output_dir, Results.SAMPLE_FILE)
        self.aggregate_stats_file = \
            os.path.join(output_dir, Results.AGGREGATE_STATS_FILE)
        self.locus_index_file = \
            os.path.join(output_dir, Results.LOCUS_INDEX_FILE)
        self.transfrags_gtf_file = \
            os.path.join(output_dir, Results.TRANSFRAGS_GTF_FILE)
        self.transfrags_filtered_gtf_file = \
            os.path.join(output_dir, Results.TRANSFRAGS_FILTERED_GTF_FILE)
        self.splice_graph_gtf_file = \
            os.path.join(output_dir, Results.SPLICE_GRAPH_GTF_FILE)
        self.bedgraph_files = [os.path.join(output_dir, x)
                               for x in Results.BEDGRAPH_FILES]
        self.splice_bed_file = \
            os.path.join(output_dir, Results.SPLICE_BED_FILE)
        self.path_graph_stats_file = \
            os.path.join(output_dir, Results.PATH_GRAPH_STATS_FILE)
        self.assembly_gtf_file = \
            os.path.join(output_dir, Results.ASSEMBLY_GTF_FILE)
        self.assembly_bed_file = \
            os.path.join(output_dir, Results.ASSEMBLY_BED_FILE)
