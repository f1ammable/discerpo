import pefile
from capstone import *
import os
import discord
from pathlib import Path

async def processFile(file, arch, bitmode): # maybe async this, possibly slow
    match arch.lower():
        case "x86": arch = CS_ARCH_X86
        case "arm": arch = CS_ARCH_ARM
        case "arm64": arch = CS_ARCH_ARM64
        case _: return "Invalid architecture"
    match bitmode.lower():
        case "16": bitmode = CS_MODE_16
        case "32": bitmode = CS_MODE_32
        case "64": bitmode = CS_MODE_64
        case "l_endian": bitmode = CS_MODE_LITTLE_ENDIAN
        case "b_endian": bitmode = CS_MODE_BIG_ENDIAN
        case "arm": bitmode = CS_MODE_ARM
    with open(file, 'rb') as f:
        while(byte := f.read()[:4].hex()):
            magic = ''
            magic += byte.upper()
            match magic:
                case '4D5A9000': return await disassemblePE(file, arch, bitmode)
                case '7F454C46': return await disassembleELF(file)
                case 'CAFEBABE', 'FEEDFACE', 'FEEDFACF', 'CEFAEDFE', 'CFFAEDFE':return await disassembleMacho(file)
                case _: return "Invalid file"
        f.close()

async def disassemblePE(filePath, arch, bitmode):
    fileDir, fileDump = os.path.split(filePath)
    pe = pefile.PE(filePath)

    eop = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    codeSection = pe.get_section_by_rva(eop)
    codeDump = codeSection.get_data()
    codeAddr = pe.OPTIONAL_HEADER.ImageBase + codeSection.VirtualAddress

    dump = ""

    for i in Cs(arch, bitmode).disasm(codeDump, codeAddr):
        dump += "0x%x: \t%s\t%s \n" %(i.address, i.mnemonic, i.op_str)
    
    with open(f'{fileDump}.txt', 'w') as f:
        f.write(dump)
        f.close()

    return discord.File(Path(f'{fileDump}.txt').absolute())


async def disassembleELF(filePath):
    pass

async def disassembleMacho(filePath):
    pass