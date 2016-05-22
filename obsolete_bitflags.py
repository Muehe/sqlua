def unpackBitMask(bitMask):
	bits = []
	numBits=1
	while(pow(2, numBits) < bitMask):
		numBits += 1
	for x in range(-numBits, 1):
		potency = 1 << -x #pow(2, -x)
		if (bitMask >= potency):
			bitMask = bitMask - potency
			#s = "Flag on bit " + str(-x) + " is set (value " + str(potency) +")"
			#print (s)
			bits.insert(0, -x)
	return bits

def checkBit(bit, bitMask):
	set = unpackBitMask(bitMask)
	if bit in set:
		return True
	else:
		return False
