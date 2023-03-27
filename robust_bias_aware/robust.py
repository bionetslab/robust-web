import robust
import argparse


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('seeds', type=str, help='specify path to seeds')
    parser.add_argument('outfile', type=str, help='specify path to outfile')
    parser.add_argument('--network', type=str, help='Specify path to graph or identifier of networks shipped with ROBUST: BioGRID, APID, STRING', default='BioGRID')
    parser.add_argument('--namespace', type=str, choices=['ENTREZ', 'GENE_SYMBOL', 'UNIPROT', 'ENSEMBL'], default='GENE_SYMBOL')
    parser.add_argument('--alpha', default=0.25, type=float, help='specify initial fraction, default=0.25')
    parser.add_argument('--beta', default=0.9, type=float, help='specify reduction factor, default=0.9')
    parser.add_argument('--n', default=30, type=int, help='specify no. of steiner trees')
    parser.add_argument('--tau', default=0.1, type=float, help='specify threshold')
    parser.add_argument('--study-bias-scores', type=str, default='BAIT_USAGE', help='specify edge weight function used by ROBUST')
    parser.add_argument('--gamma', type=float, default=1.0, help='hyper-parameter gamma used by bias-aware edge weights.')
    return parser


if __name__ == '__main__':
    args = _get_parser().parse_args()
    if args.study_bias_scores == 'NONE':
        args.study_bias_scores = None
    _, _ = robust.run(args.seeds, args.network, args.namespace, args.alpha, args.beta, args.n, args.tau,
                      args.study_bias_scores, args.gamma, args.outfile)
    