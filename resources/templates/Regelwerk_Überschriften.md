# Regelwerk_Überschriften (H2) – B2B-Industrieprodukte

**Ziel:** Einheitliche, SEO-saubere H2-Überschriften für Produktdetailseiten. Fokus: **Instandhalter** & **Einkäufer**. Keine Werbefloskeln, keine Behauptungen, klare technische Informationen.

---

## 1) Grundformel & Limits

**Formel:**  
`{Hersteller} {Serie?} {Produkttyp} – {Eigenschaft 1}{, Eigenschaft 2?}`

**Länge:** Ziel **60–75 Zeichen**, hartes Maximum **85 Zeichen**.  
> Bei Überschreitung: zuerst **Eigenschaft 2** streichen, dann Produktterm vorsichtig kürzen (z. B. Serienzusatz weglassen).

**Max. Eigenschaften:** **2**. **Abmaße sind immer Eigenschaft 1**, wenn vorhanden.

**Nicht in H2:** Druck/Bar, Normen (DIN/EN/ISO), Temperaturbereiche, Marketing-Claims.

---

## 2) Muss-/Soll-Logik je Kategorie

### Global
- **Abmaße (Dimensionen)** sind **immer MUSS**, wenn vorhanden (z. B. „13×3,5 mm“, „3/4″“).
- **Farbe** ist **SOLL** (kaufentscheidend, Serienvarianz).  
- **Verpackungseinheit/Rollenlänge (VE/RL)** ist **Fallback**, **nie** gegen Farbe, wenn zwei Slots bereits belegt.

### Schuhe/PPE
- **MUSS:** `Größe` **und** `Weite` (belegen beide Slots).  
- **Feature/Serie** (BOA, GTX, ESD, S1/S1P/S3) **nur** wenn es im Produktnamen vorkommt **und** Länge zulässt (ersetzt keine MUSS-Felder).

### Schläuche/Leitungen/Fittings/Adapter
- **MUSS:** `Abmaße` (ID×Wandstärke o. Anschlussgröße).  
- **SOLL:** `Farbe`.  
- **Fallback:** `Rollenlänge/VE`, wenn keine Farbe vorhanden ist und noch ein Slot frei ist.

### Chemie/Fluids/Schmierstoffe
- **MUSS:** `Abmaße` gibt es hier i. d. R. nicht → stattdessen **Farbe**, wenn vorhanden.  
- **SOLL:** `Verpackungseinheit` **nur**, wenn **keine Farbe** vorhanden ist (Konfliktregel: **Farbe vor VE**).

### Generisch/Andere
- **MUSS:** `Abmaße`, wenn vorhanden; sonst `Farbe`.  
- **Fallback:** `VE/Rollenlänge`, falls weder Abmaße noch Farbe verfügbar sind.

---

## 3) Normalisierung & Schreibweise

- **Keine Abkürzungen** in H2. Vor dem Bauen der H2 **alle** Abkürzungen expandieren. Beispiele:  
  - „Wasserschl.“ → **Wasserschlauch**  
  - „Pressl.“ → **Pressluftschlauch**  
  - „Sandstrahlschl.“ → **Sandstrahlschlauch**  
  - „Heißwasserschl.“/„Heisswasserschl.“ → **Heißwasserschlauch**  
  - „ND.“ → **Niederdruck**, „HD.“ → **Hochdruck**  
  - „RL“ → **Rollenlänge**, „VE“ → **Verpackungseinheit**

- **Maße normieren:**  
  - „x“ → **×** (Multiplikationszeichen).  
  - Dezimalpunkt → **Komma** (3.5 → 3,5).  
  - Fehlendes **„mm“** ergänzen (bei metrischen Maßen).  
  - Inch-Zeichen als **″**.  
  - **Mehrteilige Maße** `A×B/C`: als **A×C mm** interpretieren (letzte Zahl = Wandstärke).

- **Einheiten:** geschütztes Leerzeichen zwischen Zahl und Einheit: `400 g`, `20 L`, `3/4″`, `400 mm`.

- **Groß-/Kleinschreibung & Marken:** Marken/Serien wie in der Quelle schreiben (BOA, GTX, ESD in Versalien). Farbwörter normal (z. B. „Schwarz“ → „Schwarz“ im Eigenschaftsblock).

---

## 4) Datenquellen & Validierung

- Zulässige Quellen: interne DB (Excel, JSON …), Webscraping und seriöse Händler/Herstellerseiten. **Keine Erfindungen.**
- **Unzureichend beschrieben** (nur Codes, unklarer Typ/Serie) → **zurückweisen** (nicht bearbeiten) und zum nächsten Artikel springen.  
  Beispiele: „SPA1557“, „1610 28“, „A40SP-S-300“ ohne Typ.
