import pefile
from capstone import *
import time
import wget

def checkMagic(file):
    


def disassemblePE(filePath):
    pe = pefile.PE(filePath)

    eop = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    codeSection = pe.get_section_by_rva(eop)
    codeDump = codeSection.get_data()
    codeAddr = pe.OPTIONAL_HEADER.ImageBase + codeSection.VirtualAddress

    md = Cs(CS_ARCH_X86, CS_MODE_64)

    for i in md.disasm(codeDump, codeAddr):
        print("0x%x: \t%s\t%s" %(i.address, i.mnemonic, i.op_str))

def dissasembleELF(filePath):
    #do cool stuff 
    return 0

downloadFile("https://cdn.discordapp.com/attachments/965258412067794964/975688240772304916/a.exe")
print(rofl)