# methods to parse and understand the data from the ttrace file from junos device
import re
import glob
import os

class ttrace_parser():
    """Parses a ttrace file and gives out a detailed story of the packet
       The init method sets the following variables:
       - dirpath: current working directory.
       - ttrace: all data in the ttrace file.
       - fpc, pfe: fpc and pfe values of the current packet.
       - mypfe: current pfedest value = fpc*4 + pfe
       - results: file handle to write into the result file.
    """

    def __init__(self, filepath):
        self.filename = os.path.basename(filepath)
        self.dirpath = os.path.dirname(os.path.abspath(filepath))
        self.file_handle = open(self.filename, 'r')
        self.ttrace = self.file_handle.read()
        self.file_handle.seek(0)
        self.fpc, self.pfe = re.findall(".*fpc-(\d+).pfe-(\d+).*", self.filename)[0]
        outfilename = self.filename.replace("trace", "result")
        self.mypfe = int(self.fpc) * 4 + int(self.pfe)
        self.resultfile = open(outfilename, 'w')
        self.resultfile.write("Results of ttrace parser on file %s\n"
                              "= = = = = = = = = = =\n\n"
                              % self.filename)
        # Starts the parsing process on the ttrace
        self.start_proc()

    def start_proc(self):
        """
        Starts the process of parsing the ttrace checking
        whether the inbound packet is ingress or egress
        If ingress it calls an ingress proc method.
        If an egress it calls an egress proc method.
        """
        regex1 = "handle_wan"
        regex2 = "handle_fabric"
        ingress = re.search(regex1, self.ttrace)
        egress = re.search(regex2, self.ttrace)
        if ingress is not None:
            self.resultfile.write("Ingress packet on\nFPC %s -- PFE %s\n"
                                  "- - - - - - - - -"
                                  % (self.fpc, self.pfe))
            self.ingress_proc()
        elif egress is not None:
            self.resultfile.write("Egress packet found in the ttrace")
            self.egress_proc() # yet to implement
        else:
            pass

    def ingress_proc(self):
        """Parsing related to ingress packet is done here."""
        self.get_pkt_info()
        self.resultfile.write("\nIngress Interfaces:")
        iif_info = re.findall(".*SetIIFNH.*iif=(\d+).(\S+).*", self.ttrace)
        for iid, iif in iif_info:
            if iif.split(".")[1] == "32770":
                self.resultfile.write("\n Cascade Interface {} "
                                "Interface ID {}".format(iif, iid))
            else:
                self.resultfile.write("\n Extended Interface {} "
                                "Interface ID {}".format(iif, iid))
        family = re.search(".*SetIIFNH[(](\S+)[)].*\n", self.ttrace).group(1)
        if family == "bridge":
            m = re.search(".*BridgeIFF.*\n", self.ttrace)
            self.file_handle.seek(m.end())
            family_info = self.file_handle.readline()
            self.resultfile.write("\n\nThe Packet is of family bridge.")
            self.resultfile.write("\nbridge info:\n {}\n".format(family_info[2:-2]))
        self.dmac_lkup()


    def get_pkt_info(self):
        # Method to print info about the packet.
        pass

    def dmac_lkup(self):
        """
        Dmac lookup method. If dmac miss is encountered
        dmac miss proc is called else dmac hit proc is called.
        """
        miss = re.search("dmac_miss", self.ttrace)
        hit = re.search("dmac_hit", self.ttrace)
        if miss is not None:
            self.resultfile.write("\n :: Dmac Lookup failed :: \n")
            self.dmacmissproc()
        self.ttrace_lkup()

    def dmacmissproc(self):
        """Gives the path of the packet when a dmac miss happens"""
        search_list = ["SetMcast",
                       "SetNH-Token",
                       "entry_fab_out",
                       "entry_wan_out",
                       "drop_out ",  # drop out reasons!
                       "SetOIFNH",
                       "send_pkt_terminate_if_all_done_2"]
        self.outpfe = []
        line = self.file_handle.readline()
        try:
            while line:
                for rx in search_list:
                    if rx in line:
                        if rx == search_list[0]:
                            self.resultfile.write("\n Multicast token {}".format(re.findall("token.=.(\d+)",
                                                         self.file_handle.readline())[0]))
                        elif rx == search_list[1]:
                            if "SetNH-Token-only" in line:
                                self.resultfile.write("\n NH-Token only set with token {}".format(re.findall("token:(\S+)",
                                                               self.file_handle.readline())[0].split("(")[0]))
                            else:
                                for pfedest, vc, token in re.findall(
                                        "pfeDest:(\d+),\s+VC\s+memberId:(\d+),\s+token:(\S+)\)",
                                        self.file_handle.readline()):
                                    if self.mypfe != int(pfedest) and \
                                                    int(pfedest) not in self.outpfe:
                                        self.outpfe.append(int(pfedest))
                                    self.resultfile.write("\n NH-Token set on \n  pfeDest: {} "
                                                       "with VC memberID: {} and token: {}".
                                                       format(pfedest, vc, token))
                        elif rx == search_list[2]:
                            self.resultfile.write("\n\n- fab out packet -")
                            pass
                        elif rx == search_list[3]:
                            self.resultfile.write("\n\n- wan out packet -")
                            pass
                        elif rx == search_list[5]:
                            iid, iname = re.findall(".*SetOIFNH.*oif=(\d*)..(\S+)\w", line)[0]
                            self.resultfile.write("\n OIF set on \n  Interface id: {} " \
                                               "\n  Interface name: {}".format(iid, iname))
                        elif rx == search_list[6]:
                            self.print_packet()
                line = self.file_handle.readline()
        except EOFError:
            self.resultfile.write("End of File")

    def print_packet(self):
        """Print packet sent out from the output interfaces."""
        self.file_handle.readline()
        self.file_handle.readline()
        buffer = ""
        line = self.file_handle.readline()
        while "Prev_PC" not in line:
            buffer += line
            line = self.file_handle.readline()
        self.resultfile.write("\nPacket sent out:\n\n{}\n".format(buffer))

    def ttrace_lkup(self):
        """Picks up the ttrace file on the outgoing PFE dest."""
        for pfedest in self.outpfe:
            fpc = pfedest / 4
            pfe = pfedest % 4
            files = glob.glob("trace_fpc-{}_pfe-{}*.txt".format(fpc, pfe))
            print files


# Call the ttrace parser class with the ttrace file name.
prsr = ttrace_parser("/Users/Shabhishek/trace.txt")