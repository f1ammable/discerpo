import pefile
from capstone import *
import os
import discord
from pathlib import Path

# Custom errors
import errors


__all__ = (
    "processFile",
    "disassemblePE",
    "disassembleELF",
    "disassembleMacho"
)


async def processFile(file):
    with open(file, 'rb') as f:
        while byte := f.read()[:4].hex():
            magic = ''
            magic += byte.upper()
            match magic: # Detect executable type
                case '4D5A9000': return await disassemblePE(file)
                case '7F454C46': return await disassembleELF(file)
                case 'CAFEBABE', 'FEEDFACE', 'FEEDFACF', 'CEFAEDFE', 'CFFAEDFE': return await disassembleMacho(file)
                case _: raise errors.InvalidMagic(magic)
        f.close()


async def disassemblePE(filePath):
    fileDir, fileDump = os.path.split(filePath)
    pe = pefile.PE(filePath)

    match hex(pe.FILE_HEADER.Machine): # Reading architecture from header
        case '0x8664': arch, bitmode = CS_ARCH_X86, CS_MODE_64
        case '0x1c0': arch, bitmode = CS_ARCH_ARM, CS_MODE_LITTLE_ENDIAN
        case '0xaa64': arch, bitmode = CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
        case '0x14c': arch, bitmode = CS_ARCH_X86, CS_MODE_32
        case _: raise errors.InvalidMachinePE(pe.FILE_HEADER.Machine)

    codeSection = pe.get_section_by_rva(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    codeDump = codeSection.get_data()
    codeAddr = pe.OPTIONAL_HEADER.ImageBase + codeSection.VirtualAddress

    asmDump = ""

    for i in Cs(arch, bitmode).disasm(codeDump, codeAddr):
        asmDump += "0x%x: \t%s\t%s \n" % (i.address, i.mnemonic, i.op_str) # Actual disassembly contents

    with open(f'{fileDump}.txt', 'w+') as f:
        f.truncate(0) # Using w+ so we can modify the file in 1 open, therefore we need to clear the file contents first
        f.write(asmDump) 
        f.seek(0) 
        for l in f.readlines(): # Deletes all nops as they take up too much space
            if "nop" not in l:
                f.write(l) 
        f.truncate() # Overwrite the file instead of adding to it
        f.close()

        # On a further note, this should be replaced by an algorithm that checks if 2 instructions are the same, deleting more than 1 occurence

    return discord.File(Path(f'{fileDump}.txt').absolute())


async def disassembleELF(filePath):
    return 'Sorry, ELF disassembly is currently not available'


async def disassembleMacho(filePath):
    return 'Sorry, Mach-O disassembly is currently not available'
