#!/usr/bin/env python3
"""
HERRAMIENTA ESPECIALIZADA - VIGUETAS, VIGAS y RIOSTRAS (NSR-10 / ACI 318, SI).
Genera: Herramienta-Diseno-Estructural.xlsx
Hojas: Instrucciones | Materiales | Viguetas | Vigas | Riostras
Filosofia: el usuario SOLO mete f'c, fy, geometria y los MOMENTOS/FUERZAS (celdas amarillas).
Calcula y VERIFICA: flexion (As, No. barras, ductilidad, separacion), cortante (estribos),
torsion, deflexiones, longitudes de desarrollo, despiece y -en vigas- diseno por capacidad.
Semaforo CUMPLE / NO CUMPLE. Unidades: MPa, mm, kN, kN*m, mm2.
"""
import math
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule

NAVY="1A237E"; GRIS="37474F"; CLARO="ECEFF1"
AZUL_IN="BBDEFB"; AMA_IN="FFF59D"; VERDE="C8E6C9"; ROJO="FFCDD2"; AMAR="FFF9C4"
thin=Side(style="thin",color="BBBBBB"); BORDER=Border(left=thin,right=thin,top=thin,bottom=thin)
CENTER=Alignment(horizontal="center",vertical="center",wrap_text=True)
LEFT=Alignment(horizontal="left",vertical="center",wrap_text=True)

def titulo(ws,a,t,span,color=NAVY):
    ws.merge_cells(f"{a}:{span}"); c=ws[a]; c.value=t
    c.font=Font(bold=True,size=13,color="FFFFFF"); c.fill=PatternFill("solid",fgColor=color); c.alignment=CENTER
def seccion(ws,row,txt,color=GRIS,span=4):
    ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=span)
    c=ws.cell(row=row,column=1,value=txt); c.font=Font(bold=True,color="FFFFFF")
    c.fill=PatternFill("solid",fgColor=color); c.alignment=LEFT
def inp(ws,row,label,val,unit="",nota="",dato=AZUL_IN,fmt=None):
    ws.cell(row=row,column=1,value=label).alignment=LEFT
    c=ws.cell(row=row,column=2,value=val); c.alignment=CENTER; c.fill=PatternFill("solid",fgColor=dato)
    if fmt: c.number_format=fmt
    ws.cell(row=row,column=3,value=unit).alignment=CENTER
    ws.cell(row=row,column=4,value=nota).alignment=LEFT
    for j in range(1,5): ws.cell(row=row,column=j).border=BORDER
def out(ws,row,label,formula,unit="",fmt="0.00",bold=False,hl=None):
    ws.cell(row=row,column=1,value=label).alignment=LEFT
    c=ws.cell(row=row,column=2,value=formula); c.alignment=CENTER; c.number_format=fmt
    if bold: c.font=Font(bold=True)
    if hl: c.fill=PatternFill("solid",fgColor=hl)
    ws.cell(row=row,column=3,value=unit).alignment=CENTER
    for j in range(1,5): ws.cell(row=row,column=j).border=BORDER
def nota(ws,row,txt):
    ws.cell(row=row,column=1,value=txt).font=Font(italic=True,size=9)
def anchos(ws):
    ws.column_dimensions["A"].width=44; ws.column_dimensions["B"].width=16
    ws.column_dimensions["C"].width=10; ws.column_dimensions["D"].width=48
def semaforo(ws,rng):
    for tok in ['"CUMPLE"','"DESPRECIABLE"','"NO CALCULAR"','"OK"']:
        ws.conditional_formatting.add(rng,CellIsRule(operator="equal",formula=[tok],fill=PatternFill("solid",fgColor=VERDE)))
    for tok in ['"NO CUMPLE"','"REVISAR"','"DISENAR"','"CALCULAR"']:
        ws.conditional_formatting.add(rng,CellIsRule(operator="equal",formula=[tok],fill=PatternFill("solid",fgColor=ROJO)))

