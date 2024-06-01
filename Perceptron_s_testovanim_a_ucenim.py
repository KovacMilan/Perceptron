import tkinter,random

canvas = tkinter.Canvas( bg = "white",
                         height = 510,
                         width = 830 )
canvas.pack()




##inicializácia váh a prahu
vahy = [[0 for j in range(20)] for i in range(20)]       
prah = 0  
##



##vizualizácia v grafockej ploche
vizualizacia_vahy = [
                    [
                    canvas.create_rectangle(i*20+420,j*20+30,(i+1)*20+420,(j+1)*20+30,
                    fill = f"#{3*hex(120+vahy[i][j]*15)[2:]}")
                    for j in range(20)
                    ]
                   for i in range(20)
                   ]
vizualizacia_vstup = [
                        [canvas.create_rectangle(i*20+10,j*20+30,(i+1)*20+10,(j+1)*20+30)
                        for j in range(20)
                        ]
                        for i in range(20)
                      ]
oznacenie_pola_vstupu = canvas.create_text(210,15, text = "Vstup", font = "Arial 15")
oznacenie_pola_vah = canvas.create_text(620,15, text = "Váhy", font = "Arial 15")
vystup = canvas.create_text(310,448,text = "", font =  "Arial 15")
chybovost = canvas.create_text(310,485, text = "", font = "Arial 10")
##



def nahodny_obdlznik():
    stred = [random.randrange(3,18),random.randrange(2,19)]
    sirka = random.randrange(6,min((19-stred[0]),stred[0]-1)*2+3)
    vyska = random.randrange(4,min((19-stred[1]),stred[1]-1)*2+3)
    return  [
                [
                    1 if stred[0] - int(sirka/2) <= j < stred[0] + int(sirka/2) and
                    stred[1] - int(vyska/2) <= i < stred[1] + int(vyska/2)
                    else 0 for j in range(20)
                ]
                for i in range(20)
            ]


def nahodny_kruh():
    stred = [random.randrange(2,18),random.randrange(2,18)]
    polomer = random.randrange(2,min(19-stred[0],19-stred[1],stred[0],stred[1])+1)
    return  [
                [
                    1 if (stred[1]-j)**2+(stred[0]-i)**2 <= polomer**2
                    else 0 for j in range(20)
                ]
                for i in range(20)
            ]


##vstupy budú útvary z tohto zoznamu:
utvary = [[nahodny_kruh(),"JE KRUH"] if random.randint(0,1)==1
          else [nahodny_obdlznik(),"NIE JE KRUH"] for i in range(40)]
##



def potencial_neuronu(vstup):
    return sum([vstup[i][j]*vahy[i][j] for i in range(20) for j in range(20)])



def aktivacna_funkcia(vstup):
    return "JE KRUH" if potencial_neuronu(vstup) > prah else "NIE JE KRUH"



def uprav_vahy(vstup):
    global vahy

    if aktivacna_funkcia(vstup) == "JE KRUH":
        for i in range(20):
            for j in range(20):
                vahy[i][j] = vahy[i][j] - vstup[i][j]
    else:
        for i in range(20):
            for j in range(20):
                vahy[i][j] = vahy[i][j] + vstup[i][j]



def posud_dalsi():
    global utvary
    utvary.insert(0,utvary.pop())
    canvas.itemconfig(vystup,text = aktivacna_funkcia(utvary[0][0]), font =  "Arial 15")
    for i in range(20):
        for j in range(20):
            if utvary[0][0][i][j] == 0:
                canvas.itemconfig(vizualizacia_vstup[i][j], fill = "white")
            else:
                canvas.itemconfig(vizualizacia_vstup[i][j], fill = "grey7")
    


def spatna_v_nespravne(vstupny_utvar = utvary[0][0]):
    uprav_vahy(vstupny_utvar)
    for i in range(20):
        for j in range(20):
            canvas.itemconfig(vizualizacia_vahy[i][j],
                              fill = f"#{3*hex(120+vahy[i][j]*15)[2:]}")

def uc_sa(pocet = 1):
    for i in range(pocet):
        for j in utvary:
            if aktivacna_funkcia(j[0]) == j[1]:
                pass
            else:
                spatna_v_nespravne(j[0])

def testuj():
    count = 0
    for i in utvary:
        if aktivacna_funkcia(i[0])==i[1]:
            pass
        else:
            count += 1
    canvas.itemconfig(chybovost, text = f"Nesprávne posúdených: {(count/40)*100}%")

##tlačidlá
b_nespravne = tkinter.Button(canvas,text = "Nesprávne", command = spatna_v_nespravne)
b_nespravne.place(x = 80, y = 475)
b_posud_dalsi = tkinter.Button(canvas, text = "Posúď ďalší", command = posud_dalsi)
b_posud_dalsi.place(x = 80, y = 435)
b_testuj = tkinter.Button(canvas,text = "Testuj", command = testuj)
b_testuj.place(x = 10, y = 435)
b_uc_sa = tkinter. Button(canvas, text = "Uč sa 1", command = uc_sa)
b_uc_sa.place(x = 10, y = 475)
##
