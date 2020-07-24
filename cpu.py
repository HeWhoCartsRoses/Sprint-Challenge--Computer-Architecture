class CPU:
    def __init__(self):
        self.ram = [0]*256
        self.reg = [0]*8
        self.reg[7] = 0xff
        self.pc = self.reg[0]
        self.fl = 0b00000000
        self.cmn = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100111: self.comp,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
        }

    def load(self, stuff):
        address = 0
        program = []
        f = open(stuff)
        for l in f:
            spl = l.split('#')[0]
            cm = spl.strip()
            if len(cm) > 0:
                program.append(int(cm[:8], 2))
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def hlt(self, a, b):
        return (0, False)

    def jeq(self, reg, b):
        if self.fl == 1:
            return self.jmp(reg)
        else:
            return(2, True)

    def jne(self, reg, b):
        if self.fl != 1:
            return self.jmp(reg)
        else:
            return(2, True)

    def jmp(self, reg):
        self.pc = self.reg[reg]
        return(0, True)

    def comp(self, a, b):
        a = self.reg[a]
        b = self.reg[b]
        if a == b:
            self.fl = 0b00000001
        elif a < b:
            self.fl = 0b00000100
        elif a > b:
            self.fl = 0b00000010
        return(3, True)

    def ldi(self, a, b):
        self.reg[a] = b
        return (3, True)

    def prn(self, a, b):
        print(self.reg[a])
        return (2, True)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, point):
        return self.ram[point]

    def ram_write(self, data, point):
        self.ram[point] = data

    def run(self):
        """Run the CPU."""
        run = True

        while run:
            IR = self.ram[self.pc]

            a = self.ram_read(self.pc + 1)
            b = self.ram_read(self.pc + 2)

            try:
                op = self.cmn[IR](a, b)
                run = op[1]
                self.pc += op[0]
            except:
                break


cpu = CPU()

cpu.load('./sctest.ls8')
cpu.run()
