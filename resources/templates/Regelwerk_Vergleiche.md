# Regelwerk_Vergleiche – B2B-Industrieprodukte

**Ziel:**  
Kompakte Vergleichstabelle verwandter Produkte **des gleichen Herstellers**, um Käufern und Instandhaltern eine schnelle Entscheidungshilfe zu bieten. Keine Werbeaussagen, nur technische und kaufrelevante Kriterien.

---

## 1) Aufbau & Struktur

- **Darstellung:** Tabelle mit **3–5 Kriterien** (Zeilen) × **2–3 Alternativen** (Spalten)  
- **Bezug:** Nur Produkte **des gleichen Herstellers** – keine Fremdmarken.  
- **Quellen:** interne Produktrelationen (`related_ids`) oder Filterlogik (z. B. Serie, Typ, Material).  
- **Ziel:** Schneller Direktvergleich ähnlicher Varianten (z. B. Größe, Material, Schutzart).  

---

## 2) Kriterien (Zeilen)

### Empfohlene Kernfelder:
1. **Größe / DN / Abmessung** – wichtigste Vergleichsbasis für physische Produkte  
2. **Leistung / Spannung / Druckbereich** – je nach Kategorie (z. B. Elektrotechnik, Pneumatik, Chemie)  
3. **Schutzart / Norm** – IP-Schutz, EN-Normen, Sicherheitsklassen  
4. **Material / Werkstoff** – technische Hauptdifferenzierung (z. B. Messing vs. Edelstahl)  
5. **Preis / Verfügbarkeit** – nur wenn im System gepflegt, keine Werbebewertungen („attraktiver Preis“ verboten)  

> **Regel:** Mindestens **3**, maximal **5** Kriterien. Wenn weniger Daten verfügbar sind → Tabelle nicht anzeigen.

---

## 3) Varianten (Spalten)

- **Spaltenüberschrift:** Serienname oder Variantenbezeichnung  
  *(z. B. „Serie XT 550“, „Serie XT 530“, „Serie XT 510“)*  
- **Reihenfolge:** Nach Funktionslogik (z. B. aufsteigende Größe oder Leistung).  
- **Nur interne Produktrelationen** verwenden – keine „ähnlichen“ Fremdartikel oder geratenen Alternativen.  

---

## 4) Datenquellen & Regeln

- **Primärquelle:** `related_ids` (systemisch gepflegte Artikelverknüpfungen).  
- **Fallback:** Produkttyp + Hersteller + Serienfilter.  
- **Keine Mischhersteller** – wenn kein interner Bezug besteht, Vergleich weglassen.  
- **Normen & Maße aus technischen Daten übernehmen**, keine freien Interpretationen.  

---

## 5) Formatierungs- & Sprachregeln

- **Darstellung:** einfache Markdown-/HTML-Tabelle (Key–Value-Stil).  
- **Keine Marketingtexte** („besser“, „höherwertig“, „Premium“) → nur Fakten.  
- **Einheiten konsistent normieren:** mm, ″, V, IP, DIN.  
- **Zahlenangaben rechtsbündig**, **Texte linksbündig** (UX-Standard für technische Tabellen).  
- **Leerzellen vermeiden** → wenn unbekannt: „–“.  

---

## 6) Beispiel

| Kriterium           | Serie XT 510 | Serie XT 530 | Serie XT 550 |
|----------------------|--------------|--------------|--------------|
| Größe               | 40           | 42           | 44           |
| Sicherheitsklasse    | S1P          | S3           | S3           |
| Material             | Textil       | Leder/Textil | Leder/Textil |
| Schutzstandard       | EN ISO 20345 | EN ISO 20345 | EN ISO 20345 |
| Preis / Verfügbarkeit | –            | auf Anfrage  | verfügbar    |

---

## 7) Validierungslogik (Pseudocode)

1. Prüfe, ob **related_ids** oder Serienfilter vorhanden sind.  
2. Prüfe, ob alle Artikel **vom selben Hersteller** stammen.  
3. Wähle **2–3 Alternativen** aus (Serien/Varianten).  
4. Fülle **3–5 Kriterien** aus den technischen Daten.  
5. Wenn weniger als 3 Kriterien verfügbar → Vergleich unterdrücken.  
6. Prüfe Maßeinheiten, Normen, Schreibweise.  
7. Endkontrolle: Nur Fakten, kein Marketing.  

---

## 8) Beispiel-Template

| Kriterium           | {Variante_1} | {Variante_2} | {Variante_3} |
|----------------------|--------------|--------------|--------------|
| Größe / DN           | {Wert_1}     | {Wert_2}     | {Wert_3}     |
| Leistung / Spannung  | {Wert_1}     | {Wert_2}     | {Wert_3}     |
| Schutzart / Norm     | {Wert_1}     | {Wert_2}     | {Wert_3}     |
| Material             | {Wert_1}     | {Wert_2}     | {Wert_3}     |
| Preis / Verfügbarkeit| {Wert_1}     | {Wert_2}     | {Wert_3}     |