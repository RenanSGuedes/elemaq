from math import pi, pow, log10

# Solução

# Tabela A-18
# HR: Aços laminados a quente
# CD: Aços estirados a frio

# Ver o tipo de aço e para o tratamento apresentado coletar:

# Sut (Resistência a tração) [MPa]
# Sy (Resistência ao escoamento) [MPa]
# Hb (Dureza Brinell) [Adimensional]

sut = int(input('Resistência a tração (MPa): '))
sy = int(input('Resistência ao escoamento (MPa): '))
hb = int(input('Dureza Brinell: (Adimensional) '))

# Analisar o Se' (Resistência a fadiga do corpo de prova)

if sut <= 1400: # MPa
  sel = .5 * sut
  print("Se' (Resistência a fadiga do corpo de prova) <= 200 kpsi (1400 MPa)")
else:
  sel = 700 # MPa
  print("Se' (Resistência a fadiga do corpo de prova) <= 100 kpsi (700 MPa)")

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

r = float(input("Raio do entalhe (mm): "))
d = float(input("Distância entre sulcos na região do entalhe (mm): "))
D = float(input("Distância entre as laterais (onde não há entalhe) (mm): "))

print("r/d = {:.3f}".format(r/d))
print("D/d = {:.3f}".format(D/d))
print("----------------------------")
print("Obtenha kts pela tabela A-15-15!")

kts = float(input("Valor de kts obtido do gráfico: "))
print("---------------------------------------------")

# Obter fator de sensibilidade (Figura 6.21)

print("Obter o valor de qshear para\n r = notch radius {:.2f} mm\n Hb = {}".format(r, hb))

qshear = float(input("Valor de qshear extraído: "))
print("------------------------------------------")

kfs = 1 + qshear * (kts - 1)

print("Portanto kfs = 1 + {:.2f} * ({:.2f} - 1)\n kfs = {:.2f}".format(qshear, kts, kfs))

# Calculo de tau0
torque = float(input("Torque (N * m): "))

tau0 = (16 * kfs * torque)/(pi * (d * .001)**(3))

tau_max = kfs * tau0

print("Tensão de cisalhamento máxima na torção: {:.3f} MPa".format(tau_max/pow(10, 6)))

# Calcular o limite de resistência a fadiga (Se)

# Antes é preciso encontrar os fatores modificadores (ka, kb, kc, kd, ke, kf)

acabamento_superficial = input("[R]etificado, [U]sinado ou laminado a frio, [L]aminado a quente, [F]orjado: ")

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
if d >= (.11 * 25.4) and d <= (2 * 25.4):
  kb = pow((d/25.4)/.3, -.107)
elif d > (2 * 25.4) and d <= (10 * 25.4):
  kb = .91 * pow(d/25.4, -.157)
elif d >= 2.79 and d <= 51:
  kb = pow(d/7.62, -.107)
else:
  kb = 1.51 * pow(d, -.157)

# kc = Tipo de carregamento

load = input("[B]ending, [A]xial ou [T]orsion: ")

if load == "B":
  kc = 1
elif load == "A":
  kc = .85
else:
  kc = .59

print("Fatores modificadores\nka = {:.3f}\nkb = {:.3f}\nkc = {:.3f}".format(ka, kb, kc))

se = ka * kb * kc * sel

print("Se (Limite de resistência a fadiga) = {:.3f} MPa".format(se))

f = float(input("Fator de carregamento (Adimensional): "))

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

