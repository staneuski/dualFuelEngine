# Difference between parameters

# Difference between Phi
# Cell data
phiCell_0 = inputs[0].CellData['Phi']
phiCell_1 = inputs[1].CellData['Phi']
output.CellData.append(phiCell_1 - phiCell_0, '∆Phi')
# Point data
phiPoint_0 = inputs[0].PointData['Phi']
phiPoint_1 = inputs[1].PointData['Phi']
output.PointData.append(phiPoint_1 - phiPoint_0, '∆Phi')

# Difference between p
# Cell data
pCell_0 = inputs[0].CellData['p']
pCell_1 = inputs[1].CellData['p']
output.CellData.append(pCell_1 - pCell_0, '∆p')
# Point data
pPoint_0 = inputs[0].PointData['p']
pPoint_1 = inputs[1].PointData['p']
output.PointData.append(pPoint_1 - pPoint_0, '∆p')

# Difference between U
# Cell data
UCell_0 = inputs[0].CellData['U']
UCell_1 = inputs[1].CellData['U']
output.CellData.append(UCell_1 - UCell_0, '∆U')
# Point data
UPoint_0 = inputs[0].PointData['U']
UPoint_1 = inputs[1].PointData['U']
output.PointData.append(UPoint_1 - UPoint_0, '∆U')