# ---------- INSTRUCCIONES ----------
def hoja_instrucciones(wb):
    ws=wb.active; ws.title="Instrucciones"; anchos(ws)
    titulo(ws,"A1","COMO USAR ESTA HERRAMIENTA (Viguetas, Vigas, Riostras)","D1")
    pasos=[("1","Ve a la hoja del elemento: Viguetas, Vigas o Riostras."),
        ("2","Llena las celdas AZULES (materiales y geometria): f'c, fy, b, h, recubrimiento, diametros."),
        ("3","Llena las celdas AMARILLAS con los MOMENTOS y FUERZAS de tu modelo (Mu+, Mu-, Vu, Tu)."),
        ("4","La hoja calcula As, No. de barras, separacion, estribos, torsion, deflexion, desarrollo y despiece."),
        ("5","Columna de CHEQUEOS: verde = CUMPLE, rojo = NO CUMPLE / REVISAR."),
        ("6","Si algo sale rojo: aumenta seccion (h o b), f'c o el acero, hasta que quede verde.")]
    r=3
    for n,t in pasos:
        ws.cell(row=r,column=1,value=n).font=Font(bold=True); ws.cell(row=r,column=1).alignment=CENTER
        ws.merge_cells(start_row=r,start_column=2,end_row=r,end_column=4)
        ws.cell(row=r,column=2,value=t).alignment=LEFT
        for j in range(1,5): ws.cell(row=r,column=j).border=BORDER
        r+=1
    seccion(ws,r+1,"LEYENDA DE COLORES")
    leg=[("Celda AZUL","Dato de entrada: materiales y geometria",AZUL_IN),
         ("Celda AMARILLA","Dato de entrada: MOMENTOS y FUERZAS (de tu modelo SAP/ETABS)",AMA_IN),
         ("Verde","El chequeo CUMPLE",VERDE),("Rojo","El chequeo NO CUMPLE / revisar",ROJO)]
    rr=r+2
    for a,b,col in leg:
        c=ws.cell(row=rr,column=1,value=a); c.fill=PatternFill("solid",fgColor=col); c.border=BORDER; c.alignment=CENTER
        ws.merge_cells(start_row=rr,start_column=2,end_row=rr,end_column=4)
        ws.cell(row=rr,column=2,value=b).alignment=LEFT; ws.cell(row=rr,column=2).border=BORDER
        rr+=1
    nota(ws,rr+1,"Especializada en viguetas, vigas y riostras. Base: NSR-10 (Titulos B, A, C) / ACI 318. Unidades SI.")

# ---------- MATERIALES ----------
def hoja_materiales(wb):
    ws=wb.create_sheet("Materiales"); anchos(ws)
    titulo(ws,"A1","TABLA DE BARRAS DE REFUERZO (referencia)","D1")
    for j,t in enumerate(["Barra No.","db (mm)","Area (mm2)","Uso tipico"],1):
        c=ws.cell(row=2,column=j,value=t); c.font=Font(bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor=GRIS); c.alignment=CENTER; c.border=BORDER
    barras=[("No.2",6.4,32,"Estribos de viguetas"),("No.3",9.5,71,"Estribos / refuerzo menor"),
            ("No.4",12.7,129,"Refuerzo longitudinal"),("No.5",15.9,199,"Refuerzo longitudinal"),
            ("No.6",19.1,284,"Vigas"),("No.7",22.2,387,"Vigas"),("No.8",25.4,510,"Vigas / columnas")]
    r=3
    for n,d,a,u in barras:
        for j,v in enumerate([n,d,a,u],1):
            c=ws.cell(row=r,column=j,value=v); c.border=BORDER; c.alignment=CENTER if j<4 else LEFT
        r+=1
    nota(ws,r+1,"Areas nominales. En las hojas el area se calcula como pi/4*db^2 a partir del diametro elegido.")

