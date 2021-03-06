#!/usr/bin/env python

import dendropy
import sys

desc = """
Will root a set of trees using a line-delimited list of taxon names to be included in the outgroup.
Requires dendropy to read and manipulate trees, thus accepts any input treefile readable by dendropy,
though the format must be specified if other than newick.
"""

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print desc
        print "usage: roottrees <treesfile> <outgroupfile> <outfile> [<format=newick|nexus|etc>]"
        sys.exit(0)

    infilepath = sys.argv[1]
    outgroups_filepath = sys.argv[2]
    outfilepath = sys.argv[3]

    ionputformat = "newick"
    for arg in sys.argv[4:]:
        argbits = arg.split("=")
        if len(argbits) > 1:
            if argbits[0] == "format":
                inputformat = argbits[1]

    trees = dendropy.TreeList.get_from_path(infilepath, inputformat)

    outgroupsfile = open(outgroups_filepath,"r")
    outgroup_names = [line.strip() for line in outgroupsfile.readlines()]

    rootedtrees = list()
    for tree in trees:

        outgroup = tree.mrca(taxon_labels=outgroup_names)
        newbrlen = outgroup.edge_length / 2
        tree.reroot_at_edge(outgroup.edge, length1=newbrlen, length2=newbrlen, update_splits=True)

        rootedtrees.append(tree)

    rootedtrees_tlist = dendropy.TreeList(rootedtrees)
    rootedtrees_tlist.write_to_path(outfilepath)
