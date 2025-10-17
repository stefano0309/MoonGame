# Struttura

Utilizzando Pygame:
1. Inizializzo lo schermo del gioco
2. Set Up schermo clock e nome schermo
3. Stage
 - 0: Schermata iniziale 
Qui è presente in alto il titolo e sotto di esso due pulsanti **play** e **quit** e un background che rimane uguale su tutti gli sfondi.

Mentre per i pulsanti **start** e **quit** usiamo il controllo eventi utilizzando le immagine e il *rect* per controllare gli eventi del mouse in modo tale che cliccando in quel area restituisca *true* ed esegua le istruzioni:

    if event.type == pygame.MOUSEBUTTONDOWN:
        if play_rect.collidepoint(event.pos):
                start = True

        if quit_rect.collidepoint(event.pos):
                 running = False

Inoltre cliccando sul pulsante *play* è possibile uscire dalla schermata con valore stage = 0 con un animazione di testo e pulsanti che escono dall alto da destra e da sinistra 
 
 - 1: Schermata di gioco
Qui è presente la navicella spaziale ovvero il **player** il background rimane lo stesso sopra l'asse **y** troviamo tra *-200 e -100* vengono generati i 5 meteoriti con un **x** tra 0 e la massima grandezza dello schermo meno *y meteor*.

Quindi per realizzare ciò creiamo una lista di **FRect** con **x** e **y** e scala del meteorite all'interno di frect.

Il **movimento** della navicella spaziale è possibile tramite delle variabili *bool* e il controllo degli eventi di pygame che controlla **premuta** e **rilascio** del tasto modificando il valore della variabile in **true** e **false** successivamente utilizziamo degli **if** per controllare quando le variabili sono vere quindi con *il tasto premuto* e fa spostare sommando e sottraendo dei valori numeri rispetto all' asse *x e y* del **rect del player** .

Successivamente nel ciclo **while** inseriamo il controllo degli *stage* che controllizamo tramite le collisioni che avvengono tra navicella e asteroidi in modo tale da rendere la variabile stage uguale  a 2 ovvero il valore della schermata di gameover.

Poi definiamo i limiti dello schermo per la navicella spaziale rispetto a **x** e **y** che sono espresse come la larghezza massima è l'altezza massima della schermata definite al set up dello schermo quindi rispetto a *x <= 0 a x >= x_max poi y <= 0 a y >= y_max*.

La schermata di **game_over** avviene quando le due hitbox 20x20 e 20x20 si toccano viene rilevato e si passa a stage 2.

- 2: Schermata di game over

Viene visualizzata una schermata con scritta **rossa** e due pulsanti che invitano a rigiocare o a uscire userei di nuovo il *quit* gia presente per lo stage 0 e aggiungerei un pulsante per il rigioco per cui va creata una nuovo **rect**. 