# ---------- bloque comun ----------
def bloque_comun(ws, T_section=False, vigueta=False):
    seccion(ws,3,"DATOS DE ENTRADA  (azul = materiales/geometria, amarillo = fuerzas)")
    inp(ws,4,"f'c",21,"MPa"); inp(ws,5,"fy (longitudinal)",420,"MPa"); inp(ws,6,"fyt (transversal)",420,"MPa")
    inp(ws,7,"b / bw (ancho)",100 if vigueta else 300,"mm")
    inp(ws,8,"h (altura total)",400 if vigueta else 500,"mm")
    inp(ws,9,"recubrimiento libre cc",25 if vigueta else 40,"mm")
    inp(ws,10,"db estribo",6.4 if vigueta else 9.5,"mm","No.2=6.4 / No.3=9.5")
    inp(ws,11,"db barra longitudinal",15.9,"mm","No.4=12.7 / No.5=15.9 / No.6=19.1")
    if T_section:
        inp(ws,12,"hf (espesor loseta)",50,"mm"); inp(ws,13,"bf (ancho efectivo ala)",850,"mm","min(L/4, bw+16hf, sep nervios)")
    else:
        inp(ws,12,"hf (no aplica)",0,"mm","0 = rectangular"); inp(ws,13,"bf (= b)","=B7","mm")
    inp(ws,14,"L (luz libre)",5000,"mm")
    inp(ws,15,"Factor apoyo",18.5,"-","16 simple / 18.5 un extr. / 21 ambos / 8 voladizo")
    inp(ws,16,"Mu+  (momento positivo)",25 if vigueta else 120,"kN*m","<-- DATO de tu modelo",dato=AMA_IN)
    inp(ws,17,"Mu-  (momento negativo)",30 if vigueta else 150,"kN*m","<-- DATO de tu modelo",dato=AMA_IN)
    inp(ws,18,"Vu  (cortante)",35 if vigueta else 140,"kN","<-- DATO de tu modelo",dato=AMA_IN)
    inp(ws,19,"Tu  (torsion)",0.3 if vigueta else 12,"kN*m","<-- DATO de tu modelo",dato=AMA_IN)
    inp(ws,20,"phi flexion",0.9,"-"); inp(ws,21,"phi cortante/torsion",0.75,"-")
    seccion(ws,23,"GEOMETRIA Y MATERIALES CALCULADOS")
    out(ws,24,"d (efectiva) = h-cc-db_estr-db_long/2","=B8-B9-B10-B11/2","mm","0.0")
    out(ws,25,"Area 1 barra long = pi/4*db^2","=PI()/4*B11^2","mm2","0")
    out(ws,26,"Av estribo (2 ramas)","=2*PI()/4*B10^2","mm2","0")
    out(ws,27,"beta1","=IF(B4<=28,0.85,MAX(0.65,0.85-0.05*(B4-28)/7))","-","0.000")
    out(ws,28,"As minimo = max(1.4/fy ; 0.25raizf'c/fy)*b*d","=MAX(1.4/B5,0.25*SQRT(B4)/B5)*B7*B24","mm2","0")
    out(ws,29,"rho maximo (ductil et=0.005)","=0.85*B27*B4/B5*(3/8)","-","0.00000")

def flexion(ws, r0, Mcell, ancho_cell, label):
    seccion(ws,r0,f"FLEXION {label}")
    out(ws,r0+1,"Rn = Mu/(phi*ancho*d^2)",f"={Mcell}*10^6/(B20*{ancho_cell}*B24^2)","MPa","0.000")
    out(ws,r0+2,"rho",f"=(0.85*B4/B5)*(1-SQRT(1-2*B{r0+1}/(0.85*B4)))","-","0.00000")
    out(ws,r0+3,"As requerido",f"=B{r0+2}*{ancho_cell}*B24","mm2","0")
    out(ws,r0+4,"As ADOPTADO = max(req, As_min)",f"=MAX(B{r0+3},B28)","mm2","0",bold=True,hl=VERDE)
    out(ws,r0+5,"a (profundidad bloque)",f"=B{r0+4}*B5/(0.85*B4*{ancho_cell})","mm","0.0")
    out(ws,r0+6,"Chequeo ductilidad (rho<=rho_max)",f'=IF(B{r0+2}<=B29,"CUMPLE","NO CUMPLE")',"","General",bold=True)
    out(ws,r0+7,"No. de barras",f"=ROUNDUP(B{r0+4}/B25,0)","barras","0",bold=True,hl=AMAR)
    out(ws,r0+8,"As provisto",f"=B{r0+7}*B25","mm2","0")
    out(ws,r0+9,"Chequeo acero (As_prov>=As_adopt)",f'=IF(B{r0+8}>=B{r0+4},"CUMPLE","NO CUMPLE")',"","General",bold=True)
    return r0+9