- **Service-/Leistungspositionen** (Fahrtkosten, Montage, Rüstkosten) → **keine H2**, als Service auslisten.
- **Validierung:** Einheiten plausibel? Abmaße vorhanden? Abkürzungen restlos entfernt? Länge ≤ 85 Zeichen?

---

## 5) Auswahl-Algorithmus (Pseudocode)

1. **Vorverarbeitung:** Trimme, **expandieren** aller Abkürzungen, Maße & Einheiten **normieren**, Druck & Normen **markieren, aber nicht ausgeben**.  
2. **Kategorie bestimmen** (Schuhe, Schlauch, Chemie, Fitting, generisch).  
3. **Produktterm** bestimmen: `{Hersteller} {Serie?} {Produkttyp}` (ohne Maße/Farbe/VE).  
4. **Eigenschaften wählen (max. 2):**  
   - **Prop1:** **Abmaße**, wenn vorhanden; sonst **Kategorie-MUSS** (z. B. Schuhe: Größe).  
   - **Prop2:** **Farbe** (falls vorhanden & Slot frei); sonst **Kategorie-SOLL/Fallback** (z. B. VE/Rollenlänge).  
   - **Druck/Normen niemals** in die H2.  
5. **Längencheck:** > 85 Zeichen → Prop2 entfernen; wenn nötig Produktterm moderat kürzen (Serienzusatz).  
6. **Finale H2 bauen:** `{Produktterm} – {Prop1}{, Prop2?}`.  
7. **Endkontrolle:** Keine Abkürzungen? Maße in Prop1? Einheiten korrekt?

---

## 6) Entscheidungsfragen (für die KI)

1. **Habe ich Abkürzungen vollständig expandiert** (auch versteckte wie „Schl.“ in zusammengesetzten Wörtern)?  
2. **Sind Abmaße vorhanden?** → Dann **immer** als **Eigenschaft 1** verwenden (normiert).  
3. **Ist Farbe vorhanden?** → Wenn ja, und Slot 2 ist frei, **Farbe aufnehmen**.  
4. **Gehört der Artikel zu Chemie/Fluids?** → Bei Konflikt **Farbe vor VE**.  
5. **Ist der Artikel ein Schuh/PPE?** → `Größe` + `Weite` sind MUSS (zählen als 2 Eigenschaften).  
6. **Enthält die Quelle nur Codes oder ist der Typ unklar?** → Artikel **zurückweisen**.  
7. **Überschreite ich 85 Zeichen?** → Eigenschaft 2 entfernen; ggf. Produktterm kürzen.  
8. **Sind Druck/Normen/Temperaturen erkannt?** → **Nie** in H2 ausgeben.  
9. **Sind Maße mehrteilig (A×B/C)?** → Als **A×C mm** interpretieren; wenn weiterhin unklar → **zurückweisen**.

---

## 7) Beispiele

- **Schlauch:** `Conti Goldschlange Wasserschlauch – 13×3,5 mm, Schwarz`  
- **Schuh:** `Atlas XT 550 BOA GTX Sicherheitsschuh – Größe 42, Weite 10`  
- **Chemie:** `Klüber ISOFLEX TOPAS NCA 52 Schmierfett – 400 g Kartusche` *(VE ist bei Chemie wichtiger als Farbe/ Farbe ist hier unwichtig)*  
- **Fitting/Adapter:** `IBC-Adapter auf Kugelauslaufhahn – 3/4″, Schwarz`

---

## 8) Bekannte Abkürzungen (Expand-Liste, erweiterbar)

| Kürzel | Ersetzt durch |
|---|---|
| Wasserschl. | Wasserschlauch |
| Sandstrahlschl. | Sandstrahlschlauch |
| Pressl. | Pressluftschlauch |
| Schl. | Schlauch |
| Heißwasserschl. / Heisswasserschl. | Heißwasserschlauch |
| ND. | Niederdruck |
| HD. | Hochdruck |
| RL | Rollenlänge |
| VE | Verpackungseinheit |

> **Implementierungshinweis:** Nach dem Erzeugen der H2 eine **zweite Prüf-Pipeline** laufen lassen: „Enthält der String noch ein Wort mit Punkt am Ende (`\w+\.`)?“ → Wenn ja, gegen **Art.grp.-Bezeichnung** ersetzen oder **zurückweisen**.

---

## 9) Was absichtlich **nicht** geregelt ist (bewusste Lücken)
- Tiefere Markenstilguides (z. B. Schreibweise bestimmter Serien).  
- Mapping von reinen Artikelcodes (**wird verworfen**, s. 4).  
- Farbe, falls sie nicht eindeutig aus Quelle hervorgeht (**nicht erfinden**).