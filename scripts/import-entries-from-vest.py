#!/usr/bin/python

import argparse
from lxml import etree
from pathlib import Path
import subprocess
import os

"""
This script is used for importing entries from the dict-fin-sme-x-vest repository
into the dict-fin-sme repository. It only import entries that do not already exist,
no merging is done.

Run as follows:

python import-entries-from-vest.py <fin-sme-x-vest file> <fin-sme file> <part-of-speech>

The output is written to the sme-fin file. Any uncertain cases are printed
to the terminal and left for the script runner to manually enter into the sme-fin file.
"""

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fin_sme_x_vest", type=Path)
    parser.add_argument("fin_sme", type=Path)
    parser.add_argument("pos", type=str)

    return parser.parse_args()

# def merge_mgs(smenob_mg, smefin_mg, id):
#     try:
#         smefin_tg = smefin_mg.xpath("./tg")[0]
#     except IndexError:
#         print(f"{id} seems to have meaning group without translation. This may be caused by a duplicate entry. Please manually check that the correct translation is chosen.")
#         return
#     smenob_mg.append(smefin_tg)

# def merge_entries(smenob_entry, smefin_entry, smefin_id):
#     # Does smefin entry contain multiple mg's?
#     smefin_mgs = smefin_entry.xpath("./mg")
#     if len(smefin_mgs) > 1:
#         print(f"entry {smefin_id} contains multiple mg's. Please move tg's to the correct mg manually")


#     # Merge
#     first_smenob_mg = smenob_entry.xpath("./mg")[0]
#     for smefin_mg in smefin_mgs:
#         merge_mgs(first_smenob_mg, smefin_mg, smefin_id)

def get_entry_id(entry):
    l = entry.xpath("./lg/l")[0]
    l_id = (l.text, l.get("pos"), l.get("type"))
    return l_id

def no_phrase_translations(entry):
    ts = entry.xpath("./mg/tg/t")
    for t in ts:
        if t.get("t_type") == "phrase":
            return False
    return True

def main(args):
    vest_tree = etree.parse(args.fin_sme_x_vest)

    finsme_tree = etree.parse(args.fin_sme)

    vest_root = vest_tree.getroot()
    finsme_root = finsme_tree.getroot()

    new_entries = []

    # Iterate through smefin entries. Look them up by l in smefin.
    for entry in vest_root.iter("e"):
        l_id = get_entry_id(entry)
        finsme_l_list = finsme_root.xpath(f'.//l[text()="{l_id[0]}"]')
        if len(finsme_l_list) >= 1:
            # Match! This does not need to be imported.
            continue
        else: # len < 1
            # No match! Add new entry to the end of the smefin file
            new_entries.append(entry)

    # for entry in finsme_root.iter("e"):
    #     for mg in entry.xpath("./mg"):
    #         fin_tgs = mg.xpath('./tg[@xml:lang="fin"]')
    #         if len(fin_tgs) == 0:
    #             tg = etree.SubElement(mg, "tg")
    #             tg.set("{http://www.w3.org/XML/1998/namespace}lang", "fin")
    #             t = etree.SubElement(tg, "t")
    #             t.text = "_FIN"                

    # Add entries not existing in smenob to the end of the file
    for entry in new_entries:
        # # Add empty smenob tg
        # for mg in entry.xpath("./mg"):
        #     tg = etree.SubElement(mg, "tg")
        #     tg.set("{http://www.w3.org/XML/1998/namespace}lang", "fin")
        #     t = etree.SubElement(tg, "t")
        #     t.text = "_NOB"
        # Only append if pos matches the specified
        if (args.pos == get_entry_id(entry)[1]):
            finsme_root.append(entry)

    finsme_tree.write(args.fin_sme, pretty_print=True, encoding="utf-8")



if __name__ == "__main__":
    raise SystemExit(main(parse_args()))