n = 81990486158830819987073862172415164961593278461441199000999472465202518599850332550812125141470698747706547832071653895197966292731285323989845213159146261837803561813706450672725878328449137240949801181034766354744732582372151328001276074276010039350214840101550595192803830418941509645225250637084951191901
e = 3
c = 29567745406946076830146052374930033424211480116321544674448562777091588294881623860014915348606939136520110465290092616212926800744828796888106944346222024613999754846412634549763305673101149427233979469362411909357450400895307369148973536710380608978693814012874175410588472106640257194122351943446376090522
mbar = 10209587263099434303402268295264783241039304732220412954880929680985232124926643894842588590120872193397691703623680
PR.<x> = PolynomialRing(Zmod(n))
xbar = x +  mbar
f = (xbar ^ e - c)
x_sol = f.monic().small_roots(X=2**192, beta=1)[0]
print(x_sol)
# b'BUAACTF{Y0u_Know_c0ppersmit_s0_w3ll!!@#$#%~!@!}\x01'
# b'BUAACTF{Y0u_Know_c0ppersmit_s0_w3ll!!@#$#%~!@!}'