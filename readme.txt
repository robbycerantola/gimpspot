Questo software è GPL

Il plug-in funziona con Gimp 2.4 e 2.6 sia su Linux che Windows con python, PyCairo, PyGtk, PyGObject installati.
Puoi scaricare tutto quel che serve in una volta sola dal link GIMP for Windowsi.

Il sorgente spot-separation.py è da rendere eseguibile e mettere sotto la directory .gimp2/plug-in/ nella directory utente.
Ci sono anche un paio di "pennelli" da mettere nella directory .gimp2/brush/.
Dopo l'istallazione del plug-in si attiverà all'apertura di un file una nuova voce del menu ,
 MyScrips sotto la quale si trovera Spot-separation .

Il primo passo da compiere , prima della separazione vera e propria è quello di creare con gli strumenti messi a
disposizione da Gimp una tavolozza (palette) appropriata per l'immagine da elaborare, con il numero di colori desiderati
scelti con lo strumento color picker tra i colori dell'immagine originale.
Attenzione, in questa versione beta del plug-in, la tavolozza deve avere un formato ben preciso stabilito al momento della 
creazione e contenere cioè sempre i colori nero (0,0,0) e bianco (255,255,255) anche se non desiderati per la selezione.
 Il formato della tavolozza è dunque :1) NERO 2)BIANCO 3)FONDO 4)COLORE 5)COLORE 6)COLORE etc. Per FONDO intendo il colore di background eventualmente presente se diverso dal bianco .
Salvata la tavolozza con un nome appropriato , ed eventualmente rinominato ogni colore se si vuole che tale nome compaia
 sul layer rispettivo, si può attivare lo script .

Lo script chiede come parametro principale proprio il nome della tavolozza preparata, ed in base a quella effettuera una 
riduzione di colori con il metodo di dithering (retinatura) specifiato di seguito : nessuno, floyd-stainberg, 
floyd-staynberg con passaggi di colore ridotti (il migliore nel maggiore dei casi) , dithering fisso .

Altri parametri:

Transparency: simula le trasparenze col dithering

Marks : disegna i crocini di registro e le indicazioni dei colori usati

Multiple files: salva nella directory corrente un file TIFF monocromatico per ogni colore risultante dalla separazione
 pronto per essere stampato direttamente o essere inviato al RIP.
Se non viene attivato, lo script salva nella directory corrente un unico file PSD multilayer .



