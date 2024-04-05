import numpy as np
import matplotlib.pyplot as plt

# Perzeptron Modell: Das Perzeptron-Klassifikationsverfahren basiert auf der Rechnung zwischen den Gewichten und der Eingabe.
# Wenn das Ergebnis positiv ist, wird die Eingabe in die eine Klasse eingestuft, andernfalls in die andere Klasse.


# Erstellung Trainingsdaten (Größe / Breite) in array + Hinzufügen des bias (1) zur Matrix + Erstellung Matrix mit Labeldaten (0en und 1en)
attributes = np.array([[37.92655435, 23.90101111],
                       [35.88942857, 22.73639281],
                       [29.49674574, 21.42168559],
                       [32.48016326, 21.7340484],
                       [38.00676226, 24.37202837],
                       [30.73073988, 22.69832608],
                       [35.93672343, 21.07445241],
                       [38.65212459, 20.57099727],
                       [35.52041768, 21.74519457],
                       [37.69535497, 20.33073640],
                       [33.00699292, 22.57063861],
                       [33.73140934, 23.81730782],
                       [43.85053380, 20.05153803],
                       [32.95555986, 24.12153986],
                       [36.38192916, 19.20280266],
                       [36.54270168, 20.45388966],
                       [33.08246118, 22.20524015],
                       [31.76866280, 21.01201139],
                       [42.24260825, 20.44394610],
                       [29.04450264, 22.46633771],
                       [30.04284328, 21.54561621],
                       [18.95626707, 19.66737753],
                       [18.60176718, 17.74023009],
                       [12.85314993, 18.42746953],
                       [28.62450072, 17.94781944],
                       [21.00655655, 19.33438286],
                       [17.33580556, 18.81696459],
                       [31.17129195, 17.23625014],
                       [19.36176482, 20.67772798],
                       [27.26581705, 16.71312863],
                       [21.19107828, 19.00673617],
                       [19.08131597, 15.24401994],
                       [26.69761925, 17.05937466],
                       [4.44136559, 3.52432493],
                       [10.26395607, 1.07729281],
                       [7.39058439, 3.44234423],
                       [4.23565118, 4.28840232],
                       [3.87875761, 5.12407692],
                       [15.12959925, 6.26045879],
                       [5.93041263, 1.70841905],
                       [4.25054779, 5.01371294],
                       [2.15139117, 4.16668657],
                       [2.38283228, 3.83347914]])

attributes = np.concatenate((attributes, np.ones(43).reshape(43, 1)), axis=1)
labels = np.concatenate((np.ones(21), np.zeros(22)))

# Erstellung Klasse Perzeptron()
class Perzeptron():

    # Definition des Grundgerüsts von der Klasse Perzeptron() für folgende Methoden und Objekte
    def __init__(self, max_loops):
        self.w = None
        self.skalierungsfaktor = None
        self.trainiert = False
        self.max_loops = max_loops
        self.fehler = np.zeros(max_loops)

    # Definition Perzeptron Funktion
    def perzeptron(self, x):
        if self.trainiert == True:
            x /= self.skalierungsfaktor
        if self.w @ x > 0:                  # Wenn Ergebnis positiv ist, wird Eingabe in eine Klasse eingestuft, andernfalls in die andere Klasse (so funktioniert Perzeptron Modell)
            return 1                        # Wenn Ergebnis negativ ist, bedeutet dies, dass Gewicht und Eingabe in entgegengesetzte Richtungen zeigen und Ergebnis in der anderen Klasse liegt
        else:
            return 0                        # Output 1 = Hund / Output 0 = kein Hund

    # Daten normalisieren (0-1) + Definition Lernprozess
    def lernschritt(self, attributes, labels, verbose=False):
        self.skalierungsfaktor = np.max(attributes, 0)
        attributes /= self.skalierungsfaktor

        loops = 0
        self.w = np.random.rand(attributes.shape[1])
        while loops < self.max_loops:
            for x, label in zip(attributes, labels):
                delta = label - self.perzeptron(x)          # wenn label = self.perzeptron (richtiger guess aus perzeptron), dann delta= 0 (1-1/0-0) sonst delta= 1/-1 (1-0/0-1) (falscher guess)
                if delta != 0:
                    self.fehler[loops] += 1
                    self.w += (delta * x)                   # Anpassung der Gewichte w (delta=1: x wird auf w addiert, delta=-1: x wird von w subtrahiert, delta=0: pass. (Machine Learning)
            if self.fehler[loops] == 0:
                self.trainiert = True
                if verbose:
                    self.visualize(attributes, labels)
                break
            loops += 1
        else:
            print("Es wurde keine Lösung gefunden.")        # wenn lernschritt nicht erfolgreich ist

    # Funktion für Visualisierung
    def visualize(self, attributes, labels):
        _, ax = plt.subplots()
        plt.title('Trainingsdaten')
        plt.xlabel('Grösse [cm]')
        plt.ylabel('Länge [cm]')
        plt.scatter(attributes[:, 0], attributes[:, 1], c=labels, cmap='coolwarm')
        x0 = np.array([0, 1])
        w = self.w
        if w[1] != 0:
            x1 = -(w[0] * x0 + w[2]) / w[1]
            plt.plot(x0, x1, color='g', label='Trennlinie der KI')
            if w[1] > 0:
                ax.fill_between(x0, x1, x1+2, alpha=0.2,
                                color='g', label='Hund')
            else:
                ax.fill_between(x0, x1, x1-1, alpha=0.2,
                                color='g', label='Hund')
            ax.set_ylim([0, max(attributes[:, 1]) * 1.1])
        plt.legend()
        plt.show()

    # Funktion zum aufzeigen Anzahl Fehler
    def falsche_klassifikationen(self):
        plt.plot(range(self.max_loops), self.fehler)
        plt.xlabel('Epoche')
        plt.ylabel('Falsche Klassifikationen')
        plt.show()

# Implementierung der Klasse Perzeptron(max_loops) in Objekt perzeptron
perzeptron = Perzeptron(100)

# Training
perzeptron.lernschritt(attributes, labels)

# Fehleranalyse
#perzeptron.falsche_klassifikationen()
#perzeptron.visualize(attributes, labels)

# Visualisierung
perzeptron.visualize(attributes, labels)

# Anwendung
x_neu = [37.92655435, 23.90101111, 1]
if perzeptron.perzeptron(x_neu) == 1:       # 1 = Hund, 0 = kein Hund
    print("Das ist ein Hund!")
else:
    print("Das ist kein Hund...")