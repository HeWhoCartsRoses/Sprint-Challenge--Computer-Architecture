class CPU:
    def __init__(self):
        self.ram = [0]*256
        self.reg = [0]*8
        self.reg[7] = 0xff
        self.pc = self.reg[0]
        self.equal = 0
        self.great = 0
        self.less = 0
        self.cmn = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mult,
            0b01000101: self.shove,
            0b01000110: self.pull,
            0b10100111: self.comp,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
        }

    def load(self, stuff):
        """Load a program into memory."""

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
        if self.equal == 1:
            self.jmp(reg)
        return(2, True)

    def jne(self, reg, b):
        if self.equal == 0:
            self.jmp(reg)
        return(2, True)

    def jmp(self, reg):
        self.pc = self.reg[reg]
        return(0, True)

    def comp(self, a, b):
        if a == b:
            self.great = 0
            self.less = 0
            self.equal = 1
        if a < b:
            self.great = 0
            self.less = 1
            self.equal = 0
        if a > b:
            self.great = 1
            self.less = 0
            self.equal = 0
        return(3, True)

    def ldi(self, a, b):
        self.reg[a] = b
        return (3, True)

    def prn(self, a, b):
        print(self.reg[a])
        return (2, True)

    def mult(self, a, b):
        self.reg[a] = self.reg[a]*self.reg[b]
        return (3, True)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def shove(self, a, b):
        self.ram[self.reg[7]-1] = self.reg[a]
        return (2, True)

    def pull(self, a, b):
        self.reg[a] = self.ram[self.reg[7]]
        self.reg[7] += 1
        return(2, True)

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
                print(self.pc)
                print(IR)
                break