# ---------- VIGUETAS ----------
def hoja_viguetas(wb):
    ws=wb.create_sheet("Viguetas"); anchos(ws)
    titulo(ws,"A1","DISENO DE VIGUETA (seccion T) - NSR-10","D1")
    bloque_comun(ws, T_section=True, vigueta=True)
    flexion(ws,31,"B16","B13","POSITIVA (+)  abajo -> ancho bf (ala)")
    flexion(ws,42,"B17","B7","NEGATIVA (-)  arriba -> ancho bw")
    seccion(ws,53,"CORTANTE (viguetas: NSR-10 C.8.13 permite 1.1*Vc)")
    out(ws,54,"Vc = 0.17*raizf'c*bw*d","=0.17*SQRT(B4)*B7*B24/1000","kN","0.00")
    out(ws,55,"1.1*Vc","=1.1*B54","kN","0.00")
    out(ws,56,"phi*1.1Vc","=B21*B55","kN","0.00")
    out(ws,57,"Vs requerido = Vu/phi - 1.1Vc","=MAX(B18/B21-B55,0)","kN","0.00")
    out(ws,58,"s requerido = Av*fyt*d/Vs","=IF(B57<=0,9999,B26*B6*B24/(B57*1000))","mm","0")
    out(ws,59,"s maximo = min(d/2,600)","=MIN(B24/2,600)","mm","0")
    out(ws,60,"s ADOPTADO","=IF(B18<=B56,B59,MIN(B58,B59))","mm","0",bold=True,hl=AMAR)
    out(ws,61,"RESULTADO","=IF(B18<=B56,\"Concreto resiste: estribos de montaje @ \"&B59&\" mm\",\"Estribos #2 @ \"&ROUND(B60,0)&\" mm\")","","General")
    out(ws,62,"phi*Vn con s adoptado","=B21*(B55+B26*B6*B24/B60/1000)","kN","0.00")
    out(ws,63,"Chequeo cortante (Vu<=phiVn)",'=IF(B18<=B62,"CUMPLE","NO CUMPLE")',"","General",bold=True)
    seccion(ws,65,"TORSION (umbral)")
    out(ws,66,"Acp=bw*h","=B7*B8","mm2","0"); out(ws,67,"pcp=2(bw+h)","=2*(B7+B8)","mm","0")
    out(ws,68,"phi*Tth = phi*0.083raizf'c*Acp^2/pcp","=B21*0.083*SQRT(B4)*(B66^2/B67)/10^6","kN*m","0.000")
    out(ws,69,"Chequeo torsion",'=IF(B19<B68,"DESPRECIABLE","DISENAR")',"","General",bold=True)
    seccion(ws,71,"DEFLEXIONES (C.9.5)")
    out(ws,72,"h minimo = L/factor","=B14/B15","mm","0")
    out(ws,73,"Chequeo deflexion",'=IF(B8>=B72,"NO CALCULAR","CALCULAR")',"","General",bold=True)
    seccion(ws,75,"LONGITUDES DE DESARROLLO (barras <=No.6)")
    out(ws,76,"ld inferior = (fy/(2.1raizf'c))*db","=(B5/(2.1*SQRT(B4)))*B11","mm","0")
    out(ws,77,"ld superior (psi_t=1.3)","=1.3*B76","mm","0")
    out(ws,78,"gancho ldh","=MAX(0.24*B5/SQRT(B4)*B11,8*B11,150)","mm","0")
    seccion(ws,80,"SEPARACION DE BARRAS Y DESPIECE")
    out(ws,81,"sep libre inferior","=IF(B38>1,(B7-2*B9-2*B10-B38*B11)/(B38-1),9999)","mm","0")
    out(ws,82,"Chequeo separacion (>=max(25,db))",'=IF(B38<=1,"CUMPLE",IF(B81>=MAX(25,B11),"CUMPLE","REVISAR"))',"","General",bold=True)
    out(ws,83,"Baston negativo: long. desde cara = Ln/4 + ld_sup","=B14/4+B77","mm","0")
    out(ws,84,"Barras (+) corren toda la luz + ld en apoyo","=B14+B76","mm","0")
    out(ws,85,"Estribos: zona confinamiento desde cara (2h)","=2*B8","mm","0")
    nota(ws,86,"En la zona de confinamiento coloca los estribos a s/2; en el resto a la s adoptada. As+ usa bf; As- usa bw (a<=hf).")
    semaforo(ws,"B31:B88")

