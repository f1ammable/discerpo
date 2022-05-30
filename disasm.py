import pefile
from capstone import *
import os
import discord
from pathlib import Path

async def processFile(file, arch, bitmode):
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
        case _: return "Invalid disasm mode"
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

    asmDump = ""

    for i in Cs(arch, bitmode).disasm(codeDump, codeAddr):
        asmDump += "0x%x: \t%s\t%s \n" %(i.address, i.mnemonic, i.op_str)
    
    with open(f'{fileDump}.txt', 'w') as f:
        f.write(asmDump)
        f.close()
    
    # Remove all nop instructions within the output as this is just adding extra space which is uneeded - currently incomplete
    # After this is done, the output should be paginated and then the PE disassembly process is finished
    #
    # with open(f'{fileDump}.txt', 'r+') as f: 
    #     lines = f.readlines()
    #     for l in range(0, lines):
    #         if "nop" in lines[l]:
    #             lines[l] = ""
    #             f.writelines(lines)
    #     f.close()

    return discord.File(Path(f'{fileDump}.txt').absolute())


async def disassembleELF(filePath):
    pass

async def disassembleMacho(filePath):
    pass