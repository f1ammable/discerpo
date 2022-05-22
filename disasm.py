import pefile
from capstone import *
import os
import discord
from pathlib import Path

async def processFile(file, arch, bitmode): # maybe async this, possibly slow
    with open(file, 'rb') as f:
        while(byte := f.read()[:4].hex()):
            magic = ''
            magic += byte.upper()
            match magic:
                case '4D5A9000': return await disassemblePE(file, arch, bitmode)
                case '7F454C46': return await disassembleELF(file)
                case 'CAFEBABE', 'FEEDFACE', 'FEEDFACF', 'CEFAEDFE', 'CFFAEDFE':return await disassembleMacho(file)
                case _: return "Invalid file"

async def disassemblePE(filePath, arch, bitmode):
    fileDir, fileName = os.path.split(filePath)
    print(fileDir)
    pe = pefile.PE(filePath)

    eop = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    codeSection = pe.get_section_by_rva(eop)
    codeDump = codeSection.get_data()
    codeAddr = pe.OPTIONAL_HEADER.ImageBase + codeSection.VirtualAddress

    md = Cs(CS_ARCH_X86, CS_MODE_64)

    dump = ""

    for i in md.disasm(codeDump, codeAddr):
        dump += "0x%x: \t%s\t%s \n" %(i.address, i.mnemonic, i.op_str)
    
    return discord.File(Path(f'{fileName}.txt').absolute())


async def disassembleELF(filePath):
    pass

async def disassembleMacho(filePath):
    pass