# ---------- VIGAS ----------
def hoja_vigas(wb):
    ws=wb.create_sheet("Vigas"); anchos(ws)
    titulo(ws,"A1","DISENO DE VIGA rectangular - flexion, cortante, torsion y capacidad - NSR-10","D1")
    bloque_comun(ws, T_section=False, vigueta=False)
    inp(ws,22,"Sistema (DMI/DMO/DES)","DES","-","DES o DMO activan diseno por capacidad",dato=AZUL_IN)
    flexion(ws,31,"B16","B7","POSITIVA (+)  centro de luz")
    flexion(ws,42,"B17","B7","NEGATIVA (-)  apoyos")
    seccion(ws,53,"CORTANTE")
    out(ws,54,"Vc = 0.17*raizf'c*b*d","=0.17*SQRT(B4)*B7*B24/1000","kN","0.00")
    out(ws,55,"phi*Vc","=B21*B54","kN","0.00")
    out(ws,56,"phi*Vc/2","=B21*B54/2","kN","0.00")
    out(ws,57,"Vs requerido = Vu/phi - Vc","=MAX(B18/B21-B54,0)","kN","0.00")
    out(ws,58,"Limite 0.33raizf'c*b*d","=0.33*SQRT(B4)*B7*B24/1000","kN","0.00")
    out(ws,59,"s max (segun Vs)","=IF(B57<=B58,MIN(B24/2,600),MIN(B24/4,300))","mm","0")
    out(ws,60,"s por resistencia = Av*fyt*d/Vs","=IF(B57<=0,9999,B26*B6*B24/(B57*1000))","mm","0")
    out(ws,61,"s por minimo (Av,min)","=B26*B6/MAX(0.062*SQRT(B4)*B7,0.35*B7)","mm","0")
    out(ws,62,"s ADOPTADO","=IF(B18<=B56,B59,MIN(B59,B60,B61))","mm","0",bold=True,hl=AMAR)
    out(ws,63,"RESULTADO","=IF(B18<=B56,\"No requiere estribos por resistencia\",\"Estribos @ \"&ROUND(B62,0)&\" mm\")","","General")
    out(ws,64,"phi*Vn con s adoptado","=B21*(B54+B26*B6*B24/B62/1000)","kN","0.00")
    out(ws,65,"Chequeo cortante (Vu<=phiVn)",'=IF(B18<=B64,"CUMPLE","NO CUMPLE")',"","General",bold=True)
    seccion(ws,67,"DISENO POR CAPACIDAD (DMO/DES)")
    out(ws,68,"a+ (bloque)","=B35*B5/(0.85*B4*B7)","mm","0.0")
    out(ws,69,"Mpr+ = 1.25*As+*fy*(d-a/2)","=1.25*B35*B5*(B24-0.5*B68)/10^6","kN*m","0.0")
    out(ws,70,"a- (bloque)","=B46*B5/(0.85*B4*B7)","mm","0.0")
    out(ws,71,"Mpr- = 1.25*As-*fy*(d-a/2)","=1.25*B46*B5*(B24-0.5*B70)/10^6","kN*m","0.0")
    out(ws,72,"Ve (cortante por capacidad) = (Mpr++Mpr-)/ln + Vu","=(B69+B71)/(B14/1000)+B18","kN","0.0")
    out(ws,73,"Cortante de diseno (DMO/DES)","=IF(OR(B22=\"DES\",B22=\"DMO\"),MAX(B18,B72),B18)","kN","0.0",bold=True,hl=AMAR)
    out(ws,74,"Chequeo capacidad (Vdiseno<=phiVn)",'=IF(B73<=B64,"CUMPLE","NO CUMPLE")',"","General",bold=True)
    seccion(ws,76,"TORSION")
    out(ws,77,"Acp=b*h","=B7*B8","mm2","0"); out(ws,78,"pcp=2(b+h)","=2*(B7+B8)","mm","0")
    out(ws,79,"phi*Tth (umbral)","=B21*0.083*SQRT(B4)*(B77^2/B78)/10^6","kN*m","0.000")
    out(ws,80,"Aoh=(b-2cc)(h-2cc)","=(B7-2*B9)*(B8-2*B9)","mm2","0")
    out(ws,81,"ph=2((b-2cc)+(h-2cc))","=2*((B7-2*B9)+(B8-2*B9))","mm","0")
    out(ws,82,"Ao=0.85*Aoh","=0.85*B80","mm2","0")
    out(ws,83,"At/s (1 rama)=Tu/(phi*2*Ao*fyt)","=IF(B19<B79,0,B19*10^6/(B21*2*B82*B6))","mm2/mm","0.000")
    out(ws,84,"Al (acero long. torsion)=(At/s)*ph*(fyt/fy)","=B83*B81*(B6/B5)","mm2","0")
    out(ws,85,"Chequeo torsion",'=IF(B19<B79,"DESPRECIABLE","DISENAR")',"","General",bold=True)
    seccion(ws,87,"DEFLEXIONES / DESARROLLO / DESPIECE")
    out(ws,88,"h minimo = L/factor","=B14/B15","mm","0")
    out(ws,89,"Chequeo deflexion",'=IF(B8>=B88,"NO CALCULAR","CALCULAR")',"","General",bold=True)
    out(ws,90,"ld inferior","=IF(B11>=19.1,(B5/(1.7*SQRT(B4)))*B11,(B5/(2.1*SQRT(B4)))*B11)","mm","0")
    out(ws,91,"ld superior (psi_t=1.3)","=1.3*B90","mm","0")
    out(ws,92,"Empalme clase B = 1.3*ld","=1.3*B90","mm","0")
    out(ws,93,"sep libre inferior","=IF(B38>1,(B7-2*B9-2*B10-B38*B11)/(B38-1),9999)","mm","0")
    out(ws,94,"Chequeo separacion",'=IF(B38<=1,"CUMPLE",IF(B93>=MAX(25,B11),"CUMPLE","REVISAR"))',"","General",bold=True)
    nota(ws,96,"Estribo total por rama = (cortante: 0.5*Av/s) + (torsion: At/s). En zona confinada (2h desde cara) usa s/2.")
    semaforo(ws,"B31:B98")

