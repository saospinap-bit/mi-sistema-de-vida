# Generador de planos de despiece en DXF (R12 ASCII, sin dependencias)
def L(x1,y1,x2,y2,lay): return f"0\nLINE\n8\n{lay}\n10\n{x1:.1f}\n20\n{y1:.1f}\n11\n{x2:.1f}\n21\n{y2:.1f}\n"
def C(x,y,r,lay): return f"0\nCIRCLE\n8\n{lay}\n10\n{x:.1f}\n20\n{y:.1f}\n40\n{r:.1f}\n"
def T(x,y,h,s,lay="TEXTO"): return f"0\nTEXT\n8\n{lay}\n10\n{x:.1f}\n20\n{y:.1f}\n40\n{h:.1f}\n1\n{s}\n"
def rect(x,y,w,h,lay):
    return L(x,y,x+w,y,lay)+L(x+w,y,x+w,y+h,lay)+L(x+w,y+h,x,y+h,lay)+L(x,y+h,x,y,lay)

def despiece_viga(ox,oy,Lm,hmm,bmm,label,ntop,nbot,estr,Mneg):
    e=[]; Lmm=Lm*1000.0
    # --- ELEVACION ---
    e.append(rect(ox,oy,Lmm,hmm,"CONCRETO"))
    # acero inferior corrido
    e.append(L(ox+40,oy+40,ox+Lmm-40,oy+40,"ACERO"))
    # bastones superiores (L/4 en cada apoyo)
    q=Lmm/4
    e.append(L(ox+40,oy+hmm-40,ox+q,oy+hmm-40,"ACERO"))
    e.append(L(ox+Lmm-q,oy+hmm-40,ox+Lmm-40,oy+hmm-40,"ACERO"))
    # estribos (ticks verticales): confinados en extremos, sueltos al centro
    x=ox+60
    while x<ox+Lmm-60:
        e.append(L(x,oy+30,x,oy+hmm-30,"ESTRIBO"))
        x += 85 if (x-ox<2*hmm or x-ox>Lmm-2*hmm) else 150
    # cota de longitud
    e.append(L(ox,oy-120,ox+Lmm,oy-120,"COTA"))
    e.append(T(ox+Lmm/2-300,oy-230,90,f"L = {Lm:.2f} m","COTA"))
    # etiquetas
    e.append(T(ox,oy+hmm+260,130,f"{label}   |   Mu(-)={Mneg} kN.m   |   seccion {int(bmm)}x{int(hmm)} mm","TEXTO"))
    e.append(T(ox+q+60,oy+hmm+90,90,f"{ntop} bastones sup. (L/4 + ld)","TEXTO"))
    e.append(T(ox+Lmm/2-300,oy-60,90,f"{nbot} barras inf. corridas","TEXTO"))
    e.append(T(ox+60,oy-60,80,f"Estribos {estr}","TEXTO"))
    # --- SECCION transversal (a la derecha) ---
    sx=ox+Lmm+500; sy=oy
    e.append(rect(sx,sy,bmm,hmm,"CONCRETO"))
    rbar=12
    # barras inferiores
    nb=max(2,nbot)
    for i in range(nb):
        xx=sx+45+(bmm-90)*(i/(nb-1) if nb>1 else 0.5)
        e.append(C(xx,sy+45,rbar,"ACERO"))
    # barras superiores
    nt=max(2,ntop)
    for i in range(nt):
        xx=sx+45+(bmm-90)*(i/(nt-1) if nt>1 else 0.5)
        e.append(C(xx,sy+hmm-45,rbar,"ACERO"))
    e.append(rect(sx+30,sy+30,bmm-60,hmm-60,"ESTRIBO"))
    e.append(T(sx,sy+hmm+90,90,f"Sec. {int(bmm)}x{int(hmm)}","TEXTO"))
    e.append(T(sx,sy-180,80,f"Sup: {ntop}#5  Inf: {nbot}#5","TEXTO"))
    return "".join(e)

def despiece_riostra(ox,oy,Lm,label):
    e=[]; Lmm=Lm*1000.0; hmm=300; bmm=300
    e.append(rect(ox,oy,Lmm,hmm,"CONCRETO"))
    e.append(L(ox+40,oy+40,ox+Lmm-40,oy+40,"ACERO"))
    e.append(L(ox+40,oy+hmm-40,ox+Lmm-40,oy+hmm-40,"ACERO"))  # 4#5 simetrico, corridas
    x=ox+60
    while x<ox+Lmm-60:
        e.append(L(x,oy+30,x,oy+hmm-30,"ESTRIBO")); x+= 100 if (x-ox<2*hmm or x-ox>Lmm-2*hmm) else 150
    e.append(L(ox,oy-120,ox+Lmm,oy-120,"COTA")); e.append(T(ox+Lmm/2-300,oy-230,90,f"L = {Lm:.2f} m","COTA"))
    e.append(T(ox,oy+hmm+200,120,f"{label}  |  Viga de amarre 300x300 mm  |  4 Nº5 (2 sup + 2 inf)  |  Estribos Nº3 @150 (@100 conf.)","TEXTO"))
    # seccion
    sx=ox+Lmm+500
    e.append(rect(sx,oy,bmm,hmm,"CONCRETO"))
    for cx in (sx+50,sx+bmm-50):
        for cy in (oy+50,oy+hmm-50): e.append(C(cx,cy,12,"ACERO"))
    e.append(rect(sx+30,oy+30,bmm-60,hmm-60,"ESTRIBO"))
    e.append(T(sx,oy+hmm+90,90,"Sec. 300x300","TEXTO"))
    return "".join(e)

