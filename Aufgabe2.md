# Bearbeitung Aufgabe 2:

## Gibt es bestimmte schwache Rotoren?

Unter der Annahme, dass alle Bytes in einem Rotor gesetzt sind nur Rotoren schwach, die irgendwelche Regelmäßigkeiten aufweisen, beispielsweise linear sind.
![vollständig lineare Rotoren](tests/empirical_analysis_results/linear_rotors.png?raw=true "vollständig lineare Rotoren")
*Beispiel mit allen Rotoren linear*
![erste Rotor ist linear](tests/empirical_analysis_results/one_linear_rotor.png?raw=true "erste Rotor ist linear")
*Beispiel mit dem ersten Rotor linear*

Wie eindeutig sichtbar ist, haben wir entweder einen starken bias mit ungleicher Verteilung oder eine Verteilung bei der nicht alle Werte belegt sind. Dies schränkt die Sicherheit deutlich ein
## Ist die BYTENIGMA krypto-grafisch stark, wenn randomisierte Rotoren gewaehlt werden?

Da es sich bei der Bytenigma um eine Konstruktion, die beinahe identisch mit der Enigma ist, handelt, sind auch die gleichen Schwachstellen der Enigma vorhanden. Das heißt, sobald Teile des Plaintexts bekannt sind, lässt sich die Rotorstellung zumindest teilweise (teilweise da nicht selbst ausprobiert und unsicher in welchem Umfang) zurückrechnen. 
Ebenso kann ein Zeichen nie auf sich selbst abgebildet werden. Entsprechend sind durch den Ciphertext Rückschlüsse auf den Plaintext möglich.


## Wie gut sind die Eigenschaften der Ununterscheidbarkeit (indistinguishability) und Neigung (bi-as) ausgepraegt

Es lassen sich Rückschlüsse auf den Plaintext vom Ciphertext ziehen, da bekannt ist, welches Zeichen **nicht** an dieser Stelle stehen kann. Ansonsten sind Ciphertexte nicht voneinander zu unterscheiden (bis auf die Länge) und keine weiteren Rückschlüsse auf den Plaintext möglich. Ansonsten ist indistinguishability gegeben. (mir ist auch kein chosen plaintext attack gelungen)


(Bias folgt im nächsten Abschnitt)

### Wie haengen diese mit der Anzahl der verwendeten Rotoren zusammen?

Je mehr Rotoren, destso geringer der Bias. In den folgenden Diagrammen wird die Anzahl der (zufällig generierten) Rotoren von 1 auf 10 erhöht. Dabei wird der Input von b'\0'*2**20 verwendet.

![](tests/empirical_analysis_results/1_rotor_random_input.png?raw=true "1 random Rotor")
*Beispiel mit 1 Rotor*

![](tests/empirical_analysis_results/2rotors.png?raw=true "2 random Rotoren")
*Beispiel mit 2 Rotoren*

![](tests/empirical_analysis_results/3rotors.png?raw=true "3 random Rotoren")
*Beispiel mit 3 Rotoren*


![](tests/empirical_analysis_results/10rotors.png?raw=true "10 random Rotoren")
*Beispiel mit 10 Rotoren*

Wie unschwer zu erkennen ist reduziert sich der Bias zunehmend (immer noch ohne 0 selbst). Bei einem Rotor ist der Bias extrem stark ausgeprägt und es sind nicht einmal alle Werte vertreten.
Mit zunehmender Anzahl Rotoren ergibt sich ein akzeptabler Bias. 
Problematisch ist jedoch die Länge des inputs. Je kürzer dieser ist, destso schlechter ist der bias, da auf Grund der Länge des Inputs nicht ausreichend viele Durchläufe erreicht werden, um alle Rotoren zu durchlaufen.
![](tests/empirical_analysis_results/100word_input_10_rotors.png?raw=true "output mit 100 Wörtern input")
*100 Wörter lorem ipsum input*

Wie unschwer zu erkennen ist, ist der Bias katastrophal.