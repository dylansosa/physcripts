#!/usr/bin/env python

if __name__ == '__main__':

    import newick3, phylo3, sys

    if len(sys.argv) < 2:
        print "usage: excise_knuckles.py <treefile>"
        sys.exit(0)

    treefname = sys.argv[1]
    treefile = open(treefname, "r")

    logfile = open("excise_knuckles.log","w")

    for line in treefile:

        tree = newick3.parse(line)

        while len(tree.children) < 2:
            # prune knuckles at the root of the tree if necessary
            only_child = tree.children[0]
            only_child.parent = None
            only_child.isroot = True
            tree = only_child
    
        # cannot edit tree while traversing, so just record knuckles as we go
        knuckles = []

        # first find the knuckles
        for parent in tree.iternodes(phylo3.PREORDER):
        
            if parent.istip:
                continue
        
            logfile.write("node '" + (str(parent.label) if parent.label != None else str(parent)) + "' has " + str(len(parent.children)) + " children\n")
        
            if len(parent.children) == 1:
                logfile.write("\tthis node will be pruned\n")
                knuckles.append(parent)

        # now graft them out
        for k in knuckles:
            k.parent.add_child(k.children[0])
            k.parent.remove_child(k)
    
        print newick3.to_string(tree) + ";"