def despiece_vigueta(ox,oy):
    e=[]; Lmm=4800.0; hmm=340; bw=150; losh=60; losw=800
    # loseta + nervio (T)
    e.append(rect(ox,oy+hmm-losh,Lmm,losh,"CONCRETO"))      # loseta
    e.append(rect(ox,oy,Lmm,hmm-losh,"CONCRETO"))           # nervio (representativo)
    e.append(L(ox+30,oy+30,ox+Lmm-30,oy+30,"ACERO"))        # 2#4 inf
    q=Lmm/4
    e.append(L(ox+30,oy+hmm-90,ox+q,oy+hmm-90,"ACERO")); e.append(L(ox+Lmm-q,oy+hmm-90,ox+Lmm-30,oy+hmm-90,"ACERO"))
    e.append(L(ox,oy-120,ox+Lmm,oy-120,"COTA")); e.append(T(ox+Lmm/2-300,oy-230,90,"L = 4.80 m (vano critico)","COTA"))
    e.append(T(ox,oy+hmm+260,120,"VIGUETA TIPO  |  nervio 150x340 + loseta 60  |  2 Nº4 sup (L/4) + 2 Nº4 inf  |  sin estribos (Vu<phi*1.1Vc)","TEXTO"))
    # seccion T
    sx=ox+Lmm+500
    e.append(rect(sx,oy+hmm-losh,losw,losh,"CONCRETO"))
    e.append(rect(sx+losw/2-bw/2,oy,bw,hmm-losh,"CONCRETO"))
    e.append(C(sx+losw/2-30,oy+45,12,"ACERO")); e.append(C(sx+losw/2+30,oy+45,12,"ACERO"))
    e.append(C(sx+losw/2-30,oy+hmm-losh-30,12,"ACERO")); e.append(C(sx+losw/2+30,oy+hmm-losh-30,12,"ACERO"))
    e.append(T(sx,oy+hmm+90,90,"Seccion en T","TEXTO"))
    return "".join(e)

def build(path,title,blocks):
    body="".join(blocks)
    # encabezado de lamina + nota de escala
    head=T(0,1200,200,title,"TITULO")+T(0,900,120,"Cotas en mm. Escala sugerida de impresion 1:25. NSR-10.","TEXTO")
    dxf="0\nSECTION\n2\nENTITIES\n"+head+body+"0\nENDSEC\n0\nEOF\n"
    open(path,"w",encoding="utf-8").write(dxf)
    return len(blocks)

VC=[("VC-1",2.50,2,2,-10),("VC-2",2.60,2,2,-7),("VC-3",2.65,6,5,-119),("VC-4",3.75,5,4,-106),("VC-5",3.81,5,4,-114),("VC-6",3.85,6,4,-122),("VC-7",3.90,6,4,-129),("VC-8",4.00,5,4,-104),("VC-9",5.10,5,3,-97)]
VR=[("VR-1",1.50,3,3,-58),("VR-2",2.50,3,3,-32),("VR-3",2.60,5,4,-97),("VR-4",2.70,4,3,-81),("VR-5",2.80,4,3,-79),("VR-6",2.95,3,3,-56),("VR-7",3.30,3,3,-39),("VR-8",3.65,3,3,-47),("VR-9",4.00,3,3,-65),("VR-10",4.18,4,3,-78),("VR-11",5.50,5,3,-104)]
RI=[("R-1",2.50),("R-2",2.60),("R-3",2.70),("R-4",2.80),("R-5",3.65),("R-6",3.85),("R-7",3.90),("R-8",4.00)]

def stack(items,fn,dy=1400):
    blocks=[]; y=0
    for it in items:
        blocks.append(fn(0,y,*it)); y-=dy
    return blocks

base="Proyectos/Diseno-Estructural/Solucion/"
import os; os.makedirs(base,exist_ok=True)
n1=build(base+"Despiece-Vigas-VC.dxf","DESPIECE VIGAS DE CARGA VC (0.30x0.40 m)",
    [despiece_viga(0,-i*1400,Lm,400,300,lbl,nt,nb,"Nº3 @86(conf)/@150",Mn) for i,(lbl,Lm,nt,nb,Mn) in enumerate(VC)])
n2=build(base+"Despiece-Vigas-VR.dxf","DESPIECE VIGAS DE RIGIDEZ VR (0.35x0.40 m)",
    [despiece_viga(0,-i*1400,Lm,400,350,lbl,nt,nb,"Nº3 @85(conf)/@150",Mn) for i,(lbl,Lm,nt,nb,Mn) in enumerate(VR)])
n3=build(base+"Despiece-Riostras-Cimentacion.dxf","DESPIECE RIOSTRAS DE CIMENTACION (0.30x0.30 m) - NSR-10 A.3.6.4.2",
    [despiece_riostra(0,-i*1100,Lm,lbl) for i,(lbl,Lm) in enumerate(RI)])
n4=build(base+"Despiece-Viguetas.dxf","DESPIECE VIGUETAS (nervio 0.15x0.34 + loseta 0.06)",[despiece_vigueta(0,0)])
print("Planos generados:",n1,"VC,",n2,"VR,",n3,"riostras,",n4,"vigueta")
# validar DXF (estructura basica)
for p in ["Despiece-Vigas-VC.dxf","Despiece-Vigas-VR.dxf","Despiece-Riostras-Cimentacion.dxf","Despiece-Viguetas.dxf"]:
    s=open(base+p).read()
    okv = s.startswith("0\nSECTION") and s.rstrip().endswith("EOF") and s.count("0\nLINE")>0
    print(f"  {p}: {'OK' if okv else 'REVISAR'}  ({s.count(chr(10)+'LINE')} lineas, {s.count('CIRCLE')} circulos, {s.count(chr(10)+'TEXT'+chr(10))} textos)")
