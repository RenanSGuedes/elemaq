from math import pi, pow, log10

'''
Uma barra sólida redonda, com 25 mm de diâmetro, tem um
sulco de profundidade 2.5 mm com um raio de 2.5 mm usinado 
nela. A barra é feita de aço AISI 1018 CD (estirado a frio) 
e sujeita a um torque puramente reverso de 200 N * m. Para a
curva deste material, considere f = 0,9.
'''

# Solução

# Tabela A-18
# HR: Aços laminados a quente
# CD: Aços estirados a frio

# Ver o tipo de aço e para o tratamento apresentado coletar:

# Sut (Resistência a tração) [MPa]
# Sy (Resistência ao escoamento) [MPa]
# Hb (Dureza Brinell) [Adimensional]

print("Tabela A-20, pg.1040")
sut = int(input('Resistência a tração (MPa): '))
sy = int(input('Resistência ao escoamento (MPa): '))
hb = int(input('Dureza Brinell: (Adimensional) '))

# Analisar o Se' (Resistência a fadiga do corpo de prova)

if sut <= 1400: # MPa
  sel = .5 * sut
  print("Se' (Resistência a fadiga do corpo de prova) <= 200 kpsi (1400 MPa)")
  print("-------------------------------------------------------------------")
else:
  sel = 700 # MPa
  print("Se' (Resistência a fadiga do corpo de prova) > 200 kpsi (1400 MPa)")
  print("-------------------------------------------------------------------")

# Calcular a tensão de cisalhamento máxima na torção
# tau_max = kfs * tau0 

# tau_max: Tensão de cisalhamento máxima
# kfs: Fator de concentração de tensão à torção
# tau0: tensão de cisalhamento nominal

# Quando houver torção:
# tau_max = (16 * kfs * torque)/(pi * d**(3))

# Cálculo do kfs

# kfs = 1 + qshear * (kts - 1)
# kts: Fator de concentração de tensão de um eixo com entalhe de anel
# qshear: Fator de sensibilidade

# Calcular o kts antes:

# É preciso obter as razões r/d e D/d

r = float(input("Raio do entalhe (r, em mm): "))
d = float(input("Diâmetro na região do entalhe (d, em mm): "))
D = float(input("Diâmetro da barra (onde não há entalhe) (D, em mm): "))
print("---------------------------------------------------------------")

print("r/d = {:.3f}".format(r/d))
print("D/d = {:.3f}".format(D/d))
print("----------------------------")
print("Obtenha kts pela tabela A-15 pg.1026 (ver geometria da peça)")

kts = float(input("Valor de kts: "))
print("---------------------------------------------------------------")

# Obter fator de sensibilidade (Figura 6.21)

print("Obter o valor de qshear para\nr = notch radius {:.2f} mm\nHb = {} (Ver figura 6-21 pg.296)".format(r, hb))

qshear = float(input("Valor de qshear: "))
print("------------------------------------------")

kfs = 1 + qshear * (kts - 1)

print("Portanto kfs = 1 + {:.2f} * ({:.2f} - 1)\nkfs = {:.2f}".format(qshear, kts, kfs))
print("------------------------------------------")

# Calculo de tau0
torque = float(input("Torque (N * m): "))

print("------------------------------------------")

tau0 = (16 * torque)/(pi * (d * .001)**(3))

tau_max = kfs * tau0

print("Tensão de cisalhamento máxima na torção: {:.3f} MPa".format(tau_max/pow(10, 6)))
print("------------------------------------------")
print("Acabamento superficial:")
# Calcular o limite de resistência a fadiga (Se)

# Antes é preciso encontrar os fatores modificadores (ka, kb, kc, kd, ke, kf)

acabamento_superficial = input("[R]etificado, [U]sinado ou laminado a frio, [L]aminado a quente, [F]orjado: ")
print("------------------------------------------")

if acabamento_superficial == "R":
  a = 1.58
  b = -.085
elif acabamento_superficial == "U":
  a = 4.51
  b = -.265
elif acabamento_superficial == "L":
  a = 57.7
  b = -.718
else:
  a = 272
  b = -.995

# ka = Acabamento Superficial
ka = a * pow(sut, b)

# kb = Fator de tamanho
if d >= 2.79 and d <= 51:
  kb = pow(d/7.62, -.107)
else:
  kb = 1.51 * pow(d, -.157)

# kc = Tipo de carregamento

print("Carregamento")
load = input("[B]ending, [A]xial ou [T]orsion: ")
print("------------------------------------------")

if load == "B":
  kc = 1
elif load == "A":
  kc = .85
else:
  kc = .59

print("Fatores modificadores\nka = {:.3f}\nkb = {:.3f}\nkc = {:.3f}".format(ka, kb, kc))

se = ka * kb * kc * sel

print("-> Se (Limite de resistência a fadiga) = {:.3f} MPa".format(se))
print("------------------------------------------")

f = float(input("Fator de carregamento (f, adimensional): "))

if load == "T":
  ssu = .67 * sut
  a1 = pow(f * ssu, 2)/se
  b1 = -(1/3) * log10(f * ssu/se)
else:
  a1 = pow(f * sut, 2)/se
  b1 = -(1/3) * log10(f * sut/se)

# Calcular o número de ciclos
print("a = {:.2f}".format(a1))
print("b = {:.2f}".format(b1))

n = ((tau_max/1000000)/a1)**(1/b1)

print("A peça resistirá por volta de {} ciclos.".format(int(n)))
print("------------------------------------------")

# Nova temperatura

kdVsTemperature = {
  "20": 1, 
  "50": 1.01, 
  "100": 1.02,
  "150": 1.025,
  "200": 1.020,
  "250": 1,
  "300": .975,
  "350": .943,
  "400": .9,
  "450": .843,
  "500": .708,
  "550": .672,
  "600": .549
}

newTemperature = input("Nova temperatura: ")
print("------------------------------------------")

kd = kdVsTemperature[newTemperature]

se_new = ka * kb * kc * kd * sel

if load == "T":
  ssu = .67 * sut
  a1 = pow(f * ssu, 2)/se_new
  b1 = -(1/3) * log10(f * ssu/se_new)
else:
  a1 = pow(f * sut, 2)/se_new
  b1 = -(1/3) * log10(f * sut/se_new)

# Calcular o número de ciclos
print("a = {:.2f}".format(a1))
print("b = {:.2f}".format(b1))
print("------------------------------------------")

n = ((tau_max/1000000)/a1)**(1/b1)

print("A {}°C a peça resistirá por volta de {} ciclos.".format(newTemperature, int(n)))
print("------------------------------------------")