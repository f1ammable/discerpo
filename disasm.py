import pefile
from capstone import *

def checkMagic(file): # maybe async this, possibly slow
    with open(file, 'rb') as f:
        while(byte := f.read()[:4].hex()):
            magic = ''
            magic += byte.upper()
            match magic:
                case '4D5A9000':
                    disassemblePE(file)
                case '7F454C46':
                    disassembleELF(file)
                case 'CAFEBABE': # Might remove this since Java class files also have this magic
                    disassembleMacho(file) # I don't like Mach-O :(
                case 'FEEDFACE':
                    disassembleMacho(file)
                case 'FEEDFACF':
                    disassembleMacho(file)
                case 'CEFAEDFE':
                    disassembleMacho(file)
                case 'CFFAEDFE':
                    disassembleMacho(file)
                case _:
                    return 'Invalid'

def disassemblePE(filePath):
    pe = pefile.PE(filePath)

    eop = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    codeSection = pe.get_section_by_rva(eop)
    codeDump = codeSection.get_data()
    codeAddr = pe.OPTIONAL_HEADER.ImageBase + codeSection.VirtualAddress

    md = Cs(CS_ARCH_X86, CS_MODE_64)

    for i in md.disasm(codeDump, codeAddr):
        print("0x%x: \t%s\t%s" %(i.address, i.mnemonic, i.op_str))

def disassembleELF(filePath):
    pass

def disassembleMacho(filePath):
    pass

print(checkMagic("files\pe"))