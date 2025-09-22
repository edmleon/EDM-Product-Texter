# Regelwerk_Kurzbeschreibung (P) – B2B-Industrieprodukte

**Ziel:** Kurze, sachliche Beschreibungen für Produktdetailseiten (unterhalb der H2-Überschrift) als P-HTML Text. Fokus: prägnante Orientierung für den Leser + SEO-Sauberkeit. Keine Werbung, sondern klare Fakten zum Einsatzzweck, Material, Kompatibilität oder Verpackung.

---

## 1) Grundformel & Limits

**Formel:** 
`{Produkttyp/Funktion} für {Einsatzzweck/Medium}, {Material/Besonderheit}, {Verpackung/Variante}`

**Länge:** Ziel: 140–160 Zeichen (optimiert für Google-Snippets). Minimum: 110 Zeichen, Maximum: 180 Zeichen. Keine Aufzählungen, sondern fließender Satzbau.

## 2) Muss-/Soll-Logik je Kategorie

### Global 
- **MUSS:** Grundfunktion / Einsatzzweck klarmachen.
- **SOLL:** Material oder konstruktives Hauptmerkmal nennen (z. B. „aus PVC“, „ölbeständig“).
- **Fallback:** Verpackungseinheit oder Rollenlänge ergänzen, wenn sonst zu kurz.

### Schuhe/PPE
- **MUSS:** Einsatzumfeld („Sicherheitsschuh für Bau & Industrie“).
- **SOLL:** Eigenschaften wie Sicherheitsklasse (S3), Material (Leder, Textil), Komfortfeatures (BOA, GTX).
- **Fallback:** Größenbereich oder Weitenoption erwähnen.

### Schläuche/Leitungen/Fittings
- **MUSS:** Medium oder Einsatzzweck („Schlauch für Druckluft“, „Fitting für IBC-Container“).
- **SOLL:** Material oder Farbe („aus EPDM, schwarz“).
- **Fallback:** Lieferform („auf Rolle zu 40 m“).

### Chemie/Fluids/Schmierstoffe
- **MUSS:** Hauptfunktion („Schmierfett für Wälzlager“).
- **SOLL:** Besondere Eigenschaft („hochtemperaturbeständig“).
- **Fallback:** Verpackung („400 g Kartusche“).

## 3) Stil & Sprachregeln

**Ton:** Sachlich, informativ, keine Adjektiv-Floskeln wie „hochwertig“, „beste Qualität“.

**Verb-Logik:** Beschreibend statt werbend: „geeignet für …“, „ausgelegt für …“, „zur Abdichtung von …“.

**Satzbau:** Kurzer Fließtext, kein Telegrammstil.

**Einheitliche Schreibweise:** Zahlen + geschütztes Leerzeichen + Einheit (400 g, 20 L).

**Außerdem:** Materialien immer nennen, wenn eindeutig. Keine Normen/Temperaturen/Druckangaben (stehen in Technischen Daten, nicht in Teaser).

## 4) Datenquellen & Validierung

**Vorgehen:** Zunächst nach Daten in manufacturer_data und product_data schauen. Dann Herstellerseiten durchsuchen. Nichts erfinden.

**Zulässig:** Herstellerangaben, interne DB, Händlertexte.

**Nicht zulässig:** Eigene Erfindungen oder Mutmaßungen.

**Prüfen:** Funktion erkennbar? Material genannt? Länge innerhalb 110–180 Zeichen? Keine Normen/Werbung?

## 5) Entscheidungslogik (Pseudocode)

1. Produktkategorie identifizieren (Schlauch, Schuh, Chemie …).
2. Einsatzzweck/Funktion in einem Satzkern formulieren.
3. Material oder Hauptmerkmal ergänzen.
4. Falls < 110 Zeichen → Verpackung oder Variante ergänzen.
5. Endkontrolle: keine Floskeln, Länge passt.

## 6) Checkliste_Kurzbeschreibung

1. Habe ich die Grundfunktion klar benannt?
    (z. B. „Schlauch für Druckluft“, „Schmierfett für Wälzlager“, „Sicherheitsschuh für Bau & Industrie“)
2. Ist das Material oder eine Hauptbesonderheit genannt?
    (z. B. „aus EPDM“, „ölbeständig“, „aus Leder mit BOA-Verschluss“)
3. Habe ich ggf. die Verpackungseinheit oder Variante ergänzt, wenn der Text sonst zu kurz wäre?
    (z. B. „auf Rolle zu 40 m“, „400 g Kartusche“)
4. Liegt die Länge zwischen 110 und 180 Zeichen?
    <110 Zeichen → prüfen, ob Verpackung/Variante ergänzt werden kann.
    180 Zeichen → kürzen (meist Nebensatz oder Zusatzinfo rausnehmen).
5. Ist der Ton sachlich und beschreibend?
    Verben: „geeignet für“, „ausgelegt für“, „zur Abdichtung von …“
    Keine Floskeln: kein „hochwertig“, „beste Qualität“, „innovativ“.
6. Enthält der Text keine Druckangaben, Normen oder Temperaturbereiche?
    (Das gehört in die Technischen Daten, nicht in den Teaser.)
7. Habe ich einen vollständigen Satz formuliert, keinen Telegrammstil?
    **Richtig:** „Schmierfett für Wälzlager und Führungen, hochtemperaturbeständig, geliefert in 400 g Kartusche.“
    **Falsch:** „Schmierfett, Wälzlager, hochtemperaturbeständig, 400 g.“
8. Sind Maßeinheiten korrekt mit geschütztem Leerzeichen gesetzt?
    (400 g, 20 L, 3/4″, 400 mm)

## 7) Beispiele

**Schlauch:** „Wasserschlauch für Gartenbau und Industrie, aus Gummi, schwarz, auf Rolle zu 40 m.“
**Schuh:** „Sicherheitsschuh S3 für Bau & Handwerk, aus Leder mit BOA-Verschluss, in Größen 39–47 verfügbar.“
**Chemie:** „Schmierfett für Wälzlager und Führungen, hochtemperaturbeständig, geliefert in 400 g Kartusche.“
**Fitting:** „Adapter für IBC-Container mit Kugelauslaufhahn, aus Kunststoff, kompatibel mit 3/4″-Anschlüssen.“