# ---------- RIOSTRAS ----------
def hoja_riostras(wb):
    ws=wb.create_sheet("Riostras"); anchos(ws)
    titulo(ws,"A1","DISENO DE RIOSTRA - flexion y cortante simple - NSR-10","D1")
    seccion(ws,3,"DATOS DE ENTRADA")
    inp(ws,4,"f'c",21,"MPa"); inp(ws,5,"fy",420,"MPa"); inp(ws,6,"fyt",420,"MPa")
    inp(ws,7,"b",100,"mm"); inp(ws,8,"h",400,"mm"); inp(ws,9,"cc",25,"mm")
    inp(ws,10,"db estribo",6.4,"mm"); inp(ws,11,"db long",12.7,"mm")
    inp(ws,12,"L (luz)",4000,"mm")
    inp(ws,13,"Mu",18,"kN*m","<-- DATO",dato=AMA_IN); inp(ws,14,"Vu",20,"kN","<-- DATO",dato=AMA_IN)
    inp(ws,15,"phi flexion",0.9,"-"); inp(ws,16,"phi cortante",0.75,"-")
    seccion(ws,18,"GEOMETRIA CALCULADA")
    out(ws,19,"d","=B8-B9-B10-B11/2","mm","0.0")
    out(ws,20,"Area barra","=PI()/4*B11^2","mm2","0")
    out(ws,21,"Av (2 ramas)","=2*PI()/4*B10^2","mm2","0")
    out(ws,22,"As minimo","=MAX(1.4/B5,0.25*SQRT(B4)/B5)*B7*B19","mm2","0")
    out(ws,23,"beta1","=IF(B4<=28,0.85,MAX(0.65,0.85-0.05*(B4-28)/7))","-","0.000")
    out(ws,24,"rho maximo","=0.85*B23*B4/B5*(3/8)","-","0.00000")
    seccion(ws,26,"FLEXION")
    out(ws,27,"Rn","=B13*10^6/(B15*B7*B19^2)","MPa","0.000")
    out(ws,28,"rho","=(0.85*B4/B5)*(1-SQRT(1-2*B27/(0.85*B4)))","-","0.00000")
    out(ws,29,"As requerido","=B28*B7*B19","mm2","0")
    out(ws,30,"Chequeo ductilidad",'=IF(B28<=B24,"CUMPLE","NO CUMPLE")',"","General",bold=True)
    out(ws,31,"As ADOPTADO","=MAX(B29,B22)","mm2","0",bold=True,hl=VERDE)
    out(ws,32,"No. de barras","=ROUNDUP(B31/B20,0)","barras","0",bold=True,hl=AMAR)
    out(ws,33,"As provisto","=B32*B20","mm2","0")
    out(ws,34,"Chequeo acero",'=IF(B33>=B31,"CUMPLE","NO CUMPLE")',"","General",bold=True)
    seccion(ws,36,"CORTANTE")
    out(ws,37,"Vc","=0.17*SQRT(B4)*B7*B19/1000","kN","0.00")
    out(ws,38,"phi*Vc","=B16*B37","kN","0.00")
    out(ws,39,"Vs requerido","=MAX(B14/B16-B37,0)","kN","0.00")
    out(ws,40,"s calculado","=IF(B39<=0,9999,B21*B6*B19/(B39*1000))","mm","0")
    out(ws,41,"s ADOPTADO","=IF(B14<=B38,MIN(B19/2,600),MIN(B40,B19/2,600))","mm","0",bold=True,hl=AMAR)
    out(ws,42,"RESULTADO",'=IF(B14<=B38,"Concreto resiste","Estribos @ "&ROUND(B41,0)&" mm")',"","General")
    seccion(ws,44,"DESARROLLO Y DESPIECE")
    out(ws,45,"ld = (fy/(2.1raizf'c))*db","=(B5/(2.1*SQRT(B4)))*B11","mm","0")
    out(ws,46,"sep libre","=IF(B32>1,(B7-2*B9-2*B10-B32*B11)/(B32-1),9999)","mm","0")
    out(ws,47,"Chequeo separacion",'=IF(B32<=1,"CUMPLE",IF(B46>=MAX(25,B11),"CUMPLE","REVISAR"))',"","General",bold=True)
    semaforo(ws,"B18:B49")

def main():
    wb=Workbook()
    hoja_instrucciones(wb); hoja_materiales(wb)
    hoja_viguetas(wb); hoja_vigas(wb); hoja_riostras(wb)
    wb.save("Herramienta-Diseno-Estructural.xlsx")
    print("OK -> Herramienta-Diseno-Estructural.xlsx (5 hojas: enfocada en viguetas, vigas, riostras)")

if __name__=="__main__":
    main()
