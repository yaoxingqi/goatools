"""Utilities for combining namedtuples."""

__copyright__ = "Copyright (C) 2016, DV Klopfenstein, H Tang. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx

def get_dict_w_id2nts(ids, id2nts, flds, dflt_null=""):
    """Return a new dict of namedtuples by combining "dicts" of namedtuples or objects."""
    assert len(ids) == len(set(ids)), "NOT ALL IDs ARE UNIQUE: {IDs}".format(IDs=ids)
    usr_id_nt = []
    # 1. Instantiate namedtuple object
    ntobj = cx.namedtuple("Nt", " ".join(flds))
    # 2. Fill dict with namedtuple objects for desired ids
    for item_id in ids:
        # 2a. Combine various namedtuples into a single namedtuple
        nts = [id2nt.get(item_id) for id2nt in id2nts]
        vals = _combine_nt_vals(nts, flds, dflt_null)
        usr_id_nt.append((item_id, ntobj._make(vals)))
    return cx.OrderedDict(usr_id_nt)

def get_list_w_id2nts(ids, id2nts, flds, dflt_null=""):
    """Return a new list of namedtuples by combining "dicts" of namedtuples or objects."""
    combined_nt_list = []
    # 1. Instantiate namedtuple object
    ntobj = cx.namedtuple("Nt", " ".join(flds))
    # 2. Fill dict with namedtuple objects for desired ids
    for item_id in ids:
        # 2a. Combine various namedtuples into a single namedtuple
        nts = [id2nt.get(item_id) for id2nt in id2nts]
        vals = _combine_nt_vals(nts, flds, dflt_null)
        combined_nt_list.append(ntobj._make(vals))
    return combined_nt_list

def combine_nt_lists(lists, flds, dflt_null=""):
    """Return a new list of namedtuples by zipping "lists" of namedtuples or objects."""
    combined_nt_list = []
    # Check that all lists are the same length
    lens = [len(lst) for lst in lists]
    assert len(set(lens)) == 1, \
        "LIST LENGTHS MUST BE EQUAL: {Ls}".format(Ls=" ".join(str(l) for l in lens))
    # 1. Instantiate namedtuple object
    ntobj = cx.namedtuple("Nt", " ".join(flds))
    # 2. Loop through zipped list
    for lst0_lstn in zip(*lists):
        # 2a. Combine various namedtuples into a single namedtuple
        combined_nt_list.append(ntobj._make(_combine_nt_vals(lst0_lstn, flds, dflt_null)))
    return combined_nt_list

def wr_py_nts(fout_py, nts, docstring=None, varname="nts"):
    """Save namedtuples into a Python module."""
    import sys
    import datetime
    if nts:
        with open(fout_py, 'w') as prt:
            first_nt = nts[0]
            nt_name = type(first_nt).__name__
            if docstring is not None:
                prt.write('"""{DOCSTRING}"""\n\n'.format(DOCSTRING=docstring))
            prt.write("# Created: {DATE}\n".format(DATE=str(datetime.date.today())))
            prt.write("import collections as cx\n\n")
            prt.write("nt_fields = [\n")
            for fld in first_nt._fields:
                prt.write('    "{F}",\n'.format(F=fld))
            prt.write("]\n\n")
            prt.write('{NtName} = cx.namedtuple("{NtName}", " ".join(nt_fields))\n\n'.format(
                NtName=nt_name))
            prt.write("# {N:,} items\n".format(N=len(nts)))
            prt.write("{VARNAME} = [\n".format(VARNAME=varname))
            for ntup in nts:
                prt.write("    {NT},\n".format(NT=ntup))
            prt.write("]\n")
            sys.stdout.write("  WROTE: {PY}\n".format(PY=fout_py))

# -- Internal methods ----------------------------------------------------------------
def _combine_nt_vals(lst0_lstn, flds, dflt_null):
    """Given a list of lists of nts, return a single namedtuple."""
    vals = []
    for fld in flds:
        fld_seen = False
        for nt_curr in lst0_lstn:
            if hasattr(nt_curr, fld):
                vals.append(getattr(nt_curr, fld))
                fld_seen = True
                break
        if fld_seen is False:
            vals.append(dflt_null) # Default val if GO id or nt val is not present
    return vals

# Copyright (C) 2016, DV Klopfenstein, H Tang. All rights reserved.
