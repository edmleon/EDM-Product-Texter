# Regelwerk_Technische_Daten – B2B-Industrieprodukte

**Ziel:**  Strukturierte, normierte, **maschinenlesbare** technische Daten für Produktdetailseiten. Fokus: **Vergleichbarkeit**, **Suchbarkeit** und **Eindeutigkeit** für Instandhalter & Einkäufer. Keine Werbetexte, nur Fakten. Als HTML Tabelle.  

---

## 1) Aufbau & Struktur

- **Darstellung:** Tabellenform (Key–Value), nicht Fließtext.  
- **Reihenfolge:** Immer nach Wichtigkeit & Vergleichbarkeit, **global einheitlich pro Kategorie**.  
- **Einheitliche Keys:** Vorab definierte Feldnamen verwenden (kein Synonym-Mix).  
- **Keine leeren Felder:** Nicht vorhandene Datenfelder weglassen, nicht mit „–“ füllen.  

---

## 2) Pflichtfelder je Kategorie

### Global (immer prüfen)
- Hersteller  
- Serie (falls vorhanden)  
- Produkttyp / Bezeichnung  
- Abmaße (mm oder ″, normiert)  
- Farbe (falls vorhanden)  
- Verpackungseinheit / Rollenlänge (falls relevant)

### Schuhe / PSA
- Größe (EU)  
- Weite  
- Sicherheitsklasse (z. B. S1P, S3)  
- Schutzmerkmale (z. B. ESD, Metallfrei)  
- Obermaterial / Futter / Sohle  

### Schläuche / Leitungen / Fittings
- Innendurchmesser (ID, mm)  
- Wandstärke (mm)  
- Außendurchmesser (OD, mm, falls relevant)  
- Anschlussgröße / Gewinde (″ oder mm)  
- Material (z. B. EPDM, PVC, Messing)  
- Farbe  
- Rollenlänge (m)  

### Chemie / Fluids / Schmierstoffe
- Produkttyp (Öl, Fett, Reiniger …)  
- Farbe (falls vom Hersteller angegeben)  
- Verpackungseinheit (z. B. 400 g Kartusche, 1 L Dose, 20 L Kanister)  
- Viskosität / Konsistenzklasse (nur wenn eindeutig angegeben)  
- Freigaben / Zertifikate (DIN/ISO/EN, aber **separat listen**)  

### Andere, je nach Produkt
- Material
- Schutzart/Norm (DIN/EN/IP)
- Leistung/Spannung/Druck
- Temperatur
- Anschluss/Thread
- Gewicht
- Gebinde/VE
- Zertifikate

---

## 3) Schreibweise & Normalisierung

- **Maße:**  
  - Multiplikationszeichen **×** statt „x“  
  - Komma statt Punkt bei Dezimalzahlen (3,5 mm statt 3.5 mm)  
  - Inch mit **″**  
  - Geschütztes Leerzeichen zwischen Zahl und Einheit (400 g, 20 L, 3/4″, 400 mm)  

- **Materialien:** Vollständig schreiben (z. B. „PVC“, „Edelstahl“, „Nitrilkautschuk“). Keine Kürzel außer international übliche (PVC, EPDM, PTFE).  

- **Farben:** Einfach, deutschsprachig („Schwarz“, „Blau“). Keine Fantasienamen.  

- **Verpackungseinheiten:** Klar formulieren: „Kartusche 400 g“, „Kanister 20 L“, „Rolle 40 m“.  

- **Normen & Zertifikate:** Eigene Zeile, Originalbezeichnung („DIN EN 388“, „ISO VG 220“).  

---

## 4) Datenquellen & Validierung

- **Quelle:** Webrecherche (Hersteller Seite). Im seltenen Fall kann eine json mit technische Daten für einen Hersteller zur Verfügung stehen.

- **Verifizierung:** Verfiziere deine Ergebnisse, keine Erfindungen, exakte technische Daten. Achte auf genaue Übereinstimmung in der Bezeichnung bzw. der Merkmalzusammensetzung.

## 5) Regeln für Aufnahme / Ausschluss

- **Nur harte Fakten** (keine Einsatzempfehlungen wie „ideal für …“).  
- **Keine Wiederholung** von H2 oder Kurzbeschreibung.  
- **Alle Angaben aus Quelle prüfen**: Plausibel? Einheit vollständig?  
- **Unklare Codes** ohne Kontext → nicht übernehmen.  
- **Service-/Leistungspositionen** (Montage, Rüstkosten) → **keine technischen Daten**.  

---

## 6) Validierungslogik (Pseudocode)

1. Quelle prüfen: Sind Maße, Material oder Verpackungseinheiten erkennbar?  
2. Kategorie bestimmen (Schlauch, Schuh, Chemie …).  
3. Pflichtfelder füllen (nur mit geprüften Daten).  
4. Maße normieren (×, Komma, mm ergänzen).  
5. Einheiten prüfen (geschütztes Leerzeichen).  
6. Normen/Zertifikate separat aufführen.  
7. Endkontrolle: Nur Fakten? Keine Werbesprache?  

---

## 7) Beispiele

**Schlauch:**  
| Hersteller | Conti |  
|------------|-------|  
| Serie | Goldschlange |  
| Produkttyp | Wasserschlauch |  
| Abmaße | 13×3,5 mm |  
| Farbe | Schwarz |  
| Material | Gummi |  
| Rollenlänge | 40 m |  

**Schuh:**  
| Hersteller | Atlas |  
| Serie | XT 550 BOA GTX |  
| Produkttyp | Sicherheitsschuh |  
| Größe | 42 |  
| Weite | 10 |  
| Klasse | S3 |  
| Eigenschaften | BOA-Verschluss, wasserdicht, ESD |  
| Material | Leder/Textil |  

**Chemie:**  
| Hersteller | Klüber |  
| Produkt | ISOFLEX TOPAS NCA 52 |  
| Typ | Schmierfett |  
| Farbe | Beige |  
| Verpackung | Kartusche 400 g |  
| Normen/Zertifikate | DIN 51825 KP2N-20 |  