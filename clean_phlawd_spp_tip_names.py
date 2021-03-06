#!/usr/bin/env python

if __name__ == '__main__':

    import newick3, phylo3, numpy, sys

    if len(sys.argv) < 2:
        print "usage: remove_badtips.py <treefile>"
        sys.exit()

    treefname = sys.argv[1]
    treefile = open(treefname, "r")
    tree = newick3.parse(treefile.readline())

    obs_names = []
    #tips_to_remove = []
    for tip in tree.leaves():

    #    print "checking name " + tip.label

        name_ok = False
        parts = tip.label.split("_")
        genus = parts[1]

        if parts[2] in ["sp", "hybrid", "aff"]:
            print "removing " + tip.label
            tip.prune()
            continue
    
        elif parts[2] == "cf":
            name_ok = True
            sp_epithet = parts[3]

        else:
            name_ok = True
            sp_epithet = parts[2]
    
            if len(parts) > 3:
                add_epithet = "_".join(parts[3:])
            else:
                add_epithet = None

        newname = "_".join([genus,sp_epithet])
        if add_epithet:
            newname += "_" + add_epithet 
    
        if name_ok:
            if newname in obs_names:
                print "removing duplicate of: " + newname
                tip.prune()

                # compress knuckle if there is one
    #            if len(parent.children) == 1:
    #                child = parent.children[0]
    #                if child.label != None:
    #                    rightlabel = child.label
    #                else:
    #                    rightlabel = ", ".join([leaf.label for leaf in child.leaves()])

    #                print "compressing a knuckle in the tree: " + leftlabel + " | " + rightlabel

    #                pp = parent.parent
    #                pp.remove_child(parent)
    #                pp.add_child(child)

            else:
                print newname
                tip.label = newname
                obs_names.append(newname)

    #nodes_to_remove = []
    for n in tree.descendants():

        nc = n
        while (not nc.istip) and len(nc.children) == 0:
            print "pruning an empty tip"
            np = nc.parent
            nc.prune()
            if np:
                nc = np
            else:
                break
        
    #    if not n.istip:
    #        if len(n.children) == 0:
    #            nodes_to_remove.insert(0,n)
    #        else:
    #            empty = True
    #            for c in n.children:
    #                if c not in nodes_to_remove:
    #                    empty = False
    #                    break
    #        if empty:
    #            nodes_to_remove.insert(0,n)

    #print ""
    #for dud in nodes_to_remove:
    #    print "removing an empty tip!"
    #    dud.parent.remove_child(dud)

    outfile = open(treefname.rsplit(".tre",1)[0] + ".renamed.tre","w")
    outfile.write(newick3.tostring(tree) + ";")
    outfile.close()
