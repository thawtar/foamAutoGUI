"""
We have a 5-bit number to represent our solver: 00000
1st bit: steady or transient (Dec: 16)
2nd bit: incompressible or compressible (Dec: 8)
3rd bit: single phase or multiphase (Dec: 4)
4th bit: energy off or energy on (Dec: 2)
5th bit: turbulence off or turbulence on (Dec: 1)

Steady, incompressible, no energy, single phase = 00000 or 00001 (simpleFoam)
Steady, incompressible, energy, single phase = 00100 or 00101 (buoyantBoussinesqSimpleFoam)
Steady, incompressible, no energy, multiphase = 00010 or 00011 (interLTSFoam)
Steady, compressible, energy, single phase = 01100 or 01101 (rhoSimpleFoam)
Transient, incompressible, no energy, single phase = 10000 or 10001 (pimpleFoam)
Transient, incompressible, energy, single phase = 10100 or 10101 (buoyantBoussinesqPimpleFoam)
Transient, incompressible, no energy, multiphase = 10010 or 10011 (interFoam)
Transient, compressible, energy, single phase = 11100 or 11101 (rhoPimpleFoam)
"""

simpleFoam = int('0b00000',2)
buoyantBoussinesqSimpleFoam = int('0b00100',2)
interLTSFoam = int('0b00010',2)
rhoSimpleFoam = int('0b01100',2)
rhoPimpleFoam = int('0b11100',2)
pimpleFoam = int('0b10000',2)
buoyantBoussinesqPimpleFoam = int('0b10100',2)
interFoam = int('0b10010',2)

# turbulent versions of the above solvers
turbSimpleFoam = int('0b00001',2)
turbbBuoyantBoussinesqSimpleFoam = int('0b00101',2)
turbInterLTSFoam = int('0b00011',2)
turbRhoSimpleFoam = int('0b01101',2)
turbRhoPimpleFoam = int('0b11101',2)
turbPimpleFoam = int('0b10001',2)
turbBuoyantBoussinesqPimpleFoam = int('0b10101',2)
turbInterFoam = int('0b10011',2)


solvers ={simpleFoam:"simpleFoam",turbSimpleFoam:"simpleFoam",buoyantBoussinesqSimpleFoam:"buoyantBoussinesqSimpleFoam",
          turbbBuoyantBoussinesqSimpleFoam:"buoyantBoussinesqSimpleFoam",buoyantBoussinesqPimpleFoam:"buoyantBoussinesqPimpleFoam",
          turbBuoyantBoussinesqPimpleFoam:"buoyantBoussinesqPimpleFoam",turbInterLTSFoam:"interLTSFoam",interLTSFoam:"interLTSFoam",
          pimpleFoam:"pimpleFoam",turbPimpleFoam:"pimpleFoam",interFoam:"interFoam",turbInterFoam:"interFoam",
          rhoSimpleFoam:"rhoSimpleFoam",turbRhoSimpleFoam:"rhoSimpleFoam",rhoPimpleFoam:"rhoPimpleFoam",
          turbRhoPimpleFoam:"turbRhoPimpleFoam"}

transient = 0       # 0 means steady. if 1, transient
compressible = 0    # 0 means incompressible. If 1, compressible
energy = 0          # 0 means no energy equation. If 1, energy is considered
multiphase = 0      # 0 means single phase. If 1, multiphase is considered
turbulence = 0      # 0 means laminar. If 1, turbulence modeling used

def computeSolverKey(transient=0,compressible=0,energy=0,multiphase=0,turbulence=0):
    if(transient):
        transient = 16
    if(compressible):
        compressible = 8
    if(energy):
        energy = 4
    if(multiphase):
        multiphase = 2
    if(turbulence):
        turbulence = 1 # is it even necessary?
    solverKey = transient|compressible|energy|multiphase|turbulence
    return solverKey

def test():
    transient = 0  # 0 means steady. if 1, transient
    compressible = 0  # 0 means incompressible. If 1, compressible
    energy = 0  # 0 means no energy equation. If 1, energy is considered
    multiphase = 0  # 0 means single phase. If 1, multiphase is considered
    turbulence = 0  # 0 means laminar. If 1, turbulence modeling used

    trans = input("Transient?[Y/n]")
    comp = input("Compressible?[Y/n]")
    en = input("Energy equation?[Y/n]")
    mphase=input("Multiphase?[Y/n]")
    turb = input("Turbulence modeling?[Y/n]")
    if(trans=="Y"):
        transient = 1
    if(comp=="Y"):
        compressible=1
        energy = 1 # compressible flows need energy term on. This will overwrite the energy on input
    if(en=="Y"):
        energy = 1
    if(mphase=="Y"):
        multiphase=1
    if(turb=="Y"):
        turbulence=1
    solverKey = computeSolverKey(transient,compressible,energy,multiphase,turbulence)
    print(solverKey)
    if(solverKey not in solvers.keys()):
        print("Error... No solver found. Exiting...")
        exit(-1)
    print("Solver: ",solvers[solverKey])

while(1):
    test()