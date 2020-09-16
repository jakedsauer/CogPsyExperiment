def errorCorrection(error): #corrects for close distances near degree 0
    if error >= 180.0:
        error -= 360.0
    elif error <= -180.0:
        error += 360.0
    return error

print(errorCorrection(359-1))
